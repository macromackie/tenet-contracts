---
name: test-support-modules
message: Declare each test helper and fixture once, in its own file of the package's test support folder, and never copy it into another test file.
---

## Rules

Apply this contract to helpers and fixtures that tests, smoke checks, and test scripts use; a test file below is any file that only those checks run.
Declare one test support folder for each package, such as a `testing` folder beside the package's scripts or a `support` folder inside its tests folder.
Put each fixture server, fixture builder, and harness helper in that folder in its own file, named for its behavior, such as `start-process`, as `code-module-file-roles` requires.
Where a contract such as `code-typescript-module-boundaries` gives each folder an entry point, import every helper through the test support folder's entry point.
Declare a helper or fixture that two test files of one package use once in that folder, and import it from every file that uses it.
When tests of several packages need one helper, declare it once in a test support package that each of those packages depends on only for tests.
A helper copied into a second test file is a violation even when the copy was changed afterward, such as a process launcher that removes one fewer environment variable.
Two helpers that share a name but do different work, such as two fake providers that record different calls, are not copies and may stay in their files when each is named for its own work.
A helper or fixture that only one test file uses, such as building that file's seed records, may stay in that file.
`code-ownership-and-boundaries` keeps the test support folder out of production builds.
Enforce the copy rule with the copy detector that `code-duplicated-blocks` configures, and suppress a finding only as `code-lint-suppressions` allows.

Violation: two test files each declare `startProcess({ command })`, and only one of them removes the parent's credentials from the child's environment.
Allowed: both test files import `startProcess` through the test support folder's entry point, which re-exports it from the `start-process` file.

## Checks

Run the repository's copy detector over its test files and confirm that it reports no block copied between two files.
For each helper or fixture a change adds to a test file, does the test support folder or another test file already declare the same work under any name, including a copy with some steps changed?
For each helper a change adds to the test support folder, does it sit in its own file, named for its behavior?
