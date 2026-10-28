---
name: code-typescript-module-state
message: Keep no TypeScript module state that changes after loading, hold each cache in its owner, end module-level literals with `as const`, and type module-level sets and maps read-only.
requires-tenet: 0.11.0
---

## Rules

Never declare state, at module level or in a static class field, that code changes after the module loads, such as a map that requests fill; `code-typescript-const-bindings` already forbids the `let` and `var` bindings that could hold it.
Keep a cache in the object or closure whose lifetime it shares, such as a field of the object that serves the cached repository.
A value that a function creates and changes before it returns is not module state.

End each module-level object or array literal with a constant assertion, `as const`, whether or not the module exports it, including in the constants file that `code-module-file-roles` requires.
When the literal must match a declared type, follow the assertion with `satisfies` and that type, such as `{ ... } as const satisfies Record<OrderStatus, string>`.
Never annotate the constant that holds a module-level literal, because an annotation such as `Record<OrderStatus, string>` replaces the read-only literal type with a type that code may change.
Write each array type after `satisfies` read-only, as `code-typescript-input-immutability` requires.
A mutable one there, even inside a type argument such as `Record<OrderStatus, Role[]>`, makes the asserted array mutable.
Never wrap a module-level literal in `Object.freeze`, which makes only its top level read-only; end the literal with `as const` instead.
A primitive constant, such as `const MAX_ATTEMPTS = 3`, already has a read-only literal type and needs neither form.
A constant whose value a call returns, such as a schema or a builder's result, takes its function's declared type, and that call's literal arguments need no assertion.

Annotate each module-level `Set` or `Map` constant as `ReadonlySet<T>` or `ReadonlyMap<K, V>`, such as `const endedStates: ReadonlySet<SandboxState> = new Set([...])`.
Neither `as const` nor `satisfies` makes a collection read-only, so a collection takes the annotation that a literal never takes.

A module constant keeps its literal types, and a comparison with a computed value, such as `attempt >= backoff.maxAttempts`, needs no wider type.
Where code needs a wider type, such as an array that later holds other sizes, annotate where the value is read, such as `const sizes: number[] = [defaults.pageSize]`.
When a dependency's parameter requires a mutable array, pass it a copy, as `code-typescript-input-immutability` requires.

Scripts and tests, whose top level `code-script-entry-points` governs, are outside these rules, and the lint exempts them by a declared path pattern.
A server's entry file serves requests, so it is not a script.
Enforce these rules with the repository's lint, and configure it to report each module-level literal without `as const` and each module-level set or map without a read-only annotation.
Configure it also to report each such literal's annotation and a literal inside `Object.freeze`.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Its path patterns, which a repository may override, exempt scripts and tests by common folders and suffixes.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `const tokens = new Map<string, Token>()` at module level, filled by every request that the process serves.
Violation: `export const statusLabels: Record<OrderStatus, string> = { ... }` annotates a module-level literal, so code may reassign its labels.
Allowed: `export const statusLabels = { ... } as const satisfies Record<OrderStatus, string>` and `const endedStates: ReadonlySet<SandboxState> = new Set([SandboxState.Stopped, SandboxState.Failed])` at module level.
Allowed: `readonly #tokens = new Map<Purpose, Token>()` on the object that uses them.

## Checks

Run the repository's lint from the repository root, and confirm that it reports a module-level literal without `as const`, an annotated module-level literal, and a module-level `Set` without `ReadonlySet`.
For each module-level value or static class field a change adds that the lint passes, such as a value that a factory returns, can code change it after the module loads?
For each cache a change adds, which object or closure owns it, and does the cache end when that owner ends?
For each wider type a change writes for a module constant's value, is it stated where the value is read rather than on the constant or through an assertion?
Does a change widen the declared script and test path pattern to cover a file that serves requests?
