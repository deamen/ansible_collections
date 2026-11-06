install_proton_drive_cli
========================

Install the [Proton Drive CLI](https://github.com/ProtonDriveApps/sdk/blob/main/cli/README.md) for the connecting user.

The role reads the release manifest at `https://proton.me/download/drive/cli/version.json`, downloads the `proton-drive` binary for the host platform to `~/.local/bin/proton-drive` and verifies its SHA-512 checksum. A rerun replaces the binary when a newer release is published. It then deploys `~/.bashrc.d/proton_drive_cli.sh`, which exports `PROTON_DRIVE_CREDENTIALS_STORE`. Every task runs as the connecting user without privilege escalation.

Requirements
------------

- Fact gathering must be enabled; the role uses `ansible_facts['env']['HOME']` and `ansible_facts['architecture']`.
- `~/.bashrc` must source the files in `~/.bashrc.d`, as Fedora's default `.bashrc` does.
- The default `unsafe_file` credentials store keeps the session in plaintext `~/.local/share/proton-drive-cli/auth-session.json`. Use `keychain` where an OS secret store such as GNOME Keyring is available.

Sign in after the role has run, in a new login shell:

```sh
proton-drive auth login
```

Role Variables
--------------

| Variable | Default | Description |
| --- | --- | --- |
| `proton_drive_cli_credentials_store` | `unsafe_file` | Where the CLI keeps the session: `keychain`, `pass` or `unsafe_file` |
| `proton_drive_cli_platform` | `linux/x64` or `linux/arm64` | Platform to download, as named in the manifest, e.g. `linux/x64-musl` |
| `proton_drive_cli_release_channel` | `Stable` | Release category to install the latest release from |

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Install the Proton Drive CLI
  hosts: localhost
  connection: local
  become: false
  tasks:
    - name: Install the Proton Drive CLI for the current user
      ansible.builtin.import_role:
        name: deamen.proton.install_proton_drive_cli
```

The collection also ships `deamen.proton.install_proton_drive_cli`, a playbook that runs the role against localhost:

```sh
ansible-playbook deamen.proton.install_proton_drive_cli
```

License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
