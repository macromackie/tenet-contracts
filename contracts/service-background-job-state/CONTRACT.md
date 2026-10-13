---
name: service-background-job-state
message: Read job state only from its status, allow only declared transitions, and complete on the current attempt's verdict.
---

## Rules

Keep each job's lifecycle state in one status field, and read it only from that field and the timestamps written with it.
Never infer lifecycle state from a result payload, an output file, a linked record, or the job's input.
Declare the allowed status transitions in one place in code, and reject every write outside them.
Make terminal statuses final: no write changes a job's status after it reaches one.
Record a verdict that arrives after a terminal status as a diagnostic, not as a status change.
Retry before a terminal status as a new attempt of the same job; after a terminal status, create a new job that references the finished one.
Write each transition as a conditional update on the current status, so concurrent writers cannot both apply.
Return a stale claim to the waiting status through a declared transition that records its own timestamp.

Write the completion timestamp only in the update that sets a terminal status, and give every other event time its own field.
Give each dispatch attempt an identity, and complete a job only on the verdict of its current attempt.
Ignore verdicts that belong to earlier attempts.
Let required outputs gate completion but never cause it: require the current attempt's verdict, then check the outputs.
Fail a dispatched job whose attempt shows no sign of running after a declared grace period; never complete it from stored outputs.

Reserve the result field for the terminal outcome, and give data that a job gains before then its own field.
Never write the job's input after creation.
Write only the fields a transition owns; never rewrite a whole structured field from an earlier read, which drops other writers' changes.

## Checks

Search changed conditions for lifecycle decisions read from results, outputs, linked records, or input instead of status.
Reconcile a job that was dispatched but has no running attempt yet; confirm it is neither completed nor failed before the grace period ends.
Deliver a verdict from an earlier attempt and a late verdict after a terminal status; confirm neither changes the status.
Review each status write against the declared transitions and confirm it conditions on the current status.
Confirm the completion timestamp is written only together with a terminal status.
