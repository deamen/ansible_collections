---
name: ansible-collection-skeleton-skill
description: Creates an Ansible collection skeleton using `ansible-galaxy collection init`. Activate when asked to "create an ansible collection skeleton", "init a collection", or similar; supports namespace auto-detection inside `collections/ansible_collections/`.
license: Complete terms in LICENSE.txt
---

# Ansible Collection Skeleton Creator Skill


## Instructions

1. Run `helper_scripts/init_collection.py --collection <namespace.collection_name>` to create a new Ansible collection skeleton.
2. Run `helper_scripts/fix_ansible_collection_lint.py --collection <namespace.collection_name>` to apply fixes for common ansible-lint issues in generated skeletons.
3. Run `pre-commit run --all-files` in the repository's root directory to apply configured hooks.
4. Run `ansible-lint` to detect linting issues; when `ansible-lint` reports problems, follow the deterministic fixes described below.
5. Return CLI output and a short list of created files (or the error message if the command fails).

## Troubleshooting

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

 - When a generated collection fails `ansible-lint`, the agent follows a small set of deterministic fixes and provides clear instructions. Before running `ansible-lint`, the agent will attempt to run the skill-bundled `./scripts/fix_ansible_collection_lint.py` when available, falling back to a repository-root `fix_ansible_collection_lint.py` when present; when no script is available or additional issues remain, apply the manual fixes below one-by-one and re-run `ansible-lint` after each change.

- Fix: missing changelog
  - Problem: `galaxy.yml` may require a changelog file (e.g., `CHANGELOG.md`) to be present.
  - Fix: add a `CHANGELOG.md` to the collection root with an initial release entry.

- Fix: collection license metadata
  - Problem: `galaxy.yml` may contain an inconsistent SPDX header or missing/incorrect `license`/`license_file` keys.
  - Fix: ensure the top of `galaxy.yml` contains a matching SPDX comment and set `license` to the correct SPDX identifier and `license_file` to the license filename. Example:

```yaml
# SPDX-License-Identifier: GPL-3.0-or-later
namespace: <namespace>
name: <collection>
version: 1.0.0
readme: README.md
authors:
  - <your name>
description: Short description
license: GPL-3.0-or-later
license_file: LICENSE
```

- Fix: `requires_ansible` missing in `meta/runtime.yml`
  - Problem: some ansible-lint rules expect a `requires_ansible` key in `meta/runtime.yml`.
  - Fix: add `requires_ansible: '>=2.9.10'` under the YAML frontmatter. Example:

```yaml
# SPDX-License-Identifier: GPL-3.0-or-later
---
requires_ansible: '>=2.18.0'
```

- Fix: missing `LICENSE` file
  - Problem: `license_file` references `LICENSE` but the file is not present in the collection root.
  - Fix: copy the appropriate license text into `collections/ansible_collections/<namespace>/<collection>/LICENSE` (or adjust `license_file` to point to an existing file).

- How the agent uses these fixes
  - After `ansible-galaxy` creates the skeleton, run:

```
ansible-lint collections/ansible_collections/<namespace>/<collection>
```

  - Apply the fixes above for errors that match the described problems, then re-run `ansible-lint`.
  - If other ansible-lint rules fail, present the exact linter message and a suggested small patch for the user to confirm.
