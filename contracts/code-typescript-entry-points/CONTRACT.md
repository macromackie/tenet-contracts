---
name: code-typescript-entry-points
message: Keep each TypeScript entry point a list of named re-exports from the files that declare them, re-export from no other file, and never add a file named after a sibling folder.
---

## Rules

This contract extends `code-typescript-module-boundaries` and `code-typescript-package-boundaries`, which define a folder's and a package's entry points.
An entry point is a folder's index module, such as `index.ts` or `index.tsx`, or a source file that the package manifest's exports map lists, by its own path or by its own build output.
Re-export only from an entry point.
Give an entry point only named re-exports, written as `export { name } from './file.ts'`, `export type { Name } from './types.ts'`, or `export * as Uuid from './uuid.ts'` for a file whose exports callers use under one name, and comments.
Give a namespace re-export the PascalCase form of its file's stem, such as `Uuid` for `uuid.ts` or `OrderStatus` for `order-status.ts`, and leave the namespace's word out of each name inside that file, such as `generate` and `validate` for `Uuid.generate` and `Uuid.validate`.
Never export an object that code uses only to call its functions by fixed property names, such as `export const uuidModule = { generate, validate } as const`.
This holds whether the object defines the functions inline or gathers them; export the functions from their file and re-export that file under a namespace instead.
An object that code indexes with a computed key, such as `exporters[format]`, or passes as an implementation of an interface type, such as a `Logger`, is not such an object, and neither is the object that a factory function returns with functions that close over its dependencies, such as `createInvoiceStore({ sql })` returning `{ settleInvoice }`.
Importing a name and exporting it again is a re-export, so write it as `export { name } from` its source.
Keep every other statement out of an entry point, including a registry, a lookup table, or one object assembled from the folder's files.
Declare each value and type that an entry point shares in the file that `code-module-file-roles` assigns it and `code-typescript-file-names` names, such as `schemas.ts` for a schema or `exporters.ts` for an `exporters` record.
Re-export a symbol of the entry point's own folder, nested folders included, from the file that declares it or from a nested folder's own entry point; `code-typescript-module-boundaries` governs symbols of other folders.
Never add a file named after a sibling folder, such as `invoice-export.ts` beside `invoice-export/`, whether it serves as that folder's entry point or as a separate module.
A file whose exports a runtime or framework loads, or whose declarations a compiler accepts only in that file, such as a server's main module, a page route, or a style-variables file, is not an entry point under these rules, and may declare and re-export what that tool requires in the format that `code-typescript-package-boundaries` preserves.
Exempt generated files and copied third-party source that no exports map lists from these rules by a declared path pattern, but never an index module that a tool writes from its own folder's hand-written files.
Enforce these rules with the repository's checks, and suppress a finding only as `code-lint-suppressions` allows.

Violation: `invoice-export/index.ts` imports three exporters and declares the `exporters` record from them.
Violation: `uuid/uuid.ts` declares `export const uuidModule = { generate: generateUuid, validate: validateUuid } as const;`.
Allowed: `invoice-export/exporters.ts` declares the `exporters` record, and `invoice-export/index.ts` holds only `export { exporters } from './exporters.ts';`.
Allowed: `uuid/uuid.ts` exports `generate` and `validate`, `uuid/index.ts` holds only `export * as Uuid from './uuid.ts';`, and callers write `Uuid.generate()`.

## Checks

Run the repository's checks from the repository root, and confirm that they fail on default exports, wildcard re-exports, namespace re-exports outside entry points, import-then-export, declarations in entry points, re-exports outside entry points, and files named after a sibling folder.
Confirm that the checks treat every source file of each exports map, named by its exact path, as an entry point, and exempt only the files that a runtime, framework, or compiler requires and the generated files and copied third-party source that no exports map lists.
For each file a change exempts as runtime-loaded or compiler-required, does a runtime or framework load it or a compiler accept its declarations only there, and does it export only what that tool requires?
For each object a change exports, does code index it with a computed key, pass it as an implementation of an interface type, or receive it from a factory whose functions close over dependencies, or does code only call its functions by fixed property names?
For each namespace re-export a change adds, is the namespace the PascalCase form of its file's stem?
Does a change turn an entry-point rule off, lower its severity, or narrow the files it covers?
