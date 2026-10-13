---
name: security-cli-credential-lifecycle
message: Store CLI credentials owner-only and atomically, bound to their origin, and never print them or accept them as arguments.
---

## Rules

Store only the service's own credential and its metadata, never upstream provider credentials.
Make credential files readable and writable only by their owner.
Replace credential files atomically.
Bind each stored credential to the origin that issued it, and send it only to that origin.
Send credentials only over TLS, except to a loopback address during development.
Reject redirects on authenticated requests.
Do not extract or copy credentials owned by another tool; use that tool's own authenticated interface.

Read secrets from a file or standard input, never from a literal command-line argument.
Apply the same validation and private, atomic storage to imported credentials as to issued ones.
Never print tokens or request headers, including in error and import-failure output.
Print a new credential's metadata, file path, and expiry instead of its secret.
Keep the active login when creating an additional credential.

Show the actual expiry after login, and the server origin and scope in status output.
Explain how to replace saved credentials and automation secrets when a credential is expired, revoked, or invalid.
On logout, revoke the credential on the server before deleting it locally.
Forget a credential locally when the server rejects it as unauthenticated, and retain it after network errors and failed revocations.
Do not claim remote revocation when the server only rejected authentication or when an import replaced local credentials.

## Checks

Inspect the credential file's permissions, and confirm writes go through a temporary file and an atomic rename.
Point a saved credential at another origin and at a redirecting endpoint, and confirm the CLI does not send it.
Run login, key creation, import, and failure paths, and search stdout, stderr, and process arguments for the secret.
Simulate an unauthenticated response, a network error, and a failed revocation during logout, and inspect what remains on disk and what the CLI reports.
Does any command define an argument that takes a secret value?
