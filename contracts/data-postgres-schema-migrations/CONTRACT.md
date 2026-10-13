---
name: data-postgres-schema-migrations
message: Bound every DDL lock wait, build indexes concurrently, validate NOT VALID constraints, and read dependents from the catalog.
---

## Rules

Set a bounded `lock_timeout` for migration DDL, so a blocked statement fails the deploy instead of queuing reads and writes behind it.
Create and drop indexes on tables in use with `CONCURRENTLY`, outside a transaction block.
Raise `lock_timeout` to a bounded value only around a concurrent index build, which waits for older transactions, and restore the previous value even when the build fails.
Rebuild an index that an interrupted concurrent build left invalid, by dropping it concurrently and creating it again or with `REINDEX INDEX CONCURRENTLY`.
Never use `CREATE INDEX CONCURRENTLY IF NOT EXISTS`, which keeps an invalid index in place.
Run `ANALYZE` on a table after creating an expression index on it, because building the index collects no statistics for the expression.

Add a foreign key or check constraint to a populated table as `NOT VALID`, so adding it does not scan the table while holding its lock.
Run `VALIDATE CONSTRAINT` for every `NOT VALID` constraint in a later transaction, such as a following migration or job, or state in the migration why existing rows stay unchecked.
On Postgres 12 or later, set `NOT NULL` on a populated table only after validating a `CHECK (column IS NOT NULL)` constraint, which lets the statement skip its scan, then drop that check.

When a migration drops and re-adds, renames, or replaces a key or constraint, or rewrites values that foreign keys reference, read the dependents from `pg_constraint` when the migration runs.
Include composite keys that contain the column, and move each discovered child column together with the parent value.
Re-add each dropped constraint from `pg_get_constraintdef(oid)`, so it returns unchanged.
Before re-adding a key as `NOT VALID` after moving values, count the child rows that still hold the old value and raise an error naming them if any remain.
Union a hand-written list of dependents that no constraint records, such as derived slugs, with the catalog's set, and never use it in place of that set.
When a migration must name each dependent, compare the named set with the catalog's set before changing anything, and raise an error listing any difference.

Test catalog discovery on Postgres with a dependent the migration does not name, because other engines have no `pg_constraint`.

## Checks

Review each DDL statement on an existing table for the lock it takes and a bounded lock wait.
Confirm each concurrent index build runs outside a transaction block, restores `lock_timeout` on failure, and replaces an invalid index left by a failed attempt.
List each `NOT VALID` constraint the change adds and find its `VALIDATE CONSTRAINT` step or stated reason.
After a migration run, query `pg_index` for indexes with `indisvalid = false` and expect none.
Run each key-changing migration on Postgres with an unnamed dependent seeded, and confirm its rows moved and its key exists again.
