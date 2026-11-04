deploy_git_conf
===============

Deploy git configuration file.

Requirements
------------

The git configuration tasks run as `git_data.user` via `become_user`, so the
target host needs `sudo` and the connecting user must be able to become that
user. An existing `.gitconfig` that is not owned by `git_data.user` (for example
one created by an earlier run as root) is handed back to that user.

GitHub and Gist credentials come from the GitHub CLI (`gh auth login`). The role
makes `gh auth git-credential` the only credential helper for
`https://github.com` and `https://gist.github.com`, so helpers inherited from
`/etc/gitconfig` or a generic `[credential]` section (such as the VS Code dev
container helper) are not consulted for GitHub. It also removes the legacy
`credential.https://github.com/.username` and `.helper` (gopass) settings.

Role Variables
--------------

All variables are provided via the `git_data` dictionary:

| Variable | Required | Default | Description |
|---|---|---|---|
| `git_data.user` | yes | `""` | Linux username; sets the `.gitconfig` path to `/home/<user>/.gitconfig` |
| `git_data.email` | yes | `""` | Git `user.email` |
| `git_data.username` | yes | `""` | Git `user.name` |
| `git_data.signing_key` | yes | `""` | GPG signing key fingerprint for `user.signingkey` |

Dependencies
------------

`community.general` collection (provides `community.general.git_config`).

Example Playbook
----------------

```yaml
- name: Deploy git global configuration
  hosts: all
  roles:
    - role: deamen.git.deploy_git_conf
      vars:
        git_data:
          user: "alice"
          email: "alice@example.com"
          username: "Alice Smith"
          signing_key: "ABCDEF1234567890"
```


License
-------

GPL-3.0-or-later

Author Information
------------------

Song Tang <stang@mmz.au>
