# manage_subuid_subgid Module

## Description

The `manage_subuid_subgid` module manages subordinate UID and GID ranges for users to enable rootless container functionality with Podman and other container runtimes.

This module:
- Automatically calculates the next available subordinate UID/GID range
- Adds entries to `/etc/subuid` and `/etc/subgid` using `usermod`
- Is fully idempotent - won't modify existing entries
- Validates inputs and provides detailed error messages

## Requirements

- Linux system with `usermod` command (part of shadow-utils package)
- Root/sudo privileges to modify `/etc/subuid` and `/etc/subgid`
- Python 3.9+

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| username | str | yes | - | The username for which to add subordinate UID and GID ranges |
| range_size | int | no | 65536 | The number of subordinate IDs to allocate for the user |

## Return Values

| Key | Type | Description |
|-----|------|-------------|
| changed | bool | Whether the module made any changes |
| msg | str | A message describing what happened |
| subuid_range | dict | The subordinate UID range (keys: start, end) |
| subgid_range | dict | The subordinate GID range (keys: start, end) |

## Examples

### Basic Usage

```yaml
- name: Add subuid and subgid ranges for user podman
  deamen.podman.manage_subuid_subgid:
    username: podman
```

### Custom Range Size

```yaml
- name: Add ranges with custom size
  deamen.podman.manage_subuid_subgid:
    username: containeruser
    range_size: 100000
```

### Complete Playbook Example

```yaml
---
- name: Setup rootless container user
  hosts: all
  become: true
  tasks:
    - name: Create podman user
      ansible.builtin.user:
        name: podman
        uid: 5000
        group: podman
        create_home: yes
        shell: /bin/bash

    - name: Configure subordinate ranges
      deamen.podman.manage_subuid_subgid:
        username: podman
      register: subid_result

    - name: Display configured ranges
      ansible.builtin.debug:
        msg: >
          Configured subuid: {{ subid_result.subuid_range.start }}-{{ subid_result.subuid_range.end }},
          subgid: {{ subid_result.subgid_range.start }}-{{ subid_result.subgid_range.end }}

    - name: Enable linger for user
      ansible.builtin.command:
        cmd: loginctl enable-linger podman
      changed_when: true
```

## Check Mode

The module supports Ansible's check mode (dry-run). When run with `--check`, it will:
- Check if the user already has subordinate ranges configured
- Calculate what ranges would be assigned
- Report what changes would be made
- **NOT** actually modify `/etc/subuid` or `/etc/subgid`

Example:
```yaml
- name: Preview changes before applying
  deamen.podman.manage_subuid_subgid:
    username: podman
  check_mode: yes
```

## Notes

- The module uses the `usermod` command to add subordinate ranges, which automatically handles file locking and atomic updates
- Subordinate ID ranges start from 100000 by default to avoid conflicts with system IDs
- The module is idempotent - running it multiple times for the same user will not create duplicate entries
- Both subuid and subgid ranges are added in a single module execution
- Check mode is fully supported - use it to preview changes before applying them

## Author

Song Tang (@deamen)

## License

GNU General Public License v3.0+
