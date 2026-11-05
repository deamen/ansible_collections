config_dev_runtime_env
=========

Configures the runtime environment for development.

Requirements
------------


Role Variables
--------------



| Variable                | Description                                                                 | Default/Example Value                  |
|-------------------------|-----------------------------------------------------------------------------|----------------------------------------|
| current_user            | Username for project directory and aliases.                                  | $(id -u -n)                            |
| prj_home                | Base home directory for project structure.                                   | /home                                  |
| ansible_user_dir        | Home directory for the target user (used for .bashrc.d, Ref, Prj, etc).      | {{ ansible_env.HOME }}                 |
| ansible_galaxy_executable | Path to ansible-galaxy executable.                                         | /usr/bin/ansible-galaxy or custom path |
| ansible_pip_executable  | Path to pip executable for installing requirements.                          | /usr/bin/pip3.14, /usr/bin/pip3.9, etc |
| config_dev_runtime_env_force_deploy_aliases | Redeploy aliases.sh even if it exists. Overwrites local edits; a backup is kept next to it. | false |

These variables are used to generate the PRJ_DIR and related aliases in the deployed aliases.sh file.

aliases.sh exports `GPG_TTY` in interactive shells for pinentry-curses, and defines `unlock_gpg`, which prompts for the
GPG passphrase once so gpg-agent caches both the signing and decryption subkeys, e.g. before
`ansible_vault_pass_gpg.sh` runs `gpg --batch` or before a signed git commit.

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
