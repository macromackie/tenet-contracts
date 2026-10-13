---
name: code-typescript-compiler-strictness
message: Type-check every TypeScript package under strict compiler settings that no file relaxes.
---

## Rules

Enable `strict` and `noUncheckedIndexedAccess` in every package's compiler configuration.
Do not relax those options for a package, directory, or file to make a change compile.
Do not disable type checking for a file with `@ts-nocheck`.
Suppress a single expected error only with `@ts-expect-error` and a reason, never with `@ts-ignore`.
Type-check each package against its own compiler configuration, including its tests and scripts.

## Checks

Run each affected package's type check from its package root.
Confirm each changed compiler configuration still enables `strict` and `noUncheckedIndexedAccess`.
Search the change for `@ts-nocheck`, `@ts-ignore`, and `@ts-expect-error` without a reason.
