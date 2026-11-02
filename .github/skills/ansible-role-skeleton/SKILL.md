---
name: ansible-role-skeleton
description: Creates an Ansible role skeleton using `ansible-galaxy role init`. Activate when asked to "create an ansible role skeleton", "init a role", or similar.
license: GPL-3.0-or-later
---

# Ansible Role Skeleton Creator Skill


## Instructions

1. Run `helper_scripts/init_role.py --role <namespace.collection.role_name>` to create a new Ansible role skeleton; it also applies fixes for common ansible-lint issues in generated skeletons.
2. Run `pre-commit run --all-files` in the repository's root directory to apply configured hooks.
3. Run `ansible-lint` to detect linting issues; if problems remain, present the exact linter message and a suggested fix.
4. Return CLI output and a short list of created files (or the error message if the command fails).
