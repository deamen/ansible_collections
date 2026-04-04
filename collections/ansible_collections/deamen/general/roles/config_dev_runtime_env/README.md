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

These variables are used to generate the PRJ_DIR and related aliases in the deployed aliases.sh file.

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
