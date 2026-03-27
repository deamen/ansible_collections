Install Podman Role
=========

Role for installing Podman and related packages on supported Linux distributions.

Requirements
------------

Nothing yet

Role Variables
--------------

No role-specific variables yet.

Dependencies
------------

Nothing yet

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
