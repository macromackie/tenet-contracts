---
name: data-store-ownership
message: Give each owner of persisted data one store module that alone names, parses, reads, and writes it, behind functions named for records and changes.
---

## Rules

This contract extends `code-ownership-and-boundaries`, which gives each durable fact one owner, to the code that reads and writes persisted data.
Persisted data is data that code writes and later reads back, in the same process or another one, such as database tables, files in a state directory, and keys in a key-value store.
Inputs that code reads but never writes, such as source files, fixtures, and configuration, are not persisted data.
A configurable storage root, such as a state directory's location or a storage binding, is a setting that the settings module of `code-environment-settings` decodes and the store module receives as an input, so the naming rules below cover what lies beneath that root and not the root's location.
These rules govern product source; tests, fixtures, and smoke checks are outside them, and the lint exempts their paths.

Declare one store module for each owner of persisted data, and mark it by its path, such as a `store` folder or a `store` file.
Name each table, stored file, state directory, and storage key only inside its store module.
Declare each stored file, state directory, and storage key name once in the store module, as a named constant such as `RESULTS_FILE`.
Outside the store module, never write a stored name as a literal, open a stored file, query a table, or read or write a key; call the store module's functions instead.
A report, an audit, or a comparison that reads finished data is outside the store module, and calls the store's read functions, such as `readFinishedResults({ run })`.
Parse each kind of stored record in one function of the store module, and never parse that record anywhere else.

Name each store function that code outside the store module calls for the record it reads or the change it writes, such as `listPendingInvoices()` or `markInvoicePaid({ invoice })`.
Never name such a function only for a storage operation, such as `read`, `write`, `put`, or `execute`.
A function that only the store module calls, such as an append-only line writer, may be named for its storage operation.
So may the one exported store function that runs its caller's store calls in one transaction, such as `runInTransaction`.

Configure the repository's lint or a project script to fail on a declared stored name written as a literal outside its store module, and on a key-value storage call outside it.
Suppress a finding only in the form that `code-lint-suppressions` requires.

Violation: an audit command joins `results.jsonl` onto a run directory and parses each line itself, while the run store writes that file.
Allowed: the run store declares `RESULTS_FILE` once and parses the file in `readFinishedResults({ run })`, which the audit calls.

## Checks

From the repository root, run the repository's checks, and confirm that they fail on a declared stored name written as a literal outside its store module in every declared store path.
For each kind of stored record a change touches, how many modules parse or write it?
Does a change read a file, table, or key that a store module owns without calling that store?
Does each store function that a change exposes to other modules name a record or a change rather than a storage operation?
