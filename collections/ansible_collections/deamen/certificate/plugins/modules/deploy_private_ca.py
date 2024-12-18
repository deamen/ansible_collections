#!/usr/bin/python

# Copyright: (c) 2024 Song Tang github.com/deamen
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: deploy_private_ca
short_description: Deploy a private CA certificate to a Linux server
description:
  - Writes the content of a private CA certificate to the system's trust store directory.
  - Updates the system trust store using the `update-ca-trust` command.
options:
  private_ca:
    description: The content of the private CA certificate in PEM format.
    required: true
    type: str
  filename:
    description: The filename for the CA certificate.
    default: custom-ca.crt
    type: str
author: Song Tang (@deamen)
"""

EXAMPLES = """
- name: Deploy a private CA certificate
  deploy_private_ca:
    private_ca: |
      -----BEGIN CERTIFICATE-----
      MIIDXTCCAkWgAwIBAgIJAL8AO9lD...
      -----END CERTIFICATE-----
    filename: my-custom-ca.crt
"""

def main():
    # Define module arguments
    module_args = {}

    # Initialize the Ansible module
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    # Command to update the system trust store
    update_command = "update-ca-trust"

    # Run the command and capture results
    rc, out, err = module.run_command(update_command)

    # Handle errors if the command fails
    if rc != 0:
        module.fail_json(msg=f"Failed to run '{update_command}'. Error: {err}")

    # Exit successfully if the command runs without issues
    module.exit_json(
        changed=True,
        msg="Private CA deployed successfully and trust store updated.",
    )

if __name__ == "__main__":
    main()
