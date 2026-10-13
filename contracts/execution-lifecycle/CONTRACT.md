---
name: execution-lifecycle
message: Bound work and preserve authoritative results through failure and interruption.
---

## Rules

Give concurrency, deadlines, retries, cancellation, and cleanup explicit owners.
Bound paid and external work across nested operations; independent retry layers must not multiply the intended budget.
Retry known transient failures within that budget, not valid unfavorable assessments.
Do not claim exactly-once effects without a supporting mechanism.

Preserve completed work and visible failure states when resuming durable operations.
Define what can repeat after interruption.
Surface failures to save authoritative results; never claim work was retained when persistence failed.
A task with external resources must have a cleanup path owned by its lifecycle.

Derive reports and terminal displays from authoritative execution state.
Cosmetic progress and optional diagnostics must not decide success.
Record meaningful transitions and failures at boundaries using consistent identities and bounded, redacted diagnostics; avoid repeated logging through every helper.

## Checks

Trace success, failure, and cancellation through the affected owner.
Check the total request budget, retained results, and resource cleanup, including delegated work.
For recovery changes, exercise the relevant interruption or restart path and inspect saved state.
Run the existing lifecycle tests; a passing type check does not establish recovery.
