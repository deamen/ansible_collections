---
name: molecule-init-skill
description: Creates a molecule scenario using `helper_scripts/init_molecule.py`. Activate when asked to "create molecule scenario", "init molecule scenario", or similar.
license: GPL-3.0-or-later
---

# Molecule Scenario Creator Skill


## Instructions


- Run `helper_scripts/init_molecule.py --collection <namespace.collection>` to create a new molecule scenario named `default`, when user did not specify a scenario name. If user specified a scenario name, use that instead of `default`.
- Run `helper_scripts/init_molecule.py --collection <namespace.collection> --scenario <scenario_name>` to create a new molecule scenario with the specified name.
- Return CLI output and a short list of created files (or the error message if the command fails).
