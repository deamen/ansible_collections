"""Shared utilities for Ansible collection and role management scripts."""

import os
import subprocess
import sys

DEFAULT_COLLECTION_PATH = "collections/ansible_collections/"


def get_git_config_value(key):
    """Return a git config value by key, or None if not found."""
    try:
        result = subprocess.run(
            ["git", "config", "--get", key],
            capture_output=True,
            text=True,
            check=True,
        )
        value = result.stdout.strip()
        return value if value else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_git_author(fallback="your name"):
    """Return the git-configured author string.

    When both name and email are available the return value is
    ``'Name <email>'``.  When only a name exists the name is returned on its
    own.  If neither is configured the function falls back to the
    ``GIT_AUTHOR_NAME``, ``USER``, or ``USERNAME`` environment variables,
    and finally to the *fallback* parameter.

    Args:
        fallback: String to return when no author can be determined.
    """
    name = get_git_config_value("user.name")
    email = get_git_config_value("user.email")

    if name and email:
        return f"{name} <{email}>"
    if name:
        return name

    return (
        os.environ.get("GIT_AUTHOR_NAME")
        or os.environ.get("USER")
        or os.environ.get("USERNAME")
        or fallback
    )


def parse_github_remote_url(url):
    """Parse a git remote URL and return a dict with owner, repo, and canonical https url.

    SSH and https GitHub remote URLs are supported.  The returned dict has keys: owner, repo, url.

    Returns None when the url does not look like a GitHub remote.
    """
    if not url:
        return None
    u = url.strip()
    if u.endswith(".git"):
        u = u[:-4]

    path = None
    if u.startswith("git@github.com:"):
        path = u[len("git@github.com:") :]
    else:
        for prefix in (
            "ssh://git@github.com/",
            "https://github.com/",
            "http://github.com/",
            "git://github.com/",
        ):
            if u.startswith(prefix):
                path = u[len(prefix) :]
                break
        if path is None:
            idx = u.find("github.com/")
            if idx != -1:
                path = u[idx + len("github.com/") :]

    if not path:
        return None
    parts = path.split("/")
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1]
    https_url = f"https://github.com/{owner}/{repo}"
    return {"owner": owner, "repo": repo, "url": https_url}


def get_git_remote_info(root_dir):
    """Return parsed git remote info for the repo at *root_dir*, or None.

    The returned dict contains: owner, repo, url, default_branch.
    """
    try:
        out = subprocess.check_output(
            ["git", "-C", root_dir, "remote", "-v"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return None

    remote_url = None
    # Prefer 'upstream' fetch remote, then 'origin', then any fetch remote.
    for name in ("upstream", "origin"):
        for line in out.splitlines():
            parts = line.split()
            if (
                len(parts) >= 3
                and parts[2].startswith("(")
                and "fetch" in parts[2]
                and parts[0] == name
            ):
                remote_url = parts[1]
                break
        if remote_url:
            break

    if not remote_url:
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 3 and "fetch" in parts[2]:
                remote_url = parts[1]
                break

    if not remote_url:
        return None

    parsed = parse_github_remote_url(remote_url)
    if not parsed:
        return None

    # Try to discover the default branch.
    default_branch = None
    try:
        out2 = subprocess.check_output(
            ["git", "-C", root_dir, "remote", "show", "origin"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        for line in out2.splitlines():
            if "HEAD branch:" in line:
                default_branch = line.split(":", 1)[1].strip()
                break
    except Exception:
        default_branch = None

    if not default_branch:
        for candidate in ("main", "master"):
            try:
                subprocess.check_output(
                    [
                        "git",
                        "-C",
                        root_dir,
                        "rev-parse",
                        "--verify",
                        f"origin/{candidate}",
                    ],
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
                default_branch = candidate
                break
            except Exception:
                continue

    if not default_branch:
        default_branch = "master"

    parsed["default_branch"] = default_branch
    return parsed


def run_ansible_galaxy(args, quiet=False):
    """Run the ansible-galaxy CLI with *args* and return the exit code (int).

    Catches ``SystemExit`` raised by the CLI and normalises ``None`` to ``0``.
    """
    from ansible.cli.galaxy import GalaxyCLI

    cli = GalaxyCLI(args=args)
    try:
        exit_code = cli.run()
    except SystemExit as e:
        exit_code = e.code

    if exit_code is None:
        exit_code = 0

    if not quiet:
        print(f"ansible-galaxy exited with code: {exit_code}")

    return exit_code
