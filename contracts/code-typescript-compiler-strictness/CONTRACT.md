---
name: code-typescript-compiler-strictness
message: Type-check every TypeScript package under strict compiler settings that no file relaxes.
requires-tenet: 0.11.0
---

## Rules

Make every package's compiler configuration extend the one that `code-lint-strictness` ships, directly or through a base it extends, so every option that file sets applies.
Under `exactOptionalPropertyTypes`, an argument field declared `dueAt?: Date` may be left out, but a caller can never set it to `undefined`.
Without it, `dueAt?: Date` also admits an explicit `undefined`, which an `in` test still sees and which overwrites a default when spread over it.
Under `verbatimModuleSyntax`, an `import type` statement disappears and every other import statement loads its module, so the source shows each import's runtime effect.
Type stripping needs that, because it removes only imports marked `type`, and an unmarked type-only import would fail when the module loads.
Do not relax any of those options for a package, directory, or file to make a change compile.
Do not disable type checking for a file with `@ts-nocheck`.
Suppress a single expected error only with `@ts-expect-error` and a reason, never with `@ts-ignore`.
Type-check each package against its own compiler configuration, including its tests and scripts.

Configure the repository's lint to reject `@ts-nocheck`, `@ts-ignore`, and `@ts-expect-error` without a reason.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.

Violation: a package's compiler configuration enables `strict` and `noUncheckedIndexedAccess` but extends no shipped configuration, so `exactOptionalPropertyTypes` and `verbatimModuleSyntax` stay off.
Violation: a test folder's configuration disables `exactOptionalPropertyTypes`, which the package's configuration sets.
Allowed: every package's configuration extends a base that extends the shipped compiler configuration first, and the test leaves out `dueAt` for an invoice with no due date.

## Checks

Run each affected package's type check from its package root.
For each compiler configuration a change adds or edits, does the compiler's `--showConfig` output set every option that the shipped compiler configuration of `code-lint-strictness` sets?
Run the repository's lint from the repository root, and confirm that it rejects `@ts-nocheck`, `@ts-ignore`, and `@ts-expect-error` without a reason.
