config_gpg
==========

Configure GPG for a user: create the `.gnupg` directory, deploy `gpg-agent.conf`, optionally import a public key, or import a private key and set ultimate owner trust for the specified fingerprint.

When the secret key for `config_gpg_fingerprint` has an authentication key, the role can make `gpg-agent` the user's SSH agent (SSH-via-GPG). It adds `enable-ssh-support` to `gpg-agent.conf`, lists the authentication keygrips in `~/.gnupg/sshcontrol`, and deploys `~/.bashrc.d/gpg-ssh.sh`, which points `SSH_AUTH_SOCK` at `gpg-agent`. A key can authenticate when `gpg --list-secret-keys --with-colons <fingerprint>` shows `a` in the capabilities field (field 12) of a `sec` or `ssb` record that is not expired or revoked and whose secret part is present. When SSH support is off, the role leaves `enable-ssh-support` out and removes `~/.bashrc.d/gpg-ssh.sh`.

Requirements
------------

`gpg` must be installed on the target host.

For SSH support, `~/.bashrc` must source the files in `~/.bashrc.d`, as Fedora's default `.bashrc` does.

Role Variables
--------------

`config_gpg_user` is required and must identify the OS user for whom GPG is being configured.
`config_gpg_fingerprint` is required when either import option is `true`. When importing is disabled, the role internally uses `''` and the variable does not need to be specified.

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
|config_gpg_default_cache_ttl|The default time, in seconds, that a cached passphrase remains available to `gpg-agent`|7200 (2 hours)|300|
|config_gpg_fingerprint|The full fingerprint of the GPG key to configure when either import option is `true`|Required when importing|"7C694A119306CD575A5E129EF3D29D4FB47F0B00"|
|config_gpg_import_public_key|Whether to import the public key from `config_gpg_public_key`|false|true|
|config_gpg_import_secret_key|Whether to import the private key and configure owner trust|false|true|
|config_gpg_max_cache_ttl|The maximum time, in seconds, that a cached passphrase remains available to `gpg-agent`|43200 (12 hours)|3600|
|config_gpg_public_key|Armored public key content to import when `config_gpg_import_public_key` is `true`|Required when importing|"-----BEGIN PGP PUBLIC KEY BLOCK-----"|
|config_gpg_ssh_support|`auto` makes `gpg-agent` the SSH agent when the secret key has an authentication key. `true` does the same but fails when there is no authentication key, which needs `config_gpg_fingerprint` and an import option. `false` never makes `gpg-agent` the SSH agent|auto|true|
|config_gpg_secret_key_path|Path to the private key file to import. The file is removed after a successful import|"/home/{{ config_gpg_user }}/.gnupg/private_gpg.key"|"/tmp/private_gpg.key"|
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
        config_gpg_import_secret_key: true
        config_gpg_fingerprint: 7C694A119306CD575A5E129EF3D29D4FB47F0B00
        config_gpg_default_cache_ttl: 300
        config_gpg_secret_key_path: /tmp/private_gpg.key
        config_gpg_max_cache_ttl: 3600
        config_gpg_user: deploy
        # Use config_gpg_import_public_key with config_gpg_public_key to import only a public key
```

License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
