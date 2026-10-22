---
name: code-shared-definitions
message: Declare each pattern, bound, and derivation that several modules must agree on once, and import it everywhere else.
---

## Rules

A shared definition is a value that two modules must keep equal, such as a validation pattern, a numeric bound, a key derivation, or a path layout.
Closed value sets follow `code-closed-value-sets`, domain-free helpers follow `code-shared-utilities`, derived record ids follow `data-record-identifiers`, copied code blocks follow `code-duplicated-blocks`, and code that another repository holds without publishing it follows `code-cross-repository-copies`.
Declare each shared definition once, in the module or package that owns the concept, and import it everywhere it is used, including from a dependency's published entry point.
Build a narrower or combined definition from the imported one, such as by picking fields from an imported schema or tightening an imported bound.
Never write a shared definition again by hand, whether as the same literal or as the same bound inside another schema.
A comment that says a block works the same way as, matches, or mirrors another module of the same repository marks a copy of a shared definition.

Declare a minimum pattern length, and fail checks when a pattern literal at or above it, such as a regular expression, appears in two or more non-test source files of one repository.
Skip only generated files, build output, and copied third-party source, each by a declared path pattern.
A definition that only one module reads is not shared, and neither is a value that equals another by chance and changes independently of it, such as a host-name rule that matches an installation-name rule today.
A migration, and a reader that `data-stored-and-shipped-formats` freezes for an earlier stored version, keeps the literal it was written with, because it must not change when the shared definition changes.
Suppress a repeated-pattern finding only as `code-lint-suppressions` requires, and only on a literal that equals another by chance or that a migration or frozen reader keeps.

Violation: a scheduler imports the runtime package's `Engine` schema but re-declares its `cpu` and `memoryMiB` bounds by hand.
Allowed: the scheduler reads the resource bounds from the runtime package's published definition schema, and declares its own tighter ceiling from the imported bound.

## Checks

From the repository root, run the repository's checks, and confirm that they fail when one pattern literal appears in two non-test source files.
For each pattern, bound, or derivation a change adds, does an imported package or another module of the repository already declare it?
For each suppression of a repeated-pattern finding, does the suppressed literal change independently of the value it equals, or sit in a migration or frozen reader that keeps it?
