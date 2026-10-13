---
name: code-typescript-package-boundaries
message: Consume TypeScript packages only through declared dependencies and explicitly exported entry points.
---

## Rules

Give each TypeScript application and package its own manifest that declares its name, dependencies, and supported entry points.
List supported entry points in the manifest's exports map, and treat every other file as private; see `code-ownership-and-boundaries` for importing only through public entry points.
Export from each entry point only named symbols that consumers outside the package use, and never re-export every folder from one package-wide barrel.
Add an entry point only when another production consumer needs that API.
Preserve entry-point file names and export formats that a tool requires.

Declare every package you import as a dependency of the importing package rather than relying on a transitive or hoisted install.
Depend on packages in the same repository through the package manager's workspace links, and on packages from other repositories through exact published versions.

## Checks

Inspect changed imports, exports, and dependency declarations together.
Search changed imports for package subpaths that the target package's exports map does not declare.
Confirm each new entry point and export has a production consumer outside the package.
