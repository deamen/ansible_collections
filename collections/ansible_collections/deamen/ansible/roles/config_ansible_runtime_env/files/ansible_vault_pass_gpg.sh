#!/usr/bin/env bash
# Decrypt the GPG-encrypted Ansible Vault password file and write the password
# to stdout.  Set ANSIBLE_VAULT_PASSWORD_FILE to this script's path.
#
# Optional override: ANSIBLE_VAULT_GPG_FILE=/path/to/custom.gpg

set -euo pipefail

GPG_FILE="${ANSIBLE_VAULT_GPG_FILE:-${HOME}/.ansible_vault_pass.gpg}"

if [[ ! -r "$GPG_FILE" ]]; then
  printf 'ERROR: GPG-encrypted Vault password file not found or unreadable: %s\n' \
    "$GPG_FILE" >&2
  exit 1
fi

if ! gpg --quiet --batch --decrypt "$GPG_FILE" 2>/dev/null; then
  printf 'ERROR: Could not decrypt %s. Check the GPG key and gpg-agent.\n' \
    "$GPG_FILE" >&2
  exit 1
fi
