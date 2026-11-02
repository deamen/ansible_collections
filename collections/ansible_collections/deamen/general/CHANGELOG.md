# Deamen General Collection Release Notes

**Topics**

- <a href="#v1-0-4">v1\.0\.4</a>
    - <a href="#minor-changes">Minor Changes</a>
- <a href="#v1-0-3">v1\.0\.3</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-2">v1\.0\.2</a>
    - <a href="#new-roles">New Roles</a>
- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#new-modules">New Modules</a>
    - <a href="#new-roles-1">New Roles</a>

<a id="v1-0-4"></a>
## v1\.0\.4

<a id="minor-changes"></a>
### Minor Changes

* install\_dev\_packages \- add <code>gzip</code>\, <code>which</code> and <code>procps\-ng</code> to <code>essential\_packages</code> \(needed by VS Code server in minimal containers\)\.
* install\_dev\_packages \- install all packages in one transaction\.

<a id="v1-0-3"></a>
## v1\.0\.3

<a id="minor-changes-1"></a>
### Minor Changes

* Move molecule scenarios under <code>extensions/</code>\.
* install\_dev\_packages \- add <code>tmux</code> to <code>essential\_packages</code>\.

<a id="bugfixes"></a>
### Bugfixes

* Fix playbook relative path in molecule scenarios\.
* config\_dev\_runtime\_env \- add shell type directive for shellcheck to sourced scripts\.
* config\_dev\_runtime\_env \- look up <code>git\-prompt\.sh</code> under <code>/usr/share/git\-core</code> on Fedora/RHEL and Alpine\.
* install\_copilot\_cli \- check both root and non\-root copilot binary locations\.

<a id="v1-0-2"></a>
## v1\.0\.2

<a id="new-roles"></a>
### New Roles

* deamen\.general\.install\_copilot\_cli \- Deploy Microsoft Copilot CLI installation script to target hosts and execute it\.

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="bugfixes-1"></a>
### Bugfixes

* config\_dev\_runtime\_env \- fix git prompt formatting\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary"></a>
### Release Summary

Initial release of the <code>deamen\.general</code> collection\.

<a id="minor-changes-2"></a>
### Minor Changes

* config\_dev\_runtime\_env \- install pre\-commit and detect\-secrets\.

<a id="new-modules"></a>
### New Modules

* deamen\.general\.check\_is\_container \- Check if running inside a container \(Docker\, Podman\, etc\.\)

<a id="new-roles-1"></a>
### New Roles

* deamen\.general\.config\_dev\_runtime\_env \- Configures the runtime environment for development\.
* deamen\.general\.install\_dev\_packages \- Install general development packages\.
