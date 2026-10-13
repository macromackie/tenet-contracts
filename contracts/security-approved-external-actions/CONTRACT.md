---
name: security-approved-external-actions
message: Execute external writes only from an approved, exact, immutable request, once, and never replay uncertain outcomes.
---

## Rules

Keep action executors off the read path, so no read operation or read-only credential can trigger an external write.
Require a current write grant on the target, an enabled action type, and, for programmatic credentials, an action-request permission that is off by default.
Define one executor per reviewed action type, and pin its target account or tenant in configuration.
Validate exact inputs before storing a request, and reject inputs that select another executor, account, or operation.
Restrict each executor to an explicit target set enforced both by the executor and by the provider's own permission policy.

Record each request immutably with its inputs, requester, target, executor configuration revision, reason, origin context, and a caller-generated request ID that serves as its idempotency key; see `service-mutation-idempotency-keys`.
Require approval from an authorized human in a live interactive session, even when the requester holds write grants or an action-capable credential.
Bind approval to the exact request hash and the executor's credential, configuration, and policy revision; any change invalidates the approval.
Show the original requester and origin context during approval, and record the approver separately from the origin.
Expire pending requests after a declared bounded period.

Before execution, recheck the requester's credential and grants and the executor revision, then claim the request atomically so it executes at most once.
Execute with short-lived credentials scoped to the action's target, and never return them to the requester.
Never retry a provider write call automatically, even after a failure that looks transient.
When an executor reads provider state to build a write, send the version it read as a precondition if the provider supports conditional writes.

Record provider acceptance as submitted, and record applied only after confirming the effect.
Record a successful permission-only dry run as checked, distinct from submitted.
Record a definite rejection from the provider as failed.
Record a lost, timed-out, or server-error response and an abandoned claim as uncertain, and require inspecting the provider before a new request.
Persist outcomes with provider request IDs, excluding credentials and provider response bodies.

## Checks

Exercise one action through request, approval, execution, and outcome, then repeat with an expired request, a revoked approver, a changed executor revision, and a second submission.
Drop the provider response and confirm the action becomes uncertain and the provider received exactly one call.
Review each executor for an input that can change its target, account, or operation.
Can any status shown to users claim more than the provider's evidence supports?
