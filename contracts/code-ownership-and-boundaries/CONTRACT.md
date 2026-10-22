---
name: code-ownership-and-boundaries
message: Give decisions and state one owner, with explicit dependency direction.
---

## Rules

Give each operation and durable fact one owner.
Keep domain decisions separate from provider transport, storage, and terminal rendering.
Pass explicit inputs and results across those boundaries.
Identify allowed dependencies from the declaration that `code-dependency-boundaries` requires, and public entry points from the nearest package contract.
Import another package only through a declared dependency and its public entry points, never its private modules; keep relative imports inside the owning package.
Consume another repository only through versioned artifacts or explicitly configured endpoints, never through a sibling checkout or an untracked filesystem path.
Keep test fixtures out of production code and builds.

Prefer modules or folders for internal organization.
Add a package for a current ownership, runtime, dependency, or reuse boundary.
Keep cohesive state transitions together.
An abstraction should reduce the decisions and internal knowledge required of its callers; a forwarding layer alone does not establish a useful boundary.

Use the same execution path for equivalent local and deployed behavior; infrastructure adapters may differ.
When replacing a boundary, update consumers, exports, commands, and documentation together.
Account for stored data and active consumers.
Remove superseded paths, options, dependencies, fixtures, and guidance when no current need remains.
Give a necessary temporary path an owner and removal condition.

## Checks

Trace an affected operation from entry point to result.
Identify the owner of each decision and state transition.
Inspect package manifests, public exports, and outside imports together.
Confirm that no import resolves to another package's private module, a sibling checkout, or an untracked path, and that production builds contain no fixtures.
Can a caller use the operation without knowing its private sequencing or repairing its result?
Use the owning workspace's existing checks.
