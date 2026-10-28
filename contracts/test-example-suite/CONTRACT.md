---
name: test-example-suite
message: Keep a declared, fixed number of one-case example tests for each test runner as templates for temporary tests, and never count one as a regression's protection.
---

## Rules

Apply this contract to example tests, which a repository keeps only to show how to write a test, and to every temporary test for a runner and kind that has an example.

Keep, for the whole repository, at most a declared, fixed number of examples of each kind for each test runner command that CI invokes, and never let that number depend on the number of packages, modules, or features.
Count a runner command that CI invokes once per package as one command.
Mark every example by a declared path, such as an `examples` folder inside a tests folder, and keep no other test at a path that matches it.
Declare the numbers, the path marker, and the scratch folder once, such as under the installed contract's local adaptations.

Give each example its own file, holding one case with one assertion that compares a result with a literal value or a stable error code.
Write no loop, table, parameterized rows, or generator in an example, never instantiate one more than once from build configuration, and call no helper that asserts.
Call a stable public entry point that most of the package depends on, and import helpers only from the package's test support folder that `test-support-modules` defines.
Start each example with a header comment that states its kind, when to copy it, and the exact command that runs a copy.

Give each example one of two kinds, set by the boundary it crosses and never by its name or folder.
An isolated example starts no child process, opens no socket, and touches no disk outside a temporary folder.
A local-dependency example starts one local dependency, such as a database or a local server, through a fixture from the test support folder.
A test that runs the product's own entry point as its users run it is end-to-end and never an example.

Never add a case or an assertion to an example to guard a regression, and guard that regression as `test-curation` requires instead.
Never cite an example as a regression's protection, including the protection that remains when coverage is removed.
Write each example as a new file, and never cut an existing test down to make one.
Replace an example only while it passes, in a change that touches no other file.

Keep the scratch folder beside the examples, ignored by version control and still collected by the test runner, so a copy keeps the example's imports.
Start each temporary test as a copy of an example of its runner and kind, under a new file name, in that scratch folder, and keep it out of every commit as `test-curation` requires.

Violation: a repository declares two examples per package, so each new package adds two more.
Violation: an example loops over three currencies and asserts each invoice total.
Violation: a change that fixes refund rounding adds a second assertion to the isolated example and cites it as the fix's protection.
Allowed: a repository declares one isolated and one local-dependency example for each test runner command that CI invokes, under `tests/examples/`, and ignores `tests/scratch/` beside it.
Allowed: the isolated example's header gives its kind, when to copy it, and its run command, and its one case asserts `computeOrderTotal({ prices: [300, 200] })` returns `500`.

## Checks

List the tracked files that match the declared example marker from the repository root, and compare the count for each test runner command and kind with its declared number.
Does any declared number grow with the number of packages, modules, or features?
Does each changed example hold one case with one assertion of a literal value or stable error code, and no loop, table, parameterized rows, generator, asserting helper, or second instantiation from build configuration?
Does each changed example's kind match the boundary it crosses, and does its header state that kind, when to copy it, and the command that runs a copy?
Does any change add to an example to guard a regression, or cite an example as the protection that remains?
Does each change that replaces an example touch any other file, and did the replaced example pass at the base revision?
Copy each changed example into the scratch folder under a new name, run it with its header's command, confirm that the runner collects it and version control ignores it, then delete the copy.
