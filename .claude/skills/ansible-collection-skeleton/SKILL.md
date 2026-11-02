---
name: ansible-collection-skeleton
description: Creates an Ansible collection skeleton using `ansible-galaxy collection init`. Activate when asked to "create an ansible collection skeleton", "init a collection", or similar; supports namespace auto-detection inside `collections/ansible_collections/`.
---

# Ansible Collection Skeleton Creator Skill


## Instructions

1. Run `helper_scripts/init_collection.py --collection <namespace.collection_name>` to create a new Ansible collection skeleton. It also normalises `galaxy.yml`, sets `requires_ansible` in `meta/runtime.yml`, and sets up antsibull-changelog (`changelogs/config.yaml`, `changelogs/changelog.yaml` with an initial release entry, `changelogs/fragments/`, and a rendered `CHANGELOG.md`), leaving `.bak` backups of the files it rewrites; delete those backups.
2. Run `pre-commit run --all-files` in the repository's root directory to apply configured hooks.
3. Run `ansible-lint collections/ansible_collections/<namespace>/<collection>` to detect linting issues; when `ansible-lint` reports problems, apply the fixes below and re-run it after each change.
4. Return CLI output and a short list of created files (or the error message if the command fails).

## Ansible-lint fixes

- Missing changelog: run `antsibull-changelog generate` in the collection root (the script skips this step when `antsibull-changelog` is not installed). Never hand-edit `CHANGELOG.md`.
- Collection license metadata: `license` must be `GPL-3.0-or-later` as a list, with no `license_file` key alongside it:

```yaml
license:
  - GPL-3.0-or-later
```

- `requires_ansible` missing in `meta/runtime.yml`:

```yaml
---
requires_ansible: '>=2.15.0'
```

If other rules fail, present the exact linter message and a suggested small patch for the user to confirm.
