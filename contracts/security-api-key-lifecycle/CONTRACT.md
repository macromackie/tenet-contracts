---
name: security-api-key-lifecycle
message: Store issued keys as hashes bound to owner, scope, and expiry, revoke them permanently, and fail with distinct unauthenticated errors.
---

## Rules

Generate keys from a cryptographically secure random source.
Store only a hash of each key, with its owner, granted scope, expiry, and revocation state.
Return the key secret once, in the issuance response, and never from metadata, listing, or inspection endpoints.
Bind a purpose-specific key to its purpose, such as uploading invoices for one account, and deny every other operation.
Bind a capability key to its named resource, and recheck its issuer's access and revocation on each use.
Default new and existing keys to no optional grants.

Issue keys only through a live interactive session or an independent proof; an existing key cannot mint, approve, or extend another key.
Persist the requested scope and lifetime with the pending request, display them before approval, and do not let approval change them.
Approve an elevated grant only from a live interactive session of a principal who holds that grant.
Expire unclaimed issuance requests, and deliver an approved key once, bound to the request that asked for it.
Use one issuance, resolution, metadata, revocation, and audit path for every key kind.
Record issuance, elevated grants, and revocation with identifiers only, never the secret.

Give every key an explicit expiry within a declared maximum lifetime, and show the actual expiry after issuance.
Changing issuance defaults never extends existing keys.
Revoke keys permanently; re-enabling an owner, service, or membership never revives them.
Revoke keys derived from an identity, membership, or binding when that source changes or is removed.
Recheck the owner's current eligibility on every authentication, and fail closed when the eligibility source is unavailable.

Reject expired, revoked, and invalid keys as unauthenticated, such as HTTP 401, with distinct error codes that state how to recover.
State the actual expiry in an expired-key error.
Over HTTP, send a `WWW-Authenticate` challenge with every 401, and include the bearer `invalid_token` error only when the request supplied a credential.
Report a failed upstream credential that the server holds with an error other than unauthenticated, so clients keep their valid key.

## Checks

Inspect key storage and confirm it holds no plaintext secret and that each record carries owner, scope, expiry, and revocation state.
Authenticate with expired, revoked, malformed, and absent keys, and compare status, error code, message, and challenge header.
Revoke a key, disable and re-enable its owner, and confirm the key stays invalid.
Attempt to issue or extend a key using only an existing key and confirm refusal.
Change an issuance default and confirm existing expiries are unchanged.
Search logs, audit records, and metadata responses for key secrets.
