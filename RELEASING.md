# Changelogs and releases

Every collection under `collections/ansible_collections/deamen/` keeps its changelog with [antsibull-changelog](https://github.com/ansible-community/antsibull-changelog), the standard tool for Ansible collections. `CHANGELOG.md` is generated from `changelogs/changelog.yaml`; never edit either file by hand.

Install the tool once:

```bash
pip install --user antsibull-changelog
```

## Layout

```text
<collection>/
├── CHANGELOG.md               # generated
└── changelogs/
    ├── config.yaml            # antsibull-changelog settings
    ├── changelog.yaml         # release history, updated by `antsibull-changelog release`
    └── fragments/             # one YAML file per unreleased change
```

## Adding a changelog fragment

Every user-facing change adds a fragment to the collection it changes, for example `changelogs/fragments/add-tmux.yml`:

```yaml
minor_changes:
  - install_dev_packages - add ``tmux`` to ``essential_packages``.
bugfixes:
  - config_dev_runtime_env - fix git prompt formatting.
```

- Valid sections are `major_changes`, `minor_changes`, `breaking_changes`, `deprecated_features`, `removed_features`, `security_fixes`, `bugfixes`, `known_issues` and `trivial`. Use `release_summary` only at release time.
- Prefix each entry with the role or module name, end it with a full stop, and use double backticks for code.
- `trivial` entries are accepted but left out of `CHANGELOG.md`; use them for refactors and cleanups.
- New modules and roles are listed automatically when they set `version_added` (module `DOCUMENTATION`, role `meta/argument_specs.yml`). A role without `version_added` needs a fragment.

Check fragments from the collection root:

```bash
antsibull-changelog lint
```

## Pull request checks

| Workflow | Runs on | Fails when |
| --- | --- | --- |
| `check_changelog_fragment.yml` | PRs to `master` | A collection's `plugins/`, `roles/`, `playbooks/` or `meta/` changed but the PR neither adds a fragment under that collection's `changelogs/fragments/` nor releases it in `changelogs/changelog.yaml` |
| `run_changelog_lint.yml` | PRs and pushes to `master` that touch `changelogs/` | `antsibull-changelog lint` fails for any collection |

Changes to `tests/`, `extensions/`, `docs/`, `README.md` or `.github/` do not need a fragment. To skip the fragment check for a PR that changes code but needs no changelog entry, add the `skip-changelog` label.

Direct pushes to `master` are not checked for fragments; add them anyway, or the release will have no notes.

## Releasing a collection

`helper_scripts/prepare_release.py` and `helper_scripts/release.py` run the steps below. `-c` takes the collection root or `namespace.name`:

```bash
helper_scripts/prepare_release.py -c deamen.general --dry-run   # show the version it would release
helper_scripts/prepare_release.py -c deamen.general             # bump galaxy.yml, run antsibull-changelog release
git add -A collections/ansible_collections/deamen/general
git commit -m "Release deamen.general 1.1.0" && git push
helper_scripts/release.py -c deamen.general                     # tag HEAD and push the tag
```

Without `--version`, `prepare_release.py` bumps one part of the latest version in `changelogs/changelog.yaml` from the fragment sections: `breaking_changes` or `removed_features` give a major release; `major_changes`, `minor_changes` or `deprecated_features` a minor one; anything else a patch. It stops when there are no fragments. Pass `--version x.y.z` to choose the version yourself, for example when the release only adds new roles or modules through `version_added`; it must be newer than every released version.

`release.py` runs the release workflow's checks (listed below) before it creates the `release_<namespace>.<collection>_v<version>` tag, and refuses to tag a collection with uncommitted changes or an existing tag. `--no-push` creates the tag without pushing it.

To release by hand, run from the collection root, for example `collections/ansible_collections/deamen/general`:

1. Bump `version` in `galaxy.yml`, following semantic versioning (`bugfixes` only: patch; `minor_changes` or new content: minor; `breaking_changes` or `removed_features`: major).
2. Optionally add a fragment with a `release_summary`:

   ```yaml
   release_summary: Short description of this release.
   ```

3. Generate the release notes. This adds the release to `changelogs/changelog.yaml`, regenerates `CHANGELOG.md`, and deletes the consumed fragments:

   ```bash
   antsibull-changelog release
   ```

4. Review and commit the changes, and push them to `master`.
5. Tag the commit and push the tag. The tag starts the matching `release_deamen.<collection>.yml` workflow:

   ```bash
   git tag release_deamen.general_v1.0.5
   git push origin release_deamen.general_v1.0.5
   ```

## Checks in the release workflow

`ansible_collection_base_workflow.yml` runs these checks before it builds and publishes the collection to Galaxy. A failure stops the release before anything is published.

| Check | Fails when | Fix |
| --- | --- | --- |
| Tag version matches `galaxy.yml` | The tag's version differs from `version` in `galaxy.yml` | Delete the tag, then retag the commit that has the right version |
| Changelog has the release | `changelogs/changelog.yaml` has no entry for the `galaxy.yml` version | Run `antsibull-changelog release`, commit, and retag |
| No unreleased fragments | `changelogs/fragments/` has files other than `.keep` | Run `antsibull-changelog release`, commit, and retag |

To delete and recreate a tag after fixing the commit:

```bash
git tag -d release_deamen.general_v1.0.5
git push origin :refs/tags/release_deamen.general_v1.0.5
git tag release_deamen.general_v1.0.5
git push origin release_deamen.general_v1.0.5
```

## New collections

`helper_scripts/init_collection.py` sets up `changelogs/` from `helper_scripts/files/changelogs/config.yaml` with an initial release entry for the `galaxy.yml` version, and renders `CHANGELOG.md` when `antsibull-changelog` is installed. If it is not, run `antsibull-changelog generate` from the collection root.
