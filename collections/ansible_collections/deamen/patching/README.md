# Deamen Patching Collection

This repository contains the `deamen.patching` Ansible Collection.

<!--start requires_ansible-->
<!--end requires_ansible-->

## What this collection does

Patch RHEL 9/10 (dnf) and Fedora 41+ (dnf5) hosts in fixed phases: preflight checks, pre-update, download, update, post-update, reboot and post-reboot, followed by a run summary. Service-specific work plugs in through hooks, so the collection itself stays generic.

## Included content

<!--start collection content-->
### Roles

| Name | Description |
| --- | --- |
| [deamen.patching.install_system_updates](roles/install_system_updates/README.md) | Apply OS updates in fixed phases, reboot when needed, verify the host and record a run summary. |
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

## License

GNU General Public License v3.0 or later. See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) for the full text.
