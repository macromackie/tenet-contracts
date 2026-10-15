---
name: test-assertion-integrity
message: Change code to satisfy its tests; never weaken a test to match new behavior or special-case test inputs in production code.
---

## Rules

Apply this contract to tests, expected outputs, snapshots, golden files, and test configuration, and to the production code those tests exercise.
`test-curation` decides which checks to keep and when one may be deleted; this contract protects the meaning of every check that remains.

Change a test's expected outcome only when the same change deliberately changes the requirement that the test checks and records that requirement change in the files it updates, such as documentation, a specification, or a changelog entry.
When the change records no requirement change, these edits weaken a test and violate this contract: replacing an expected value with whatever the new code returns, widening an exact assertion to a type, truthiness, range, or larger tolerance check, and removing an assertion from a test that still runs.
Regenerating snapshots or golden files so that unreviewed output becomes the expectation also violates this contract.
Marking a test skipped, expected to fail, or quarantined because it fails violates this contract.
Catching the assertion failure or the error under test inside the test, or replacing the code a test is named for with a stub, violates this contract.

Never make production code detect that it runs under test, such as by reading a test runner's environment variable or checking whether a test framework is loaded.
Never return a test's expected output from production code for that test's specific input.

Tests may configure production code through its public inputs, such as arguments, injected implementations, or configuration chosen at startup.
A test may be skipped where its behavior cannot exist, such as a file-permission test on a platform without file permissions, when the skip states that reason.
Updating an expected value is allowed when the change records a deliberate change to that behavior, such as a reworded error message that the test asserts.

Violation: a change to invoice rounding also replaces `assert invoice.total == 110.25` with `assert invoice.total > 0`, and no changed file records a new requirement.
Violation: production code returns stored exchange rates whenever an environment variable that the test runner sets is present.
Allowed: a change that rewords `Order not found` to `No order with ID 42` updates the test's expected message and records the new wording in the changelog it edits.

## Checks

For each changed expected value, snapshot, golden file, tolerance, or skip marker, find the requirement change that the change records.
Search changed production code for references to test runners, test environment variables, test framework modules, and fixture values.
Run each test whose assertions changed against the base revision's production code; when it passes there too, confirm that its assertions did not become weaker.
