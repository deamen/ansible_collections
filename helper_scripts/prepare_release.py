#!/usr/bin/python3
"""Prepare a collection release.

    prepare_release.py -c PATH [--version X.Y.Z] [--dry-run]

Picks the release version, writes it to galaxy.yml, and runs
``antsibull-changelog release`` in the collection root, which records the
release in changelogs/changelog.yaml, regenerates CHANGELOG.md, and deletes
the consumed fragments.

Without --version the latest version in changelogs/changelog.yaml is bumped
by one part, chosen from the fragment sections:

    breaking_changes, removed_features          -> major
    major_changes, minor_changes,
    deprecated_features                         -> minor
    anything else (bugfixes, security_fixes, …) -> patch

Review and commit the result, then run release.py to tag it.
"""

import argparse
import os
import shutil
import subprocess
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ansible_utils import (
    format_version,
    list_fragments,
    load_galaxy,
    load_released_versions,
    parse_version,
    resolve_collection_dir,
)

MAJOR_SECTIONS = {"breaking_changes", "removed_features"}
MINOR_SECTIONS = {"major_changes", "minor_changes", "deprecated_features"}
# Sections that do not change the code; they never decide the bump.
IGNORED_SECTIONS = {"release_summary"}


def read_fragment_sections(fragments):
    """Return the set of section names used by the YAML *fragments*."""
    sections = set()
    for path in fragments:
        if not path.endswith((".yml", ".yaml")):
            continue
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if not isinstance(data, dict):
            print(f"Error: fragment is not a YAML mapping: {path}")
            sys.exit(1)
        sections.update(str(key) for key in data)
    return sections - IGNORED_SECTIONS


def bump_part(sections):
    """Return 'major', 'minor' or 'patch' for the fragment *sections*."""
    if sections & MAJOR_SECTIONS:
        return "major"
    if sections & MINOR_SECTIONS:
        return "minor"
    return "patch"


def bump_version(current, part):
    """Return *current* (a version tuple) with *part* increased by one."""
    major, minor, patch = current
    if part == "major":
        return (major + 1, 0, 0)
    if part == "minor":
        return (major, minor + 1, 0)
    return (major, minor, patch + 1)


def current_version(col_dir, galaxy):
    """Return the latest released version tuple of the collection.

    That is the highest x.y.z in changelogs/changelog.yaml, or the galaxy.yml
    version when the changelog has no release yet.
    """
    released = [parse_version(v) for v in load_released_versions(col_dir)]
    released = [v for v in released if v]
    if released:
        return max(released)
    version = parse_version(galaxy.get("version", ""))
    if not version:
        print(f"Error: galaxy.yml version '{galaxy.get('version')}' is not x.y.z.")
        sys.exit(1)
    return version


def set_galaxy_version(col_dir, version):
    """Rewrite the top-level ``version:`` line of galaxy.yml, keeping the rest as is."""
    path = os.path.join(col_dir, "galaxy.yml")
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    for i, line in enumerate(lines):
        if line.startswith("version:"):
            lines[i] = f"version: {version}\n"
            break
    else:
        print(f"Error: no top-level 'version:' line in {path}")
        sys.exit(1)
    with open(path, "w", encoding="utf-8") as fh:
        fh.writelines(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Bump the collection version and run 'antsibull-changelog release'."
    )
    parser.add_argument(
        "-c",
        "--collection",
        required=True,
        help="Path to the collection root, or 'namespace.name'",
    )
    parser.add_argument(
        "--version",
        help="Release version in x.y.z format (default: bump from the changelog fragments)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the version that would be released and change nothing",
    )
    args = parser.parse_args(argv)

    col_dir = resolve_collection_dir(args.collection)
    galaxy = load_galaxy(col_dir)
    fqcn = f"{galaxy.get('namespace')}.{galaxy.get('name')}"
    current = current_version(col_dir, galaxy)
    fragments = list_fragments(col_dir)

    if args.version:
        new = parse_version(args.version)
        if not new:
            print(f"Error: --version '{args.version}' is not in x.y.z format.")
            sys.exit(2)
        if new <= current:
            print(
                f"Error: --version {format_version(new)} must be newer than "
                f"the latest release {format_version(current)}."
            )
            sys.exit(2)
        reason = "set by --version"
    else:
        sections = read_fragment_sections(fragments)
        if not sections:
            print(
                f"Error: {fqcn} has no changelog fragments to release; "
                "add a fragment or pass --version."
            )
            sys.exit(1)
        part = bump_part(sections)
        new = bump_version(current, part)
        reason = f"{part} bump from sections: {', '.join(sorted(sections))}"

    version = format_version(new)
    print(f"{fqcn}: {format_version(current)} -> {version} ({reason})")

    if args.dry_run:
        print("Dry run: nothing changed.")
        return

    antsibull = shutil.which("antsibull-changelog")
    if antsibull is None:
        print(
            "Error: antsibull-changelog not found; install it with "
            "'pip install --user antsibull-changelog'."
        )
        sys.exit(1)

    set_galaxy_version(col_dir, version)
    print(f"Updated: {os.path.join(col_dir, 'galaxy.yml')}")

    # antsibull-changelog writes a plugin cache; drop it unless the collection
    # already keeps one, so it does not show up as a new untracked file.
    plugin_cache = os.path.join(col_dir, "changelogs", ".plugin-cache.yaml")
    had_plugin_cache = os.path.exists(plugin_cache)

    result = subprocess.run([antsibull, "release", "--version", version], cwd=col_dir)
    if not had_plugin_cache and os.path.exists(plugin_cache):
        os.remove(plugin_cache)
    if result.returncode != 0:
        print(
            "Error: antsibull-changelog release failed; galaxy.yml already has "
            f"version {version}. Fix the problem and rerun with --version {version}, "
            "or restore galaxy.yml."
        )
        sys.exit(result.returncode)

    print(
        f"Prepared {fqcn} {version}. Review and commit the changes, push them, "
        f"then run: helper_scripts/release.py -c {args.collection}"
    )


if __name__ == "__main__":
    main()
