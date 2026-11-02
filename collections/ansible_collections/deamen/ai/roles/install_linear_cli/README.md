install_linear_cli
==================

Install [linear-cli](https://github.com/schpet/linear-cli), the command-line interface for Linear.

The role runs the `linear-installer.sh` published with the `linear_cli_version` release. The installer verifies the tarball against the sha256 embedded in it, and `LINEAR_UNMANAGED_INSTALL` makes it install the `linear` binary straight into `linear_cli_install_dir` without editing `PATH`, shell rc files or installing the self-updater. The role does nothing when the installed binary already reports `linear_cli_version`.

Requirements
------------

Fact gathering must be enabled; the role uses `ansible_facts['architecture']` to pick the tarball. Only `x86_64` and `aarch64` are published.

Role Variables
--------------

| Variable | Default | Description |
| --- | --- | --- |
| `linear_cli_version` | `v3.1.0` | Release tag to install |
| `linear_cli_install_dir` | `/usr/local/bin` | Directory the `linear` binary is installed into |

Dependencies
------------

None. The role installs `tar` and `xz`, which the installer needs to unpack the archive.

Example Playbook
----------------

```yaml
- name: Install linear-cli
  hosts: all
  tasks:
    - name: Install linear-cli
      ansible.builtin.import_role:
        name: deamen.ai.install_linear_cli
```

Or run the bundled playbook:

```bash
ansible-playbook deamen.ai.install_linear_cli
```

License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
