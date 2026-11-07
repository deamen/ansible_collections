configure_keyring
=================

Install a GNOME Keyring Secret Service that a user unlocks on demand, for CLIs that store credentials through libsecret on containers and headless hosts without a desktop session.

The role installs the D-Bus session bus, gnome-keyring and libsecret, and deploys:

- `/usr/local/bin/keyring-unlock`, which starts a session bus and gnome-keyring for the calling user and unlocks the login keyring with a password typed at the prompt. The first run creates the login keyring with that password. No password is stored.
- `/etc/profile.d/keyring-bus.sh`, which exports `DBUS_SESSION_BUS_ADDRESS` in login shells once the bus is running.
- `/etc/tmpfiles.d/keyring.conf`, which creates `/run/user/<uid>` for `keyring_user` at boot, since an unprivileged user cannot create it. The role also creates the directory immediately.

By default the keyring is stateless: keyring-unlock keeps it under `/run/user/<uid>`, so it is discarded on shutdown. Set `keyring_persistent` to keep it in `~/.local/share/keyrings`.

Requirements
------------

- Fact gathering must be enabled; the default `keyring_user` uses `ansible_facts['user_id']`.
- Package names target the Red Hat family.
- Privilege escalation for the package, `/usr/local/bin`, `/etc` and `/run` tasks.

Role Variables
--------------

| Variable | Default | Description |
| --- | --- | --- |
| `keyring_create_runtime_dir` | `true` | Create `/run/user/<uid>` now and at boot through tmpfiles.d; set `false` where logind creates it |
| `keyring_persistent` | `false` | Keep the login keyring in `~/.local/share/keyrings` instead of `/run` |
| `keyring_user` | `ansible_facts['user_id']` | Non-root user the runtime directory is created for |

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Configure the keyring
  hosts: all
  become: false
  tasks:
    - name: Configure the keyring for deamen
      ansible.builtin.import_role:
        name: deamen.general.configure_keyring
      vars:
        keyring_user: deamen
```

The collection also ships `deamen.general.configure_keyring`, a playbook that runs the role against localhost for the user running it:

```sh
ansible-playbook deamen.general.configure_keyring
```

Then, as that user:

```sh
keyring-unlock
secret-tool store --label test service test
```

License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
