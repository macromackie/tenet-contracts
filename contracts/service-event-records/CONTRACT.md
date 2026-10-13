---
name: service-event-records
message: Keep events immutable, source-bound, and typed, with producer-owned retry and consumers that deduplicate by event identity.
---

## Rules

Identify each event by its source, environment, and a producer-supplied unique identifier.
Never edit a stored event; record a correcting event that references it instead.
Treat each event identity as an idempotency key; see `service-mutation-idempotency-keys`.
Commit a batch of events and their related references atomically, and acknowledge the batch only after the commit.
Make the producer own durable retry of unacknowledged events, resending their original identities and contents.
Deliver events at least once, and make consumers deduplicate by event identity.

Bind each publishing credential to one source, one environment, and its registered event types.
Keep publishing and reading separate: a publishing credential cannot read events, and a reading credential cannot publish them.
Use events to record occurrences only; an event never changes business state or replaces the authoritative record of an operation.

Register every event type with a version and a validator for its properties, and reject unknown types, versions, and properties.
Store identity, type, version, occurrence time, actor, subject, and correlation as typed, indexed fields rather than inside the payload.
Record additional references to other objects as typed rows beside the event, not as identifiers inside the payload.
Keep event-specific properties in a payload validated by the type's versioned schema, and promote a payload dimension to a typed field or rollup when a measured query needs it, not through a catch-all index.
Keep occurrence time separate from ingestion time.
Never synthesize an event or an occurrence time the producer did not record; a missing event stays a gap.
Exclude credentials, request and response bodies, prompts, and user-authored content from event properties, and reference large content by identifier.

Bound event reads by time window, result size, and deadline, and keep the window and filters fixed across pages.
Map source identities to stable destination identities when exporting, and preserve each event's identity and occurrence time on replay.
Export only properties on an explicit allowlist.

## Checks

Replay a batch with identical identities and contents; expect the existing receipts and no new events.
Inject a failure during a batch commit; confirm no event from the batch is readable and the producer still holds the batch for retry.
Publish with a credential bound to another source, or with an unregistered type; expect rejection.
Review each new event type for a version, a property validator, typed query fields, and excluded secrets and content.
Replay an export and confirm destination identities and occurrence times are unchanged.
