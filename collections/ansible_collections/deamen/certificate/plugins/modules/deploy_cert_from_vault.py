# -*- coding: utf-8 -*-
# Copyright: (c) 2024 Song Tang <github.com/deamen>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
---
module: deploy_cert_from_vault
short_description: Generate and deploy a certificate using HashiCorp Vault
description:
  - Generates a certificate using the HashiCorp Vault PKI backend and deploys it to specified locations.
  - Calls the C(gen_cert_from_vault) action plugin to generate the certificate.
  - Calls the C(deploy_certificate) action plugin to deploy the certificate.
version_added: "1.4.0"
options:
  common_name:
    description:
      - The common name (CN) for the certificate.
    required: true
    type: str
  engine_mount_point:
    description:
      - The mount point of the PKI secrets engine in Vault.
    required: true
    type: str
  role_name:
    description:
      - The role name in the PKI backend that defines permissions and policies.
    required: true
    type: str
  token:
    description:
      - The Vault token to authenticate with the PKI backend.
    required: true
    type: str
  alt_names:
    description:
      - A comma-separated list of Subject Alternative Names (SANs) for the certificate.
    required: false
    type: str
  ip_sans:
    description:
      - A comma-separated list of IP SANs for the certificate.
    required: false
    type: str
  ttl:
    description:
      - The time-to-live (TTL) duration for the certificate. Overrides role-defined TTL if specified.
    required: false
    type: str
  vault_addr:
    description:
      - The Vault server's address. Passed as the URL to the Vault API.
    required: false
    type: str
  on_target:
    description:
      - Whether to run the task on the target host.
    required: false
    type: bool
    default: false
  name:
    description:
      - Name of the certificate file (e.g., 'example.crt').
      - The key file name is derived from this by replacing '.crt' with '.key'.
    type: str
    required: false
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
  is_ca:
    description:
      - Whether the certificate is a Certificate Authority (CA) certificate.
    type: bool
    default: False
author:
  - Song Tang (@deamen)
"""

EXAMPLES = """
- name: Generate and deploy a certificate with specific SANs
  deploy_cert_from_vault:
    common_name: example.com
    engine_mount_point: pki
    role_name: example-role
    token: "{{ vault_token }}"
    vault_addr: "https://vault.example.com"
    alt_names: "*.example.com"
    ip_sans: "192.168.1.1,192.168.1.2"
    ttl: "24h"
    cert_dir: "/etc/ssl/certs"
    key_dir: "/etc/ssl/private"
    cert_mode: "0644"
    key_mode: "0600"
    cert_owner: "root"
    cert_group: "root"
    key_owner: "root"
    key_group: "root"

- name: Generate and deploy a certificate with minimal options
  deploy_cert_from_vault:
    common_name: example.com
    engine_mount_point: pki
    role_name: example-role
    token: "{{ vault_token }}"
    cert_dir: "/etc/ssl/certs"
    key_dir: "/etc/ssl/private"
"""
