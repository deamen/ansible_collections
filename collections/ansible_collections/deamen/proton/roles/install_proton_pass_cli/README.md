install_proton_pass_cli
=======================

Install the [Proton Pass CLI](https://protonpass.github.io/pass-cli/) for the connecting user.

The role reads the release manifest at `https://proton.me/download/pass-cli/versions.json` (`versions.beta.json` for the beta channel), downloads the `pass-cli` binary for the host architecture to `~/.local/bin/pass-cli` and verifies its SHA-256 hash. A rerun replaces the binary when a newer release is published. It then deploys `~/.bashrc.d/proton_pass_cli.sh`, which exports `PROTON_PASS_KEY_PROVIDER`. Every task runs as the connecting user without privilege escalation.

Requirements
------------

- Fact gathering must be enabled; the role uses `ansible_facts['env']['HOME']` and `ansible_facts['architecture']` (`x86_64` or `aarch64`).
- `~/.bashrc` must source the files in `~/.bashrc.d`, as Fedora's default `.bashrc` does.
- The default `fs` key provider stores the session encryption key in plaintext `local.key` next to the encrypted session in `~/.local/share/proton-pass-cli/.session`. Use `keyring` on hosts that can reach the kernel keyring; containers cannot.

Sign in after the role has run, in a new login shell:

```sh
pass-cli login
```

For headless use, log in with a personal access token instead:

```sh
PROTON_PASS_PERSONAL_ACCESS_TOKEN=pst_... pass-cli login
```

Role Variables
--------------

| Variable | Default | Description |
| --- | --- | --- |
| `proton_pass_cli_key_provider` | `fs` | Where the CLI keeps its session key: `fs` or `keyring` |
| `proton_pass_cli_release_channel` | `stable` | Release channel to install from: `stable` or `beta` |

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Install the Proton Pass CLI
  hosts: localhost
  connection: local
  become: false
  tasks:
    - name: Install the Proton Pass CLI for the current user
      ansible.builtin.import_role:
        name: deamen.proton.install_proton_pass_cli
```

The collection also ships `deamen.proton.install_proton_pass_cli`, a playbook that runs the role against localhost:

```sh
ansible-playbook deamen.proton.install_proton_pass_cli
```

License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
