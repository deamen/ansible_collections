# Deamen GPG Collection Release Notes

**Topics**

- <a href="#v2-1-0">v2\.1\.0</a>
    - <a href="#minor-changes">Minor Changes</a>
- <a href="#v2-0-0">v2\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
    - <a href="#new-roles">New Roles</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#new-roles-1">New Roles</a>

<a id="v2-1-0"></a>
## v2\.1\.0

<a id="minor-changes"></a>
### Minor Changes

* Add <code>deamen\.gpg\.config\_gpg</code> and <code>deamen\.gpg\.generate\_gpg\_key</code> playbooks for configuring GPG on localhost \(used by <code>setup\_ansible\_vault\_gpg\.py</code> from <code>deamen\.ansible</code>\)\.

<a id="v2-0-0"></a>
## v2\.0\.0

<a id="release-summary"></a>
### Release Summary

Adds public key import to <code>config\_gpg</code> and renames its key import variables\.

<a id="minor-changes-1"></a>
### Minor Changes

* config\_gpg \- add <code>config\_gpg\_import\_public\_key</code> and <code>config\_gpg\_public\_key</code> to import a public key without a private key\.

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* config\_gpg \- rename <code>config\_gpg\_private\_key\_path</code> to <code>config\_gpg\_secret\_key\_path</code>\.
* config\_gpg \- replace <code>config\_gpg\_import\_key</code> with <code>config\_gpg\_import\_secret\_key</code>\, which defaults to <code>false</code>\. Set <code>config\_gpg\_import\_secret\_key\: true</code> to keep importing the private key\.

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="minor-changes-2"></a>
### Minor Changes

* config\_gpg \- improve the role\.
* generate\_gpg\_key \- improve the role and update role metadata\.
* install\_gpg \- update role metadata\.

<a id="bugfixes"></a>
### Bugfixes

* config\_gpg \- make the role idempotent\.

<a id="new-roles"></a>
### New Roles

* deamen\.gpg\.generate\_gpg\_key \- Generate GPG key\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary-1"></a>
### Release Summary

Initial release of the <code>deamen\.gpg</code> collection\.

<a id="new-roles-1"></a>
### New Roles

* deamen\.gpg\.config\_gpg \- Configure GPG\.
* deamen\.gpg\.install\_gpg \- Install GPG packages\.
