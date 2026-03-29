#!/usr/bin/python3
"""Utility to normalize and fix common ansible-lint issues in galaxy.yml files.

Fixes applied:
- set `tags` to ['application'] when missing/empty
- always set `license` to ['GPL-3.0-or-later']
- remove empty `license_file` or when `license` is present
- ensure `version` is a string
- normalize `namespace` and `name` to lowercase
- ensure `authors` is a list (populated from git config when missing/placeholders)
- set `repository` and `homepage` from `git remote -v` (GitHub URL, without .git)
- point `documentation` to the repository `docs` folder
- point `issues` to the repository GitHub issues page
- only write file when the parsed YAML changes (preserves comments when no change)

Usage: python clean_galaxy.py [--dry-run] [-v]
"""

import argparse
import copy
import os
import shutil
import sys

import yaml
import subprocess
import re


class TwoSpaceIndentDumper(yaml.Dumper):
    """Custom YAML dumper to enforce 2-space indentation for lists."""

    def increase_indent(self, flow=False, indentless=False):
        return super(TwoSpaceIndentDumper, self).increase_indent(flow, False)


def _fix_galaxy_dict(data):
    """Return a normalized copy of the parsed galaxy.yml dict.

    The function does not mutate the input and returns (new_dict, changed_bool).
    """
    if data is None:
        data = {}

    new = copy.deepcopy(data)
    changed = False

    # tags: set default when missing or empty
    tags = new.get("tags")
    if tags is None or tags == []:
        new["tags"] = ["application"]
        changed = True
    else:
        # normalize tags to strings and lowercase
        normalized = [str(t).lower() for t in tags]
        if normalized != tags:
            new["tags"] = normalized
            changed = True

    # license: always enforce GPL-3.0-or-later
    desired_license = ["GPL-3.0-or-later"]
    if new.get("license") != desired_license:
        new["license"] = desired_license
        changed = True

    # license_file: remove when empty or when 'license' key is present
    if "license_file" in new:
        lf = new.get("license_file")
        if (
            lf is None
            or (isinstance(lf, str) and lf.strip() == "")
            or ("license" in new and new.get("license"))
        ):
            del new["license_file"]
            changed = True

    # version: ensure it's a string
    if (
        "version" in new
        and new["version"] is not None
        and not isinstance(new["version"], str)
    ):
        new["version"] = str(new["version"])
        changed = True

    # namespace and name: normalize to lowercase strings
    for key in ("namespace", "name"):
        if key in new and new[key] is not None:
            val = str(new[key])
            if val.lower() != val:
                new[key] = val.lower()
                changed = True

    # authors: ensure it's a list
    if (
        "authors" in new
        and new["authors"] is not None
        and not isinstance(new["authors"], list)
    ):
        new["authors"] = [new["authors"]]
        changed = True

    # Remove keys that are empty strings (common scaffold placeholders)
    for k in list(new.keys()):
        v = new.get(k)
        if isinstance(v, str) and v.strip() == "":
            del new[k]
            changed = True

    return new, changed


def dump_yaml_to_string(data):
    """Dump YAML with consistent formatting and 2-space indentation."""
    dumped = yaml.dump(
        data,
        Dumper=TwoSpaceIndentDumper,
        default_flow_style=False,
        sort_keys=False,
        width=1000,
    )
    # Ensure leading document marker for readability
    if not dumped.startswith("---"):
        dumped = "---\n" + dumped
    return dumped


def get_git_author():
    """Return the git configured author as 'Name <email>' or None.

    Uses `git config --get user.name` and `git config --get user.email`.
    Returns None when neither name nor email is available.
    """
    try:
        name = subprocess.check_output(
            ["git", "config", "--get", "user.name"], text=True
        ).strip()
    except Exception:
        name = ""
    try:
        email = subprocess.check_output(
            ["git", "config", "--get", "user.email"], text=True
        ).strip()
    except Exception:
        email = ""

    if not name and not email:
        return None
    if name and email:
        return f"{name} <{email}>"
    return name or email


def parse_github_remote_url(url: str):
    """Parse a git remote URL and return a dict with owner, repo and canonical https url.

    Returns None when the url does not look like a GitHub remote.
    """
    if not url:
        return None
    u = url.strip()
    if u.endswith(".git"):
        u = u[:-4]

    path = None
    if u.startswith("git@github.com:"):
        path = u[len("git@github.com:") :]
    else:
        for prefix in (
            "ssh://git@github.com/",
            "https://github.com/",
            "http://github.com/",
            "git://github.com/",
        ):
            if u.startswith(prefix):
                path = u[len(prefix) :]
                break
        if path is None:
            idx = u.find("github.com/")
            if idx != -1:
                path = u[idx + len("github.com/") :]

    if not path:
        return None
    parts = path.split("/")
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1]
    canonical = f"https://github.com/{owner}/{repo}"
    return {"owner": owner, "repo": repo, "url": canonical}


def get_git_remote_info(root_dir: str):
    """Return parsed git remote info for the repo at root_dir or None.

    Result contains keys: owner, repo, url, default_branch
    """
    try:
        out = subprocess.check_output(
            ["git", "-C", root_dir, "remote", "-v"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return None

    remote_url = None
    for line in out.splitlines():
        parts = line.split()
        if (
            len(parts) >= 3
            and parts[2].startswith("(")
            and "fetch" in parts[2]
            and parts[0] == "origin"
        ):
            remote_url = parts[1]
            break

    if not remote_url:
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 3 and "fetch" in parts[2]:
                remote_url = parts[1]
                break

    if not remote_url:
        return None

    parsed = parse_github_remote_url(remote_url)
    if not parsed:
        return None

    # try to discover default branch
    default_branch = None
    try:
        out2 = subprocess.check_output(
            ["git", "-C", root_dir, "remote", "show", "origin"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        for line in out2.splitlines():
            if "HEAD branch:" in line:
                default_branch = line.split(":", 1)[1].strip()
                break
    except Exception:
        default_branch = None

    if not default_branch:
        for candidate in ("main", "master"):
            try:
                subprocess.check_output(
                    [
                        "git",
                        "-C",
                        root_dir,
                        "rev-parse",
                        "--verify",
                        f"origin/{candidate}",
                    ],
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
                default_branch = candidate
                break
            except Exception:
                continue

    if not default_branch:
        default_branch = "master"

    parsed["default_branch"] = default_branch
    return parsed


def process_galaxy_file(file_path, repo_info=None, dry_run=False, verbose=False):
    """Process a single galaxy.yml file. Returns True if file was updated."""
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            original_text = fh.read()

        original_dict = yaml.safe_load(original_text)
        new_dict, changed_by_fix = _fix_galaxy_dict(original_dict)

        # Try to set authors from git config when authors are missing or look like placeholders
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

        # Use git remote info to set repository/homepage/documentation/issues when available
        changed_by_repo = False
        if repo_info:
            repo_url = repo_info.get("url")
            default_branch = repo_info.get("default_branch", "master")

            # repository: set when missing or clearly a placeholder
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
                # look for pattern: collections/ansible_collections/<namespace>/<collection>
                if "collections" in parts:
                    idx = parts.index("collections")
                    if idx + 3 < len(parts) and parts[idx + 1] == "ansible_collections":
                        collection_parts = parts[idx : idx + 4]
                        collection_path = "/".join(collection_parts)
                        collection_url = (
                            f"{repo_url}/tree/{default_branch}/{collection_path}"
                        )
            except Exception:
                collection_url = None

            # homepage: prefer the collection path when available, otherwise repo root
            homepage_val = new_dict.get("homepage")
            homepage_target = collection_url if collection_url else repo_url

            def _norm(u):
                return str(u).rstrip("/") if u else ""

            if collection_url:
                # override homepage to collection path when it's different
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

            # documentation: point to the docs folder under the collection path when possible
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

            # issues: point to the GitHub issues page for the repo
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

        # Backup the original file
        shutil.copyfile(file_path, file_path + ".bak")

        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(new_text)

        print(f"Updated: {file_path} (backup at {file_path}.bak)")
        return True

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False


def process_runtime_file(file_path, dry_run=False, verbose=False):
    """Process a single meta/runtime.yml file. Returns True if file was updated."""
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            original_text = fh.read()

        original_dict = yaml.safe_load(original_text) or {}
        changed = False

        # Ensure requires_ansible exists
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
    """Recursively process all galaxy.yml and meta/runtime.yml files under root_dir."""
    updated = 0
    # Collect git remote info once for the repository root
    repo_info = get_git_remote_info(root_dir)
    if verbose and repo_info:
        print(
            f"Using git remote: {repo_info.get('url')} (default branch: {repo_info.get('default_branch')})"
        )
    for root, _, files in os.walk(root_dir):
        for fname in files:
            if fname == "galaxy.yml":
                file_path = os.path.join(root, fname)
                if process_galaxy_file(
                    file_path, repo_info=repo_info, dry_run=dry_run, verbose=verbose
                ):
                    updated += 1
            elif fname == "runtime.yml" and os.path.basename(root) == "meta":
                file_path = os.path.join(root, fname)
                if process_runtime_file(file_path, dry_run=dry_run, verbose=verbose):
                    updated += 1
    return updated


def ensure_changelog(root_dir, dry_run=False, verbose=False):
    """Create a basic CHANGELOG.md in each collection if one does not exist.

    Scans for paths matching collections/ansible_collections/<namespace>/<collection>.
    Returns the number of changelogs created (or that would be created in dry-run).
    """
    created = 0

    # If root_dir itself points at a collection directory like
    # .../collections/ansible_collections/<namespace>/<collection>,
    # just operate on that single collection.
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
                # abs_root should already be the collection directory when --collection was used
                candidates.append(abs_root)
    except Exception:
        candidates = []

    def _create_md(target_path):
        header = (
            "# Changelog\n\n"
            "All notable changes to this collection will be documented in this file.\n\n"
            "The format is based on Keep a Changelog "
            "(https://keepachangelog.com/en/1.0.0/) and this project follows Semantic Versioning.\n\n"
            "## Unreleased\n\n"
            "- Initial scaffold\n"
        )
        if dry_run:
            if verbose:
                print(f"DRY RUN - would create: {target_path}")
        else:
            with open(target_path, "w", encoding="utf-8") as fh:
                fh.write(header)
            print(f"Created: {target_path}")

    # Prefer direct path when present (only if we haven't set a candidate above)
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
        # Fallback: walk and detect ansible_collections directories
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
        md_path = os.path.join(col_dir, "CHANGELOG.md")
        rst_path = os.path.join(col_dir, "CHANGELOG.rst")
        if os.path.exists(md_path) or os.path.exists(rst_path):
            continue
        _create_md(md_path)
        created += 1

    return created


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Normalize galaxy.yml files to reduce ansible-lint warnings"
    )
    # No positional root_dir: operate relative to repository root (current working directory).
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--collection",
        "-c",
        dest="collection",
        help="Process only the specified collection in 'namespace.collection' format",
    )
    # Ensure changelogs are always created for collections/ansible_collections
    # (previously controlled via --ensure-changelog flag)

    args = parser.parse_args(argv)

    repo_root = os.path.abspath(".")

    # Determine the target root_directory:
    # - If --collection specified: collections/ansible_collections/<namespace>/<collection>
    # - Otherwise: collections/ansible_collections (process all collections)
    if args.collection:
        col = args.collection.strip()
        if "." not in col:
            print("Error: --collection must be in 'namespace.collection' format.")
            return 2
        namespace, collection = col.split(".", 1)
        # normalize parts to lowercase and strip whitespace
        namespace = namespace.strip().lower()
        collection = collection.strip().lower()
        root_directory = os.path.join(
            repo_root, "collections", "ansible_collections", namespace, collection
        )
    else:
        root_directory = os.path.join(repo_root, "collections", "ansible_collections")

    if not os.path.isdir(root_directory):
        print(f"Error: The directory '{root_directory}' does not exist.")
        return 2

    if args.verbose:
        print(
            f"Searching for galaxy.yml files under: {os.path.abspath(root_directory)}"
        )

    updated_count = process_galaxy_files(
        root_directory, dry_run=args.dry_run, verbose=args.verbose
    )

    # Always ensure changelog files exist for collections
    changelog_count = ensure_changelog(
        root_directory, dry_run=args.dry_run, verbose=args.verbose
    )

    if args.dry_run:
        print(f"Dry run complete. Files that would be updated: {updated_count}")
        print(f"Dry run: changelogs that would be created: {changelog_count}")
    else:
        print(f"Processing complete. Files updated: {updated_count}")
        print(f"Changelogs created: {changelog_count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
