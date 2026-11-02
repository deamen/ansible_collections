#!/usr/bin/python3
"""Ansible collection management tool.

Initialises a new Ansible collection and automatically applies lint fixes:

    init_collection.py --collection namespace.name [--init-path PATH] [-v] [--force]

Shared utilities (get_git_author, get_git_remote_info, run_ansible_galaxy, …)
live in ansible_utils.py.
"""

import argparse
import datetime
import os
import shutil
import subprocess
import sys

import yaml

# Ensure the directory containing this script is on the path so that
# ansible_utils can always be imported regardless of cwd.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ansible_utils import (
    DEFAULT_COLLECTION_PATH,
    get_git_author,
    get_git_remote_info,
    run_ansible_galaxy,
)

# ---------------------------------------------------------------------------
# YAML helpers
# ---------------------------------------------------------------------------


class TwoSpaceIndentDumper(yaml.Dumper):
    """Custom YAML dumper that enforces 2-space indentation for lists."""

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def dump_yaml_to_string(data):
    """Dump *data* to a YAML string with consistent 2-space indentation."""
    dumped = yaml.dump(
        data,
        Dumper=TwoSpaceIndentDumper,
        default_flow_style=False,
        sort_keys=False,
        width=1000,
    )
    if not dumped.startswith("---"):
        dumped = "---\n" + dumped
    return dumped


# ---------------------------------------------------------------------------
# galaxy.yml normalisation
# ---------------------------------------------------------------------------


def _fix_galaxy_dict(data):
    """Return a normalised galaxy.yml dict and a bool indicating whether any changes were made."""
    if data is None:
        data = {}

    changed = False

    # tags: set default when missing or empty
    tags = data.get("tags")
    if tags is None or tags == []:
        data["tags"] = ["application"]
        changed = True
    else:
        normalized = [str(t).lower() for t in tags]
        if normalized != tags:
            data["tags"] = normalized
            changed = True

    # license: always enforce GPL-3.0-or-later
    desired_license = ["GPL-3.0-or-later"]
    if data.get("license") != desired_license:
        data["license"] = desired_license
        changed = True

    # license_file: remove when empty or when 'license' key is present
    if "license_file" in data:
        lf = data.get("license_file")
        if (
            lf is None
            or (isinstance(lf, str) and lf.strip() == "")
            or ("license" in data and data.get("license"))
        ):
            del data["license_file"]
            changed = True

    # version: ensure it's a string
    if (
        "version" in data
        and data["version"] is not None
        and not isinstance(data["version"], str)
    ):
        data["version"] = str(data["version"])
        changed = True

    # namespace and name: normalise to lowercase
    for key in ("namespace", "name"):
        if key in data and data[key] is not None:
            val = str(data[key])
            if val.lower() != val:
                data[key] = val.lower()
                changed = True

    # authors: ensure it is a list
    if (
        "authors" in data
        and data["authors"] is not None
        and not isinstance(data["authors"], list)
    ):
        data["authors"] = [data["authors"]]
        changed = True

    # Remove keys that are empty strings (scaffold placeholders)
    for k in list(data.keys()):
        v = data.get(k)
        if isinstance(v, str) and v.strip() == "":
            del data[k]
            changed = True

    return data, changed


def process_galaxy_file(file_path, repo_info=None, dry_run=False, verbose=False):
    """Process a single galaxy.yml file.  Returns True if the file was updated."""
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            original_text = fh.read()

        original_dict = yaml.safe_load(original_text)
        new_dict, changed_by_fix = _fix_galaxy_dict(original_dict)

        # Fill in authors from git config when missing or placeholder-like.
        changed_by_authors = False
        git_author = get_git_author()
        if git_author:
            authors = new_dict.get("authors")
            placeholder = False
            if not authors or (isinstance(authors, list) and len(authors) == 0):
                placeholder = True
            elif (
                isinstance(authors, list)
                and len(authors) == 1
                and isinstance(authors[0], str)
            ):
                val = authors[0].lower()
                if "example" in val or "your name" in val or "you@" in val:
                    placeholder = True

            if placeholder:
                new_dict["authors"] = [git_author]
                changed_by_authors = True

        # Use git remote info to set repository/homepage/documentation/issues.
        changed_by_repo = False
        if repo_info:
            repo_url = repo_info.get("url")
            default_branch = repo_info.get("default_branch", "master")

            repo_val = new_dict.get("repository")
            if not repo_val or (
                "example" in str(repo_val).lower()
                or "example.com" in str(repo_val).lower()
            ):
                new_dict["repository"] = repo_url
                changed_by_repo = True

            # Compute collection-specific URL from the file path when possible.
            collection_url = None
            try:
                abs_path = os.path.abspath(file_path)
                parts = abs_path.split(os.sep)
                if "collections" in parts:
                    idx = parts.index("collections")
                    if idx + 3 < len(parts) and parts[idx + 1] == "ansible_collections":
                        collection_path = "/".join(parts[idx : idx + 4])
                        collection_url = (
                            f"{repo_url}/tree/{default_branch}/{collection_path}"
                        )
            except Exception:
                collection_url = None

            homepage_val = new_dict.get("homepage")
            homepage_target = collection_url if collection_url else repo_url

            def _norm(u):
                return str(u).rstrip("/") if u else ""

            if collection_url:
                if _norm(homepage_val) != _norm(homepage_target):
                    new_dict["homepage"] = homepage_target
                    changed_by_repo = True
            else:
                if not homepage_val or (
                    "example" in str(homepage_val).lower()
                    or "example.com" in str(homepage_val).lower()
                ):
                    new_dict["homepage"] = homepage_target
                    changed_by_repo = True

            if collection_url:
                docs_url = f"{collection_url}/docs"
            else:
                docs_url = f"{repo_url}/tree/{default_branch}/docs"

            doc_val = new_dict.get("documentation")
            if collection_url:
                if _norm(doc_val) != _norm(docs_url):
                    new_dict["documentation"] = docs_url
                    changed_by_repo = True
            else:
                if not doc_val or "example" in str(doc_val).lower():
                    new_dict["documentation"] = docs_url
                    changed_by_repo = True

            issues_url = f"{repo_url}/issues"
            issues_val = new_dict.get("issues")
            if not issues_val or "example" in str(issues_val).lower():
                new_dict["issues"] = issues_url
                changed_by_repo = True

        if not (changed_by_fix or changed_by_authors or changed_by_repo):
            if verbose:
                print(f"No lint-related changes needed: {file_path}")
            return False

        new_text = dump_yaml_to_string(new_dict)

        if dry_run:
            print(f"DRY RUN - would update: {file_path}")
            return True

        shutil.copyfile(file_path, file_path + ".bak")
        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(new_text)

        print(f"Updated: {file_path} (backup at {file_path}.bak)")
        return True

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False


def process_runtime_file(file_path, dry_run=False, verbose=False):
    """Process a single meta/runtime.yml file.  Returns True if the file was updated."""
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            original_text = fh.read()

        original_dict = yaml.safe_load(original_text) or {}
        changed = False

        if "requires_ansible" not in original_dict or not original_dict.get(
            "requires_ansible"
        ):
            original_dict["requires_ansible"] = ">=2.15.0"
            changed = True

        if not changed:
            if verbose:
                print(f"No runtime changes needed: {file_path}")
            return False

        new_text = dump_yaml_to_string(original_dict)

        if dry_run:
            print(f"DRY RUN - would update runtime file: {file_path}")
            return True

        shutil.copyfile(file_path, file_path + ".bak")
        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(new_text)

        print(f"Updated runtime: {file_path} (backup at {file_path}.bak)")
        return True

    except Exception as e:
        print(f"Error processing runtime file {file_path}: {e}")
        return False


def process_galaxy_files(root_dir, dry_run=False, verbose=False):
    """Recursively process all galaxy.yml and meta/runtime.yml files under *root_dir*."""
    updated = 0
    repo_info = get_git_remote_info(root_dir)
    if verbose and repo_info:
        print(
            f"Using git remote: {repo_info.get('url')} "
            f"(default branch: {repo_info.get('default_branch')})"
        )
    for root, _, files in os.walk(root_dir):
        for fname in files:
            if fname == "galaxy.yml":
                file_path = os.path.join(root, fname)
                if process_galaxy_file(
                    file_path,
                    repo_info=repo_info,
                    dry_run=dry_run,
                    verbose=verbose,
                ):
                    updated += 1
            elif fname == "runtime.yml" and os.path.basename(root) == "meta":
                file_path = os.path.join(root, fname)
                if process_runtime_file(file_path, dry_run=dry_run, verbose=verbose):
                    updated += 1
    return updated


CHANGELOG_CONFIG_TEMPLATE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "files", "changelogs", "config.yaml"
)


def init_changelog(col_dir, dry_run=False, verbose=False):
    """Set up antsibull-changelog in a collection directory.

    Writes changelogs/config.yaml (from the template), changelogs/changelog.yaml
    with an initial release entry for the galaxy.yml version, and an empty
    changelogs/fragments/ directory, then renders CHANGELOG.md with
    antsibull-changelog when it is installed.
    """
    changelogs_dir = os.path.join(col_dir, "changelogs")
    if dry_run:
        if verbose:
            print(f"DRY RUN - would create: {changelogs_dir}")
        return

    with open(os.path.join(col_dir, "galaxy.yml"), encoding="utf-8") as fh:
        galaxy = yaml.safe_load(fh) or {}
    namespace = str(galaxy.get("namespace", ""))
    name = str(galaxy.get("name", ""))
    version = str(galaxy.get("version", "1.0.0"))

    with open(CHANGELOG_CONFIG_TEMPLATE, encoding="utf-8") as fh:
        config = yaml.safe_load(fh)
    config["title"] = f"{namespace.title()} {name.replace('_', ' ').title()} Collection"

    changelog = {
        "ancestor": None,
        "releases": {
            version: {
                "changes": {
                    "release_summary": f"Initial release of the ``{namespace}.{name}`` collection."
                },
                "release_date": datetime.date.today().isoformat(),
            }
        },
    }

    os.makedirs(os.path.join(changelogs_dir, "fragments"), exist_ok=True)
    open(os.path.join(changelogs_dir, "fragments", ".keep"), "w").close()
    with open(os.path.join(changelogs_dir, "config.yaml"), "w", encoding="utf-8") as fh:
        yaml.safe_dump(config, fh, sort_keys=False)
    with open(
        os.path.join(changelogs_dir, "changelog.yaml"), "w", encoding="utf-8"
    ) as fh:
        yaml.safe_dump(changelog, fh, sort_keys=False)
    print(f"Created: {changelogs_dir}")

    if shutil.which("antsibull-changelog") is None:
        print(
            "Warning: antsibull-changelog not found; run "
            "'antsibull-changelog generate' in the collection root to render CHANGELOG.md."
        )
        return
    subprocess.run(["antsibull-changelog", "generate"], cwd=col_dir, check=True)
    print(f"Created: {os.path.join(col_dir, 'CHANGELOG.md')}")


def ensure_changelog(root_dir, dry_run=False, verbose=False):
    """Set up antsibull-changelog in each collection that is missing it.

    Returns the number of changelogs created (or that would be created during
    a dry run).
    """
    created = 0

    candidates = []
    try:
        abs_root = os.path.abspath(root_dir)
        root_parts = abs_root.split(os.sep)
        if "collections" in root_parts:
            idx = root_parts.index("collections")
            if (
                idx + 3 < len(root_parts)
                and root_parts[idx + 1] == "ansible_collections"
            ):
                candidates.append(abs_root)
    except Exception:
        candidates = []

    if not candidates:
        collections_base = os.path.join(root_dir, "collections", "ansible_collections")
        if os.path.isdir(collections_base):
            for namespace in sorted(os.listdir(collections_base)):
                ns_dir = os.path.join(collections_base, namespace)
                if not os.path.isdir(ns_dir):
                    continue
                for collection in sorted(os.listdir(ns_dir)):
                    col_dir = os.path.join(ns_dir, collection)
                    if os.path.isdir(col_dir):
                        candidates.append(col_dir)
    else:
        for cur_root, dirs, _ in os.walk(root_dir):
            if (
                os.path.basename(cur_root) == "ansible_collections"
                and os.path.basename(os.path.dirname(cur_root)) == "collections"
            ):
                for namespace in sorted(os.listdir(cur_root)):
                    ns_dir = os.path.join(cur_root, namespace)
                    if not os.path.isdir(ns_dir):
                        continue
                    for collection in sorted(os.listdir(ns_dir)):
                        col_dir = os.path.join(ns_dir, collection)
                        if os.path.isdir(col_dir):
                            candidates.append(col_dir)

    for col_dir in candidates:
        if os.path.exists(os.path.join(col_dir, "changelogs", "config.yaml")):
            continue
        init_changelog(col_dir, dry_run=dry_run, verbose=verbose)
        created += 1

    return created


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Initialise a new Ansible collection and automatically apply lint fixes."
        )
    )
    parser.add_argument(
        "--collection",
        required=True,
        help="Collection name in 'namespace.collection' format",
    )
    parser.add_argument(
        "--init-path",
        default=DEFAULT_COLLECTION_PATH,
        help=f"Path where the collection will be created (default: {DEFAULT_COLLECTION_PATH})",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the collection directory if it already exists",
    )

    known = parser.parse_args(argv)

    col = known.collection.strip()
    if "." not in col:
        print("Error: --collection must be in 'namespace.collection' format.")
        sys.exit(2)

    # --- init ---------------------------------------------------------------
    galaxy_args = [
        "ansible-galaxy",
        "collection",
        "init",
        "--init-path",
        known.init_path,
        col,
    ]
    if known.force:
        galaxy_args.append("--force")

    exit_code = run_ansible_galaxy(galaxy_args)
    if exit_code != 0:
        sys.exit(exit_code)

    # --- fix (automatic) ----------------------------------------------------
    namespace, collection = col.split(".", 1)
    namespace = namespace.strip().lower()
    collection = collection.strip().lower()
    root_directory = os.path.join(
        os.path.abspath(known.init_path), namespace, collection
    )

    if not os.path.isdir(root_directory):
        print(
            f"Warning: Collection directory '{root_directory}' not found; skipping lint fixes."
        )
        sys.exit(0)

    if known.verbose:
        print(f"Applying lint fixes under: {root_directory}")

    updated_count = process_galaxy_files(root_directory, verbose=known.verbose)
    changelog_count = ensure_changelog(root_directory, verbose=known.verbose)

    print(f"Lint fixes applied. Files updated: {updated_count}")
    print(f"Changelogs created: {changelog_count}")


if __name__ == "__main__":
    main()
