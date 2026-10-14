---
name: release-public-source-export
message: Export only allowlisted files from a committed private revision, validated in isolation, without private context or history.
---

## Rules

Export only regular files named in an explicit allowlist; a file's location never makes it public.
Read exported files from a committed source revision, and refuse to export while a listed file has uncommitted changes.
Refuse symlinks, absolute paths, parent-relative paths, and duplicate entries in the allowlist.
Keep private context notes, agent instructions, credentials, environment files, and source history out of the export.
Never export an instruction, context, or agent-tooling folder wholesale; list each public file in it individually.
Refuse to export when a public file contains a name from a declared list of internal names, such as private products, services, and people, using an automated scan that runs before the destination changes.
Refuse to export when a relative link in an exported document points outside the export.

Refuse to export into a destination with uncommitted or untracked changes.
Record a fingerprint of each exported snapshot, and refuse to export when the destination's tracked files differ from the last exported snapshot.
Bring public changes into the private source before the next export, and never delete the export record or force-push to bypass that refusal.
Build and validate the export in a temporary workspace that holds only the exported files, and change the destination only after validation passes.
Make the exported snapshot build and pass its checks without the private repository, its tools, or sibling checkouts.
Refuse to write when the destination's head changed during validation.
Preserve the destination's history, and never overwrite or delete its untracked or ignored files that the export does not list.
Record the source revision with each published snapshot, such as in its commit, release notes, or a manifest.
Keep exporting separate from publishing: the export tool never commits, tags, or pushes, and a person reviews the destination diff before publication.

## Checks

Add an unlisted file, a symlink, and an uncommitted change to a listed file, and confirm the export omits or refuses each.
Edit a tracked file in the destination after the last export, and confirm the next export refuses.
Put an internal name and a link to an unexported path in a public file, and confirm the export refuses before the destination changes.
Run the export's validation, and confirm it builds and checks the snapshot in a temporary workspace without the private repository.
After an export, confirm destination history and ignored files are unchanged, nothing was committed or pushed, and the snapshot records its source revision.
