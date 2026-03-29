#!/usr/bin/env python3
"""
Script to clean up Ansible roles for ansible-lint violations.

This script:
1. Removes SPDX-License-Identifier lines from all YAML files
2. Replaces meta/main.yml with a standardized template
3. Replaces tests/test.yml with a standardized template (if it contains '- hosts: localhost')
4. Replaces tests/inventory with a standardized template
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

DEFAULT_COLLECTION_PATH = "collections/ansible_collections/"


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

TEST_TEMPLATE = """---
- name: Dummy test playbook for your_role role
  hosts: localhost
  become: true
  tasks:
    - name: Import role via FQCN
      ansible.builtin.import_role:
        name: your_namespace.your_collection.your_role
"""

INVENTORY_TEMPLATE = """---
all:
  hosts:
    # localhost is added here to avoid typing -i localhost,
    # when we need to run playbooks on localhost.
    localhost:
"""


def get_git_author():
    """Return the git-config `user.name` if available, otherwise fallback.

    Falls back to environment variables or 'your name' when not found.
    """
    try:
        name = (
            subprocess.check_output(
                ["git", "config", "--get", "user.name"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
        if name:
            return name
    except Exception:
        pass

    # Fallbacks
    return (
        os.environ.get("GIT_AUTHOR_NAME")
        or os.environ.get("USER")
        or os.environ.get("USERNAME")
        or "your name"
    )


def remove_spdx_license(file_path):
    """
    Remove SPDX-License-Identifier lines from a file.

    Args:
        file_path: Path to the file to clean

    Returns:
        bool: True if file was modified, False otherwise
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Filter out SPDX license lines
        new_lines = [line for line in lines if "SPDX-License-Identifier" not in line]

        # Check if file was modified
        if len(new_lines) != len(lines):
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            return True

        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return False


def replace_meta_main(role_dir):
    """
    Replace meta/main.yml with the standard template if it contains 'author: your name'.

    Args:
        role_dir: Path to the role directory

    Returns:
        bool: True if file was replaced, False otherwise
    """
    meta_path = Path(role_dir) / "meta" / "main.yml"

    if not meta_path.exists():
        print(f"Warning: {meta_path} does not exist, skipping...")
        return False

    try:
        # Check if file contains 'author: your name'
        with open(meta_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "author: your name" in content:
            author = get_git_author()
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


def replace_test_yml(role_dir, fqcn):
    """
    Replace tests/test.yml with the standard template, replacing placeholders with the FQCN values.

    Args:
        role_dir: Path to the role directory
        fqcn: Fully Qualified Collection Name (namespace.collection.role_name)

    Returns:
        bool: True if file was replaced, False otherwise
    """
    test_path = Path(role_dir) / "tests" / "test.yml"

    if not test_path.exists():
        print(f"Warning: {test_path} does not exist, skipping...")
        return False

    try:
        # Parse the FQCN
        namespace, collection, role_name = fqcn.split(".")

        # Replace placeholders in the template
        customized_template = TEST_TEMPLATE.replace("your_namespace", namespace)
        customized_template = customized_template.replace("your_collection", collection)
        customized_template = customized_template.replace("your_role", role_name)

        # Check if file contains '- hosts: localhost'
        with open(test_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "- hosts: localhost" in content:
            with open(test_path, "w", encoding="utf-8") as f:
                f.write(customized_template)
            print(f"Replaced: {test_path}")
            return True
        else:
            print(f"Skipping {test_path} (does not contain '- hosts: localhost')")
            return False
    except Exception as e:
        print(f"Error replacing {test_path}: {e}", file=sys.stderr)
        return False


def replace_inventory(role_dir):
    """
    Replace tests/inventory with the standard template and rename to inventory.yml.

    Args:
        role_dir: Path to the role directory

    Returns:
        bool: True if file was replaced, False otherwise
    """
    inventory_path = Path(role_dir) / "tests" / "inventory"
    inventory_yml_path = Path(role_dir) / "tests" / "inventory.yml"

    if not inventory_path.exists():
        print(f"Warning: {inventory_path} does not exist, skipping...")
        return False

    try:
        # Write template to inventory.yml
        with open(inventory_yml_path, "w", encoding="utf-8") as f:
            f.write(INVENTORY_TEMPLATE)

        # Remove old inventory file if it still exists
        if inventory_path.exists():
            inventory_path.unlink()

        print(f"Replaced and renamed: {inventory_path} -> {inventory_yml_path}")
        return True
    except Exception as e:
        print(f"Error replacing {inventory_path}: {e}", file=sys.stderr)
        return False


def find_files_to_clean(directory):
    """
    Recursively find all YAML files to clean in a directory.

    Args:
        directory: Directory to search

    Yields:
        Path objects for each YAML file found
    """
    path = Path(directory)

    # Find YAML files
    for pattern in ["*.yml", "*.yaml"]:
        for file_path in path.rglob(pattern):
            if file_path.is_file():
                yield file_path


def clean_role(role_dir, fqcn):
    """
    Clean up an Ansible role directory.

    Args:
        role_dir: Path to the role directory
        fqcn: Fully Qualified Collection Name (namespace.collection.role_name)
    """
    role_path = Path(role_dir)

    if not role_path.exists():
        print(f"Error: Directory {role_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    if not role_path.is_dir():
        print(f"Error: {role_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Cleaning role directory: {role_dir}")
    print("-" * 60)

    # Find and process all YAML files
    modified_count = 0
    total_count = 0

    for file_path in find_files_to_clean(role_path):
        total_count += 1
        if remove_spdx_license(file_path):
            print(f"Cleaned: {file_path}")
            modified_count += 1

    print(f"\nProcessed {total_count} files, modified {modified_count} files")

    # Replace meta/main.yml
    print("\nReplacing meta/main.yml with template...")
    replace_meta_main(role_path)

    # Replace tests/test.yml if applicable
    print("\nReplacing tests/test.yml with template...")
    replace_test_yml(role_path, fqcn)

    # Replace tests/inventory
    print("\nReplacing tests/inventory with template...")
    replace_inventory(role_path)

    print("\nCleanup complete!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Clean up Ansible roles for ansible-lint violations"
    )
    parser.add_argument(
        "--role",
        required=True,
        help="Role name in FQCN format: <namespace>.<collection>.<role_name>",
    )

    args = parser.parse_args()

    fqcn = args.role
    parts = fqcn.split(".")
    if len(parts) == 3:
        namespace, collection, role_name = parts
        role_path = os.path.join(
            DEFAULT_COLLECTION_PATH, namespace, collection, "roles", role_name
        )

        if os.path.isdir(role_path):
            clean_role(role_path, fqcn)
        else:
            print(
                f"Error: Role directory not found for FQCN '{fqcn}'.\n"
                f"Checked: {role_path}",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        print(
            "Error: --role must be FQCN format '<namespace>.<collection>.<role_name>'",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
