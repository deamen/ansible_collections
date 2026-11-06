install_himalaya
================

Install the [himalaya](https://github.com/pimalaya/himalaya) email CLI for the connecting user and deploy a minimal configuration.

The role deploys `~/.local/bin/install_himalaya.sh`, which runs the upstream `install.sh` with `PREFIX=~/.local`, and runs it unless `~/.local/bin/himalaya` already exists. It then deploys `~/.config/himalaya/config.toml` with one IMAP account. Every task runs as the connecting user without privilege escalation.

Requirements
------------

- Fact gathering must be enabled; the role uses `ansible_facts['env']['HOME']`.
- `curl`, `gzip` and `tar` must be installed; the role checks for them but does not install them.
- The default password command uses `/usr/local/bin/gpg_cat.sh` from `deamen.ansible.config_ansible_runtime_env` and reads the password from `himalaya_password_gpg_file`, which you create yourself, for example:

  ```sh
  printf '%s' 'my-password' | gpg --encrypt --recipient <key-id> --output ~/.config/himalaya/selfhosted.gpg
  ```

Role Variables
--------------

| Variable | Default | Description |
| --- | --- | --- |
| `himalaya_account_name` | `selfhosted` | Name of the account in `config.toml` |
| `himalaya_display_name` | `Your Name` | Display name used when sending mail |
| `himalaya_email` | `you@mail.example.com` | Email address of the account |
| `himalaya_imap_server` | `imaps://mail.example.com:993` | IMAP server URL; use `imap://host:143` with `himalaya_imap_starttls` |
| `himalaya_imap_starttls` | `false` | Upgrade the IMAP connection with STARTTLS |
| `himalaya_imap_username` | `himalaya_email` | IMAP login name |
| `himalaya_mailbox_aliases` | `inbox: INBOX`, `sent: Sent`, `drafts: Drafts`, `trash: Trash` | Mailbox aliases mapped to IMAP folders |
| `himalaya_password_command` | `/usr/local/bin/gpg_cat.sh --gpg_file <himalaya_password_gpg_file>` | Command that prints the IMAP password |
| `himalaya_password_gpg_file` | `~/.config/himalaya/<himalaya_account_name>.gpg` | GPG encrypted password file for the default command |

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Install himalaya
  hosts: localhost
  connection: local
  become: false
  tasks:
    - name: Install himalaya for the current user
      ansible.builtin.import_role:
        name: deamen.general.install_himalaya
      vars:
        himalaya_display_name: Jane Doe
        himalaya_email: jane@example.org
        himalaya_imap_server: imaps://mail.example.org:993
```

The collection also ships `deamen.general.install_himalaya`, a playbook that runs the role against localhost:

```sh
ansible-playbook deamen.general.install_himalaya -e himalaya_email=jane@example.org
```

License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
