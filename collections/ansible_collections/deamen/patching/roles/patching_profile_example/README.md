# patching_profile_example

Starter profile for [`deamen.patching.install_system_updates`](../install_system_updates/README.md). It documents the profile contract and only prints debug messages, so it is safe to enable as-is to see when each phase runs.

## What a profile is

A profile is a role that keeps all the patching steps for one service together, versioned and tested like any other role. `install_system_updates` runs every role listed in `patching_profiles` with `ansible.builtin.include_role`, once per extension phase, with `patching_phase` set to the phase:

| Phase | Runs | Typical work |
| --- | --- | --- |
| `excludes` | after preflight, before anything changes | append package globs to `patching_profile_excludes` |
| `pre_update` | after the metadata clean, before the download | stop the service, enter maintenance mode, add version locks |
| `post_update` | after the update, before the reboot decision | stop services that must stay down across the reboot |
| `post_reboot` | after the reboot (or when none was needed), before the generic checks | start the service, leave maintenance mode, remove version locks |

Profiles run in `patching_profiles` order, before the hooks of the same phase. The `excludes` phase runs profiles only.

## Writing a profile in your own collection

1. Copy this role into your collection as `roles/patching_profile_<service>/`, for example `example.infra.patching_profile_db`.
2. Keep `tasks/main.yml` as it is. It includes `tasks/<patching_phase>.yml` from the role when the file exists and does nothing otherwise, so the profile only implements the phases it needs.
3. Delete the phase files you do not need and fill in the others. Each file here explains what belongs in it and which facts are available.
4. Prefix the variables the profile owns with the profile name (`patching_profile_db_*`) and document them in `defaults/main.yml` and `meta/argument_specs.yml`. Keep `patching_phase` in the argument specs.
5. Enable the profile for the hosts that run the service, for example in `group_vars/db_servers.yml`:

   ```yaml
   patching_profiles:
     - example.infra.patching_profile_db
   ```

## Facts a profile can read

| Fact | Meaning |
| --- | --- |
| `patching_phase` | The phase being run |
| `patching_profile_excludes` | Package globs collected from profiles so far (`excludes` phase) |
| `patching_kernel_before` | Kernel running before the update (from `pre_update`) |
| `patching_update_result` | Result of the install task (from `post_update`; undefined when the update failed) |
| `patching_update_failed` | `true` when the download or update failed |
| `patching_rebooted` | `true` when the host rebooted (`post_reboot`) |

## Failure handling

When the download or update fails, `install_system_updates` skips the reboot and runs the `post_update` and then the `post_reboot` phase as cleanup before it fails the host. A profile that changed state in `pre_update` must undo it in one of them and must check `patching_update_failed`, for example to start a service again instead of leaving it stopped for a reboot that will not happen.

## Role variables

`patching_phase` is set by `install_system_updates` and validated against [`meta/argument_specs.yml`](meta/argument_specs.yml). Do not set it yourself.

## License

GPL-3.0-or-later
