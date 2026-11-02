---
name: ansible-role-skeleton
description: Creates an Ansible role skeleton using `ansible-galaxy role init`. Activate when asked to "create an ansible role skeleton", "init a role", or similar.
license: GPL-3.0-or-later
---

# Ansible Role Skeleton Creator Skill


## Instructions

1. Run `helper_scripts/init_role.py --role <namespace.collection.role_name>` to create a new Ansible role skeleton under the collection's `roles/` directory. Add `--force` to overwrite an existing role directory. The script also:
   - replaces the generated `README.md` with the repository template and removes the `tests/` folder
   - with a full FQCN, strips `SPDX-License-Identifier` lines from the role's YAML files and replaces `meta/main.yml` with the standard template (author from git config, `company: Yobibyte`, `license: GPL-3.0-or-later`)
2. Run `pre-commit run --all-files` in the repository's root directory to apply configured hooks.
3. Run `ansible-lint` to detect linting issues; if problems remain, present the exact linter message and a suggested fix.
4. Return CLI output and a short list of created files (or the error message if the command fails).
