#!/usr/bin/python3
import argparse
import os
import shutil
import sys

DEFAULT_COLLECTION_PATH = "collections/ansible_collections/"
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "files", "molecule_template")
DEFAULT_TEMPLATE_DIR = os.path.join(TEMPLATE_PATH, "default")
TEMPLATE_REQUIREMENTS_FILE = os.path.join(TEMPLATE_PATH, "requirements.yml")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Init a Molecule scenario for an Ansible collection"
    )
    parser.add_argument(
        "--collection",
        required=True,
        help="Collection name (namespace.collection)",
    )
    parser.add_argument(
        "--scenario",
        required=False,
        default="default",
        help="Scenario name (will be created under collection's molecule/ directory). Defaults to 'default'",
    )
    return parser.parse_args()


def get_collection_molecule_path(collection_fqcn):
    parts = collection_fqcn.split(".")
    if len(parts) != 2:
        raise ValueError("Collection FQCN must be in the form <namespace>.<collection>")
    namespace, collection = parts
    return os.path.join(
        DEFAULT_COLLECTION_PATH, namespace, collection, "extensions", "molecule"
    )


def ensure_collection_requirements_file(molecule_dir):
    requirements_src = TEMPLATE_REQUIREMENTS_FILE
    requirements_dst = os.path.join(molecule_dir, "requirements.yml")

    if os.path.exists(requirements_dst):
        return

    if os.path.exists(requirements_src):
        shutil.copyfile(requirements_src, requirements_dst)
        print(f"Copied collection requirements to {requirements_dst}")
        return

    print(
        f"Template requirements not found: {requirements_src}",
        file=sys.stderr,
    )


def main():
    args = parse_args()
    molecule_dir = get_collection_molecule_path(args.collection)
    scenario_dir = os.path.join(molecule_dir, args.scenario)

    if os.path.exists(scenario_dir):
        print(f"Scenario directory already exists: {scenario_dir}", file=sys.stderr)
        sys.exit(1)

    source_dir = DEFAULT_TEMPLATE_DIR
    if not os.path.exists(source_dir):
        print(
            f"Default template scenario directory not found: {source_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    os.makedirs(molecule_dir, exist_ok=True)
    ensure_collection_requirements_file(molecule_dir)

    print(f"Copying template from {source_dir} to {scenario_dir}")
    shutil.copytree(source_dir, scenario_dir)
    print(f"Molecule scenario '{args.scenario}' created at {scenario_dir}")


if __name__ == "__main__":
    main()
