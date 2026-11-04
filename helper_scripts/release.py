#!/usr/bin/python3
"""Tag a prepared collection release and push the tag.

    release.py -c PATH [--remote origin] [--no-push]

Run after prepare_release.py once its changes are committed and pushed.
Creates the ``release_<namespace>.<name>_v<version>`` tag on HEAD for the
galaxy.yml version and pushes it, which starts the matching
``release_<namespace>.<name>.yml`` workflow.

Before tagging it runs the release workflow's checks, so a release that
would fail there stops here instead:

- changelogs/changelog.yaml has an entry for the galaxy.yml version
- changelogs/fragments/ has no files other than .keep
- the collection has no uncommitted changes
- the tag does not exist yet
"""

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ansible_utils import (
    list_fragments,
    load_galaxy,
    load_released_versions,
    parse_version,
    resolve_collection_dir,
)


def git(col_dir, *args, check=True):
    """Run git in *col_dir* and return its stripped stdout."""
    result = subprocess.run(
        ["git", "-C", col_dir, *args], capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f"Error: git {' '.join(args)} failed: {result.stderr.strip()}")
        sys.exit(result.returncode)
    return result.stdout.strip()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Tag a prepared collection release and push the tag."
    )
    parser.add_argument(
        "-c",
        "--collection",
        required=True,
        help="Path to the collection root, or 'namespace.name'",
    )
    parser.add_argument(
        "--remote", default="origin", help="Git remote to push to (default: origin)"
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Create the tag locally but do not push it",
    )
    args = parser.parse_args(argv)

    col_dir = resolve_collection_dir(args.collection)
    galaxy = load_galaxy(col_dir)
    fqcn = f"{galaxy.get('namespace')}.{galaxy.get('name')}"
    version = str(galaxy.get("version", ""))
    tag = f"release_{fqcn}_v{version}"

    errors = []
    if not parse_version(version):
        errors.append(f"galaxy.yml version '{version}' is not x.y.z")
    if version not in load_released_versions(col_dir):
        errors.append(
            f"changelogs/changelog.yaml has no release {version}; run prepare_release.py"
        )
    fragments = list_fragments(col_dir)
    if fragments:
        names = ", ".join(os.path.basename(f) for f in fragments)
        errors.append(
            f"unreleased fragments in changelogs/fragments/: {names}; run prepare_release.py"
        )
    if git(col_dir, "status", "--porcelain", "--", "."):
        errors.append("the collection has uncommitted changes; commit them first")
    if git(col_dir, "tag", "--list", tag):
        errors.append(f"tag {tag} already exists")

    if errors:
        print(f"Error: cannot release {fqcn} {version}:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    if not git(col_dir, "branch", "--remotes", "--contains", "HEAD", check=False):
        print(
            f"Warning: HEAD is not on any remote branch; push the release commit "
            f"to {args.remote} as well."
        )

    git(col_dir, "tag", tag)
    print(f"Created tag {tag} on {git(col_dir, 'rev-parse', '--short', 'HEAD')}")

    if args.no_push:
        print(f"Not pushed. To publish: git push {args.remote} {tag}")
        return

    git(col_dir, "push", args.remote, tag)
    print(f"Pushed {tag} to {args.remote}; the release_{fqcn}.yml workflow will run.")


if __name__ == "__main__":
    main()
