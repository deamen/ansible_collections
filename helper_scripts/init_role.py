#!/usr/bin/python3
from ansible.cli.galaxy import GalaxyCLI
import sys
import argparse
import os

DEFAULT_COLLECTION_PATH = "collections/ansible_collections/"
DEFAULT_INIT_PATH = DEFAULT_COLLECTION_PATH


def main():
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
    known, unknown = parser.parse_known_args()

    role_arg = known.role
    init_path = known.init_path
    role_name = role_arg

    parts = role_arg.split(".") if role_arg else []
    if len(parts) == 3:
        namespace, collection, role_name = parts
        # Only compute collection-based init path when user did not override --init-path
        if known.init_path == DEFAULT_INIT_PATH:
            init_path = os.path.join(
                DEFAULT_COLLECTION_PATH, namespace, collection, "roles"
            )

    args = [
        "ansible-galaxy",
        "role",
        "init",
        "--init-path",
        init_path,
        role_name,
    ] + unknown

    cli = GalaxyCLI(args=args)
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
