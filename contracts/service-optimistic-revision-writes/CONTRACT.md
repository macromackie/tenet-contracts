---
name: service-optimistic-revision-writes
message: Write against the expected revision, reject a stale edit whole, and preserve the rejected draft.
---

## Rules

Give each editable record a revision that every accepted write advances.
Use a counter or content version as the revision, not a wall-clock timestamp.
Require every update to name the revision it replaces, and require a create to state that no record exists yet, such as expected revision zero.
Compare the expected revision and apply the write in one atomic step, such as a conditional update or a row lock held through the write.
Return a distinct conflict outcome for a stale revision; never merge the edit silently or let the last writer win.

Treat a record and the children it owns, such as line items or aliases, as one aggregate saved in one transaction at one expected revision.
Reject the entire edit when any part fails, whether from a stale revision, a uniqueness violation, or a child that belongs to another record.
Validate that every child identifier in an edit belongs to the edited record; never move another record's child because its identifier was submitted.
Enforce child ownership and uniqueness with storage constraints as well as in the service.
Leave the stored record and its children unchanged after a rejected edit.

Return the current revision with a conflict, so the client can reload the record and show what changed; `ui-presentation-state` keeps the rejected draft.

Record the actor and time of each accepted revision.
Store accepted revisions as immutable history when earlier versions must stay readable, and apply the record's current access checks to every earlier revision.
Keep a record's identity, creator, and creation time fixed across revisions.
Send writes from imports, background jobs, and other non-interactive paths through the same expected-revision check as interactive edits.

## Checks

Start two edits from the same revision and submit both; expect one acceptance, one conflict, and the accepted edit stored.
Submit an edit whose child change conflicts while its other fields are valid; confirm nothing from the edit was stored.
Submit a stale edit; confirm the conflict response carries the current revision.
Review each update statement: does its condition include the expected revision, or does it read and then write without a lock?
