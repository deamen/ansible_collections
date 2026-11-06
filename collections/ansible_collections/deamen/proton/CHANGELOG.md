# Deamen Proton Collection Release Notes

**Topics**

- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#new-roles">New Roles</a>

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary"></a>
### Release Summary

Initial release of the <code>deamen\.proton</code> collection\, which holds roles and playbooks for Proton tools\.

<a id="minor-changes"></a>
### Minor Changes

* Add the <code>install\_proton\_drive\_cli</code> playbook\, which runs the <code>install\_proton\_drive\_cli</code> role against localhost\.
* install\_proton\_drive\_cli \- export <code>PROTON\_DRIVE\_CREDENTIALS\_STORE</code> from <code>\~/\.bashrc\.d/proton\_drive\_cli\.sh</code>\, set to <code>unsafe\_file</code> by default for hosts without an OS secret store\.

<a id="new-roles"></a>
### New Roles

* deamen\.proton\.install\_proton\_drive\_cli \- Install the Proton Drive CLI for the connecting user\.
