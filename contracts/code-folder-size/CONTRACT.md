---
name: code-folder-size
message: Keep every source folder within lint-enforced limits on its file count and depth, and name and justify each exempt folder in the lint configuration.
requires-tenet: 0.11.0
---

## Rules

Declare each package's source roots, including its test and script folders, a maximum number of files that share one extension directly inside one folder, and a maximum number of folder levels below a source root.
Count a folder directly inside a source root as its first level.
Enforce both limits with the repository's file-layout lint on every folder under a declared source root.
A repository may use the checker under `assets/`, whose policy schema and example configuration declare source roots, standalone source files, filename suffixes, shebang scripts, and justified exclusions.
That configuration sets 20 same-extension files per folder and 4 folder levels; a repository may override either declared limit.
The checker also enforces the source file length that `code-module-file-roles` requires; its example configuration sets 300 lines, including blank lines and comments.
When a change would put a folder over its file limit, move the files that serve one behavior into a subfolder before adding the file, instead of raising the limit.
Name and scope each new subfolder as `code-module-structure-and-control-flow` requires for a module.
Exempt a folder only with the configuration entry that `code-lint-suppressions` requires for a finding that reports no line, such as for route segments that a framework requires.
Add a file to an exempt folder only when the system that the exemption's reason names requires that file there.
An exemption without a reason, an exemption that also covers the folder's subfolders, and a limit raised for every folder to admit one folder are violations.
Leave out of both limits, by a declared path pattern, folders whose entries are data rather than source, such as test fixture projects.

Violation: a change adds a file to `src/billing/`, which is at its file limit, and raises the limit for every folder.
Allowed: a change moves the four files that compute tax into `src/billing/tax/` before adding the new file to `src/billing/`.

## Checks

Run the repository's file-layout lint from the repository root.
For the shipped checker, follow its usage instructions under `assets/`, declare the repository's policy, and run it from the repository root.
For each change to the layout lint configuration, does it keep the declared limits, and does each new exemption name one folder with a reason specific to it?
For each file a change adds to an exempt folder, does the system that the exemption's reason names require that file there?
