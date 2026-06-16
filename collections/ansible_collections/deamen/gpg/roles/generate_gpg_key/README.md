generate_gpg_key
================

An Ansible role that generates an Ed25519 primary GPG key and an encryption subkey (Curve25519) in a non-interactive way. The role is intentionally small and opinionated: it requires a name and email and will skip creation when a secret key for the given email already exists.

Requirements
------------

- GnuPG must be installed on the target host (`gpg` or `gpg2`).
- Run the task as the user that should own the key (use `become_user`) so the key is created in the intended keyring.

Role Variables
--------------

- `gpg_key_real_name` (string, required) — Real name for the UID (e.g. "Alice Example").
- `gpg_key_email` (string, required) — Email address for the UID and the lookup key.
- `gpg_params_path` (string, optional) — Temporary path for the GPG batch parameter file. Default: `/tmp/gpg_params`.

Dependencies
------------

- System: `gpg`/`gnupg` must be installed.
- No role dependencies.

Example Playbook
----------------

Generate a key as a specific user (recommended — keys are created in that user's home):

```yaml
- name: Generate GPG key for user
  hosts: all
  become: true
  tasks:
    - name: Generate GPG key for alice
      ansible.builtin.import_role:
        name: deamen.gpg.generate_gpg_key
      vars:
        gpg_key_real_name: "Alice Example"
        gpg_key_email: "alice@example.com"
      become: true
      become_user: alice
```

If running the playbook as the target user already (no become_user):

```yaml
- name: Generate GPG key as current user
  hosts: all
  become: true
  tasks:
    - name: Generate GPG key as current user
      ansible.builtin.import_role:
        name: deamen.gpg.generate_gpg_key
      vars:
        gpg_key_real_name: "Alice Example"
        gpg_key_email: "alice@example.com"
```


License
-------

GPL-3.0-or-later

Author Information
------------------

stang <stang@mmz.au>
