# Deamen Podman Collection Release Notes

**Topics**

- <a href="#v1-0-2">v1\.0\.2</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#minor-changes-1">Minor Changes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#new-modules">New Modules</a>
    - <a href="#new-roles">New Roles</a>

<a id="v1-0-2"></a>
## v1\.0\.2

<a id="minor-changes"></a>
### Minor Changes

* Declare collection dependencies\.
* install\_podman \- apply a podman\-in\-podman workaround when running inside a container\.

<a id="bugfixes"></a>
### Bugfixes

* install\_podman \- make the role idempotent\.

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="minor-changes-1"></a>
### Minor Changes

* Update the ansible\-native molecule test\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary"></a>
### Release Summary

Initial release of the <code>deamen\.podman</code> collection\.

<a id="new-modules"></a>
### New Modules

* deamen\.podman\.manage\_subuid\_subgid \- Manage subordinate UID and GID ranges for users\.

<a id="new-roles"></a>
### New Roles

* deamen\.podman\.install\_podman \- Install Podman and related packages\; prepare host for running containers \(rootful and rootless\)\.
