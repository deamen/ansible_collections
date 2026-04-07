config_gpg
==========

Configure GPG for a given user: ensures the `.gnupg` directory exists, deploys
`gpg-agent.conf`, imports the private key (if not already present), and sets
ultimate owner-trust on the key's fingerprint.

Requirements
------------

- `gnupg2` and a `pinentry` program must be installed on the target host (see the
  `deamen.gpg.install_gpg` role).
- The GPG private key file must already be present on the target host at the path
  defined by `config_gpg_private_key_path` before the role is run.

Role Variables
--------------

| Variable | Default | Description |
|---|---|---|
| `config_gpg_fingerprint` | `''` | Full fingerprint of the GPG key to import and trust. |
| `config_gpg_private_key_path` | `/home/{{ config_gpg_user }}/.gnupg/private_gpg.key` | Path to the private key file on the **managed host**. Removed after import. |
| `config_gpg_user` | `''` | Username that owns the GPG keyring. |

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Configure GPG for alice
  hosts: workstations
  roles:
    - role: deamen.gpg.config_gpg
      vars:
        config_gpg_fingerprint: 'AABBCCDDEEFF00112233445566778899AABBCCDD'
        config_gpg_user: alice
```

License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
