---
name: test-curation
message: Treat development tests as disposable, and commit only checks that guard consequential regressions and declared example tests.
requires-tenet: 0.11.0
---

## Rules

Apply this contract to added, changed, and removed tests, fixtures, and test-only dependencies; adopting it does not require deleting an existing suite wholesale.
A change that touches no test, fixture, test report, or test-only dependency leaves this contract unaffected.
Test freely during development with temporary tests, probes, broad cases, and manual checks, and treat their results as development evidence.
Keep temporary tests, probes, fixtures, and test-only dependencies out of every commit, including intermediate commits and commits pushed only to run CI, unless a retained check uses them.
Passing locally or catching the original bug does not by itself justify keeping a test.

Keep example tests as `test-example-suite` requires; they need no guarded regression to be retained and no reason or remaining protection to be deleted, but the rule below against hiding a regression still covers them.
Retain a new automated check only when it guards a concrete, consequential regression that existing checks miss and its outcome is stable and observable.
Consequential regressions include leaked credentials, lost or corrupted data, incorrect charges, repeated paid work, unbounded work, swallowed errors, and broken cancellation, recovery, or publication safety.
Name the guarded regression and the gap in existing coverage in the change description for each retained new check.
Apply the same retention standard to every kind of test; do not keep or reject a test because it is called unit, integration, end-to-end, or smoke.
Test each guarantee at the boundary that owns it, extending an existing representative flow when one reaches that boundary.

Leave structure and conventions to types, linters, contracts, and code review rather than tests.
Do not assert private helpers, internal data shapes, internal call counts, incidental copy, rendered snapshots, or behavior owned by a dependency.
Do not repeat a test per fixture or variant unless the variant changes the guarded behavior.
Keep distinct concerns in separate cases; do not merge unrelated scenarios to reduce the reported test count.
Treat sampled or model-graded scores as measurements, not exact expected values.
Apart from a declared example limit, do not set coverage-percentage targets, test-count targets, or test-count gates.

Removing or skipping a test, case, or assertion deletes the coverage it provided.
Delete existing coverage only for a stated duplicate, a superseded requirement, or behavior explicitly accepted as development-only verification, and name the protection that remains.
Never loosen or delete a check to hide a regression; difficulty, slowness, or an unfavorable result is not a reason to remove it.

Synchronize concurrent tests with explicit gates and bounded cleanup rather than sleeps.
Where the test runner takes a per-test timeout, give every test one as a number literal, only to bound a hung test, never to define expected ordering.
Fix a flaky test's fixture ownership or synchronization instead of raising timeouts, adding retries, or deleting the only protection against a critical failure.
Record live provider checks as separate evidence, and do not present a mocked provider as proof of live provider behavior.
Write temporary test reports and outputs outside tracked source.

## Checks

Inspect each commit, not only the complete diff, for temporary tests, probes, fixtures, reports, and test-only dependencies.
For each retained new check, can the author name the consequential regression, the gap in existing coverage, and why its boundary detects the defect?
For removed or weakened coverage, identify the remaining protection or the explicit acceptance of development-only verification.
Temporarily break the critical behavior a changed check guards, confirm the check fails for that reason, then restore the implementation and remove the probe.
Run the affected tests with the repository's standard test command.
Run the repository's lint and this contract's `assets/` configuration over its test files from the repository root, and confirm they fail on a test that declares no timeout.
