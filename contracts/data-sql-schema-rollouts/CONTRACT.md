---
name: data-sql-schema-rollouts
message: Ship schema changes that the previous release and existing rows survive, in batches an interrupted deploy resumes.
---

## Rules

Write every migration for the previous release running against the new schema, during the rollout and after a code rollback.
Ship a migration in the same deploy as the code that uses it only when it is additive: a nullable or defaulted column, a new table, or a new non-unique index.
Do not drop, rename, or narrow a column, table, or type that the previous release reads or writes.
Do not add a `NOT NULL` column without a default while the previous release can insert rows without it.
Set `NOT NULL` only after every running release writes the column and a backfill has filled the existing rows.
Land a destructive change in a later deploy than the code that stopped depending on the old shape.
Rename by expand and contract: add the new column, write both, backfill, switch reads, and drop the old column in a later deploy.

Before adding a constraint or rewriting stored values, count the production rows it would reject or change for each kind of row: nulls, legacy values, duplicates, orphans, and every status.
Record those counts with the change for review.
Handle each kind of row before the statement that would fail on it: fix it, exclude it with a predicate and a comment explaining why, or refuse with an error that names the rows.
Never let a constraint violation be the first report of a kind of row.
Make each data rewrite converge: a second run changes nothing, and rows already in the new shape are left alone.
Match the exact old value in a rewrite, so a value that merely contains it is never changed.

Write bulk data work as a loop that commits each bounded batch and repeats until no rows match, so an interrupted run resumes.
Select only rows the current pass can change, so a batch of rows it cannot fix neither ends the loop early nor repeats forever.
Make every statement that commits before a possible interruption safe to run again.
Keep a statement that cannot be batched, such as one that rewrites a whole table, out of deploy-time migrations, and replace it with a new structure filled by a batched backfill across deploys.
State in each expensive migration why it is safe to run: batched and convergent, or small enough to run at once, with its measured row count.

Test each migration that constrains or rewrites rows on the production database engine, seeded with each counted kind of row, including rows that must not change.
Run a data rewrite twice in that test and assert that the second run changes nothing.

## Checks

For each added migration, ask whether the previous release reads or writes anything it drops, renames, narrows, or makes required.
Confirm the change records production counts for each kind of row a new constraint or rewrite could reject or change.
Run each constraining or rewriting migration on the production database engine with every counted kind of row seeded.
Interrupt a batched migration partway and rerun it; confirm it resumes and converges.
Review each bulk statement for a batched convergent loop or a stated measured row count.
