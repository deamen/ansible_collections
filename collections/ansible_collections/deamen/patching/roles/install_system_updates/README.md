# install_system_updates

Apply OS updates to RHEL 9/10 (dnf) and Fedora 41+ (dnf5) hosts in fixed phases, reboot when needed, check the host afterwards and record a run summary.

## Requirements

- RHEL 9 or 10, or Fedora 41 or later. Any other package manager fails the run before anything changes.
- Root on the managed host: run the role with `become: true`. Writing the summary file runs on the controller without `become`.
- Check mode is not supported. The role stops at its first task when run with `--check`.

## Run order

The order is fixed; hooks cannot change it.

1. **skip** (when `patching_skip`): write the summary with `status: skipped` and end the host. See [Skipping a host](#skipping-a-host).
2. **platform**: gather minimal facts, assert dnf or dnf5, install `dnf-plugins-core` or `dnf5-plugins` (for `needs-restarting`) and `procps-ng`. The install is left out in report-only mode.
3. **preflight** (when `patching_preflight`): free space for each path in `patching_preflight_min_free_mb`, wait for other `dnf`/`dnf5`/`yum`/`rpm` processes to finish, then `dnf check`.
4. **report-only** (when `patching_report_only`): list pending updates, write the summary and end the host. See [Report-only mode](#report-only-mode).
5. **pre_update**: record the running kernel, `dnf clean all`, then the `pre_update` hooks.
6. **download** (when `patching_download_first`): download updates without installing them.
7. **update**: install updates and register `patching_update_result`.
8. **post_update**: the `post_update` hooks.
9. **reboot**: run `needs-restarting -r` when updates were installed, then reboot according to `patching_reboot`.
10. **post_reboot**: report the kernel before and after; after a reboot, read the default boot kernel and the newest installed kernel; run the `post_reboot` hooks; fail if the running kernel is not the default and newest one (`patching_verify_kernel`); then check `patching_post_reboot_services`, `patching_post_reboot_ports` and `patching_post_reboot_urls`, in that order.
11. **summary**: always, including after a failure.

The post-reboot phase runs even when the host did not reboot, so cleanup in the `post_reboot` hooks always happens. Hooks can read `patching_rebooted` to tell the two cases apart.

## Skipping a host

Set `patching_skip: true` for a host (in its `host_vars`, for example) to leave it out of a run without removing it from the inventory. Set `patching_skip_reason` to say why; it is only read when `patching_skip` is true.

```yaml
patching_skip: true
patching_skip_reason: Change freeze until the quarter-end close
```

The role writes the summary with `status: skipped` and the reason in `skip_reason`, then ends the host with `meta: end_host`. Nothing else runs on it: no platform or preflight checks and no hooks. The host is not failed and the play carries on for the other hosts, but no later task in the play runs on the skipped host.

## Report-only mode

`patching_report_only: true` shows what a run would update without changing the host. After the platform and preflight checks the role:

- lists pending updates with `dnf check-update` (dnf) or `dnf5 check-upgrade` (dnf5), refreshing the repository metadata first, with `--security` when `patching_security_only` is set and `--exclude` for each glob in `patching_effective_excludes`
- records the pending package names in the summary's `packages`
- sets `reboot_required` when a pending package usually needs a reboot: `kernel`, `kernel-core`, `glibc`, `systemd`, `dbus` or `linux-firmware`
- writes the summary with `mode: report_only` and ends the host with `meta: end_host`

It does not install the role's tools (`dnf-plugins-core`/`dnf5-plugins`, `procps-ng`), run hooks, clean the package cache, download or install updates, or reboot. When `pgrep` is not installed, the preflight wait for other package transactions is skipped. Report-only mode is the way to preview a run, since check mode is not supported.

## Hooks

`patching_pre_update_hooks`, `patching_post_update_hooks` and `patching_post_reboot_hooks` are lists of task files, included in list order in their phase. Use them for steps a service needs around patching, such as stopping it before the update or checking it afterwards.

```yaml
patching_pre_update_hooks:
  - "{{ playbook_dir }}/patching/stop_app.yml"
patching_post_reboot_hooks:
  - "{{ playbook_dir }}/patching/start_app.yml"
```

Hooks can read these facts:

| Fact | Meaning |
| --- | --- |
| `patching_kernel_before` | Kernel running before the update |
| `patching_update_result` | Result of the install task |
| `patching_update_failed` | `true` when the download or install failed |
| `patching_rebooted` | `true` when the role rebooted the host |
| `patching_effective_excludes` | Package globs excluded from this run |

## Failure handling

- A failure in platform, preflight or report-only stops the host before anything changed. No hooks run.
- When the download or install fails, the role sets `patching_update_failed: true`, skips the reboot, runs the `post_update` hooks and then the `post_reboot` hooks so they can undo their `pre_update` changes, skips the kernel and health checks, and fails the host. Hooks must handle `patching_update_failed`, for example by starting a service again instead of leaving it stopped for a reboot that will not happen.
- When the kernel check fails, the `post_reboot` hooks still run before the host fails.
- If the host does not come back within `patching_reboot_timeout`, nothing more can run on it. Check by hand what the `post_reboot` hooks would have done.

## Run summary

The role always sets the `patching_summary` fact and prints it:

```json
{
  "excludes": [],
  "failed_step": "none",
  "finished": "2026-11-10T22:04:51.120934+00:00",
  "host": "web1.example.com",
  "kernel_after": "6.12.0-55.el10.x86_64",
  "kernel_before": "6.12.0-48.el10.x86_64",
  "mode": "update",
  "packages": ["Installed: kernel-core-6.12.0-55.el10.x86_64"],
  "reboot_required": true,
  "rebooted": true,
  "skip_reason": "none",
  "started": "2026-11-10T21:58:02.871233+00:00",
  "status": "ok",
  "update_failed": false
}
```

`mode` is `update`, or `report_only` with `patching_report_only`. `status` is one of:

| Status | Meaning |
| --- | --- |
| `ok` | Updates were installed, or in report-only mode, updates are pending |
| `no_updates` | Nothing to install, or in report-only mode, nothing pending |
| `failed` | The run failed; `failed_step` names the step (`none` otherwise) |
| `skipped` | `patching_skip` was set; `skip_reason` holds `patching_skip_reason` (`none` otherwise) |

`packages` lists the updated packages, or the pending package names in report-only mode. In report-only mode `reboot_required` says whether a pending package usually needs a reboot. With `patching_summary_write: true` the summary is also written to `patching_summary_dir/<inventory_hostname>.json` on the controller.

## Role variables

All variables, their types and defaults are documented in [`meta/argument_specs.yml`](meta/argument_specs.yml) and validated when the role starts. Run `ansible-doc -t role deamen.patching.install_system_updates` to read them.

## Example playbook

```yaml
- name: Patch web servers
  hosts: webservers
  become: true
  serial: 1
  tasks:
    - name: Install system updates
      ansible.builtin.include_role:
        name: deamen.patching.install_system_updates
      vars:
        patching_exclude_packages:
          - nginx*
        patching_post_reboot_services:
          - nginx.service
        patching_post_reboot_urls:
          - url: http://127.0.0.1/
            status: 200
```

## License

GPL-3.0-or-later
