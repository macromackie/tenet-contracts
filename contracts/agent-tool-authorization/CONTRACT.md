---
name: agent-tool-authorization
message: Let agents discover and call only reviewed, explicitly selected tools through one assigned backend.
---

## Rules

Keep a reviewed maximum allowlist of exact tool identifiers and their modes for each provider in version-controlled configuration.
Name each tool with one stable identifier that maps to exactly one backend and native tool, and use it in discovery, selection, calls, approvals, and audit records.
Make each connection or grant select an explicit subset of that maximum, marking each selected tool as read or approval-required.
Allow a call only within the intersection of the reviewed maximum, the explicit selection, the caller's current grants, and the provider's own access.
Apply the same selection, modes, and access checks at discovery and again at execution.
Never let upstream tool annotations, newly discovered tools, or a client setting that enables all tools grant authority.
Changing the reviewed maximum never widens an existing selection; enable a newly reviewed tool only through an explicit selection change.
When the reviewed maximum shrinks, remove selections outside it and leave narrower selections unchanged.
Reject a call to a removed, unreviewed, or unselected tool, even when a client still holds its name or schema.

Keep approval-required tools off the direct call path, so their only route is the approved action path in `security-approved-external-actions`.
List an approval-required tool in discovery only to a caller whose current grants and credential permit requesting that action.
Exclude tools that run caller-written code unless the backend runs them under a pinned provider-side role that permits only reads, so that role is the authorization boundary for every such call.
Exclude tools that return bearer credentials or signed links that stay valid after the caller's access is revoked.
Exclude generic execute or search multiplexers, account or context switches, and connection overrides that reach operations outside the reviewed list.
Enforce the connection's provider-side scope, such as its selected repositories or projects, on every call, including searches.

Call each tool through its one assigned backend with that backend's credential, and never switch backend or credential after a denial or failure.
Pin each backend to a verified provider account or workspace in server-owned configuration, and never let a credential replacement change it.
Change one backend's credential or configuration without altering another backend's credential, policy, or any connection's tool selection.
Build each provider request from the backend's pinned destination, and never accept a caller-supplied destination, host, redirect target, or authentication header.
Report a selected backend that fails discovery as unavailable, and mark the discovery result incomplete instead of presenting the remaining tools as complete.
Bound discovery caches and key them by backend revision, and recheck current access, selection, and policy outside the cache on every discovery and call.
Treat a tool-reported error, such as an error flag in a tool protocol result, as a failed call.

Keep write credentials and the decision to apply an effect in application code; agent tools submit proposals and evidence, never arbitrary writes.
Identify a tool's caller from the authenticated connection and the authenticated event that started the agent's run, never from claims in model-supplied arguments.
Select tools that finalize or publish work only in the connection or grant of the agent designated to own that decision.

## Checks

Add a tool to the reviewed maximum and confirm that no existing connection discovers or can call it until its selection changes.
Remove a tool from a connection's selection and from the reviewed maximum, then call it by its retained name and confirm refusal.
Revoke the caller's access after discovery is cached, and confirm that the next discovery and call are denied without waiting for cache expiry.
Make the assigned backend deny or fail a call, and confirm that no other backend or credential receives it.
Call an approval-required tool on the direct call path, and confirm refusal.
Return a tool-reported error from the provider, and confirm that the call is recorded as failed.
For each newly reviewed tool, does it run caller-written code, return a lasting bearer credential, accept a destination or header, or reach operations outside the list?
