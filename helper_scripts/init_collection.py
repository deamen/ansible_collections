#!/usr/bin/python3
from ansible.cli.galaxy import GalaxyCLI
import sys
import argparse

DEFAULT_INIT_PATH = "collections/ansible_collections/"


def main():
    parser = argparse.ArgumentParser(description="Init an Ansible collection (helper)")
    parser.add_argument(
        "--init-path",
        default=DEFAULT_INIT_PATH,
        help="Path where the collection will be created",
    )
    parser.add_argument(
        "--collection", required=True, help="Collection name (namespace.collection)"
    )
    known, unknown = parser.parse_known_args()

    args = [
        "ansible-galaxy",
        "collection",
        "init",
        "--init-path",
        known.init_path,
        known.collection,
    ] + unknown

    cli = GalaxyCLI(args=args)
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
