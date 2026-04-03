#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: check_is_container
short_description: Check if running inside a container (Docker, Podman, etc.)
description:
  - Checks for well-known container marker files to determine if the host is running inside a container.
  - This is more reliable than ansible_virtualization_type for some container engines (e.g., buildah).
version_added: "1.0.0"
author:
  - deamen(@deamen)
notes:
  - Looks for /.dockerenv and /run/.containerenv marker files.
"""

EXAMPLES = r"""
- name: Check if running in a container
  deamen.general.check_is_container:
  register: container_check
"""

RETURN = r"""
is_container:
  description: Whether the host is running inside a container.
  returned: always
  type: bool
  sample: true
marker_found:
  description: List of marker files found.
  returned: always
  type: list
  elements: str
  sample: ["/.dockerenv"]
"""

from ansible.module_utils.basic import AnsibleModule
import os

CONTAINER_MARKERS = [
    "/.dockerenv",
    "/run/.containerenv",
]


def run_module():
    module_args = dict()
    result = dict(
        changed=False,
        is_container=False,
        marker_found=[],
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    found = []
    for marker in CONTAINER_MARKERS:
        if os.path.exists(marker):
            found.append(marker)
    result["marker_found"] = found
    result["is_container"] = bool(found)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
