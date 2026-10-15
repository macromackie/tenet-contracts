---
name: data-alembic-revision-history
message: Keep one Alembic head, never delete or re-identify a merged revision, and undo applied work with a new revision.
---

## Rules

Apply these rules to Alembic revision files and to the code that runs migrations; changes to other files do not affect them.
A revision is merged once the default branch contains it; review each change against the branch it merges into, where every revision file that already exists is merged.

Set a new revision's `down_revision` to the current head of the default branch, and keep the docstring's `Revises:` line equal to it.
Check the head again after every rebase, and re-parent the revision onto any revision the default branch gained.
When the default branch already has two heads, add a merge revision whose `down_revision` names both.
Keep exactly one head on the default branch, because every path that runs `alembic upgrade head` fails while two exist.

Keep every merged revision file.
Never change a merged revision's `revision` or `down_revision`, including by renaming it to a new identifier.
Stop a merged revision from running by tombstoning it: keep the file and both identifiers, make `upgrade()` and `downgrade()` do nothing, and record why in the docstring.
Do the corrected work in a new revision at the head, written to converge whether or not the tombstoned revision already ran.
Never rewrite a merged revision's work in place, such as a column type, server default, index, or data statement in its `upgrade()`, because databases that recorded it will not run it again.

Write `downgrade()` to reverse the schema change for local development, tests, and deliberate operator rollback.
When `upgrade()` drops data that `downgrade()` cannot restore, restore the structure empty and name the lost data in a comment.
Raise an error naming the lost data only when an empty restore would mislead, such as after a revision that deletes rows without changing the schema.
Leave `downgrade()` empty only in a merge revision or when there is nothing to reverse, and say why in a comment or the docstring.

Undo an applied revision in production with a new revision at the head that reverses it, not with a downgrade.
Keep the migration runner forward-only: it upgrades, does nothing, or fails, and never downgrades on its own.
Treat a manual production downgrade as an operator action that needs the data owner's approval, and tombstone the revision first or the next deploy reapplies it.
Make statements that run before an `autocommit_block()` safe to run again, because entering the block commits them and a retry repeats them.

## Checks

Run `alembic heads` and expect exactly one head, the new revision.
Compare revision files, `revision` values, and `down_revision` values against the merge base, and treat a deleted file or changed identifier as a violation.
Run `upgrade`, `downgrade`, and `upgrade` again for each new revision on a scratch database.
Review each `downgrade()` for a reversal, a named data loss, or a stated reason for being empty.
Review each fix to a merged revision for a tombstone plus a new revision rather than an in-place rewrite.
