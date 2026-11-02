---
name: ansible-collection-skeleton-skill
description: Creates an Ansible collection skeleton using `ansible-galaxy collection init`. Activate when asked to "create an ansible collection skeleton", "init a collection", or similar; supports namespace auto-detection inside `collections/ansible_collections/`.
license: Complete terms in LICENSE.txt
---

# Ansible Collection Skeleton Creator Skill


## Instructions

1. Run `helper_scripts/init_collection.py --collection <namespace.collection_name>` to create a new Ansible collection skeleton. Add `-v` for verbose output, or `--force` to overwrite an existing collection directory.
2. Delete the `.bak` backups the script leaves next to the files it rewrites (`galaxy.yml.bak`, `meta/runtime.yml.bak`).
3. Run `pre-commit run --all-files` in the repository's root directory to apply configured hooks.
4. Run `ansible-lint collections/ansible_collections/<namespace>/<collection>` to detect linting issues; when `ansible-lint` reports problems, follow the manual fixes described below.
5. Return CLI output and a short list of created files (or the error message if the command fails).

## Troubleshooting

- Collection directory already exists: re-run with `--force` only after the user confirms overwriting it.
- Permission errors: suggest choosing a writable `--init-path` or adjusting permissions.
- Missing `collections/ansible_collections/`: offer to create the directory after confirmation.
- `ansible-galaxy` not on PATH: suggest installing Ansible and show the command to check (`ansible-galaxy --version`).

## Example prompts

- "Create an ansible collection skeleton named `monitoring.prometheus_exporter`."
- "Init a new collection `my_collection` (use default namespace)."
- If ambiguous: "Create a collection called `utils`. Which namespace should I use? Detected: `deamen`, `acmecorp`."

## References

- ansible-galaxy collection init docs: https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html#init

## Ansible-lint fixes

`init_collection.py` applies these fixes automatically after `ansible-galaxy collection init`:

- `galaxy.yml`: sets `license` to `['GPL-3.0-or-later']` and removes `license_file`, defaults empty `tags` to `['application']`, lowercases `namespace`, `name`, and `tags`, fills `authors` from git config, fills `repository`, `homepage`, `documentation`, and `issues` from the GitHub remote, and drops empty placeholder keys
- `meta/runtime.yml`: adds `requires_ansible: '>=2.15.0'` when missing
- `CHANGELOG.md`: creates one when the collection has neither `CHANGELOG.md` nor `CHANGELOG.rst`

When a generated collection still fails `ansible-lint`, apply the matching manual fix below and re-run `ansible-lint` after each change:

- Missing changelog: add a `CHANGELOG.md` to the collection root with an initial release entry.
- License metadata: `license` must be a list with no `license_file` key alongside it:

```yaml
license:
  - GPL-3.0-or-later
```

- `requires_ansible` missing in `meta/runtime.yml`:

```yaml
---
requires_ansible: '>=2.15.0'
```

If other ansible-lint rules fail, present the exact linter message and a suggested small patch for the user to confirm.
