---
name: release-artifact-provenance
message: Publish only verified bytes from a successful default-branch check, without rebuilding them.
---

## Rules

Publish only artifacts exported by a successful default-branch push check in this repository.
Pull-request, manual, and failed check runs grant no publication authority.
Verify the repository identity, workflow, triggering event, branch, source revision, run, attempt, and successful conclusion before obtaining deployment credentials, and again immediately before external effects.
Authorize publication with immutable repository and owner identifiers; a repository name is not an immutable identity.
Make automatic publication match its triggering event and the current default-branch revision, and skip superseded revisions and attempts.
Re-activate an earlier verified artifact only by explicit recovery selection; rollback does not undo stored data changes.

Seal each exported artifact's complete file inventory with content digests, source identity, revision, run, and attempt.
Download the exact selected run and attempt, and verify the complete inventory and digests before using it.
Reject symlinks, missing files, extra files, changed bytes, and artifacts from another source identity.
Publish and deploy the checked bytes without rebuilding or recompiling them.
Overlay only runtime account identifiers, secrets, and settings onto checked artifacts during deployment.
Verify a package or binary as published by unpacking the archive and exercising its public entry points; a source-level check does not qualify it.
Inspect package contents before publication, and never publish local credentials, local state, private fixtures, or private inputs.

Give published packages explicit exports, exact versions, and an explicitly configured registry visibility.
Keep published versions immutable, and refuse replacement bytes under an existing version.
Update moving pointers such as latest-release manifests and installers only after every artifact in the release passes verification.

Serialize production activation without canceling in-flight deployments.
Keep each component's deployment environment and credentials separate.
Preserve existing secret identifiers, database roles, service names, and storage identities until an explicitly reviewed cutover changes them.
Bind each runtime qualification result to the checked source revision and deployment attempt it covers.
Record publication and post-deployment verification as separate outcomes; a healthy response does not prove authenticated or provider-dependent behavior.

## Checks

Review the check workflow, artifact exporter, release workflow, and publisher together.
Exercise rejection of tampered, extra-file, and wrong-attempt artifacts when changing artifact verification.
Confirm that pull-request and manual check runs cannot reach deployment credentials.
Confirm that an explicit recovery selection publishes an earlier verified artifact without rebuilding it.
After changing activation, verify the published version or deployed revision of each affected component.
