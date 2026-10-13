---
name: service-transaction-side-effects
message: Emit best-effort effects after commit, and commit durable delivery intent with the state change.
---

## Rules

Do not call external systems, such as analytics, notifications, queues, or other services, inside a database transaction.
Emit a best-effort effect only after its transaction commits, so a failed commit emits nothing.
Capture the values an effect needs, such as generated identifiers, before the transaction scope closes, and pass them to the effect explicitly.
Do pure preparation, such as token generation and payload building, before the transaction, and move only the external call after it.
Return success to the caller only after the commit.

Write the records a state change owns, such as its events, audit entries, and receipts, in the same transaction as the change.
Classify each effect as best-effort or required; a send after commit is best-effort only.
Commit the intent for a required effect, such as an outbox row or dispatch request, in the same transaction as the state change.
Derive required effects from committed intent, not by polling business records for changes.
Deliver committed intent from a server-side dispatcher that claims work with bounded leases and runs without any client present.
Retry delivery with a stable key derived from the intent, so the receiver never repeats accepted work after a lost acknowledgement.
Mark intent delivered only after the receiver acknowledges it; a send attempt is not delivery.

When an external call must precede the state change, record its intent first as `code-execution-lifecycle` requires, and record its observed result in a following transaction.
If recording that result fails, leave a visible gap; never repeat the external call or report success.

## Checks

Review each external client call in changed code and confirm it sits outside every transaction scope.
Force a commit failure, such as a constraint violation, and confirm no best-effort effect was emitted.
Stop the process between commit and dispatch, restart it, and confirm the required effect is delivered and applied once.
Drop a delivery acknowledgement and confirm the retry reuses the same key without repeating accepted work.
Inject a failure while recording an external call's result, and confirm the call is not repeated and no success is reported.
