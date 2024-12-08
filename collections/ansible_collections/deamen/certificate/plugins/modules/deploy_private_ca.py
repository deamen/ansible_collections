#!/usr/bin/python

# Copyright: (c) 2024 Song Tang github.com/deamen
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
---
module: deploy_private_ca
short_description: Deploy a private CA certificate to a Linux server
description:
  - Writes the content of a private CA certificate to the system's trust store directory.
  - Updates the system trust store using the `update-ca-trust` command.
  - "Ensures the task runs only on supported Linux distributions: AlmaLinux, CentOS, RedHat, Rocky, or Fedora."
version_added: "1.0.0"
options:
  private_ca:
    description:
      - The content of the private CA certificate in PEM format.
    required: true
    type: str
  filename:
    description:
      - The name of the file to save the private CA certificate as.
      - Defaults to 'custom-ca.crt'.
    required: false
    type: str
    default: 'custom-ca.crt'
author:
  - Your Name (@your_github_handle)
"""

EXAMPLES = """
- name: Deploy a private CA certificate with default filename
  deploy_private_ca:
    private_ca: |
      -----BEGIN CERTIFICATE-----
      MIIDXTCCAkWgAwIBAgIJAL8AO9lD...
      -----END CERTIFICATE-----

- name: Deploy a private CA certificate with a custom filename
  deploy_private_ca:
    private_ca: |
      -----BEGIN CERTIFICATE-----
      MIIDXTCCAkWgAwIBAgIJAL8AO9lD...
      -----END CERTIFICATE-----
    filename: my-custom-ca.crt
"""

from ansible.module_utils.basic import AnsibleModule
import os
import platform
import subprocess


def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return (
            result.returncode,
            result.stdout.decode("utf-8").strip(),
            result.stderr.decode("utf-8").strip(),
        )
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout.decode("utf-8").strip(), e.stderr.decode("utf-8").strip()


def main():
    module_args = {
        "private_ca": {"type": "str", "required": True},
        "filename": {"type": "str", "default": "custom-ca.crt"},
    }

    # Initialize the Ansible module
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    private_ca = module.params["private_ca"]
    filename = module.params["filename"]
    ca_trust_path = "/etc/pki/ca-trust/source/anchors/"
    update_command = "update-ca-trust"
    dest_file = os.path.join(ca_trust_path, filename)

    # Check if the OS is supported
    supported_distros = ["AlmaLinux", "CentOS", "RedHat", "Rocky", "Fedora"]
    distro = platform.linux_distribution(full_distribution_name=False)[0]

    if distro not in supported_distros:
        module.fail_json(
            msg=f"Unsupported distribution: {distro}. This module supports: {', '.join(supported_distros)}."
        )

    try:
        # Ensure the CA trust directory exists
        os.makedirs(ca_trust_path, exist_ok=True)

        # Write the certificate content to the destination file
        with open(dest_file, "w") as f:
            f.write(private_ca)

        # Run update-ca-trust
        returncode, stdout, stderr = run_command(update_command)
        if returncode != 0:
            module.fail_json(msg=f"Failed to run '{update_command}'. Error: {stderr}")

        # Return success
        module.exit_json(
            changed=True,
            msg=f"Private CA deployed successfully to {dest_file} and trust store updated.",
        )

    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
