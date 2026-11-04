# CLAUDE.md

Source repository for the `deamen.*` Ansible collections, released to Ansible Galaxy via GitHub workflows.

## Layout

- `collections/ansible_collections/deamen/<collection>/` — one directory per collection (`account`, `ai`, `ansible`, `certificate`, `general`, `git`, `gpg`, `podman`)
- `helper_scripts/` — scaffolding and release scripts; `init_role.py` and `init_collection.py` apply lint fixes automatically, `prepare_release.py` and `release.py` release a collection, `ansible_utils.py` holds the shared helpers
- `helper_scripts/files/molecule_template/` — template copied by `init_molecule.py`, excluded from `ansible-lint`
- `helper_scripts/files/changelogs/config.yaml` — antsibull-changelog config template used by `init_collection.py`
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

## Changelogs

See `RELEASING.md` for the full process. Each collection uses [antsibull-changelog](https://github.com/ansible-community/antsibull-changelog) (`pip install antsibull-changelog`). `CHANGELOG.md` and `changelogs/changelog.yaml` are generated; never edit `CHANGELOG.md` by hand.

- Every user-facing change adds a fragment `changelogs/fragments/<short-description>.yml` in the affected collection, using the sections from `changelogs/config.yaml` (`minor_changes`, `bugfixes`, `breaking_changes`, …). Prefix entries with the role or module name, e.g. `- install_dev_packages - add ``tmux`` to ``essential_packages``.`
- Never put `playbook` in a fragment filename (e.g. use `configure-gpg-for-user.yml`, not `configure-gpg-for-user-playbook.yml`): `ansible-lint` treats `*playbook*.yml` as a playbook and fails `syntax-check`. `.ansible-lint` maps `changelogs/fragments/*.yml` to the `yaml` kind as a guard; keep that mapping. Run a whole-repo `ansible-lint` after adding a fragment, since linting only changed role or playbook paths misses it.
- `antsibull-changelog release` lists new modules and roles automatically when they set `version_added` (module `DOCUMENTATION`, role `meta/argument_specs.yml`); no fragment is needed just to announce them.
- PRs that change `plugins/`, `roles/`, `playbooks/` or `meta/` in a collection must add a fragment to that collection, or release it in the same PR (`.github/workflows/check_changelog_fragment.yml`); label the PR `skip-changelog` when no entry is needed.
- Validate fragments with `antsibull-changelog lint` from the collection root.
- To release: `helper_scripts/prepare_release.py -c <namespace.collection>` bumps `version` in `galaxy.yml` from the fragments (or `--version x.y.z`) and runs `antsibull-changelog release`; commit and push, then `helper_scripts/release.py -c <namespace.collection>` pushes the `release_<namespace>.<collection>_v<version>` tag. Pushing a tag publishes to Galaxy, so only run `release.py` when asked.

## Secrets

Secrets are stored with Ansible Vault, never in plain text. See `.claude/rules/ansible-style.md` for the `vars`/`vault` layout.
