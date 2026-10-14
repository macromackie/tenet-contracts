---
name: llm-code-review-publication
message: Publish automated review results against the reviewed head revision, and approve only on complete, current, clean evidence.
---

## Rules

Associate every published review, comment, approval, and status check with the explicit head revision it reviewed.
Before each publication, recheck the live change's eligibility, base revision, and head revision, and publish nothing as current when any of them differs from what was reviewed.
Keep automated event intake, publication, and approval as separately enabled settings, and recheck the publication and approval settings at each write.
Give the publishing credential write access to reviews, comments, and checks only, never to repository contents.

Approve automatically only when policy enables approval, mandatory checks and requirement coverage are complete, and no current or disputed earlier finding remains.
Never approve from a partial, stale, failed, uncertain, or unsupported review result.
After publishing, recheck the head revision and policy, and withdraw an approval that a newer revision or newer policy has superseded, even for the same head.
When the code host offers no atomic revision check and write, keep each approval bound to its revision and reconcile the race after writing, as `code-execution-lifecycle` requires.
Publishing a report never by itself proves that the review completed or that the change is eligible for approval.

Resolve a finding thread only after verifying the finding's disposition at the reviewed revision, and reopen the thread when that verification becomes stale.
Never treat an author reply or a resolved thread alone as evidence that a finding is fixed.
When the code host denies the capability to resolve threads, keep the verified disposition reply, mark resolution unavailable, and do not block the final review.

Derive status checks from the owned review outcome, never from intermediate progress.
Identify each status check by its external identity, and serialize its writes with the review's other publications so an older in-progress update cannot overwrite a completed check.
Keep check reconciliation pending until the code host confirms the terminal state, independently of whether other deliveries succeeded.
Publish incomplete, blocked, superseded, and uncertain reviews as distinct check states that never read as success.

Give each publication write an operation identity, and reconcile uncertain writes as `code-execution-lifecycle` and `security-approved-external-actions` require.
Treat a missing marker after a timed-out write as uncertainty, never as evidence that writing again is safe.
Reuse an existing review or comment only after verifying its author, marker, payload, and revision.
Recover an accepted publication under its own retained authority after the review's deadline, but refuse recovery for cancelled or failed reviews, obsolete application builds, and superseded revisions.

## Checks

Push a new revision between the pre-publication check and the write, and confirm that the publication names the reviewed revision and any approval is withdrawn.
Drop the response to a successful write, and add another actor's comment that copies the marker, and confirm that the publisher reconciles without a duplicate or a false reuse.
Finish reviews as partial, failed, uncertain, and with a disputed finding, and confirm that none approves and each check shows a non-success state.
Deliver an in-progress check update after the terminal update, and confirm that the terminal state remains.
Reply to a finding as the author without a fix, and confirm that the thread stays unresolved.
Disable approval while publication stays enabled, and confirm that reviews publish without approving.
After deployment, inspect the code host for the exact review, comment, and check identities and their revisions; a health check is not publication evidence.
