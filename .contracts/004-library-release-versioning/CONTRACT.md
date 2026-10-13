---
name: library-release-versioning
message: Release classified changes as semantic version tags that never discard adopters' edits.
---

## Rules

Publish the library only as `vX.Y.Z` tags, each with a matching changelog section.
Record each change under `## Unreleased` until the release that ships it.
Classify each changed contract or skill as Tightened, Loosened, Clarified, Added, or Removed.
Tightened means code that complied with the previous text can now violate it.
Loosened means code that violated the previous text can now comply.
Clarified means no code changes compliance.
Treat a rename as a removal plus an addition, and name the replacement.
A Tightened or Removed entry makes a major release, an Added or Loosened entry a minor release, and Clarified entries alone a patch release.
State the minimum Tenet version a release needs when it changes.
Never move or delete a published tag.
Never ask adopters to discard local adaptations to take an update.

## Checks

Is every contract and skill changed since the last tag classified in the changelog?
Does the version number match the strongest class in the release?
For each Clarified entry, could any code's compliance change?
Install the release's contracts into a scratch repository with the stated minimum Tenet version and run `tenet validate`.
