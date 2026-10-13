---
name: security-resource-access-control
message: Authorize every request on the server from current grants; logins, plain links, and caller-supplied facts grant nothing.
---

## Rules

Authorize every request on the server against the principal's current account state, memberships, grants, and revocations.
Deny disabled, unverified, and revoked principals even when their credential is otherwise valid.

A successful login establishes a principal and grants no access; each service authorizes it against its own resources and grants.
A link, shared URL, or reference inside content grants no access by itself to the resource it points to.
Caller-supplied attribution, context, selection identifiers, or capability flags never grant access or prove a relationship between records.
Never derive authority from user-editable or descriptive data such as display names, contact emails, titles, or directory teams.
Grant access through a capability, such as a sharing code, only after validating its stored record, and take its owner and authority from that record, never from values supplied beside it.
Consume a single-use capability atomically with the action it authorizes.

Keep one authoritative grant model per resource kind; do not keep parallel access flags that can disagree with it.
Never let a grant on one resource or scope widen access to another.
Keep the authority to administer grants separate from the authority to read or change the resources they cover.
Give each credential type an explicit capability ceiling; a programmatic credential gains administrative or bypass powers only through an explicit grant.
Authorize a delegated request only when both the human subject and the acting service hold the required grants.
When acting on another principal's behalf, resolve access from that principal's current grants, never the operator's.
Give new resources and migrated records only explicitly declared grants.
Records attached to a private resource inherit its audience, and removing a reader removes access to its history and attachments.

Apply access scope before lookup, search, counting, and pagination, so results and totals never reflect records the principal cannot read.
Check authorization and apply the write it guards atomically, such as in one transaction or one scoped statement.
Resolve a name selector to exactly one permitted resource, or fail and ask the caller to disambiguate.
Never fall back to a more privileged credential or another principal after a denial.
Keep authorization decisions out of shared caches, and never serve a principal-specific response from a cache shared across principals.

Answer a missing or invalid credential as unauthenticated, such as HTTP 401.
Answer a request for a resource the principal may not know exists as not found, such as HTTP 404, with the identical status and body for missing, unpublished, and foreign-owned resources.
Answer forbidden, such as HTTP 403, only when the principal may already know the resource exists, such as a visible resource it may read but not change.
Record administrative grant changes with principal, credential, and target identifiers, excluding secrets.

## Checks

Exercise each changed operation with no credential, an invalid credential, a disabled principal, a principal without the grant, and another owner's principal, and compare statuses and bodies.
Revoke a grant or membership and confirm the next request is denied without a restart or cache expiry.
Does any access decision read login state, a link, an attribution field, a client-supplied capability flag, or user-editable profile data?
Compare the responses for a missing resource and another owner's private resource; can a principal tell them apart?
Check that search results, listing totals, and pagination exclude records the principal cannot read.
Present a capability with a substituted owner, and a single-use capability a second time, and confirm both are refused.
Review administrative, delegated, and service paths for access they inherit without an explicit grant.
