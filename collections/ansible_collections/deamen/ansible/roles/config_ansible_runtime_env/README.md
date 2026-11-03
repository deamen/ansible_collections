config_ansible_runtime_env
=========

Configure Ansible Runtime Environment

Requirements
------------


Role Variables
--------------

| Variable                  | Description                                                        | Default                   |
|---------------------------|--------------------------------------------------------------------|---------------------------|
| ansible_galaxy_executable | Path to ansible-galaxy executable.                                 | /usr/bin/ansible-galaxy   |
| ansible_pip_executable    | Path to pip executable for installing molecule and requirements.   | /usr/bin/pip3             |
| install_molecule_via_pip  | Install molecule with pip. Set to false when installed otherwise.  | true                      |
| unversioned_python_packages | Packages providing `/usr/bin/python` for `setup_ansible_vault_gpg.py`. | [python-unversioned-command] |

The role also installs `/usr/local/bin/ansible_vault_pass_gpg.sh`, which decrypts `~/.ansible_vault_pass.gpg`
(override with `ANSIBLE_VAULT_GPG_FILE`) and prints the Ansible Vault password. `deamen.general.config_dev_runtime_env`
sets `ANSIBLE_VAULT_PASSWORD_FILE` to it when both files exist.

`/usr/local/bin/setup_ansible_vault_gpg.py` is installed alongside it for the one-time setup. By default it imports the
GPG secret key from `~/.gnupg/private_gpg.key` (removed after a successful import) via the `deamen.gpg.config_gpg`
playbook, then writes a random vault password encrypted to that key into `~/.ansible_vault_pass.gpg`. Use `--gpg-file`
to import another file, or `--key-name` and `--key-email` to generate a new key with `deamen.gpg.generate_gpg_key`.


Dependencies
------------


Example Playbook
----------------


License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
