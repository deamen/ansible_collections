#!/usr/bin/python
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
---
module: deploy_certificate
short_description: Deploy a certificate and key to specified locations
description:
  - This module deploys a single certificate and key to specified file paths.
version_added: "1.1.0"
options:
  name:
    description:
      - Name of the certificate file (e.g., 'example.crt').
      - The key file name is derived from this by replacing '.crt' with '.key'.
    type: str
    required: True
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
  cert_mode:
    description:
      - File permissions for the certificate file.
    type: str
    default: "0644"
  key_mode:
    description:
      - File permissions for the key file.
    type: str
    default: "0600"
  cert_owner:
    description:
      - User name or ID to set as the owner of the certificate file.
    type: str
    default: "root"
  cert_group:
    description:
      - Group name or ID to set as the group owner of the certificate file.
    type: str
    default: "root"
  key_owner:
    description:
      - User name or ID to set as the owner of the key file.
    type: str
    default: "root"
  key_group:
    description:
      - Group name or ID to set as the group owner of the key file.
    type: str
    default: "root"
  cert_content:
    description:
      - Content of the certificate to write to the certificate file.
    type: str
    required: True
  key_content:
    description:
      - Content of the key to write to the key file.
      - This is sensitive information and will not appear in logs.
    type: str
    required: True
  is_ca:
    description:
      - Whether the certificate is a Certificate Authority (CA) certificate.
    type: bool
    default: False
author:
  - Song Tang (@deamen)
"""

EXAMPLES = """
- name: Deploy a single certificate and key
  deploy_certificate:
    name: "example.crt"
    cert_content: |
      -----BEGIN CERTIFICATE-----
      ...
      -----END CERTIFICATE-----
    key_content: |
      -----BEGIN PRIVATE KEY-----
      ...
      -----END PRIVATE KEY-----
"""
