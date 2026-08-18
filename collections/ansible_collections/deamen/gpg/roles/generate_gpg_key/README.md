generate_gpg_key
================

Generate GPG keys with an Ed25519 primary signing key and a Curve25519 encryption subkey.

Requirements
------------

`gpg` must be installed on the target host.

Role Variables
--------------

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
|gpg_key_real_name|The real name of the GPG key owner|N.A.|"Jane Doe"|
|gpg_key_email|The email address of the GPG key owner|N.A.|"jane.doe@example.com"|
|gpg_key_passphrase|The passphrase to protect the GPG key. If omitted or empty, the key is generated without passphrase protection|N.A.|"s3cr3tP@ss"|
|gpg_params_path|The temporary path for the GPG batch params file|"/tmp/gpg_params"|"/tmp/my_gpg_params"|

Dependencies
------------

No role dependencies.

Example Playbook
----------------

```yaml
- name: Generate GPG key
  hosts: localhost

  tasks:
    - name: Import the deamen.gpg.generate_gpg_key role
      ansible.builtin.import_role:
        name: deamen.gpg.generate_gpg_key
      vars:
        gpg_key_real_name: Jane Doe
        gpg_key_email: jane.doe@example.com
        gpg_key_passphrase: "{{ vault_gpg_passphrase }}"
```

License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
