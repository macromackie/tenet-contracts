# Package README check

Run from the repository root, replacing the installed contract path and the workspace root:

```bash
uv run --script .contracts/031-docs-package-readme/assets/uv/check-package-readmes.py --root .
```

The script requires Python 3.14 or later and has no package dependencies. It reads the member patterns from the first
of these files that `--root` holds: `pnpm-workspace.yaml` (`packages`, with `!` exclusions), a `Cargo.toml` with
`[workspace]`, or a `pyproject.toml` with `[tool.uv.workspace]` (`members` and `exclude`). A member is a folder that
matches a pattern and holds the manager's manifest: `package.json`, `Cargo.toml`, or `pyproject.toml`. The name and the
description come from the manifest's top level, `[package]`, or `[project]`. A description inherited from the
workspace is refused, because the README must equal a sentence that the manifest itself states. Any other workspace
file stops the check with a message that names the three it reads.

A package README is checked for its title, the description sentence, the headings `## Layout`, `## Use`, and
`## Never` in that order, the form of each Layout line, the existence of each Layout path, and its line count. A group
README is checked for its title, one sentence, a table with one row for each package directly inside the folder, and
its line count. Set other limits with `--maximum-package-lines` and `--maximum-group-lines`; the defaults are 30 and 15.

The command reports every finding and exits unsuccessfully. It changes no files and cannot tell whether a Layout
description, a Use section, or a Never item is true.
