install_claude_code
===================

Install the [Claude Code](https://code.claude.com/docs) CLI for a user with the native installer.

The role downloads `https://claude.ai/install.sh` and runs it as `claude_code_user`. The installer checks the binary against the sha256 in the release manifest, puts the `claude` launcher in `~/.local/bin` of that user and the binary under `~/.local/share/claude`. Claude Code updates itself after installation.

The installer is skipped when `claude` is already installed for the user and `claude_code_version` is a channel (`stable` or `latest`), or when the installed `claude` reports the exact `claude_code_version`.

Requirements
------------

- Fact gathering must be enabled; the role uses `ansible_facts['architecture']` and `ansible_facts['user_id']`. Only `x86_64` and `aarch64` are supported.
- `claude_code_user` must already exist.
- When `claude_code_user` is not the connecting user, the role becomes that user, so the connecting user needs privilege escalation to it.

Role Variables
--------------

| Variable | Default | Description |
| --- | --- | --- |
| `claude_code_user` | required | Existing user to install Claude Code for |
| `claude_code_version` | `stable` | Release channel (`stable` or `latest`) or an exact version such as `2.1.0` |

Dependencies
------------

None. The role installs `curl`, which the installer uses to download the binary.

Example Playbook
----------------

```yaml
- name: Install Claude Code
  hosts: all
  tasks:
    - name: Install Claude Code for vagrant
      ansible.builtin.import_role:
        name: deamen.ai.install_claude_code
      vars:
        claude_code_user: vagrant
```

License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
