---
name: code-python-uv-scripts
message: Run each Python repository script with `uv run --script`, and declare its dependencies in its own PEP 723 inline metadata block.
---

## Rules

Apply this contract to every script written in Python that a person or CI runs to work on the repository, and not to programs the product ships.
Start each executable Python script with `#!/usr/bin/env -S uv run --script`, and run every Python script with `uv run --script`, never with an interpreter from an activated or project environment.
Give each Python script a PEP 723 inline script metadata block that lists every package it imports outside the standard library, even when that list is empty, because without the block `uv run --script` runs the script in the surrounding project's environment.

Violation: `export-invoices.py` has no metadata block and imports a YAML parser that only the surrounding project installs.
Allowed: `export-invoices.py` starts with `#!/usr/bin/env -S uv run --script` and lists its YAML parser under `dependencies` in its `# /// script` block.

## Checks

Run each changed Python script the way the repository runs it, such as through its task runner, from a shell with no activated environment.
Search Python scripts for a first line other than `#!/usr/bin/env -S uv run --script`, for a missing `# /// script` block, and for imports outside the standard library that the block does not list.
