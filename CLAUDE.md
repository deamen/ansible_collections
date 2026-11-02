# CLAUDE.md

Source repository for the `deamen.*` Ansible collections, released to Ansible Galaxy via GitHub workflows.

## Layout

- `collections/ansible_collections/deamen/<collection>/` — one directory per collection (`account`, `ai`, `ansible`, `certificate`, `general`, `git`, `gpg`, `podman`)
- `helper_scripts/` — scaffolding scripts; `init_role.py` and `init_collection.py` apply lint fixes automatically, `ansible_utils.py` holds the shared helpers
- `helper_scripts/files/molecule_template/` — template copied by `init_molecule.py`, excluded from `ansible-lint`
- `.github/workflows/` — lint, sanity, molecule, and per-collection release workflows

## Environment

```bash
ansible-galaxy install -r requirements.yml
```

`ansible.cfg` adds `collections/` to `collections_path` so `ansible-lint` resolves roles inside the local collections.

## Verification

Run these before proposing a change as done. Prefer scoping to changed files.

```bash
ansible-playbook --syntax-check <playbook>
ansible-lint <paths>
yamllint <paths>
pre-commit run --files <paths>          # or --all-files
```

For collection modules and plugins, from the collection root:

```bash
ansible-test sanity --test validate-modules
```

Never run `ansible-playbook` against real hosts. `--check --diff` dry runs only when explicitly asked.

`ansible-lint` skips `var-naming[no-role-prefix]` and excludes `helper_scripts/files/molecule_template/`. `yamllint` has `line-length` disabled. Python is formatted with `black` via pre-commit.

pre-commit is enabled but not enforced locally; pre-commit.ci and the GitHub workflows run the equivalent checks.

## Secrets

Secrets are stored with Ansible Vault, never in plain text. See `.claude/rules/ansible-style.md` for the `vars`/`vault` layout.
