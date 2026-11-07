# Deamen General Collection Release Notes

**Topics**

- <a href="#v1-3-0">v1\.3\.0</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#new-roles">New Roles</a>
- <a href="#v1-2-0">v1\.2\.0</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#new-roles-1">New Roles</a>
- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#minor-changes-2">Minor Changes</a>
- <a href="#v1-0-5">v1\.0\.5</a>
    - <a href="#minor-changes-3">Minor Changes</a>
- <a href="#v1-0-4">v1\.0\.4</a>
    - <a href="#minor-changes-4">Minor Changes</a>
- <a href="#v1-0-3">v1\.0\.3</a>
    - <a href="#minor-changes-5">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-2">v1\.0\.2</a>
    - <a href="#new-roles-2">New Roles</a>
- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes-6">Minor Changes</a>
    - <a href="#new-modules">New Modules</a>
    - <a href="#new-roles-3">New Roles</a>

<a id="v1-3-0"></a>
## v1\.3\.0

<a id="minor-changes"></a>
### Minor Changes

* Add the <code>configure\_keyring</code> role to install a GNOME Keyring Secret Service that a user unlocks on demand with <code>keyring\-unlock</code>\, for containers and headless hosts\.

<a id="new-roles"></a>
### New Roles

* deamen\.general\.configure\_keyring \- Install a GNOME Keyring Secret Service that a user unlocks on demand\.

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="minor-changes-1"></a>
### Minor Changes

* Add the <code>install\_himalaya</code> role to install the himalaya email CLI for the connecting user and deploy a minimal configuration\.

<a id="new-roles-1"></a>
### New Roles

* deamen\.general\.install\_himalaya \- Install the himalaya email CLI for the connecting user\.

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="minor-changes-2"></a>
### Minor Changes

* config\_dev\_runtime\_env \- add <code>config\_dev\_runtime\_env\_force\_deploy\_aliases</code> to redeploy <code>aliases\.sh</code> when it already exists\.
* config\_dev\_runtime\_env \- add <code>unlock\_gpg</code> to <code>aliases\.sh</code> to cache the GPG signing and decryption passphrases in <code>gpg\-agent</code>\, and export <code>GPG\_TTY</code> in interactive shells\.

<a id="v1-0-5"></a>
## v1\.0\.5

<a id="minor-changes-3"></a>
### Minor Changes

* config\_dev\_runtime\_env \- define <code>ansiblev</code> and <code>ansible\-playbookv</code> as bash functions instead of aliases wrapping functions\.
* config\_dev\_runtime\_env \- use <code>ANSIBLE\_VAULT\_PASSWORD\_FILE</code> when <code>\~/\.ansible\_vault\_pass\.gpg</code> and the gpg helper script exist\, and only pass <code>\-\-ask\-vault\-pass</code> when no vault password file is configured\.

<a id="v1-0-4"></a>
## v1\.0\.4

<a id="minor-changes-4"></a>
### Minor Changes

* install\_dev\_packages \- add <code>gzip</code>\, <code>which</code> and <code>procps\-ng</code> to <code>essential\_packages</code> \(needed by VS Code server in minimal containers\)\.
* install\_dev\_packages \- install all packages in one transaction\.

<a id="v1-0-3"></a>
## v1\.0\.3

<a id="minor-changes-5"></a>
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

<a id="new-roles-2"></a>
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

<a id="minor-changes-6"></a>
### Minor Changes

* config\_dev\_runtime\_env \- install pre\-commit and detect\-secrets\.

<a id="new-modules"></a>
### New Modules

* deamen\.general\.check\_is\_container \- Check if running inside a container \(Docker\, Podman\, etc\.\)

<a id="new-roles-3"></a>
### New Roles

* deamen\.general\.config\_dev\_runtime\_env \- Configures the runtime environment for development\.
* deamen\.general\.install\_dev\_packages \- Install general development packages\.
