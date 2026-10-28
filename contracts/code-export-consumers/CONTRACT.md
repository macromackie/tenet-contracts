---
name: code-export-consumers
message: Give every export, source file, and dependency a production consumer, and let the repository's dead-code check prove it.
---

## Rules

This contract extends `code-ownership-and-boundaries`, which removes superseded paths and dependencies, to every export, source file, and dependency.
Export a declaration only when another source file imports it; a function, constant, type, or schema that only its own file uses stays unexported, which in a language that lets another file import every top-level name means giving it the language's private name form, such as a leading underscore.
In a language that marks which names another file may import, such as with an export statement or a visibility keyword, never start a name with an underscore to mark it private, except a binding, parameter, or field that the code never reads.
A type that an exported declaration's signature uses counts as used by that declaration's consumers, so its file may export it although no other file imports it.
Give each export of a package entry point a production consumer outside the package, or a public-API marker that names its consumer outside the repository.
An export of production source that only tests import has no consumer, because tests reach code through the entry points that production uses; the files of a test support folder or test support package that `test-support-modules` requires, including the package's entry point, export to tests, so each of their exports needs a test consumer instead of a production one.
Reach every source file from an entry point: a manifest export, a file that a runtime or framework loads, or a script that a repository task runs.
Remove a dependency that no source file imports, no configuration file names, and no repository task runs.

Run the repository's dead-code check on every package, configured to report entry-point exports, unreachable files, and unused dependencies, and fail on any finding.
Run it once counting imports from tests and once counting only production consumers, with the files of test support folders and packages left out, so that it reports both unused test helpers and exports that only tests import.
Let the check read the runtime's or framework's own configuration, such as the server's deployment file, so that the exports the runtime loads count as used; a plain entry for that file still reports them.
Treat a public-API marker and each ignore entry in the check's configuration as suppressions under `code-lint-suppressions`, and name in each reason the consumer that the check cannot see, such as another repository, a framework, or a binary that a task runs.
An ignore entry may also exclude files that are not the package's source, such as fixture projects or generated output.
An ignore entry that hides an unused file, export, or dependency is a violation, and so is a public-API marker whose reason names a test, a script in the repository, a planned use, or no consumer; a change in another repository that imports the export from the release that adds it is a consumer, not a planned use.

Violation: a records file declares `export function formatUsd({ micros }: FormatUsdInput): string`, and no other file imports `formatUsd`.
Allowed: a published client entry point marks its `InvoiceClient` type as public API, and the marker's reason names the other repository that imports it.

## Checks

Run the repository's dead-code check from the repository root in both modes, and confirm that each one fails on a finding.
For each public-API marker or ignore entry a change adds, does its reason name a consumer that the check cannot see, or a set of files that are not source?
For each entry a change adds to the check's configuration, does a runtime, a framework, or a repository task load that file?
