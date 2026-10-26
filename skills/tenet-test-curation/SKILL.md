---
name: tenet-test-curation
description: Write, review, or slim tests and evals, especially before committing a feature or refactor.
license: MIT
---

# Test curation

Investigate broadly during development. Commit the smallest durable suite that protects important behavior, plus any
declared example tests.

## While developing

Use temporary tests, detailed assertions, probes, live evals, terminal recordings, and manual browser checks freely.
Before a risky refactor, characterize the behavior you need to preserve. Keep exploratory work local until you know
which checks deserve ongoing maintenance. Manual verification is useful evidence; record what you actually observed.

## Before committing

For each retained test or eval case other than a declared example test, name the consequential failure, the gap in
existing coverage, and the smallest clear protection. Consider fixtures, setup, dependencies, runtime, and failure
diagnosis together. Prefer extending an existing representative flow when it covers the gap clearly; keep a separate
case when it exposes a distinct failure. Explore combinations temporarily rather than retaining every variation
encountered during development.

Remove duplicated coverage and assertions about incidental wording, formatting, helper calls, or private data shapes.
Test a guarantee at its owning boundary; repeat it at integration level only when the wiring can fail independently.
Use explicit synchronization for concurrency tests. A timeout bounds a hung test; it should not define expected timing.

Do not optimize a test count or combine unrelated scenarios into one large test. Keep only assertions needed to tell
whether the important result is correct. Types and clear implementation can carry straightforward structure.

Before deleting a meaningful check, identify duplicate protection, a superseded requirement, or why development-only
verification is sufficient. A slow or failing case alone is not grounds for removal. Never conceal a regression.
For critical coverage you change, temporarily break the protected behavior, see the check fail, then restore the code.

Remove temporary harnesses and generated artifacts before committing. Preserve useful reports outside tracked source
and summarize local verification in the delivery notes. A recorded live run is evidence, not a permanent guarantee.

## Evals

Use the repository's eval guidance, when available, for fixture selection, grader audits, and controlled comparisons.
Keep the existing runner and fixture format. Use deterministic offline checks for budgets, validation, state transitions,
and reports; small model comparisons for semantic decisions; full reviewer evals for the combined workflow. A lower
layer cannot establish the higher layer's quality. Run repository-required validation for judgment changes.

Pair a meaningful failure with a valid counterpart when overflagging is plausible. Keep expectations outside assessed
inputs and include relevant expected-clean outcomes. Model variation is a measurement, not flaky deterministic behavior:
do not assert exact confidence, retry until green, or trim difficult cases to improve scores.

## Examples

- [Rust](references/rust.md): assert decisions and protocol behavior without locking down presentation.
- [TypeScript](references/typescript.md): test completed UI behavior and asynchronous ownership.

Run the checks required by the repository instructions. Explain removed coverage and any accepted limitation.
