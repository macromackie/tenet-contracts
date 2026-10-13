---
name: web-write-lifecycle
message: Define each write once, show it saved only on acknowledgment, and retry only when the endpoint makes retries safe.
---

## Rules

Define each persisted write and its cache effects once, in application code beside the resource it changes.
Keep required cache updates in that definition so they still run after the initiating view closes.
Prevent duplicate submissions of the same write while it is pending.
Show pending and error state beside the action that started the write.
Send back unchanged the server fields that the form does not edit.

Show a write as saved only after the server acknowledges it, and show a timeout or lost response as an uncertain outcome, not a rejection.
Mark an optimistic update as pending until acknowledgment, and keep its rollback and reconciliation in the same write definition.
Reconcile the acknowledged response into that resource's cache entry or editor state before refetching, and show the server-normalized values.
Cancel older reads of the resource, or order them after the write, so they cannot overwrite the acknowledged result.
Report a failed follow-up read as a refresh failure, and keep the acknowledged state visible rather than relabeling the write as failed.

Submit the revision or precondition observed when editing began, and do not let a background refresh replace it silently; see `service-optimistic-revision-writes`.
Do not retry a write automatically unless the endpoint makes retries safe, such as by accepting an idempotency key that every retry reuses; see `service-mutation-idempotency-keys`.

Keep a one-time secret returned by a write in the initiating form's state, never in the cache, and clear it when the form closes.

## Checks

Fail the follow-up read after a successful write, and confirm the acknowledged value stays visible with a refresh failure.
Drop a write's response, and confirm the outcome shows as uncertain and is retried automatically only where the endpoint makes retries safe.
Submit the same write twice while the first is pending, and confirm only one request is sent.
Review each write's retry configuration against the endpoint's documented retry safety.
For a write that returns a one-time secret, confirm the secret never enters the cache and that closing and reopening the form clears it.
