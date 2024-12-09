#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
---
module: deploy_certificate
short_description: Deploy certificates and keys to specified locations
description:
  - This module deploys certificates and keys to specified file paths.
  - It allows setting file permissions, ownership, and managing sensitive content like private keys.
version_added: "1.1.0"
options:
  certificates:
    description:
      - A list of certificate and key definitions to be deployed.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Name of the certificate file (full path).
          - Used to derive the key file path with a .key extension.
        type: str
        required: True
      owner:
        description:
          - User name or ID to set as the owner of the certificate and key files.
        type: str
        default: null
      group:
        description:
          - Group name or ID to set as the group owner of the certificate and key files.
        type: str
        default: null
      cert_dir:
        description:
          - Directory to store the certificate file.
        type: str
        default: "/etc/pki/tls/certs/"
      key_dir:
        description:
          - Directory to store the key file.
        type: str
        default: "/etc/pki/tls/private/"
      certfile_mode:
        description:
          - File permissions for the certificate file.
        type: str
        default: "0644"
      keyfile_mode:
        description:
          - File permissions for the key file.
        type: str
        default: "0600"
      cert_content:
        description:
          - Content of the certificate to write to the certificate file.
        type: str
        default: null
      key_content:
        description:
          - Content of the key to write to the key file.
          - This is sensitive information and will not appear in logs.
        type: str
        default: null
author:
  - Your Name (@your_github_handle)
"""

EXAMPLES = """
- name: Deploy certificates and keys
  deploy_certificate:
    certificates:
      - name: "/etc/ssl/certs/example.crt"
        owner: "root"
        group: "root"
        certfile_mode: "0644"
        keyfile_mode: "0600"
        cert_content: |
          -----BEGIN CERTIFICATE-----
          ...
          -----END CERTIFICATE-----
        key_content: |
          -----BEGIN PRIVATE KEY-----
          ...
          -----END PRIVATE KEY-----
      - name: "/etc/ssl/certs/another_example.crt"
        owner: "nginx"
        group: "nginx"
        certfile_mode: "0644"
        keyfile_mode: "0600"
        cert_content: |
          -----BEGIN CERTIFICATE-----
          ...
          -----END CERTIFICATE-----
        key_content: |
          -----BEGIN PRIVATE KEY-----
          ...
          -----END PRIVATE KEY-----
"""

from ansible.module_utils.basic import AnsibleModule
import os


def is_valid_crt_filename(filename):
    # Check if it contains no path components and ends with '.crt'
    return os.path.basename(filename) == filename and filename.endswith(".crt")


def deploy_certificate(module, params):
    """
    Deploys certificates and keys based on provided parameters.
    """
    results = []
    certificates = params.get("certificates", [])

    for cert in certificates:
        cert_name = cert["name"]

        if not is_valid_crt_filename(cert_name):
            module.fail_json(
                msg=f"The name field is not a valid crt filename(example.crt): {cert_name}"
            )

        cert_default_dir = "/etc/pki/tls/certs/"
        cert_dir = cert.get("cert_dir", cert_default_dir)
        cert_path = os.path.join(cert_dir, cert_name)

        key_default_dir = "/etc/pki/tls/private/"
        key_dir = cert.get("key_dir", key_default_dir)
        key_path = os.path.join(key_dir, cert_name.replace(".crt", ".key"))

        # Set defaults for ownership and permissions
        owner = cert.get("owner", None)
        group = cert.get("group", None)
        certfile_mode = cert.get("certfile_mode", "0644")
        keyfile_mode = cert.get("keyfile_mode", "0600")

        # Prepare results for check mode
        changes = {"cert_file": False, "key_file": False}

        # Check certificate file
        if cert.get("cert_content"):
            if not os.path.exists(cert_path) or open(cert_path).read() != cert["cert_content"]:
                changes["cert_file"] = True

        # Check key file
        if cert.get("key_content"):
            if not os.path.exists(key_path) or open(key_path).read() != cert["key_content"]:
                changes["key_file"] = True

        if module.check_mode:
            results.append({"cert_path": cert_path, "key_path": key_path, "changes": changes})
            continue

        # Deploy certificate file
        if cert.get("cert_content"):
            try:
                with open(cert_path, "w") as cert_file:
                    cert_file.write(cert["cert_content"])
                os.chmod(cert_path, int(certfile_mode, 8))
                if owner or group:
                    uid = int(owner) if owner and owner.isdigit() else -1
                    gid = int(group) if group and group.isdigit() else -1
                    os.chown(cert_path, uid, gid)
                results.append({"cert_path": cert_path, "changed": True})
            except Exception as e:
                module.fail_json(msg=f"Failed to deploy certificate: {cert_path}. Error: {e}")

        # Deploy key file
        if cert.get("key_content"):
            try:
                with open(key_path, "w") as key_file:
                    key_file.write(cert["key_content"])
                os.chmod(key_path, int(keyfile_mode, 8))
                if owner or group:
                    uid = int(owner) if owner and owner.isdigit() else -1
                    gid = int(group) if group and group.isdigit() else -1
                    os.chown(key_path, uid, gid)
                results.append({"key_path": key_path, "changed": True})
            except Exception as e:
                module.fail_json(msg=f"Failed to deploy key: {key_path}. Error: {e}")

    return results


def main():
    module_args = {
        "certificates": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "owner": {"type": "str", "default": None},
                "group": {"type": "str", "default": None},
                "cert_dir": {"type": "str", "default": "/etc/pki/tls/certs/"},
                "key_dir": {"type": "str", "default": "/etc/pki/tls/private/", "no_log": False},
                "certfile_mode": {"type": "str", "default": "0644"},
                "keyfile_mode": {"type": "str", "default": "0600", "no_log": False},
                "cert_content": {"type": "str", "default": None},
                "key_content": {"type": "str", "default": None, "no_log": True},
            },
        },
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    try:
        results = deploy_certificate(module, module.params)
        module.exit_json(
            changed=any(result.get("changed", False) for result in results), results=results
        )
    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
