config_gpg
==========

Configure GPG for a user: create the `.gnupg` directory, deploy `gpg-agent.conf`, optionally import a private key, and set ultimate owner trust for the specified fingerprint.

Requirements
------------

`gpg` must be installed on the target host.

Role Variables
--------------

`config_gpg_user` is required and must identify the OS user for whom GPG is being configured.
`config_gpg_fingerprint` is required when `config_gpg_import_key` is `true`. When importing is disabled, the role internally uses `''` and the variable does not need to be specified.

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
|config_gpg_default_cache_ttl|The default time, in seconds, that a cached passphrase remains available to `gpg-agent`|60|300|
|config_gpg_fingerprint|The full fingerprint of the GPG key to configure when `config_gpg_import_key` is `true`|Required when importing|"CDCBA462EC82AB64E1025EA1995DB095D9F44CDE"|
|config_gpg_import_key|Whether to import the private key. Set to `false` to skip the import tasks when the key is already present|true|false|
|config_gpg_max_cache_ttl|The maximum time, in seconds, that a cached passphrase remains available to `gpg-agent`|120|3600|
|config_gpg_private_key_path|Path to the private key file to import|"/home/{{ config_gpg_user }}/.gnupg/private_gpg.key"|"/tmp/private_gpg.key"|
|config_gpg_user|The required OS user for whom GPG is being configured|Required|"deploy"|

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Configure GPG for deploy user
  hosts: all

  tasks:
    - name: Import the deamen.gpg.config_gpg role
      ansible.builtin.import_role:
        name: deamen.gpg.config_gpg
      vars:
        config_gpg_fingerprint: CDCBA462EC82AB64E1025EA1995DB095D9F44CDE
        config_gpg_default_cache_ttl: 300
        config_gpg_private_key_path: /tmp/private_gpg.key
        config_gpg_max_cache_ttl: 3600
        config_gpg_user: deploy
        # Set config_gpg_import_key: false to skip import when key already exists
```

License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
