install_linear_cli
==================

Install [linear-cli](https://github.com/schpet/linear-cli), the command-line interface for Linear.

The role runs the `linear-installer.sh` published with the `linear_cli_version` release. The installer verifies the tarball against the sha256 embedded in it, and `LINEAR_UNMANAGED_INSTALL` makes it install the `linear` binary straight into `linear_cli_install_dir` without editing `PATH`, shell rc files or installing the self-updater. The download is skipped when the installed binary already reports `linear_cli_version`.

The role also installs the linear-cli [skill](https://github.com/schpet/linear-cli#skills), which helps AI agents use the CLI:

- **Claude Code**: as the connecting user, it adds the `schpet/linear-cli` marketplace and installs the `linear-cli@linear-cli` plugin, unless they are already present. This is skipped when `linear_cli_claude_code_bin` does not exist, so install Claude Code (for example with `deamen.ai.install_claude_code`) before this role. Update the plugin with `claude plugin marketplace update linear-cli` and `claude plugin update linear-cli@linear-cli`.
- **Other agents**: it deploys `install-linear-cli-skill` into `linear_cli_install_dir`. Run it when needed; it runs `npx skills add schpet/linear-cli` through [skills.sh](https://skills.sh/) and passes its arguments on. It needs Node.js and npm, which the role does not install.

Requirements
------------

Fact gathering must be enabled; the role uses `ansible_facts['architecture']` to pick the tarball. Only `x86_64` and `aarch64` are published.

Role Variables
--------------

| Variable | Default | Description |
| --- | --- | --- |
| `linear_cli_version` | `v3.1.0` | Release tag to install |
| `linear_cli_install_dir` | `/usr/local/bin` | Directory the `linear` binary and `install-linear-cli-skill` are installed into |
| `linear_cli_claude_code_skill` | `true` | Install the skill into Claude Code for the connecting user |
| `linear_cli_claude_code_bin` | `~/.local/bin/claude` | Claude Code binary used to install the skill |
| `linear_cli_skills_installer` | `true` | Deploy `install-linear-cli-skill` for other agents |

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
