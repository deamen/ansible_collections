# Ansible Collection - deamen.gpg

Install and manage GPG

## Playbooks

Both playbooks target `localhost` and need `config_gpg_user`; GPG packages are installed with `become`.

| Playbook | Description |
|----------|-------------|
| `deamen.gpg.config_gpg` | Install GPG and run `config_gpg` with longer gpg-agent cache TTLs. Pass the `config_gpg_*` variables to import a key. |
| `deamen.gpg.generate_gpg_key` | As above, then prompt for a passphrase and generate a key pair (`gpg_key_real_name`, `gpg_key_email`). |
