# Ansible Collection - deamen.gpg

Install and manage GPG

## Playbooks

All playbooks need `config_gpg_user`; GPG packages are installed with `become`. `config_gpg` and `generate_gpg_key` target `localhost`; `configure_gpg_for_user` targets inventory hosts.

| Playbook | Description |
|----------|-------------|
| `deamen.gpg.config_gpg` | Install GPG and run `config_gpg`. Pass the `config_gpg_*` variables to import a key. |
| `deamen.gpg.generate_gpg_key` | As above, then prompt for a passphrase and generate a key pair (`gpg_key_real_name`, `gpg_key_email`). |
| `deamen.gpg.configure_gpg_for_user` | Install GPG and run `config_gpg` on inventory hosts (`hosts: all`; limit with `-l`). No key is imported unless `config_gpg_import_secret_key` or `config_gpg_import_public_key` is set. |
