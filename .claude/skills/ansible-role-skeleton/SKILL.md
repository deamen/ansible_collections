---
name: ansible-role-skeleton
description: Creates an Ansible role skeleton using `ansible-galaxy role init`. Activate when asked to "create an ansible role skeleton", "init a role", or similar.
---

# Ansible Role Skeleton Creator Skill


## Instructions

1. Run `helper_scripts/init_role.py --role <namespace.collection.role_name>` to create a new Ansible role skeleton. With a full FQCN it also replaces the README, removes `tests/`, strips SPDX headers, and writes the standard `meta/main.yml`.
2. Run `pre-commit run --all-files` in the repository's root directory to apply configured hooks.
3. Run `ansible-lint` on the new role; if problems remain, present the exact linter message and a suggested small patch for the user to confirm.
4. Return CLI output and a short list of created files (or the error message if the command fails).
