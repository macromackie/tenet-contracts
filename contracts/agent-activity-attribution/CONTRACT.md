---
name: agent-activity-attribution
message: Attribute activity to individual agents without letting attribution grant access or change outcomes.
---

## Rules

Treat agent runtime, instance, and thread identifiers as attribution only, and take authority from the credential and current grants as `security-resource-access-control` requires.
Never treat matching agent or thread identifiers as proof of ancestry, delegation, or shared ownership between agents or records.
Validate and bound agent context once, at the authenticated boundary, and pass only the validated value inward.
Reject malformed, oversized, or partial agent context at that boundary, such as an instance identifier without its runtime.
Leave a request without agent context unattributed rather than failing it.

Keep an individual agent's identity stable when it continues or resumes the same work.
Give each fork and independent worker its own identity, even when it shares credentials, a thread, or an execution environment with another agent.
Never derive an individual identity from a machine-wide, repository-wide, or shared-session value.
Resolve an agent's identity from explicit per-invocation input first, then the runtime's own per-agent identity, then environment fallbacks.
Supply agent context with each command when workers share an execution environment, instead of through shared environment state.
Generate unique thread identifiers, and fail a creation that collides with an existing thread instead of joining it.

Discover agent activity from authenticated requests without requiring agents to register first.
Record each attributed request's owner, credential reference, validated agent context, route template, method, status, duration, and any action reference.
Never store raw headers, credentials, request inputs, query strings, or provider response bodies in activity records.
Never let a failure to record activity change the business outcome or repeat a provider operation, and record a safe gap diagnostic instead.
Carry an action's originating agent context, which `security-approved-external-actions` records with the request, into its audit record, and never relabel it on retry or duplicate submission.

Label caller-authored notes and progress updates separately from observed requests and authoritative provider outcomes.
Require individual agent context on every caller-authored note.
Never present inactivity, silence, or a successful request as completion of a task.
Store an agent's liveness heartbeat as one overwritten record per agent and thread, and keep it out of activity history and counts.
Show missing and partial attribution as gaps instead of filling them with inferred identities.

Compute activity summaries as `data-metric-definitions` requires for derived metrics.
Count requests separately from the service operations they perform, and keep uncertain action outcomes and unattributed requests in summaries.

## Checks

Send the same request with complete, missing, and partial agent context, and confirm that complete and missing context give the same result while partial context is rejected at the boundary.
Run two workers that share one credential and environment, plus a fork of one, and confirm that each records a distinct identity while a resumed worker keeps its own.
Force activity recording to fail, and confirm that the operation returns its normal result, the provider receives one call, and a gap diagnostic is recorded.
Retry an action request, and confirm that its origin context is unchanged in the request and its audit record.
Inspect stored activity records for headers, credentials, request inputs, query strings, or provider response bodies.
Page through an activity summary, and confirm that its window and totals match the same summary computed without pagination.
Does any access decision read an agent, instance, or thread identifier?
