---
name: code-measured-value-names
message: End the name of every numeric limit, duration, and bound with a declared unit, counted noun, or unitless measure that the repository's lint enforces.
---

## Rules

Include the unit in the name of a limit or duration whose type does not carry it.
Declare a list of unit suffixes, such as `Ms`, `Seconds`, `Bytes`, `Chars`, and `Usd`, and spell each one the same way in every language of the repository, changing only its case, such as `timeoutMs` and `timeout_ms`.
Declare a list of measure words, such as `timeout`, `deadline`, `delay`, `interval`, `limit`, `size`, and `budget`, and a list of counted nouns and unitless measures, such as `Attempts`, `Pages`, and `Ratio`.
Configure the repository's lint to reject a numeric constant, variable, field, class field, parameter, or schema key whose last word is a measure word or whose first word is `max` or `min`, unless its last word is a listed unit, counted noun, or unitless measure, such as `maxAttempts`.
Add to the lists only a unit, a counted noun, or a unitless measure, never a word that names neither, such as `Value` or `Amount`.

A value whose type carries its unit, such as a duration, a date, or a named unit type, needs no suffix.
Convert a value to another unit only into a name that carries the new unit, such as `timeoutMs = timeoutSeconds * MILLISECONDS_PER_SECOND`.
Write a name that another system fixes, such as a library's `timeout` option or a wire field, only in the call or mapping that meets that system, map it there to or from a name or type that carries its unit, and suppress any finding that remains as `code-lint-suppressions` requires, with a reason that names that system.
Keep the external name of a stored or shipped field that the repository owns, as `data-stored-and-shipped-formats` requires, through a serializer rename where one exists and otherwise with a suppressed finding.
Exempt generated files and copied third-party source from these rules by a declared path pattern, and map each limit or duration they carry to a name or type that carries its unit where owned code first reads it.

Violation: `const UPLOAD_LIMIT = UPLOAD_LIMIT_MEBIBYTES * BYTES_PER_MEBIBYTE` is compared with a body's byte length, and its name does not say bytes.
Allowed: `UPLOAD_LIMIT_BYTES`, `timeoutSeconds`, `maxAttempts`, and a `retryDelay` whose type is a duration.

## Checks

Run the repository's lint on the changed files, and confirm it reports no limit, duration, or bound without a listed unit, counted noun, or unitless measure.
For each numeric limit or duration that the lint cannot see, such as one returned by a call, does its name or its type carry its unit?
For each value a change converts to another unit, does the new name carry the new unit, and does the flow keep one unit as `data-and-apis` requires?
Does the change add a list entry that is neither a unit, a counted noun, nor a unitless measure?
For each suppression of this rule that a change adds, does its reason name the system that fixes the name?
