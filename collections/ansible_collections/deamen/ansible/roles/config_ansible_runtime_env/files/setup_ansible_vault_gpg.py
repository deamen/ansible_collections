#!/usr/bin/env python
"""One-time setup: secure Ansible Vault password with GPG encryption.

Import the GPG secret key from ~/.gnupg/private_gpg.key (default):
    setup_ansible_vault_gpg.py

Import a GPG secret key from another file:
    setup_ansible_vault_gpg.py --gpg-file /path/to/key.asc

Generate a new GPG key instead:
    setup_ansible_vault_gpg.py --key-name "Song Tang" --key-email stang@mmz.au

After setup, point Ansible at the retrieval script:
    export ANSIBLE_VAULT_PASSWORD_FILE=/usr/local/bin/ansible_vault_pass_gpg.sh
"""

from __future__ import annotations

import argparse
import contextlib
import getpass
import json
import os
import secrets
import shutil
import string
import subprocess
import sys
import tempfile
from pathlib import Path

GNUPG_HOME = Path.home() / ".gnupg"

_DEFAULT_VAULT_FILE = Path.home() / ".ansible_vault.yml"
_DEFAULT_GPG_ENCRYPTED = Path.home() / ".ansible_vault_pass.gpg"
# Same as config_gpg_secret_key_path in deamen.gpg.config_gpg
_DEFAULT_GPG_SECRET_KEY = GNUPG_HOME / "private_gpg.key"


# ---------------------------------------------------------------------------
# Low-level utilities
# ---------------------------------------------------------------------------


def check_prerequisites() -> None:
    for cmd in ("gpg", "gpgconf", "ansible-playbook"):
        if not shutil.which(cmd):
            sys.exit(f"ERROR: {cmd} is required but not found. Install it and re-run.")


def shred_file(path: Path) -> None:
    if not path.exists():
        return
    if shutil.which("shred"):
        subprocess.run(["shred", "--remove", "--force", str(path)], check=False)
    else:
        path.unlink(missing_ok=True)


# This decorator (@contextlib.contextmanager) makes the function usable
# inside a 'with' block, without needing to write a class.
#
# Think of it as splitting the function in two halves around 'yield':
#   - Before yield: setup (creating the file, locking permissions)
#   - After yield: cleanup (shredding the file)
#
# The 'with' block runs setup, gives you the yielded value, then runs
# cleanup when the block ends — even if something goes wrong.
@contextlib.contextmanager
def sensitive_temp_file():
    """Yield a Path to a temporary file, then shred it on exit."""
    fd, name = tempfile.mkstemp()
    os.close(fd)
    path = Path(name)
    path.chmod(0o600)
    try:
        yield path
    finally:
        shred_file(path)


# ---------------------------------------------------------------------------
# Ansible
# ---------------------------------------------------------------------------


def run_playbook(playbook: str, extra_vars: dict[str, str]) -> None:
    """Run a collection playbook by FQCN without any vault password file."""
    env = {**os.environ}
    # Unset ANSIBLE_VAULT_PASSWORD_FILE to avoid accidental use of an existing vault password file
    # This could happen when we are generating a new GPG key and the user has already set ANSIBLE_VAULT_PASSWORD_FILE in their environment.
    env.pop("ANSIBLE_VAULT_PASSWORD_FILE", None)
    subprocess.run(
        [
            "ansible-playbook",
            "--inventory",
            "localhost,",
            # JSON is required; bare YAML multi-line strings are not reliably detected by ansible-playbook
            # Only @file yaml is supported for extra-vars, but we want to avoid creating a temporary file
            "--extra-vars",
            json.dumps(extra_vars),
            playbook,
        ],
        env=env,
        check=True,
    )


# ---------------------------------------------------------------------------
# GPG key generation
# ---------------------------------------------------------------------------


def get_fingerprint(email_or_id: str, env: dict[str, str]) -> str:
    """Return the primary key fingerprint for the given email or key ID."""
    result = subprocess.run(
        ["gpg", "--with-colons", "--list-keys", email_or_id],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    for line in result.stdout.splitlines():
        if line.startswith("fpr:"):
            return line.split(":")[9].upper()
    raise RuntimeError(f"No GPG key found for {email_or_id!r}")


def generate_key(key_name: str, key_email: str, config_gpg_user: str) -> str:
    """Run the generate_gpg_key playbook (which prompts for passphrase); return fingerprint."""
    run_playbook(
        "deamen.gpg.generate_gpg_key",
        {
            "config_gpg_user": config_gpg_user,
            "gpg_key_real_name": key_name,
            "gpg_key_email": key_email,
        },
    )
    return get_fingerprint(key_email, dict(os.environ))


# ---------------------------------------------------------------------------
# GPG key import
# This part is still working in progress;
# it is not yet fully tested or documented.
# ---------------------------------------------------------------------------


def get_fingerprint_from_file(gpg_key_file: Path) -> str:
    """Extract the primary fingerprint from a key file without importing it."""
    result = subprocess.run(
        [
            "gpg",
            "--batch",
            "--with-colons",
            "--import-options",
            "show-only",
            "--import",
            str(gpg_key_file),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    for line in result.stdout.splitlines():
        if line.startswith("fpr:"):
            return line.split(":")[9].upper()
    raise RuntimeError(f"Could not extract fingerprint from {gpg_key_file}")


def import_key(gpg_key_file: Path, config_gpg_user: str) -> str:
    """Stage the key file and run the config_gpg playbook; return the fingerprint.

    The default key file is handed to config_gpg as is, which removes it after
    a successful import. Any other file is staged as a copy so it is left alone.
    """
    fingerprint = get_fingerprint_from_file(gpg_key_file)
    if gpg_key_file == _DEFAULT_GPG_SECRET_KEY:
        staged = gpg_key_file
    else:
        GNUPG_HOME.mkdir(mode=0o700, exist_ok=True)
        fd, staged_name = tempfile.mkstemp(
            dir=GNUPG_HOME, prefix="private_gpg_", suffix=".key"
        )
        os.close(fd)
        staged = Path(staged_name)
        staged.chmod(0o600)
        shutil.copyfile(str(gpg_key_file), str(staged))
    try:
        run_playbook(
            "deamen.gpg.config_gpg",
            {
                "config_gpg_import_secret_key": "true",
                "config_gpg_user": config_gpg_user,
                "config_gpg_fingerprint": fingerprint,
                "config_gpg_secret_key_path": str(staged),
            },
        )
    finally:
        # The config_gpg handler normally removes it; shred anything left behind,
        # but never the default key file, which may still be needed after a failure
        if staged != gpg_key_file:
            shred_file(staged)
    return fingerprint


# ---------------------------------------------------------------------------
# Vault password
# ---------------------------------------------------------------------------


def generate_password() -> str:
    """Generate a cryptographically random 20-character vault password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Guarantee at least one from each character class.
    required = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]
    filler = [secrets.choice(alphabet) for _ in range(16)]
    password = required + filler
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def encrypt_vault_password(fingerprint: str, output_file: Path) -> None:
    """Generate a random vault password and GPG-encrypt it to the given key."""
    with sensitive_temp_file() as plain_file:
        plain_file.write_text(generate_password())
        subprocess.run(
            [
                "gpg",
                "--encrypt",
                "--recipient",
                fingerprint,
                "--trust-model",
                "always",
                "--output",
                str(output_file),
                str(plain_file),
            ],
            check=True,
        )
    output_file.chmod(0o600)
    print(f"GPG-encrypted Vault password written to: {output_file}")


# ---------------------------------------------------------------------------
# Retrieval script installation
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="One-time setup: secure Ansible Vault password with GPG encryption.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "After setup:\n"
            "  export ANSIBLE_VAULT_PASSWORD_FILE=/usr/local/bin/ansible_vault_pass_gpg.sh"
        ),
    )
    parser.add_argument(
        "--gpg-file",
        metavar="FILE",
        help=f"GPG secret key to import  [{_DEFAULT_GPG_SECRET_KEY}]",
    )
    parser.add_argument(
        "--key-name",
        metavar="NAME",
        help="Name for a new GPG key; generate a key instead of importing one",
    )
    parser.add_argument(
        "--key-email",
        metavar="EMAIL",
        help="Email for a new GPG key; generate a key instead of importing one",
    )
    parser.add_argument(
        "--config-gpg-user",
        metavar="USER",
        default=os.environ.get("USER") or getpass.getuser(),
        help="OS user for whom GPG is configured [default: USER environment variable or current user]",
    )
    parser.add_argument(
        "--vault-file",
        metavar="PATH",
        default=str(_DEFAULT_VAULT_FILE),
        help=f"Ansible Vault secrets file  [{_DEFAULT_VAULT_FILE}]",
    )
    parser.add_argument(
        "--gpg-encrypted-file",
        metavar="PATH",
        default=str(_DEFAULT_GPG_ENCRYPTED),
        help=f"GPG-encrypted vault password file  [{_DEFAULT_GPG_ENCRYPTED}]",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing GPG-encrypted vault password file",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not args.config_gpg_user:
        sys.exit("ERROR: --config-gpg-user is required when USER is not set.")
    # A new vault password would lock out anything encrypted with the old one
    if Path(args.gpg_encrypted_file).exists() and not args.force:
        sys.exit(
            f"ERROR: {args.gpg_encrypted_file} already exists. "
            "Use --force to replace it with a new vault password."
        )
    if args.key_name or args.key_email:
        if args.gpg_file:
            sys.exit(
                "ERROR: --gpg-file cannot be combined with --key-name/--key-email."
            )
        if not args.key_name:
            sys.exit("ERROR: --key-name is required when generating a new GPG key.")
        if not args.key_email:
            sys.exit("ERROR: --key-email is required when generating a new GPG key.")
    else:
        args.gpg_file = args.gpg_file or str(_DEFAULT_GPG_SECRET_KEY)
        if not Path(args.gpg_file).is_file():
            sys.exit(
                f"ERROR: GPG key file not readable: {args.gpg_file}\n"
                "Pass --gpg-file, or --key-name and --key-email to generate a new key."
            )


def print_instructions(vault_file: str) -> None:
    print(f"""
Setup complete.

Next steps:

1. Activate the vault password helper.

   Either open a new terminal, or run this command in the current terminal:

       source ~/.bashrc.d/aliases.sh

2. Encrypt your vault file by running:

       ansible-vault encrypt {vault_file}
""")


def main() -> None:
    args = parse_args()
    validate_args(args)
    check_prerequisites()

    try:
        if args.gpg_file:
            fingerprint = import_key(Path(args.gpg_file), args.config_gpg_user)
        else:
            fingerprint = generate_key(
                args.key_name, args.key_email, args.config_gpg_user
            )
        print(f"\nGPG key fingerprint: {fingerprint}")
        encrypt_vault_password(fingerprint, Path(args.gpg_encrypted_file))
    except KeyboardInterrupt:
        sys.exit("\nAborted.")
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        sys.exit(f"ERROR: {exc}")

    print_instructions(args.vault_file)


if __name__ == "__main__":
    main()
