---
name: data-record-identifiers
message: Give each new record a random UUID, derive an id only where a retry or rebuild must reproduce it, build each derived kind in one named function, and never parse an id.
---

## Rules

Identify each new record, job, or effect by a random UUID, generated where it is created or by the caller that requests it.
Derive an id where a retry or a rebuild must produce the same id again, such as an effect that a retried job must find by id or a row rebuilt from another system's records, and where equal content must share one id, such as a digest of a request's inputs.
Build a derived id from facts that every attempt reads unchanged, or generate it once and store it before the first attempt, never from a value that differs between attempts, such as the current time, a counter held in memory, or a random value generated on each attempt.
Derive no other id.
Build each kind of derived id in one named function that takes its parts as named fields, such as `refundEffectId({ invoice })`, and build that kind nowhere else.
When code stores a record under a derived id, store each of the id's parts in its own field of that record, and read a part from that field.
An id that code sends to another system, such as an idempotency key, needs no stored parts there.
Never recover a part from an id or branch on its format, such as by splitting it on a separator, taking a substring, matching a pattern, or comparing a prefix.
Validating an id's characters and length where it enters the system is allowed.
Compare or look up an id only as a whole value.

Violation: `const invoice = effectId.split(':')[0]` recovers the invoice from an effect id.
Allowed: a retried job must find its refund effect by id, so `refundEffectId({ invoice })` builds that id, and the effect row stores `invoice` in its own field.

## Checks

For each id a change creates, is it a random UUID, or does a named retry, rebuild, or content match need to produce the same id again?
For each effect that a retry repeats, does every attempt use the same id?
For each kind of derived id, does exactly one named function build it, and does every record that holds it store its parts in their own fields?
Search the change for splitting, substrings, pattern matches, and prefix comparisons applied to an id.
