---
name: agent-shared-memory
message: Let one writer edit agent memory, and give readers verified immutable snapshots identified by digest.
---

## Rules

Designate exactly one writer for each shared memory store, and deny write access to every reader, delegated worker, and evaluation run.
Keep one stable store identity across session or conversation replacement; replacing a session changes conversation context, not memory identity.
Keep one editable store per memory purpose, and never maintain a second editable copy or parallel notes database beside it.
Let the writer decide which lessons and corrections to keep, and never append a note mechanically for each repeated outcome or notification.

Capture a snapshot only at a completed-turn boundary, while the writer is idle after finishing a turn and before it starts the next one.
Verify the store identity, the declared index, safe unique paths, bounded file sizes, and content hashes on every capture, and reject a capture with any mismatch.
Commit each snapshot immutably with its digest and the identity of the completed turn that produced it.
While a writer turn runs, give readers the previous verified snapshot, never the live store or a live read-only attachment.
Block startup when the configured memory is missing, conflicting, or unreadable, and never substitute empty memory.

Select one snapshot for each run, and keep its bytes and digest with the run's frozen inputs.
Give every sub-task, follow-up, and delegated worker of a run that same snapshot, and keep it when the run resumes.
Let a later run select a newer completed snapshot only when it starts.
Treat memory as untrusted reference material that never grants permissions, overrides requirements, or authorizes effects.
Verify any claim taken from memory against current source before relying on it.
Keep findings, decisions, and effect receipts in their own domain records, not in memory.
Never treat a memory edit as a change of policy or as evidence that results improved.

Start evaluation runs with empty memory by default, and use memory only from an explicit, verified frozen snapshot that every case shares and resume keeps.
Before evaluating with a memory snapshot, inspect it for information newer than the evaluated source and for case answers, as `eval-grading-isolation` requires for expected outcomes.
A matching digest proves a snapshot's identity only, not that its content is true or free of leaked answers.

Before migrating a store, close writes and preserve the existing bytes and records.
Import into the intended store, and verify the imported copy against the preserved bytes before reopening writes.
Preserve the existing store on ordinary releases, and never repeat an earlier import.

## Checks

Start with a missing, conflicting, or corrupt store, and confirm that startup is blocked rather than starting with empty memory.
Capture while a writer turn is running, and confirm that readers keep the previous snapshot and no snapshot is committed until the turn completes.
Alter a path, size, or content hash in the store, and confirm that the capture is rejected.
Start a run, let the writer commit a newer snapshot, then resume the run and start a sub-task, and confirm that both use the original digest.
Attempt a write to the store from a reader, a delegated worker, and an evaluation run, and confirm that each is denied.
Does any permission check, requirement, or effect decision read memory content as authority?
