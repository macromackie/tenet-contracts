---
name: code-execution-lifecycle
message: Bound work and preserve authoritative results through failure and interruption.
---

## Rules

Give concurrency, deadlines, retries, cancellation, and cleanup explicit owners.
Bound paid and external work across nested operations; give each request exactly one retry owner so that retry layers cannot multiply the intended budget.
Retry known transient failures within that budget, not valid unfavorable results.

Preserve completed work and visible failure states when resuming durable operations.
Define which steps and external effects can repeat after interruption.
Durably record a required external effect's intent and a stable operation identity before starting it, and reconcile an interrupted effect through that identity.
Reject reuse of an operation identity with different inputs.
Never automatically replay an external effect whose outcome is uncertain unless the external system deduplicates it by its operation identity; otherwise reconcile it with that system or surface it for a decision.
When an external system cannot check a precondition and apply an effect atomically, reconcile after the effect and state the remaining race.
Do not claim exactly-once effects without a supporting mechanism.
Surface failures to save authoritative results; never claim work was retained when persistence failed.

A task with external resources must have a cleanup path, owned by its lifecycle, that still runs when its caller fails.
Do not treat cleanup as proof that an external effect was rolled back; keep the effect's record until it is reconciled.

Derive reports and terminal displays from authoritative execution state.
Cosmetic progress and optional diagnostics must not decide success.
Record meaningful transitions and failures at boundaries using consistent identities and bounded, redacted diagnostics; avoid repeated logging through every helper.

## Checks

Trace success, failure, and cancellation through the affected owner.
Check the total request budget, retained results, and resource cleanup, including delegated work.
For recovery changes, exercise the relevant interruption or restart path and inspect saved state.
Interrupt an external effect after its intent is recorded and before its outcome is confirmed, and confirm that recovery reconciles it without applying the effect twice.
Submit a reused operation identity with different inputs and confirm that it is rejected.
Run the existing lifecycle tests; a passing type check does not establish recovery.
