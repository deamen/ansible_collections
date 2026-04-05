Install Podman Role
=========

Role for installing Podman and related packages on supported Linux distributions.

Requirements
------------

Nothing yet

Role Variables
--------------

The following variables can be used to customize this role. Default values are
defined in this role's `defaults/main.yml` and may vary by distribution:

- `podman_default_pkgs`:
  List of base Podman packages to install. The default is an OS-specific list
  of packages required to run Podman.

- `podman_docker_pkgs`:
  List of additional packages used to emulate Docker tooling (for example,
  providing a Docker-compatible CLI on top of Podman). Defaults are
  OS-specific.

- `podman_user`:
  User account under which Podman-related configuration may be applied
  (for example, setting up user-level containers or configuration files).
  The default is defined in `defaults/main.yml`.

- `emulate_docker`:
  Boolean flag that controls whether Docker emulation should be enabled
  (for example, installing Docker-compatible wrappers or packages). The
  default is `false` (see `defaults/main.yml`).

Dependencies
------------

- deamen.general.check_is_container

Example Playbook
----------------

```yaml
---
- hosts: all
  become: true

  tasks:
    - name: Install Podman
      ansible.builtin.import_role:
        name: deamen.podman.install_podman
```

License
-------

GPLv3

Author Information
------------------

https://github.com/deamen
