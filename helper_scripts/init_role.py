#!/usr/bin/python3
"""Ansible role management tool.

Initialises a new Ansible role and automatically applies lint fixes:

    init_role.py --role [namespace.collection.]role_name [--init-path PATH] [--force]

Shared utilities (get_git_author, run_ansible_galaxy, DEFAULT_COLLECTION_PATH, …)
live in ansible_utils.py.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

# Ensure the directory containing this script is on the path so that
# ansible_utils can always be imported regardless of cwd.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ansible_utils import (
    DEFAULT_COLLECTION_PATH,
    get_git_author,
    run_ansible_galaxy,
)

# ---------------------------------------------------------------------------
# Templates used by the fix subcommand
# ---------------------------------------------------------------------------

META_TEMPLATE = """---
galaxy_info:
    author: {author}
    description: your role description
    company: Yobibyte
    license: GPL-3.0-or-later

    min_ansible_version: "2.14"

    galaxy_tags: []

dependencies: []
"""


# ---------------------------------------------------------------------------
# init subcommand helpers
# ---------------------------------------------------------------------------


def build_readme_template(role_name):
    """Return a README.md template string populated with *role_name* and author."""
    author_line = get_git_author(fallback="author_info")

    header = f"{role_name}\n{'=' * len(role_name)}\n\n"

    body = f"""A brief description of the role goes here.

Requirements
------------


Role Variables
--------------


Dependencies
------------


Example Playbook
----------------


License
-------

GPL-3.0-or-later

Author Information
------------------

{author_line}

"""
    return header + body


def customize_role(init_path, role_name):
    """Replace the generated README and remove the tests/ folder for *role_name*."""
    role_dir = os.path.join(init_path, role_name)

    readme_path = os.path.join(role_dir, "README.md")
    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(build_readme_template(role_name))
        print(f"Replaced README.md in {role_dir} with custom template")
    except Exception as e:
        print(f"Warning: Could not replace README.md: {e}", file=sys.stderr)

    tests_dir = os.path.join(role_dir, "tests")
    if os.path.exists(tests_dir):
        try:
            shutil.rmtree(tests_dir)
            print(f"Removed tests/ folder from {role_dir}")
        except Exception as e:
            print(f"Warning: Could not remove tests/ folder: {e}", file=sys.stderr)


def determine_role_path(role_arg, init_path):
    """Return ``(role_name, resolved_init_path)`` from a FQCN or simple role name.

    When *role_arg* is a 3-part FQCN (``namespace.collection.role``) and the
    caller did not override *init_path*, the path is resolved to the roles/
    directory of the named collection.
    """
    role_name = role_arg
    parts = role_arg.split(".") if role_arg else []

    if len(parts) == 3:
        namespace, collection, role_name = parts
        if init_path == DEFAULT_COLLECTION_PATH:
            init_path = os.path.join(
                DEFAULT_COLLECTION_PATH, namespace, collection, "roles"
            )

    return role_name, init_path


# ---------------------------------------------------------------------------
# fix subcommand helpers
# ---------------------------------------------------------------------------


def remove_spdx_license(file_path):
    """Remove SPDX-License-Identifier lines from *file_path*.

    Returns True if the file was modified.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = [line for line in lines if "SPDX-License-Identifier" not in line]

        if len(new_lines) != len(lines):
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            return True

        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return False


def replace_meta_main(role_dir):
    """Replace meta/main.yml with the standard template when it contains
    the placeholder ``author: your name``.

    Returns True if the file was replaced.
    """
    meta_path = Path(role_dir) / "meta" / "main.yml"

    if not meta_path.exists():
        print(f"Warning: {meta_path} does not exist, skipping...")
        return False

    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "author: your name" in content:
            author = get_git_author(fallback="your name")
            with open(meta_path, "w", encoding="utf-8") as f:
                f.write(META_TEMPLATE.format(author=author))
            print(f"Replaced: {meta_path}")
            return True
        else:
            print(f"Skipping {meta_path} (does not contain 'author: your name')")
            return False
    except Exception as e:
        print(f"Error replacing {meta_path}: {e}", file=sys.stderr)
        return False


def find_yaml_files(directory):
    """Yield Path objects for every YAML file found recursively under *directory*."""
    path = Path(directory)
    for pattern in ("*.yml", "*.yaml"):
        for file_path in path.rglob(pattern):
            if file_path.is_file():
                yield file_path


def clean_role(role_dir, fqcn):
    """Apply all lint fixes to an Ansible role directory."""
    role_path = Path(role_dir)

    if not role_path.exists():
        print(f"Error: Directory {role_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    if not role_path.is_dir():
        print(f"Error: {role_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Cleaning role directory: {role_dir}")
    print("-" * 60)

    modified_count = 0
    total_count = 0
    for file_path in find_yaml_files(role_path):
        total_count += 1
        if remove_spdx_license(file_path):
            print(f"Cleaned: {file_path}")
            modified_count += 1

    print(f"\nProcessed {total_count} files, modified {modified_count} files")

    print("\nReplacing meta/main.yml with template...")
    replace_meta_main(role_path)

    print("\nCleanup complete!")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Initialise a new Ansible role and automatically apply lint fixes."
        )
    )
    parser.add_argument(
        "--role",
        required=True,
        help=(
            "Role name. FQCN format: <namespace>.<collection>.<role_name> "
            "or simple role name"
        ),
    )
    parser.add_argument(
        "--init-path",
        default=DEFAULT_COLLECTION_PATH,
        help=(
            f"Path where the role will be created (default: {DEFAULT_COLLECTION_PATH})"
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the role directory if it already exists",
    )

    known = parser.parse_args(argv)

    role_name, init_path = determine_role_path(known.role, known.init_path)

    # --- init ---------------------------------------------------------------
    galaxy_args = [
        "ansible-galaxy",
        "role",
        "init",
        "--init-path",
        init_path,
        role_name,
    ]
    if known.force:
        galaxy_args.append("--force")

    exit_code = run_ansible_galaxy(galaxy_args)
    if exit_code != 0:
        sys.exit(exit_code)

    # --- fix (automatic) ----------------------------------------------------
    customize_role(init_path, role_name)

    # Apply deeper lint fixes when a full FQCN was supplied.
    parts = known.role.split(".")
    if len(parts) == 3:
        role_dir = os.path.join(init_path, role_name)
        clean_role(role_dir, known.role)


if __name__ == "__main__":
    main()
