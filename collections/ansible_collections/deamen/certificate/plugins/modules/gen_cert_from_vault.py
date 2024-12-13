# -*- coding: utf-8 -*-
# Copyright: (c) 2024 Song Tang <github.com/deamen>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
---
module: gen_cert_from_vault
short_description: Generate a certificate using HashiCorp Vault PKI backend
description:
  - Generates a certificate using the HashiCorp Vault PKI backend.
  - Wraps the C(community.hashi_vault.vault_pki_generate_certificate) module for easier usage.
  - Delegates the task to localhost by default and sets authentication mode to C(token).
version_added: "1.3.0"
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
author:
  - Song Tang (@deamen)
notes:
  - Ensure that the Vault server and PKI engine are configured correctly.
  - Delegation is set to C(localhost) by default.
seealso:
  - module: community.hashi_vault.vault_pki_generate_certificate
"""

EXAMPLES = """
- name: Generate a certificate with specific SANs
  gen_cert_from_vault:
    common_name: example.com
    engine_mount_point: pki
    role_name: example-role
    token: "{{ vault_token }}"
    vault_addr: "https://vault.example.com"
    alt_names: "*.example.com"
    ip_sans: "192.168.1.1,192.168.1.2"
    ttl: "24h"

- name: Generate a certificate with minimal options
  gen_cert_from_vault:
    common_name: example.com
    engine_mount_point: pki
    role_name: example-role
    token: "{{ vault_token }}"
"""
