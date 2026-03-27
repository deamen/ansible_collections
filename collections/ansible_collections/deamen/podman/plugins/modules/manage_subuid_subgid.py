#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: manage_subuid_subgid
short_description: Manage subordinate UID and GID ranges for users
description:
  - This module manages subordinate UID and GID ranges for users to enable rootless containers.
  - It automatically calculates the next available range and adds it to /etc/subuid and /etc/subgid.
  - The module is idempotent and will not modify existing entries for a user.
  - Supports check mode to preview changes without applying them.
version_added: "1.0.0"
options:
  username:
    description:
      - The username for which to add subordinate UID and GID ranges.
    type: str
    required: true
  range_size:
    description:
      - The number of subordinate IDs to allocate for the user.
    type: int
    default: 65536
author:
  - Song Tang (@deamen)
"""

EXAMPLES = """
- name: Add subuid and subgid ranges for user podman
  deamen.podman.manage_subuid_subgid:
    username: podman

- name: Add subuid and subgid ranges with custom range size
  deamen.podman.manage_subuid_subgid:
    username: containeruser
    range_size: 100000
"""

RETURN = """
changed:
  description: Whether the module made any changes
  returned: always
  type: bool
  sample: true
msg:
  description: A message describing what happened
  returned: always
  type: str
  sample: "Subuids and subgids added for user podman: 100000-165535, 100000-165535"
subuid_range:
  description: The subordinate UID range that was added or already exists
  returned: always
  type: dict
  sample: {"start": 100000, "end": 165535}
subgid_range:
  description: The subordinate GID range that was added or already exists
  returned: always
  type: dict
  sample: {"start": 100000, "end": 165535}
"""

from ansible.module_utils.basic import AnsibleModule
import os

# Use system defaults for subuid and subgid files
SUBUID_FILE = "/etc/subuid"
SUBGID_FILE = "/etc/subgid"


def get_next_range(filepath, range_size):
    """
    Calculate the next available range from a subuid or subgid file.

    Args:
        filepath: Path to the subuid or subgid file
        range_size: Size of the range to allocate

    Returns:
        tuple: (start, end) of the next available range
    """
    max_end = 0

    if not os.path.exists(filepath):
        # If file doesn't exist, start from a safe default
        return (100000, 100000 + range_size - 1)

    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(":")
                if len(parts) != 3:
                    continue

                try:
                    start = int(parts[1])
                    count = int(parts[2])
                    end = start + count - 1
                    if end > max_end:
                        max_end = end
                except (ValueError, IndexError):
                    continue
    except IOError as e:
        # If we can't read the file, fail the module
        raise RuntimeError(f"Failed to read {filepath}: {str(e)}")

    next_start = max_end if max_end == 0 else max_end + 1
    # Ensure we start from at least 100000 for subordinate IDs
    if next_start < 100000:
        next_start = 100000

    return (next_start, next_start + range_size - 1)


def user_has_entry(filepath, username):
    """
    Check if a user already has an entry in the subuid or subgid file.

    Args:
        filepath: Path to the subuid or subgid file
        username: Username to check for

    Returns:
        tuple: (bool, dict) - (has_entry, range_info) where range_info is {"start": int, "end": int} or None
    """
    if not os.path.exists(filepath):
        return (False, None)

    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(username + ":"):
                    parts = line.split(":")
                    if len(parts) == 3:
                        try:
                            start = int(parts[1])
                            count = int(parts[2])
                            end = start + count - 1
                            return (True, {"start": start, "end": end})
                        except (ValueError, IndexError):
                            continue
    except IOError as e:
        raise RuntimeError(f"Failed to read {filepath}: {str(e)}")

    return (False, None)


def add_subuid_subgid_ranges(module, username, range_size):
    """
    Add subordinate UID and GID ranges for a user using usermod command.

    Args:
        module: AnsibleModule instance
        username: Username to add ranges for
        range_size: Size of ranges to allocate

    Returns:
        dict: Result dictionary with changed status and message
    """
    # Check if user already has entries
    has_subuid, subuid_info = user_has_entry(SUBUID_FILE, username)
    has_subgid, subgid_info = user_has_entry(SUBGID_FILE, username)

    if has_subuid and has_subgid:
        return {
            "changed": False,
            "msg": f"User {username} already has subordinate UID and GID ranges configured",
            "subuid_range": subuid_info,
            "subgid_range": subgid_info,
        }

    # Calculate next available ranges
    subuid_start, subuid_end = get_next_range(SUBUID_FILE, range_size)
    subgid_start, subgid_end = get_next_range(SUBGID_FILE, range_size)

    changed = False

    # Add subuid range if not present
    if not has_subuid:
        if module.check_mode:
            # In check mode, just report what would be done
            changed = True
        else:
            cmd = ["usermod", f"--add-subuids={subuid_start}-{subuid_end}", username]
            rc, stdout, stderr = module.run_command(cmd, check_rc=False)
            if rc != 0:
                module.fail_json(
                    msg=f"Failed to add subordinate UIDs for user {username}",
                    rc=rc,
                    stdout=stdout,
                    stderr=stderr,
                    cmd=" ".join(cmd),
                )
            changed = True
    else:
        subuid_start = subuid_info["start"]
        subuid_end = subuid_info["end"]

    # Add subgid range if not present
    if not has_subgid:
        if module.check_mode:
            # In check mode, just report what would be done
            changed = True
        else:
            cmd = ["usermod", f"--add-subgids={subgid_start}-{subgid_end}", username]
            rc, stdout, stderr = module.run_command(cmd, check_rc=False)
            if rc != 0:
                module.fail_json(
                    msg=f"Failed to add subordinate GIDs for user {username}",
                    rc=rc,
                    stdout=stdout,
                    stderr=stderr,
                    cmd=" ".join(cmd),
                )
            changed = True
    else:
        subgid_start = subgid_info["start"]
        subgid_end = subgid_info["end"]

    result = {
        "changed": changed,
        "subuid_range": {"start": subuid_start, "end": subuid_end},
        "subgid_range": {"start": subgid_start, "end": subgid_end},
    }

    if changed:
        if module.check_mode:
            result["msg"] = (
                f"Would add subordinate UID and GID ranges for user {username}: "
                f"{subuid_start}-{subuid_end}, {subgid_start}-{subgid_end}"
            )
        else:
            result["msg"] = (
                f"Subordinate UID and GID ranges added for user {username}: "
                f"{subuid_start}-{subuid_end}, {subgid_start}-{subgid_end}"
            )
    else:
        result["msg"] = (
            f"User {username} already has subordinate UID and GID ranges configured"
        )

    return result


def main():
    """Main module execution."""
    module_args = {
        "username": {"type": "str", "required": True},
        "range_size": {"type": "int", "default": 65536},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    username = module.params["username"]
    range_size = module.params["range_size"]

    # Validate range size
    if range_size <= 0:
        module.fail_json(msg="range_size must be a positive integer")

    # Execute the main logic
    result = add_subuid_subgid_ranges(module, username, range_size)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
