# Deamen Ansible Collection Release Notes

**Topics**

- <a href="#v1-0-2">v1\.0\.2</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#new-roles">New Roles</a>

<a id="v1-0-2"></a>
## v1\.0\.2

<a id="minor-changes"></a>
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

<a id="minor-changes-1"></a>
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
