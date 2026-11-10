# patching_fleet_report

Aggregate the per-host `patching_summary` facts of a patching run into one fleet report on the controller: counts per outcome, a per-host table, a `patching_fleet_report` fact and two report files.

## Requirements

- Runs on the controller only. Use it as the last play of the patching playbook with `hosts: localhost`, `become: false` and `gather_facts: false`.
- The patching plays earlier in the same playbook run `deamen.patching.install_system_updates`, which sets `patching_summary` on each host.

## Why a separate final play

The report must see every host of the run. A `run_once` task inside the patching play cannot do that when the play uses `serial`:

- `run_once` runs once per batch and only sees the hosts of the current batch.
- When every host in the last batch fails, no host is left to run the `run_once` task, so the report never runs, which is exactly the run you most need it for.

A final play on `localhost` runs after all batches. Facts set on a host survive into later plays even after the host failed, so failed hosts still report the summary they recorded.

Ansible skips every later play, this one included, when it aborts the playbook: `max_fail_percentage` exceeded, `any_errors_fatal` tripped, or every host of a batch failed or was unreachable. To get a report for runs that fail, rescue the patching role's failure in the patching play and stop patching further hosts yourself, then fail the run after the report. [`examples/patch_hosts.yml`](../../examples/patch_hosts.yml) does this.

## Outcomes

Each host in `patching_fleet_report_hosts` gets one status, checked in this order:

| Status | When |
| --- | --- |
| `unreachable` | The host has no `patching_summary`: it was unreachable, failed before the role ran, lost its connection during the run (for example a reboot that did not come back), or is not in the inventory |
| `skipped` | The summary `status` is `skipped`; the report keeps `skip_reason` |
| `failed` | The summary `status` is `failed`; the report keeps `failed_step` |
| `report_only` | The summary `mode` is `report_only`; `package_count` is the number of pending updates |
| `updated` | The summary `status` is `ok` |
| `no_updates` | Anything else, normally summary `status` `no_updates` |

`rebooted` is counted separately from the summary's `rebooted` flag. Keys a summary does not have, such as `skip_reason` or `profiles`, fall back to `none` or an empty list.

## Output

- Prints the counts (with skip reasons, failed steps and unreachable host names) and a per-host table.
- Sets the fact `patching_fleet_report`:

  ```json
  {
    "counts": {
      "failed": 1,
      "no_updates": 3,
      "rebooted": 6,
      "report_only": 0,
      "skipped": 1,
      "total": 12,
      "unreachable": 0,
      "updated": 7
    },
    "generated": "2026-11-10T22:31:07.514027+00:00",
    "hosts": [
      {
        "failed_step": "none",
        "finished": "2026-11-10T22:04:51.120934+00:00",
        "host": "web1.example.com",
        "kernel_after": "6.12.0-55.el10.x86_64",
        "kernel_before": "6.12.0-48.el10.x86_64",
        "mode": "update",
        "package_count": 42,
        "profiles": [],
        "rebooted": true,
        "skip_reason": "none",
        "started": "2026-11-10T21:58:02.871233+00:00",
        "status": "updated"
      }
    ]
  }
  ```

- Writes `patching_summary_dir/fleet-<UTC timestamp>.json` with the same content, and `fleet-<UTC timestamp>.md` with the counts and the per-host table as markdown. The directory is created when missing. Each run writes new files, so older reports are kept. Writing them is not reported as a change, since they record the run rather than manage state.

## Role variables

All variables are documented in [`meta/argument_specs.yml`](meta/argument_specs.yml) and validated when the role starts. Run `ansible-doc -t role deamen.patching.patching_fleet_report` to read them.

| Variable | Default | Description |
| --- | --- | --- |
| `patching_fleet_report_hosts` | required | Inventory hostnames to report on, usually the group the patching plays targeted |
| `patching_summary_dir` | `{{ playbook_dir }}/patching_reports` | Directory the report files are written to; the same variable and default as `install_system_updates` uses for the per-host summaries |

## Example playbook

A minimal run. With `max_fail_percentage: 0`, a failed host ends the playbook before the report; see [`examples/patch_hosts.yml`](../../examples/patch_hosts.yml) for a run that reports failures too.

```yaml
- name: Patch servers in batches
  hosts: patch_targets
  become: true
  max_fail_percentage: 0
  serial:
    - 1
    - 25%
  tasks:
    - name: Install system updates
      ansible.builtin.include_role:
        name: deamen.patching.install_system_updates

- name: Report on the patching run
  hosts: localhost
  become: false
  gather_facts: false
  tasks:
    - name: Write the fleet report
      ansible.builtin.include_role:
        name: deamen.patching.patching_fleet_report
      vars:
        patching_fleet_report_hosts: "{{ groups['patch_targets'] }}"
```

## License

GPL-3.0-or-later
