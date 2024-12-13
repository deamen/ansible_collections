===========================================
Deamen Certificate Collection Release Notes
===========================================

.. contents:: Topics

v1.3.0
======

Release Summary
---------------

Add gen_certificate_from_vault module

Major Changes
-------------

- Add gen_certificate_from_vault module, runs on localhost by default

v1.2.0
======

Major Changes
-------------

- Refactor module deamen.certificate.deploy_certificate as action plugin

Deprecated Features
-------------------

- Role: deamen.certificate.deploy_certificate

v1.1.0
======

Release Summary
---------------

This release adds deploy_certificates module to the collection.
It is favoured over the deploy_certificate role.
The role will be deprecated in the next release.

New Modules
-----------

- deploy_certificate - Deploy certificates and keys to specified locations

v1.0.0
======

New Plugins
-----------

Filter
~~~~~~

- hello_world - A custom filter plugin for Ansible.

New Modules
-----------

- deploy_private_ca - Deploy a private CA certificate to a Linux server
