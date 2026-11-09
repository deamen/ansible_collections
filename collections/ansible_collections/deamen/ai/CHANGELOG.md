# Deamen AI Collection Release Notes

**Topics**

- <a href="#v2-3-0">v2\.3\.0</a>
    - <a href="#minor-changes">Minor Changes</a>
- <a href="#v2-2-0">v2\.2\.0</a>
    - <a href="#minor-changes-1">Minor Changes</a>
- <a href="#v2-1-0">v2\.1\.0</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#new-roles">New Roles</a>
- <a href="#v2-0-0">v2\.0\.0</a>
    - <a href="#minor-changes-3">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
    - <a href="#new-roles-1">New Roles</a>
- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#new-roles-2">New Roles</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes-4">Minor Changes</a>
    - <a href="#new-roles-3">New Roles</a>

<a id="v2-3-0"></a>
## v2\.3\.0

<a id="minor-changes"></a>
### Minor Changes

* install\_linear\_cli \- the playbook now targets <code>all</code> instead of <code>all\:\!localhost</code> so it can run against localhost\, which the <code>buildah\_fedora\-codespace</code> image build needs \([https\://github\.com/deamen/ansible\_collections/pull/112](https\://github\.com/deamen/ansible\_collections/pull/112)\)\.

<a id="v2-2-0"></a>
## v2\.2\.0

<a id="minor-changes-1"></a>
### Minor Changes

* install\_linear\_cli \- deploy <code>install\-linear\-cli\-skill</code> into <code>linear\_cli\_install\_dir</code>\, which installs the skill for other AI agents on demand with <code>npx skills add</code> \(<code>linear\_cli\_skills\_installer</code>\)\.
* install\_linear\_cli \- install the linear\-cli skill into Claude Code for the connecting user when Claude Code is installed \(<code>linear\_cli\_claude\_code\_skill</code>\)\.

<a id="v2-1-0"></a>
## v2\.1\.0

<a id="minor-changes-2"></a>
### Minor Changes

* Add the <code>install\_claude\_code</code> role to install the Claude Code CLI for a user with the native installer\.

<a id="new-roles"></a>
### New Roles

* deamen\.ai\.install\_claude\_code \- Install the Claude Code CLI for a user with the native installer\.

<a id="v2-0-0"></a>
## v2\.0\.0

<a id="minor-changes-3"></a>
### Minor Changes

* Add <code>buildah\_alpine\_llamacpp\.yml</code> playbook to build statically linked <code>llama\-cli</code> and <code>llama\-server</code> with OpenBLAS on Alpine Linux\.
* Add <code>install\_linear\_cli\.yml</code> playbook to install linear\-cli with the new <code>install\_linear\_cli</code> role\.

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* Rename <code>buildah\_fedora\-llamacpp\.yml</code> playbook to <code>buildah\_fedora\_llamacpp\.yml</code> so it can be run by its FQCN <code>deamen\.ai\.buildah\_fedora\_llamacpp</code>\; it now writes the llama\.cpp executables to <code>build\_outputs/llama\.cpp/fedora</code> under the current directory instead of <code>\.\./out/llama</code> relative to the playbook \(override with <code>llamacpp\_output\_dir</code>\)\.

<a id="new-roles-1"></a>
### New Roles

* deamen\.ai\.install\_linear\_cli \- Install linear\-cli\, the command\-line interface for Linear\.

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="new-roles-2"></a>
### New Roles

* deamen\.ai\.install\_pi\_code \- Install pi\-coding\-agent globally with npm\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary"></a>
### Release Summary

Initial release of the <code>deamen\.ai</code> collection\.

<a id="minor-changes-4"></a>
### Minor Changes

* Add <code>buildah\_fedora\-llamacpp\.yml</code> playbook\.

<a id="new-roles-3"></a>
### New Roles

* deamen\.ai\.install\_gemini\_cli \- Install gemini\-cli\, the command\-line interface for Gemini\.
* deamen\.ai\.install\_npm \- Install Node\.js and npm packages\.
