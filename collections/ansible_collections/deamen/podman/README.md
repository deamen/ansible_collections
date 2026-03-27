# Deamen Podman Collection

This repository contains the `deamen.podman` Ansible Collection.

<!--start requires_ansible-->
<!--end requires_ansible-->

## What this collection does

Manage and set up Podman on Linux hosts, including:
- Install Podman and related packages
- Configure registries, storage, and policy
- Manage images and containers
- Generate and manage systemd units for rootless/rootful containers
- Basic integration helpers for compose-like workflows

## External requirements

Some modules and roles may require external packages on the managed node (e.g., Podman CLI and systemd). Check role or plugin docs for specifics.

## Included content

<!--start collection content-->
<!-- List roles/modules/plugins once added. -->
<!--end collection content-->

## Using this collection

```bash
ansible-galaxy collection install deamen.podman
```

Or via `requirements.yml`:

```yaml
collections:
  - name: deamen.podman
```

Upgrade to the latest version:

```bash
ansible-galaxy collection install deamen.podman --upgrade
```

Install a specific version (`X.Y.Z`):

```bash
ansible-galaxy collection install deamen.podman:==X.Y.Z
```

See Ansible docs: https://docs.ansible.com/ansible/latest/user_guide/collections_using.html

## Quickstart example

Example play to ensure Podman is present and a container is running (role and modules to be provided in this collection):

```yaml
- name: Manage Podman
  hosts: all
  become: true
  collections:
    - deamen.podman
  tasks:
    - name: Ensure Podman is installed
      package:
        name: podman
        state: present

    # Placeholder for upcoming modules/roles
    # - name: Run a container
    #   deamen.podman.podman_container:
    #     name: hello
    #     image: quay.io/podman/hello
    #     state: started
```

## Release notes

See the changelog: https://github.com/deamen/ansible_collections/blob/master/collections/ansible_collections/deamen/podman/CHANGELOG.md

## Roadmap

- Roles for install and configuration (rootless and rootful)
- Modules or action plugins for container/image lifecycle
- Helpers to generate systemd units
- Molecule scenarios for testing

## More information

- Ansible Collection overview: https://github.com/ansible-collections/overview
- Ansible User guide: https://docs.ansible.com/ansible/devel/user_guide/index.html
- Ansible Developer guide: https://docs.ansible.com/ansible/devel/dev_guide/index.html
- Ansible Collections Checklist: https://github.com/ansible-collections/overview/blob/main/collection_requirements.rst
- Ansible Community code of conduct: https://docs.ansible.com/ansible/devel/community/code_of_conduct.html
- The Bullhorn (Ansible Contributor newsletter): https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn
- News for Maintainers: https://github.com/ansible-collections/news-for-maintainers

## Licensing

GNU General Public License v3.0 or later.

See LICENSE to see the full text.
