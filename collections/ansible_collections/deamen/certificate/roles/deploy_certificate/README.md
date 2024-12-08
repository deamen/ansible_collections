Certificate Role
=========

Role for managing TLS/SSL certificate issuance and renewal

Requirements
------------

Nothing yet

Role Variables
--------------

## Variables

| Parameter         | Description                                          |  Type  | Required | Default                |
| ----------------- | ---------------------------------------------------- | :----: | :------: | ---------------------- |
| cert_dir          | The directory where the certificates will be stored. | string |    no    | /etc/pki/tls/certs     |
| key_dir           | The directory where the certificates will be stored. | string |    no    | /etc/pki/tls/private   |
| cert_file         | The filename of the certificate.                     | string |    no    | {{ ansible_fqdn }}.crt |
| key_file          | The filename of the private key.                     | string |    no    | {{ ansible_fqdn }}.key |
| cert_file_content | The content of the certificate                       | string |   yes    | -                      |
| key_file_content  | The content of the private key                       | string |   yes    | -                      |

Dependencies
------------
Nothing yet

Example Playbook
----------------

```yaml
---
- hosts: webserver

  tasks:
    - name: Deploy Let's encrypt certificate
      ansible.builtin.import_role:
        name: deamen.certificate.deploy_certificate
      vars:
        cert_file_content: "{{ letsencrypt_certificate }}"
        key_file_content: "{{ letsencrypt_private_key }}"

```

License
-------

GPLv3

Author Information
------------------

https://github.com/deamen
