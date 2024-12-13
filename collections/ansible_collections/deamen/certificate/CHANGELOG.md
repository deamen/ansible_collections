# Deamen Certificate Collection Release Notes

**Topics**

- <a href="#v1-3-0">v1\.3\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#major-changes">Major Changes</a>
- <a href="#v1-2-0">v1\.2\.0</a>
    - <a href="#major-changes-1">Major Changes</a>
    - <a href="#deprecated-features">Deprecated Features</a>
- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#new-modules">New Modules</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#new-plugins">New Plugins</a>
        - <a href="#filter">Filter</a>
    - <a href="#new-modules-1">New Modules</a>

<a id="v1-3-0"></a>
## v1\.3\.0

<a id="release-summary"></a>
### Release Summary

Add gen\_certificate\_from\_vault module

<a id="major-changes"></a>
### Major Changes

* Add gen\_certificate\_from\_vault module\, runs on localhost by default

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="major-changes-1"></a>
### Major Changes

* Refactor module deamen\.certificate\.deploy\_certificate as action plugin

<a id="deprecated-features"></a>
### Deprecated Features

* Role\: deamen\.certificate\.deploy\_certificate

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="release-summary-1"></a>
### Release Summary

This release adds deploy\_certificates module to the collection\.
It is favoured over the deploy\_certificate role\.
The role will be deprecated in the next release\.

<a id="new-modules"></a>
### New Modules

* deploy\_certificate \- Deploy certificates and keys to specified locations

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="new-plugins"></a>
### New Plugins

<a id="filter"></a>
#### Filter

* hello\_world \- A custom filter plugin for Ansible\.

<a id="new-modules-1"></a>
### New Modules

* deploy\_private\_ca \- Deploy a private CA certificate to a Linux server
