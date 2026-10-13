---
name: security-oauth-authorization-server
message: Issue audience-bound tokens through PKCE, and never let a login confer authorization.
---

## Rules

Use the authorization-code flow with PKCE and the `S256` challenge method for every client that signs in a user, and disable the implicit and password grants.
Register server-side browser applications as confidential clients with individually hashed secrets.
Register each public client explicitly for its own consumer; it cannot reuse a confidential client's registration.
Register first-party clients from validated, checked-in configuration, and disable clients omitted from it when reconciling.
Keep dynamic client registration disabled unless a reviewed configuration enables it.
Compare redirect URIs with their registered values by exact string match, allowing only the port of a native client's loopback redirect to vary.
Give each application a distinct resource audience.

Issue short-lived access tokens with a declared lifetime.
Give central sessions and refresh credentials a declared lifetime that only their use extends.
Rotate a public client's refresh credential on every use unless it is sender-constrained, and revoke the rotated family when a used credential is presented again.
Verify issuer, audience, expiry, signature with an expected algorithm, token type, and required identity claims before trusting a token.
Keep logout and revocation effective for the full lifetime of sessions and refresh credentials.
Expose session introspection only to registered services, and check the token's client and the live session before returning identity data.
Rate-limit login and token endpoints with counters that survive restarts.

Never link an external identity to an existing account implicitly.
Link an external identity to an existing account only from a session already signed in to that account, or from a pre-approved record that matches a provider-verified email.
Key each linked external identity by provider and the provider's stable subject identifier, never by email, and enforce that key's uniqueness with a storage constraint.
Never infer a verified email from upstream profile data that does not assert verification.
Version identity bindings so dependent credentials detect a changed binding, and do not advance the version when nothing changed.
Keep application permissions out of identity records and directory bindings; each application authorizes from its own grants, as `security-resource-access-control` requires.

## Checks

Attempt authorization without PKCE, with the `plain` challenge method, with an inexact redirect URI, and with another client's credentials, and confirm refusal.
Present tokens with the wrong audience, issuer, type, signature, or algorithm, or past expiry, to a consuming service and confirm rejection.
Revoke a session and confirm refresh and introspection fail before its lifetime ends.
Present a public client's already rotated refresh credential and confirm it and its successors are revoked.
Remove a client from configuration, reconcile, and confirm it can no longer authorize.
Review every account-linking path for a link established from unverified or user-editable data.
