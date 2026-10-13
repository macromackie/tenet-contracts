---
name: service-mutation-idempotency-keys
message: Commit a caller-generated key's receipt with the mutation, return it on exact retries, and reject conflicting reuse.
---

## Rules

Accept a caller-generated idempotency key, such as a UUID, on every mutation a client may retry.
Generate the key once per intended operation, persist or show it before the first attempt, and reuse it on every retry of that operation.
Derive keys for server-to-server retries from the durable operation's identity, never from the attempt.

Scope each key to the authenticated principal, and bind it to the operation and a fingerprint of the canonical request content.
Commit the receipt with the mutation in one transaction, covering every record of a batch.
Enforce key uniqueness per principal in storage, so concurrent first attempts produce one mutation.
Look up the key before resolving mutable defaults or current selections, so a retry matches the original request rather than current state.
Look up the key before checking an expected revision, so a retry of an accepted update returns the accepted revision instead of a conflict; see `service-optimistic-revision-writes`.

Return the original receipt on an exact retry without repeating effects.
Reject reuse of a principal's key with a different operation or content as a conflict, and leave accepted work unchanged.
Never let a retry relabel the original request's context, reason, or attribution.
Declare how long receipts remain retrievable, and never extend that window on retry.

## Checks

Send one mutation twice with the same key and confirm one effect and identical receipts.
Reuse a key with changed content or another operation, and confirm a conflict with stored state unchanged.
Send the same key from another principal and confirm it neither reads nor changes the first principal's receipt.
Send two concurrent first attempts with one key and confirm a single mutation.
Drop the response after commit, retry, and confirm the client recovers the original receipt.
Retry an accepted revision-checked update and confirm it returns the accepted revision.
