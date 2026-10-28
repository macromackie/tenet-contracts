---
name: code-numeric-literals
message: Give every number except -1, 0, and 1 a named constant that holds one literal, and build each derived constant from other constants' names.
requires-tenet: 0.11.0
---

## Rules

Give every number in code a named constant and refer to the number by that name, so a reader learns what it means and a change edits one declaration.
A named constant is a constant binding or read-only field whose whole value is one number, such as `const MAX_ATTEMPTS = 60` or `readonly maxAttempts = 60`.
A reassignable variable, such as `let maxAttempts = 50`, is not a named constant, and neither is a parameter's default, such as `listInvoices({ maxPages = 50 }: ListInvoicesInput)`.
Only -1, 0, and 1 may stay bare anywhere, in every language, and 2 takes a name like every other number.
A number may also stay bare as an enumeration member's value or as an index into an array or a type, such as `rows[3]`.
A number may also stay bare as a type alias's whole value or a member of its union, such as `type RetryCount = 3 | 5`, which names it.
Elsewhere in a type, such as `{ retryCount: 3 | 5 }`, refer to such an alias instead of the number.
A number may also stay bare as an object property's whole value, in an object literal, a property assignment, or a markup attribute, because the property names it.

Give each constant one literal at most, besides -1, 0, and 1, and compose a derived constant from other constants' names, such as `UPLOAD_CHUNK_BYTES = UPLOAD_CHUNK_MEBIBYTES * BYTES_PER_MEBIBYTE`.
Never write a derived constant as arithmetic on numbers that need a name, such as `5 * 1024 ** 2`, or as its computed value, such as `5242880`.
Name each constant for what its number means, never for its digits, such as `SIXTY`, and carry its unit as `code-measured-value-names` requires.
Put each named constant where `code-module-file-roles` puts named constants.
A number that a declared closed set holds, such as an HTTP status code, takes that set's member as its name under `code-closed-value-sets`.

Test files, matched by a declared path pattern, may write numbers bare, because a test states the exact values it sends and expects.
Exempt generated files and copied third-party source from these rules by a declared path pattern.

Configure the repository's lint to report each bare number outside these exemptions, in every language whose lint offers such a rule, and leave the others to review.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
That file keeps only -1, 0, and 1 bare and matches test files by common folders and suffixes, and a repository may override the test pattern alone.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `if (attempt > 60)` and `const UPLOAD_CHUNK_BYTES = 5 * 1024 ** 2` leave the reader to guess what 60, 5, 1024, and 2 mean.
Allowed: `UPLOAD_CHUNK_MEBIBYTES = 5` and `BYTES_PER_KIBIBYTE = 1024` each hold one number, and `BYTES_PER_MEBIBYTE = BYTES_PER_KIBIBYTE * BYTES_PER_KIBIBYTE` and `UPLOAD_CHUNK_BYTES = UPLOAD_CHUNK_MEBIBYTES * BYTES_PER_MEBIBYTE` compose them.
Allowed: `{ maxAttempts: 60 }` and `type RetryCount = 3 | 5` keep their numbers bare, because the property and the alias name them.

## Checks

Run the repository's lint from the repository root, and confirm that it reports `if (attempt > 60)` in a source file and not in a test file.
For each constant a change derives from other quantities, is it an expression of named constants rather than arithmetic on numbers that need a name, or its computed value?
Does a constant that a change adds take its name from what the number means, rather than from its digits?
Does a change keep a number other than -1, 0, or 1 bare, or widen the test path pattern to files that are not tests?
Does the change give a named constant to each number the lint misses outside these exemptions, such as a markup child, a parse call's radix, or an object key?
