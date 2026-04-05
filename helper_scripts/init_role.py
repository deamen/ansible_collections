#!/usr/bin/python3
"""
Ansible Role Initialization Helper

This script initializes Ansible roles using ansible-galaxy and customizes them
by replacing the default README with a template and removing the tests folder.
"""

import argparse
import os
import shutil
import subprocess
import sys

from ansible.cli.galaxy import GalaxyCLI

DEFAULT_COLLECTION_PATH = "collections/ansible_collections/"
DEFAULT_INIT_PATH = DEFAULT_COLLECTION_PATH


def get_git_config_value(key):
    """Get a value from git config."""
    try:
        result = subprocess.run(
            ["git", "config", "--get", key], capture_output=True, text=True, check=True
        )
        value = result.stdout.strip()
        return value if value else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_author_info():
    """Get author information from git config."""
    name = get_git_config_value("user.name")
    email = get_git_config_value("user.email")

    if name and email:
        return f"{name} <{email}>"
    elif name:
        return name
    else:
        return "author_info"


def build_readme_template(role_name):
    """Build the README template for the role."""
    author_line = get_author_info()

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
    """Customize the created role by replacing README and removing tests."""
    role_dir = os.path.join(init_path, role_name)

    # Replace README.md with template
    readme_path = os.path.join(role_dir, "README.md")
    readme_template = build_readme_template(role_name)

    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_template)
        print(f"Replaced README.md in {role_dir} with custom template")
    except Exception as e:
        print(f"Warning: Could not replace README.md: {e}", file=sys.stderr)

    # Remove tests/ folder
    tests_dir = os.path.join(role_dir, "tests")
    if os.path.exists(tests_dir):
        try:
            shutil.rmtree(tests_dir)
            print(f"Removed tests/ folder from {role_dir}")
        except Exception as e:
            print(f"Warning: Could not remove tests/ folder: {e}", file=sys.stderr)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Init an Ansible role (helper)")
    parser.add_argument(
        "--init-path",
        default=DEFAULT_INIT_PATH,
        help="Path where the role will be created (overrides FQCN-derived path)",
    )
    parser.add_argument(
        "--role",
        required=True,
        help="Role name. FQCN format: <namespace>.<collection>.<role_name> or simple role name",
    )
    return parser.parse_known_args()


def determine_role_path(role_arg, init_path):
    """Determine the role name and init path based on FQCN or simple name."""
    role_name = role_arg
    parts = role_arg.split(".") if role_arg else []

    if len(parts) == 3:
        namespace, collection, role_name = parts
        # Only compute collection-based init path when user did not override --init-path
        if init_path == DEFAULT_INIT_PATH:
            init_path = os.path.join(
                DEFAULT_COLLECTION_PATH, namespace, collection, "roles"
            )

    return role_name, init_path


def run_ansible_galaxy(args):
    """Run ansible-galaxy role init and return exit code."""
    cli = GalaxyCLI(args=args)
    try:
        exit_code = cli.run()
    except SystemExit as e:
        exit_code = e.code

    # Some CLI implementations return None on success; normalize to 0
    if exit_code is None:
        exit_code = 0

    print(f"ansible-galaxy role init exited with code {exit_code}")
    return exit_code


def main():
    """Main entry point."""
    known, unknown = parse_arguments()

    role_arg = known.role
    init_path = known.init_path

    role_name, init_path = determine_role_path(role_arg, init_path)

    args = [
        "ansible-galaxy",
        "role",
        "init",
        "--init-path",
        init_path,
        role_name,
    ] + unknown

    exit_code = run_ansible_galaxy(args)

    if exit_code == 0:
        customize_role(init_path, role_name)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
