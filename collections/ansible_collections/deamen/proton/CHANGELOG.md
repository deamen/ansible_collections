# Deamen Proton Collection Release Notes

**Topics**

- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#new-roles">New Roles</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#new-roles-1">New Roles</a>

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="minor-changes"></a>
### Minor Changes

* Add the <code>install\_proton\_pass\_cli</code> playbook\, which runs the <code>install\_proton\_pass\_cli</code> role against localhost\.
* install\_proton\_pass\_cli \- export <code>PROTON\_PASS\_KEY\_PROVIDER</code> from <code>\~/\.bashrc\.d/proton\_pass\_cli\.sh</code>\, set to <code>fs</code> by default because containers cannot reach the kernel keyring\.

<a id="new-roles"></a>
### New Roles

* deamen\.proton\.install\_proton\_pass\_cli \- Install the Proton Pass CLI for the connecting user\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary"></a>
### Release Summary

Initial release of the <code>deamen\.proton</code> collection\, which holds roles and playbooks for Proton tools\.

<a id="minor-changes-1"></a>
### Minor Changes

* Add the <code>install\_proton\_drive\_cli</code> playbook\, which runs the <code>install\_proton\_drive\_cli</code> role against localhost\.
* install\_proton\_drive\_cli \- export <code>PROTON\_DRIVE\_CREDENTIALS\_STORE</code> from <code>\~/\.bashrc\.d/proton\_drive\_cli\.sh</code>\, set to <code>unsafe\_file</code> by default for hosts without an OS secret store\.

<a id="new-roles-1"></a>
### New Roles

* deamen\.proton\.install\_proton\_drive\_cli \- Install the Proton Drive CLI for the connecting user\.
