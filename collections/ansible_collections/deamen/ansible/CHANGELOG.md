# Changelog

All notable changes to this collection will be documented in this file.

The format is based on Keep a Changelog (https://keepachangelog.com/en/1.0.0/) and this project follows Semantic Versioning.

## Unreleased

- Initial scaffold

## 1.0.2

- Declare dependency on `deamen.general` (used by `configure_system_ansible_runtime_env.yml`).
- `configure_system_ansible_runtime_env.yml` configures the connecting user instead of root; only pip installs use become.
- `config_ansible_runtime_env`: skip collection install when `~/Prj/ansible/requirements.yml` is absent.
- `config_ansible_runtime_env`: default `ansible_pip_executable` to `/usr/bin/pip3` so it works on any Fedora release.
- `config_ansible_runtime_env`: add `install_molecule_via_pip` (default `true`).
