---
name: security-delegated-credential-vending
message: Mint a capped, expiring, narrowly scoped child credential per request, return it once, and delete it when it ends.
---

## Rules

Vend only credentials minted for one request from a stored parent credential, and never return a stored credential, including the parent.
Give every minted credential an expiry and a spend or rate limit that the provider enforces.
Keep each requested limit and lifetime within a declared, reviewed ceiling for its credential kind, and refuse a request that exceeds it.
Scope each minted credential to the narrowest resource and permission the operation needs, such as read access to one project.
Key any cache of provider-issued tokens by every input that sets their scope, such as the configuration revision, installation, selected resources, and permissions.
Name each minted credential at the provider deterministically from its vend, so the credential can be found without the create response.

Require a reason and a caller-generated request identifier on each vend request, and treat the identifier as the vend's idempotency key under `service-mutation-idempotency-keys`.
Return the existing vend for a replayed request identifier without minting again.
Record each vend's caller, calling credential, parent credential, configuration revision, origin context, limit, and lifetime, excluding secret values.
Check the caller's identity, access to the parent credential, enabled state, and the reviewed ceiling when the request arrives, and again immediately before minting.
Check the caller's declared budgets, such as live credential count and spend per period, before minting.
Mint at most once per vend, and only for the credential that requested it.
When a vend needs approval, mint only after an approval of that exact vend or under a live grant that covers it.
Give each pending vend a declared deadline, and expire it unminted when collection arrives later.
Refuse vends to service and delegated callers unless an explicit grant allows them to vend.

Return the minted value once, in the response that mints it.
Keep the minted value out of stored records, logs, audit records, error messages, approval views, browser storage, and server-rendered pages.
Store only the provider's handle needed to find and delete the minted credential.
Pass a received credential only to the process that uses it, such as through that process's environment, and never print it or write it to a file.

Never retry a provider create whose response was lost; find the credential by its deterministic name and delete it.
Treat a credential the provider reports as already deleted as deleted.
Delete each minted credential at expiry, when its vend is revoked, and when the parent credential or the caller's credential expires or is revoked.
Sweep the provider for credentials named as vends that no live vend record owns, and delete them.

## Checks

Inspect a minted credential at the provider and confirm its expiry, limit, and scope stay within the declared ceiling.
Replay a vend request identifier with identical and with changed inputs, and confirm one minted credential and a conflict.
Revoke the caller's credential between request and collection, and confirm nothing is minted.
Drop the provider's create response, and confirm no second create is sent and the sweep deletes the credential by name.
Expire and revoke a vend, and end its parent and caller credentials, and confirm each minted credential is deleted at the provider.
Search stored records, logs, audit records, errors, and every response except the minting one for the minted value.
