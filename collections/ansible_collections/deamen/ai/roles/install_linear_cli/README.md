install_linear_cli
==================

Install [linear-cli](https://github.com/schpet/linear-cli), the command-line interface for Linear.

The role runs the `linear-installer.sh` published with the `linear_cli_version` release. The installer verifies the tarball against the sha256 embedded in it, and `LINEAR_UNMANAGED_INSTALL` makes it install the `linear` binary straight into `linear_cli_install_dir` without editing `PATH`, shell rc files or installing the self-updater. The download is skipped when the installed binary already reports `linear_cli_version`.

The role also installs the linear-cli [skill](https://github.com/schpet/linear-cli#skills), which helps AI agents use the CLI. As the connecting user, it downloads the GitHub source archive of the `linear_cli_version` tag and copies its `skills/linear-cli` directory into `~/.claude/skills/linear-cli`, where Claude Code loads it as a personal skill. The skill comes from the same tag as the binary, so it describes the installed version. `~/.claude/skills/linear-cli/.linear-cli-version` records the version; the copy is skipped while it matches, and the directory is replaced when `linear_cli_version` changes. Neither Claude Code nor Node.js is needed. For another agent, copy or link `~/.claude/skills/linear-cli` into that agent's skills directory.

Earlier releases installed the skill as the `linear-cli@linear-cli` Claude Code plugin, and deployed `install-linear-cli-skill`, which ran `npx skills add`. linear-cli removed the plugin upstream, so the role now removes `install-linear-cli-skill` from `linear_cli_install_dir`. Remove a leftover plugin with `claude plugin uninstall linear-cli@linear-cli` and `claude plugin marketplace remove linear-cli`.

Requirements
------------

Fact gathering must be enabled; the role uses `ansible_facts['architecture']` to pick the tarball. Only `x86_64` and `aarch64` are published.

Role Variables
--------------

| Variable | Default | Description |
| --- | --- | --- |
| `linear_cli_version` | `v3.1.0` | Release tag to install |
| `linear_cli_install_dir` | `/usr/local/bin` | Directory the `linear` binary is installed into |
| `linear_cli_claude_code_skill` | `true` | Copy the skill into `~/.claude/skills/linear-cli` of the connecting user |

Dependencies
------------

None. The role installs `tar` and `xz`, which the installer needs to unpack the release archive, and `gzip`, which unpacking the source archive for the skill needs.

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
