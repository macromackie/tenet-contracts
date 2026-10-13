---
name: code-typescript-module-boundaries
message: Share code across source folders only through each folder's explicit named-export entry point.
---

## Rules

Give each source folder that other folders import an entry point, `index.ts` unless a tool requires another file name.
Export every value and type the folder shares by name from that entry point.
Do not use default exports, wildcard re-exports, or namespace re-exports in source folders, except where a tool defines the export format.
Export a symbol from a folder's entry point only when production code outside the folder uses it.

Import another folder only through its entry point, including type-only imports, re-exports, and dynamic imports.
Treat nested folders as part of their parent's boundary; give a nested folder its own entry point only when an outside consumer needs it.
Share behavior that several folders need through its own named folder, not by importing another folder's private file.
Keep the import graph between folders acyclic.
Import sibling folders directly from production modules, not through the package's own entry point; tests and examples may use the package entry point to exercise the consumer API.
Keep server-only modules out of entry points that browser code imports.

## Checks

Run the repository's import-boundary lint rule, if one exists, for cross-folder imports, re-exports, type imports, and dynamic imports that bypass the target's entry point.
Run the repository's import-cycle check, or trace changed cross-folder imports for cycles where none exists.
Review each changed entry point, and confirm every named export has a production consumer outside its folder.
Trace outside imports of a moved file to the entry point that exposes it.
