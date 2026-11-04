# Deamen Git Collection Release Notes

**Topics**

- <a href="#v2-0-0">v2\.0\.0</a>
    - <a href="#removed-features-previously-deprecated">Removed Features \(previously deprecated\)</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#new-roles">New Roles</a>

<a id="v2-0-0"></a>
## v2\.0\.0

<a id="removed-features-previously-deprecated"></a>
### Removed Features \(previously deprecated\)

* deploy\_git\_conf \- the <code>git\_data\.github\_username</code> and <code>git\_data\.github\_helper</code> options were removed\; GitHub credentials now always come from the GitHub CLI\.

<a id="bugfixes"></a>
### Bugfixes

* deploy\_git\_conf \- make <code>gh auth git\-credential</code> the only credential helper for <code>https\://github\.com</code> and <code>https\://gist\.github\.com</code>\, so inherited helpers \(such as the VS Code dev container helper\) no longer answer first\, and remove the legacy <code>credential\.https\://github\.com/\.username</code> and gopass helper settings that made <code>gh</code> refuse to supply a token\.
* deploy\_git\_conf \- run the <code>git\_config</code> tasks as <code>git\_data\.user</code> so <code>\.gitconfig</code> is no longer created owned by root when the play uses <code>become</code>\, and hand an existing root\-owned <code>\.gitconfig</code> back to the user\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary"></a>
### Release Summary

Initial release of the <code>deamen\.git</code> collection\.

<a id="new-roles"></a>
### New Roles

* deamen\.git\.deploy\_git\_conf \- Deploy git configuration file\.
