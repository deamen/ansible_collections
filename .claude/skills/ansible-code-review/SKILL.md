---
name: ansible-code-review
description: Reviews changed Ansible code (playbooks, roles, collections, molecule scenarios) against the repository rules in .claude/rules/ansible-style.md before a commit. Activate before committing Ansible changes, or when asked to "review the ansible code", "check the ansible rules", or similar.
---

# Ansible Code Review Skill

Review only the Ansible files this change touches, against the rules in `.claude/rules/ansible-style.md`. The rules file is the source of truth. This skill lists the checks to run; when a check and the rules file disagree, follow the rules file.

## Instructions

1. **Scope the review.** Collect the changed files with `git diff --name-only origin/master...HEAD` plus any uncommitted changes (`git status --short`). Keep the `.yml`, `.yaml`, `.j2` and `.py` files under `collections/ansible_collections/`. Skip `tests/`, `docs/` and `README.md`, which are not Ansible code. If nothing is in scope, say so and stop.

2. **Read the rules.** Read `.claude/rules/ansible-style.md` in full. Do not restate it in the report; cite the rule heading each finding breaks.

3. **Run the mechanical checks.** Use the patterns below on the in-scope files, then read each hit in context. A hit is a candidate, not a finding: a comment or an intentional case may explain it.

   - **Bare boolean conditions** (rule: "Always use the `| bool` filter"). A variable used alone in `when:`, or after `not`, or in a list of conditions, needs `| bool`. Patterns to read:
     - `grep -nE '^\s*(- )?when:\s*[A-Za-z_][A-Za-z0-9_.]*\s*$'`
     - `grep -nE '^\s+- [A-Za-z_][A-Za-z0-9_.]*\s*$'` inside a `when:` list
     - `grep -nE 'when:.*\bnot [A-Za-z_]'`
     - `grep -nE '(failed_when|changed_when|until):\s*[A-Za-z_][A-Za-z0-9_.]*\s*$'`
     - A bare variable inside a multi-line `when: >-` block.
     - Fix: `when: some_flag | bool`, `when: not (some_flag | bool)`.

   - **Empty defaults** (rule: "Never use default empty values"). Patterns:
     - `grep -nE "default\((''|\"\"|\[\]|\{\}|None)\)"` (`default(omit)` is the idiom for not passing a parameter, not an empty value, so it is not flagged)
     - `grep -nE "default\(\s*(''|\"\")\s*,\s*true\)"`
     - Also look for variables defined in `defaults/main.yml` or `vars/main.yml` with values `""`, `[]`, `{}`, `null` or `~`.
     - A hit is allowed only with a comment on the same or the preceding line explaining why the empty value is needed. A bare empty default is a finding. Fix: remove the default, or add the comment.

   - **Shell and command modules** (rule: idempotent modules; use `creates:` or `removes:`). Patterns:
     - `grep -nE 'ansible\.builtin\.(shell|command|raw)|^\s+(shell|command|raw):'`
     - A hit without `creates:` or `removes:` nearby, and without a `changed_when`, is a finding. Check that the task is genuinely not replaceable by a module.

   - **FQCN** (rule: use fully qualified collection names). Look for short module names as task keys, for example `^\s+(copy|file|template|package|service|command|shell|user|stat|lineinfile|get_url|unarchive|assert|debug|fail|set_fact|include_role|import_role):`.

   - **Legacy `roles:` keyword** (rule: prefer `import_role`/`include_role` under `tasks`). Look for `^\s+roles:` in play bodies.

   - **Become placement** (rule: lowest privilege). Look for `become: true` at play level in a play whose tasks mostly do not need root, and for `become: true` on tasks with no privileged work. Any playbook that targets `localhost` must set `become: false` at the playbook level.

   - **Explicit state** (rule: set `state:` when the module allows it). Look for module tasks that omit `state:` where the module supports it.

   - **Naming** (rule: General Instructions). Every play, block and task has a `name`. Names start with a capitalised action verb, have no trailing period, and do not repeat the role name.

   - **Layout** (rule: Style). Two-space indentation, indented lists, one blank line between host blocks, task blocks, and host and include blocks. Multi-line map syntax, even for one pair. Strings unquoted unless required.

   - **Ordering** (rule: Style). Play keys in order: `hosts`, host options alphabetically, `pre_tasks`, `roles`, `tasks`. Task keys: `name`, the module, parameters, loop operators, options alphabetically, `tags`. Variables in `vars:` maps and variable files sorted alphabetically.

   - **Variable names and secrets** (rule: Style and Secret Management). `snake_case` names. No plain-text secrets. Vaulted values are referenced through a `vault_` variable from a `vars` file, and no `vault_` variable is referenced directly from a task.

4. **Run the linters on the changed paths.** From the repository root:
   - `ansible-lint <changed paths>` (the repo runs it on the whole tree, so also run `ansible-lint` with no arguments when a role or playbook changed)
   - `yamllint <changed yaml paths>`
   - `ansible-playbook --syntax-check <changed playbooks>`
   - `pre-commit run --files <changed files>`
   - For modules and plugins, `ansible-test sanity --test validate-modules` from the collection root.
   Record each command's exit code. A linter failure is a finding even when the mechanical checks found nothing.

5. **Fix what the rules make unambiguous.** Apply the fix for each clear violation, then re-run the affected linter. Leave ambiguous cases, and anything that changes behaviour beyond the rule, for the user to decide.

6. **Report.** For each finding give the file and line, the rule heading it breaks, whether it was fixed, and the command output for any linter failure. Finish with one line stating whether the change is ready to commit. Report a failing linter as failing; do not describe it as a warning.

## Notes

- Do not run `ansible-playbook` against real hosts. `--check --diff` only when the user asks for it.
- This skill reviews; it does not commit or push. Committing follows the repository's PR rule.
