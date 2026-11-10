# Deamen Patching Collection

This repository contains the `deamen.patching` Ansible Collection.

<!--start requires_ansible-->
<!--end requires_ansible-->

## What this collection does

Patch RHEL 9/10 (dnf) and Fedora 41+ (dnf5) hosts in fixed phases: preflight checks, pre-update, download, update, post-update, reboot and post-reboot, followed by a run summary. Service-specific work plugs in through profiles (roles you write in your own collections) and hooks (task files), so the collection itself stays generic.

## Included content

<!--start collection content-->
### Roles

| Name | Description |
| --- | --- |
| [deamen.patching.install_system_updates](roles/install_system_updates/README.md) | Apply OS updates in fixed phases, reboot when needed, verify the host and record a run summary. |
| [deamen.patching.patching_fleet_report](roles/patching_fleet_report/README.md) | Aggregate the per-host run summaries into a fleet report on the controller. |
| [deamen.patching.patching_profile_example](roles/patching_profile_example/README.md) | Starter patching profile that documents the profile contract; copy it to write profiles for your services. |
<!--end collection content-->

## Using this collection

```bash
ansible-galaxy collection install deamen.patching
```

Or via `requirements.yml`:

```yaml
collections:
  - name: deamen.patching
```

## Quickstart

```yaml
- name: Patch servers one at a time
  hosts: servers
  become: true
  serial: 1
  tasks:
    - name: Install system updates
      ansible.builtin.include_role:
        name: deamen.patching.install_system_updates
```

## Patching at scale

`install_system_updates` patches the hosts of the current play batch; it does not coordinate hosts with each other. Ordering, batch sizes and when to stop are set by the playbook. [`examples/patch_hosts.yml`](examples/patch_hosts.yml), with its [inventory](examples/inventory.yml), `group_vars/`, `hooks/` and `tasks/`, shows a full run:

- **Canary, then batches.** `serial: [1, "25%"]` patches one host first, then a quarter of the rest at a time; `order: sorted` gives the same sequence on every run.
- **Stop at the first failure.** When a host fails, no further host is patched. Use `max_fail_percentage: 0` (and `any_errors_fatal: true`) only as a backstop: when either one trips, or every host of a batch fails, Ansible ends the whole playbook and later plays, including the fleet report, never run. The example instead rescues the role's failure in `tasks/patch_host.yml`, skips every host after it with a recorded reason, and fails the run in the last play after the report is written.
- **Clusters.** Nodes that must be patched in a set order go in one play per role, each with `serial: 1`. A short discovery play first sorts them with `ansible.builtin.group_by` (for example into `cluster_replica` and `cluster_leader`, from a host var or from asking the service), then the replica play runs before the leader play. Because patching stops at the first failed host, the leader is not patched after a replica failed.
- **Service-level work belongs in profiles.** Draining a node, failing over, or setting monitoring downtime are steps around one service, not around the OS update. Put them in a profile role enabled with `patching_profiles` (for example in `group_vars`); a profile can `delegate_to` a load balancer, the cluster leader or a monitoring host. Quick one-off steps can be hooks.
- **Fleet report last.** Finish with a play on `localhost` that runs [`deamen.patching.patching_fleet_report`](roles/patching_fleet_report/README.md) over the patched group. It reads each host's `patching_summary`, so hosts that failed are included, and lists hosts without a summary as unreachable. It is a separate play rather than a `run_once` task inside the patching play because, with `serial`, `run_once` only sees the current batch and does not run when every host of the last batch failed.

If every host of a batch is unreachable, Ansible ends the playbook before the report play. The per-host summaries written with `patching_summary_write: true` are still in `patching_summary_dir`.

## License

GNU General Public License v3.0 or later. See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) for the full text.
