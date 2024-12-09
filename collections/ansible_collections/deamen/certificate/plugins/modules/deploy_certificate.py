#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
---
module: deploy_certificate
short_description: Deploy a certificate and key to specified locations
description:
  - This module deploys a single certificate and key to specified file paths.
  - It allows setting file permissions, ownership, and managing sensitive content like private keys.
version_added: "1.1.0"
options:
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
- name: Deploy a single certificate and key
  deploy_certificate:
    name: "example.crt"
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

- name: Deploy multiple certificates using a loop
  loop:
    - { name: "example1.crt", cert_content: "...", key_content: "...", owner: "root" }
    - { name: "example2.crt", cert_content: "...", key_content: "...", owner: "nginx" }
  ansible.builtin.include_tasks:
    file: deploy_certificate.yaml
"""

from ansible.module_utils.basic import AnsibleModule
import os


def is_valid_crt_filename(filename):
    return os.path.basename(filename) == filename and filename.endswith(".crt")


def deploy_certificate(module, params):
    """
    Deploys a single certificate and key based on provided parameters.
    """
    cert_name = params["name"]

    if not is_valid_crt_filename(cert_name):
        module.fail_json(msg=f"The name field is not a valid crt filename (example.crt): {cert_name}")

    cert_dir = params.get("cert_dir", "/etc/pki/tls/certs/")
    cert_path = os.path.join(cert_dir, cert_name)

    key_dir = params.get("key_dir", "/etc/pki/tls/private/")
    key_path = os.path.join(key_dir, cert_name.replace(".crt", ".key"))

    owner = params.get("owner", None)
    group = params.get("group", None)
    certfile_mode = params.get("certfile_mode", "0644")
    keyfile_mode = params.get("keyfile_mode", "0600")

    # Prepare results for check mode
    changes = {"cert_file": False, "key_file": False}

    if params.get("cert_content"):
        if not os.path.exists(cert_path) or open(cert_path).read() != params["cert_content"]:
            changes["cert_file"] = True

    if params.get("key_content"):
        if not os.path.exists(key_path) or open(key_path).read() != params["key_content"]:
            changes["key_file"] = True

    if module.check_mode:
        return {"cert_path": cert_path, "key_path": key_path, "changes": changes}

    try:
        if params.get("cert_content"):
            with open(cert_path, "w") as cert_file:
                cert_file.write(params["cert_content"])
            os.chmod(cert_path, int(certfile_mode, 8))
            if owner or group:
                uid = int(owner) if owner and owner.isdigit() else -1
                gid = int(group) if group and group.isdigit() else -1
                os.chown(cert_path, uid, gid)

        if params.get("key_content"):
            with open(key_path, "w") as key_file:
                key_file.write(params["key_content"])
            os.chmod(key_path, int(keyfile_mode, 8))
            if owner or group:
                uid = int(owner) if owner and owner.isdigit() else -1
                gid = int(group) if group and group.isdigit() else -1
                os.chown(key_path, uid, gid)

        return {"cert_path": cert_path, "key_path": key_path, "changed": True}
    except Exception as e:
        module.fail_json(msg=f"Failed to deploy certificate or key. Error: {e}")


def main():
    module_args = {
        "name": {"type": "str", "required": True},
        "owner": {"type": "str", "default": None},
        "group": {"type": "str", "default": None},
        "cert_dir": {"type": "str", "default": "/etc/pki/tls/certs/"},
        "key_dir": {"type": "str", "default": "/etc/pki/tls/private/", "no_log": False},
        "certfile_mode": {"type": "str", "default": "0644"},
        "keyfile_mode": {"type": "str", "default": "0600", "no_log": False},
        "cert_content": {"type": "str", "default": None},
        "key_content": {"type": "str", "default": None, "no_log": True},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    try:
        result = deploy_certificate(module, module.params)
        module.exit_json(**result)
    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
