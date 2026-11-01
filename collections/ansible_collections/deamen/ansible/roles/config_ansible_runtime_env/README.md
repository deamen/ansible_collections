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
