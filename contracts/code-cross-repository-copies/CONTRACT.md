---
name: code-cross-repository-copies
message: Keep each file that several repositories use in one source repository, and consume it from a release or as a locked copy whose hash checks verify.
---

## Rules

Keep each file or block that two repositories both use, such as a base compiler or lint configuration, a deploy helper, an export tool, a task file, a check workflow, or agent guidance, in one source repository.
Consume it from a release that the source repository publishes, as `code-ownership-and-boundaries` requires for any other repository.
Where the consumer's format can extend a published file, such as a compiler or lint configuration, extend the released file and keep no copy.
Where the format cannot extend a published file, such as agent guidance or a check workflow, keep a copy of a released revision listed in a committed lock with its path in the consumer, source repository, source path, revision, and content hash.
Fail checks when a listed copy's content hash differs from its lock entry.
Change a listed copy only by copying a newer released revision and updating its lock entry in the same commit.
Keep consumer-specific values, such as a list of private names, in the consumer's own settings file, so that the shared file stays identical in every consumer.
A comment that says a block matches, mirrors, or works the same way as code in another repository marks a copy.

A file that a tool generates in each repository from that repository's own settings, such as a release workflow, is not a copy.
An installed contract follows `contract-maintenance` and the lock its installer keeps, not this contract.
A snapshot that a public source export writes into its destination follows `release-public-source-export`, not this contract.
A value that a declared dependency already exports, such as a validation pattern or a bound, follows `code-shared-definitions`.

Violation: a second repository copies the first repository's export tool and edits the private-name list inside the copy.
Violation: a consumer appends rules about itself to its copy of shared agent guidance and replaces the lock entry's hash while its revision stays the same.
Allowed: both repositories run the export tool from the first repository's release, and each keeps its private-name list in its own settings file.

## Checks

From the repository root, run the repository's checks, and confirm that they fail when a listed copy differs from its locked hash.
Does the change add a file or block that a comment, a header, or its content marks as copied from another repository, without a release dependency or a lock entry?
For each listed copy the change edits, does its lock entry move to a newer released revision, and does the copy match that revision with no other edit?
