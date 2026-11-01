# Changelog

All notable changes to this collection will be documented in this file.

The format is based on Keep a Changelog (https://keepachangelog.com/en/1.0.0/) and this project follows Semantic Versioning.

## Unreleased
- install_dev_packages: add gzip, which and procps-ng to essential_packages (needed by VS Code server in minimal containers)
- install_dev_packages: install all packages in one transaction
- config_dev_runtime_env: look up git-prompt.sh under /usr/share/git-core on Fedora/RHEL and Alpine
- Add check_is_container module
- Add install_dev_packages role
- Add install_system_ansible role
- Initial scaffold
