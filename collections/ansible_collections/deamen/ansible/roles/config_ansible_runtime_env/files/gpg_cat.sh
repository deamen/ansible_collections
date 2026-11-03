#!/usr/bin/env bash
# Decrypt a GPG encrypted file and print its content to stdout,
# e.g. for use as an Ansible Vault password script.
#
# The file is taken from --gpg_file, falling back to the GPG_FILE environment variable.
set -euo pipefail

usage() {
  cat <<EOF
Usage: $(basename "$0") [--gpg_file <file>]

Decrypt <file> with gpg and print the result to stdout.

Options:
  --gpg_file <file>  GPG encrypted file to decrypt, overrides GPG_FILE
  -h, --help         Show this help

Environment:
  GPG_FILE           GPG encrypted file to decrypt when --gpg_file is not given
EOF
}

gpg_file="${GPG_FILE:-}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --gpg_file)
      if [[ $# -lt 2 || -z "$2" ]]; then
        echo "Error: --gpg_file requires a file argument" >&2
        exit 2
      fi
      gpg_file="$2"
      shift 2
      ;;
    --gpg_file=*)
      gpg_file="${1#--gpg_file=}"
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$gpg_file" ]]; then
  echo "Error: no GPG file given, set GPG_FILE or pass --gpg_file" >&2
  exit 2
fi

if [[ ! -r "$gpg_file" ]]; then
  echo "Error: GPG file not found or not readable: $gpg_file" >&2
  exit 1
fi

if ! gpg --quiet --batch --decrypt "$gpg_file" 2>/dev/null; then
  echo "Error: could not decrypt $gpg_file, check the GPG key and gpg-agent" >&2
  exit 1
fi
