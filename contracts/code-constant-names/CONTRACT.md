---
name: code-constant-names
message: Name each module-level constant whose value is a number or string written in source in SCREAMING_SNAKE_CASE, such as `STOP_TICK_MS`.
requires-tenet: 0.11.0
---

## Rules

A module-level constant is a binding at a module's top level, exported or not, that code never reassigns, such as a top-level `const`.
Name a module-level constant in SCREAMING_SNAKE_CASE when its value is a number or string written in source, such as `STOP_TICK_MS = 2_000` or `DEFAULT_REGION = 'eu-west-1'`.
Such a value is a literal, a template whose substitutions hold only such values, or an arithmetic or string expression of literals and other such constants.
A wrapper that keeps the value, such as parentheses, a constant assertion, or a type check, leaves the constant's case unchanged, such as `DRAFT_KIND = 'draft' as const`.
Treat exported and unexported constants alike, in source, tests, and scripts.
End such a name with the unit, counted noun, or unitless measure that `code-measured-value-names` requires, spelled in capitals, such as `REQUEST_TIMEOUT_MS` and `MAX_ATTEMPTS`.

A constant inside a function, a block, or a class, including a static or read-only field, is not a module-level constant, such as `readonly maxAttempts = 60`.
This contract sets the case of no other binding.
A module constant whose value is computed, or is not a number or string, keeps the case its language or another contract gives it.
Where a language's compiler or another contract requires SCREAMING_SNAKE_CASE for every constant, whatever its value, as `code-rust-source-structure` does, those constants keep it.

Keep a name that a framework or another system fixes, such as an exported route option that a web framework reads by name.
Suppress its finding as `code-lint-suppressions` requires, with a reason that names that system.
Exempt generated files and copied third-party source from these rules by a declared path pattern.

Configure the repository's lint to report each module-level constant whose case these rules contradict, in every language whose lint can match it, and leave the others to review.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Its rules report a number or string written in source under a name that is not SCREAMING_SNAKE_CASE.

Violation: `const requestTimeoutMs = 35_000` at a module's top level.
Allowed: `const REQUEST_TIMEOUT_MS = 35_000` and `const UPLOAD_CHUNK_BYTES = UPLOAD_CHUNK_MEBIBYTES * BYTES_PER_MEBIBYTE`.

## Checks

Run the repository's lint from the repository root, and confirm it reports a top-level `const requestTimeoutMs = 35_000`.
Is each module-level constant a change adds that only aliases another, such as an imported one, SCREAMING_SNAKE_CASE when their value is a number or string written in source?
Where the lint does not cover a language, does each module-level constant a change adds there whose value is a number or string written in source use SCREAMING_SNAKE_CASE?
For each suppression of these rules that a change adds, does its reason name the framework or system that fixes the name?
Does a change widen the generated or third-party path pattern to cover source that the repository writes?
