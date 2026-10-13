---
name: data-object-upload-lifecycle
message: Reserve metadata before bytes, publish only after verified storage, and delete only unreferenced objects.
---

## Rules

Keep uploaded bytes in private object storage and their ownership and lifecycle metadata in the application's database.
Reserve an upload record before writing any bytes, keyed by a caller-generated identifier and bound to its owner, declared size, and content digest.
Reject a declared size outside the application's declared bounds before accepting bytes.
Treat the upload identifier as an idempotency key, so an exact retry recovers the same upload and a conflicting retry never replaces stored content; see `service-mutation-idempotency-keys`.
Accept parts of a multi-part upload only from the reserving owner, and require a repeated part to match the stored part's digest.
Verify the declared size and digest over the received bytes before marking storage complete.

Expose metadata, links, and listings for an object only after its storage is complete and verified.
Publish a record's reference to a new object only after the object is stored, under the record's expected revision and an ownership constraint.
Leave the current object referenced and readable when a replacement fails or conflicts.
Keep a pending upload recoverable after an uncertain storage response, including a lost completion, and resolve it by checking storage rather than assuming failure.
Keep derived objects, such as re-encoded images and thumbnails, under the identity and lifecycle of their original, and reuse a stored derivative instead of repeating paid transformation work.

Give pending uploads a declared expiry after which cleanup owns them and aborts any unfinished multi-part storage.
Delete only objects that no published record references; never delete a referenced object.
Serialize cleanup against publication with a lock and a lifecycle check, so an object cannot be published while it is being deleted.
Keep enough metadata to retry cleanup after a partial failure, and let a later run resume it.
Never delete ready, user-visible content because of an inferred expiry.
Delete a ready object so that no record is left pointing at missing bytes, and let a failed deletion be repeated.

Resume an interrupted client upload after the last stored part.
Verify the size and digest of downloaded bytes before reporting a download complete.

## Checks

Lose the storage acknowledgment of an upload, retry it, and confirm the same upload completes once with the declared bytes.
Send bytes whose digest differs from the declaration; expect refusal and nothing published.
Run cleanup concurrently with a publication; confirm the published object and its bytes survive.
Fail a replacement after its bytes are stored; confirm the previous object stays referenced and readable.
Interrupt cleanup and rerun it; confirm it resumes and deletes no referenced object.
Review each deletion path: can it remove bytes that a record still references, or leave a record pointing at missing bytes?
