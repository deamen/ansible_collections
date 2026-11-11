# Deamen Patching Collection Release Notes

**Topics**

- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#minor-changes">Minor Changes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#new-roles">New Roles</a>

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="minor-changes"></a>
### Minor Changes

* install\_system\_updates \- add <code>patching\_update\_timeout</code> \(default <code>3600</code> seconds\)\, which fails the download or install step when it hangs\, for example on a stalled mirror\. The failure is handled like any other update failure\. <code>needs\-restarting \-r</code> now fails after 300 seconds\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary"></a>
### Release Summary

Initial release of the <code>deamen\.patching</code> collection\.

<a id="new-roles"></a>
### New Roles

* deamen\.patching\.install\_system\_updates \- Apply OS updates to RHEL and Fedora hosts in fixed phases\.
* deamen\.patching\.patching\_fleet\_report \- Aggregate the per\-host patching summaries of a run into a fleet report\.
* deamen\.patching\.patching\_profile\_example \- Starter patching profile showing the profile contract\.
