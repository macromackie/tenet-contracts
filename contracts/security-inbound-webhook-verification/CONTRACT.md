---
name: security-inbound-webhook-verification
message: Verify each webhook over its raw body, bind it to the expected source, and store it once before processing.
---

## Rules

Verify each delivery's signature over the exact raw request body before parsing or storing it.
Compare signatures in constant time, and reject a delivery whose signature is missing, malformed, or invalid.
When the protocol signs a timestamp, reject deliveries outside a declared replay window.
Bind each delivery to the installation, tenant, account, or channel configured for it before durable acceptance, and reject every other source.
Match the source by the provider's immutable identifiers, never by names or email addresses in the payload.
Drop deliveries outside the configured scope, such as an unselected project, before reading from or writing to the provider.
A valid signature authenticates only the provider; resolve any actor the payload names through your own identity records and current grants, as `security-resource-access-control` requires.

Store each accepted delivery durably before acknowledging it, and process it asynchronously after acknowledgment.
Deduplicate deliveries by the provider's delivery identifier, and acknowledge a duplicate without processing it again.
Keep stored deliveries immutable and separate from the provider state they report, which later deliveries or reads may replace.
Treat delivery as lossy and unordered, and recover missed deliveries through bounded reconciliation with the provider.
Refer to deliveries and verification outcomes by identifier in logs, errors, and audit records, never with raw bodies, signatures, or signing secrets.
Put only record identifiers in interactive messages sent through a provider, and decide each signed callback from your own records, including whether the person who acted may decide.

Hold signing secrets as `security-server-secret-storage` requires, and rotate a signing secret by accepting both the old and new secret only during a declared overlap.

## Checks

Send a delivery whose body changed after signing, one with an invalid signature, and one with a stale timestamp, and confirm each is rejected before parsing and nothing is stored.
Send a correctly signed delivery for an unconfigured installation and one for an out-of-scope resource, and confirm rejection without provider reads.
Redeliver one delivery identifier, and confirm one stored delivery and one processing run.
Fail processing after acknowledgment and restart, and confirm the delivery is processed from storage.
Search logs, errors, and audit records for raw bodies, signatures, and signing secrets.
