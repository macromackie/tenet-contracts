---
name: code-typescript-module-state
message: Keep no TypeScript state at module level or in a static class field that changes after the module loads, hold each cache in the object or closure that owns it, and give module constants read-only types.
---

## Rules

Never declare state, at module level or in a static class field, that code changes after the module loads, such as a map that requests fill; `code-typescript-const-bindings` already forbids the `let` and `var` bindings that could hold it.
Keep a cache in the object or closure whose lifetime it shares, such as a field of the object that serves the cached repository.
Give each module-level collection or object constant, including those in the constants file that `code-module-file-roles` requires, a read-only type, such as `ReadonlySet<SandboxState>`, or a constant assertion, such as `as const`.
A value that a function creates and changes before it returns is not module state.
Scripts and tests, whose top level `code-script-entry-points` governs, are outside these rules, and the lint exempts them by a declared path pattern.
A server's entry file serves requests, so it is not a script.
Enforce these rules with the repository's lint, and suppress a finding only as `code-lint-suppressions` allows.

Violation: `const tokens = new Map<string, Token>()` at module level, filled by every request that the process serves.
Allowed: `const ENDED: ReadonlySet<SandboxState> = new Set([SandboxState.Stopped, SandboxState.Failed])` at module level, and `readonly #tokens = new Map<Purpose, Token>()` on the object that uses them.

## Checks

Run the repository's lint from the repository root; it reports module-level bindings that change and module-level collections and objects without a read-only type.
For each module-level value or static class field a change adds that the lint passes, such as a value that a factory returns, can code change it after the module loads?
For each cache a change adds, which object or closure owns it, and does the cache end when that owner ends?
Does a change widen the declared script and test path pattern to cover a file that serves requests?
