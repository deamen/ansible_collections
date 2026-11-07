# Deamen Ansible Collection Release Notes

**Topics**

- <a href="#v1-3-0">v1\.3\.0</a>
    - <a href="#minor-changes">Minor Changes</a>
- <a href="#v1-2-0">v1\.2\.0</a>
    - <a href="#minor-changes-1">Minor Changes</a>
- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#minor-changes-2">Minor Changes</a>
- <a href="#v1-0-3">v1\.0\.3</a>
    - <a href="#minor-changes-3">Minor Changes</a>
- <a href="#v1-0-2">v1\.0\.2</a>
    - <a href="#minor-changes-4">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#minor-changes-5">Minor Changes</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#new-roles">New Roles</a>

<a id="v1-3-0"></a>
## v1\.3\.0

<a id="minor-changes"></a>
### Minor Changes

* configure\_ansible\_development\_env \- install linear\-cli after Claude Code\, so <code>deamen\.ai\.install\_linear\_cli</code> installs the linear\-cli skill into Claude Code\. Requires <code>deamen\.ai</code> 2\.2\.0 or later\.

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="minor-changes-1"></a>
### Minor Changes

* config\_ansible\_runtime\_env \- install <code>/usr/local/bin/gpg\_cat\.sh</code>\, a generic GPG decrypt script that reads the file from <code>\-\-gpg\_file</code> or the <code>GPG\_FILE</code> environment variable\.
* config\_ansible\_runtime\_env \- install <code>antsibull\-changelog</code> with pip\, used to release collections\; set <code>install\_antsibull\_changelog\_via\_pip\=false</code> to skip it\.
* configure\_ansible\_development\_env \- install Claude Code for the connecting user with <code>deamen\.ai\.install\_claude\_code</code>\; <code>deamen\.ai</code> is now required at <code>\>\=2\.1\.0</code>\.

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="minor-changes-2"></a>
### Minor Changes

* Add <code>configure\_ansible\_development\_env\.yml</code> playbook to install and configure a full Ansible development environment \(system Ansible\, dev packages\, runtime env\, Copilot CLI\, podman and linear\-cli\)\.
* Declare dependencies on <code>deamen\.podman</code> and <code>deamen\.ai</code> \(roles used by <code>configure\_ansible\_development\_env\.yml</code>\)\.

<a id="v1-0-3"></a>
## v1\.0\.3

<a id="minor-changes-3"></a>
### Minor Changes

* Declare dependency on <code>deamen\.gpg</code> \(playbooks used by <code>setup\_ansible\_vault\_gpg\.py</code>\)\.
* config\_ansible\_runtime\_env \- install GPG packages with <code>deamen\.gpg\.install\_gpg</code>\.
* config\_ansible\_runtime\_env \- install <code>/usr/local/bin/ansible\_vault\_pass\_gpg\.sh</code> to read the Ansible Vault password from the GPG\-encrypted <code>\~/\.ansible\_vault\_pass\.gpg</code> \(override with <code>ANSIBLE\_VAULT\_GPG\_FILE</code>\)\.
* config\_ansible\_runtime\_env \- install <code>/usr/local/bin/setup\_ansible\_vault\_gpg\.py</code> to create <code>\~/\.ansible\_vault\_pass\.gpg</code>\, importing the GPG secret key from <code>\~/\.gnupg/private\_gpg\.key</code> by default\.
* config\_ansible\_runtime\_env \- install <code>unversioned\_python\_packages</code> \(default <code>python\-unversioned\-command</code>\) for the <code>\#\!/usr/bin/env python</code> shebang of <code>setup\_ansible\_vault\_gpg\.py</code>\.

<a id="v1-0-2"></a>
## v1\.0\.2

<a id="minor-changes-4"></a>
### Minor Changes

* Declare dependency on <code>deamen\.general</code> \(used by <code>configure\_system\_ansible\_runtime\_env\.yml</code>\)\.
* Move molecule scenarios under <code>extensions/</code>\.
* config\_ansible\_runtime\_env \- add <code>install\_molecule\_via\_pip</code> option \(default <code>true</code>\)\.
* config\_ansible\_runtime\_env \- default <code>ansible\_pip\_executable</code> to <code>/usr/bin/pip3</code> so it works on any Fedora release\.
* config\_ansible\_runtime\_env \- install molecule via pip\.
* configure\_system\_ansible\_runtime\_env\.yml \- configure the connecting user instead of root\; only pip installs use become\.
* install\_system\_ansible \- install <code>sshpass</code>\.

<a id="bugfixes"></a>
### Bugfixes

* Fix playbook relative path in molecule scenarios\.
* config\_ansible\_runtime\_env \- skip collection install when <code>\~/Prj/ansible/requirements\.yml</code> is absent\.

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="minor-changes-5"></a>
### Minor Changes

* install\_system\_ansible \- remove role\-level tests\.

<a id="bugfixes-1"></a>
### Bugfixes

* config\_ansible\_runtime\_env \- check the <code>molecule</code> group is defined before checking membership\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary"></a>
### Release Summary

Initial release\. The Ansible roles were moved here from <code>deamen\.general</code>\.

<a id="new-roles"></a>
### New Roles

* deamen\.ansible\.config\_ansible\_runtime\_env \- Configure Ansible runtime environment\.
* deamen\.ansible\.install\_system\_ansible \- Install ansible from system package manager\.
