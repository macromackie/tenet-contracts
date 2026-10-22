---
name: code-typescript-module-boundaries
message: Share code across source folders only through each folder's explicit named-export entry point, and keep imports between files acyclic, type-only and dynamic imports included.
---

## Rules

Give each source folder that other folders import an entry point, `index.ts` unless a tool requires another file name.
Export every value and type the folder shares by name from that entry point.
Do not use default exports or wildcard re-exports in source folders, except where a tool defines the export format, and write a namespace re-export only in an entry point, as `code-typescript-entry-points` allows.
Export a symbol from a folder's entry point only when production code outside the folder uses it.

Import another folder only through its entry point, including type-only imports, re-exports, and dynamic imports.
Treat nested folders as part of their parent's boundary, and expose what an outside consumer needs from a nested folder through the parent's entry point.
Share behavior that several folders need through its own named folder, not by importing another folder's private file.
Keep the import graph between source files acyclic, and count type-only imports, type re-exports, and dynamic imports as edges of that graph.
Break a cycle by moving the declarations both sides need into the module that owns them, as `code-module-file-roles` places types and constants; changing an import to a type-only import does not break a cycle.
Import sibling folders directly from production modules, not through the package's own entry point; tests and examples may use the package entry point to exercise the consumer API.
Keep server-only modules out of entry points that browser code imports.

Enforce the cycle and entry-point rules with a dependency check that resolves each import to a file, never with a pattern over import text.
Configure that check to fail on a cycle through any import, on an import that bypasses an entry point, and on a relative import it cannot resolve.
Suppress a cycle or entry-point finding only as `code-lint-suppressions` allows.

Violation: `orders/totals.ts` adds `import type { Invoice } from '../invoices.ts'` while `invoices.ts` imports `./orders/index.ts`.
Allowed: `Invoice` moves to `billing/types.ts`, and both files import it through `billing/index.ts`, which imports neither of them.

## Checks

Run the repository's dependency check from the workspace root, and confirm that its configuration fails on type-only, re-export, and dynamic-import cycles, on entry-point bypasses, and on unresolved relative imports.
For each change to that configuration, does every one of those rules stay at error for every source folder?
Does a cycle fix move the shared declarations into the module that owns them, not into a forwarding layer that `code-ownership-and-boundaries` rejects?
Review each changed entry point, and confirm every named export has a production consumer outside its folder.
Trace outside imports of a moved file to the entry point that exposes it.
