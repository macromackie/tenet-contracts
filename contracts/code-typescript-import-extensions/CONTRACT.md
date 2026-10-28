---
name: code-typescript-import-extensions
message: Name the imported file in each relative TypeScript import by its own name and extension, such as `./harness.ts`, never a bare path, a folder, or the emitted `.js` name.
requires-tenet: 0.11.0
---

## Rules

This contract extends `code-typescript-compiler-strictness`, which type-checks every package, and covers every TypeScript file, including tests and scripts.
It governs the specifier of each import, re-export, import-equals declaration, dynamic import, and `import()` type.
A relative specifier starts with `./` or `../`, or is `.` or `..`.
Name the imported file in each relative specifier by its own name and extension, such as `./harness.ts`, `./order-row.tsx`, `./export-invoices.mts`, or `./legacy.cts`.
Never omit the extension, such as `./harness`, even where a bundler or the compiler's resolution finds the file without it.
Never name a folder, such as `./orders` or `./orders/`; import the folder's entry point by its file name, such as `./orders/index.ts`.
Never write the name the compiler emits, such as `./harness.js` for `harness.ts` or `./export-invoices.mjs` for `export-invoices.mts`, because a runtime that strips types finds no such file.
Name every other imported file by its full name too, such as `./prices.json` or `../docs/usage.md`, with any query a bundler reads after it, such as `./usage.md?raw`.
A package specifier, such as `@acme/orders/client`, names an entry of that package's exports map, so it takes only the extension the map lists.

Enable `allowImportingTsExtensions` in each compiler configuration that sets `noEmit` or `emitDeclarationOnly`, where a bundler or a runtime that strips types loads the source.
Enable `rewriteRelativeImportExtensions` in each compiler configuration that emits the JavaScript that runs, so its output names `./harness.js` where the source names `./harness.ts`.
Answer a compiler error about a `.ts` specifier by enabling one of those options, never by dropping the extension or writing the emitted name.

Fail the repository's lint on each relative specifier whose path, before any query, does not end in `.ts`, `.tsx`, `.mts`, `.cts`, or a declared data or asset extension.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
The shipped files also accept listed data and asset extensions, such as `.json`, `.css`, and `.svg`, and a repository may add another such extension.
Never add a dotted part of a source file's name to that list, such as `gen` in `route-tree.gen.ts`, because its specifier must still end in `.ts`.
Remove an extension from the lint's list when a source file's name carries it as a dotted part, such as `css` in `theme.css.ts`.
A repository that also imports that kind of file keeps the extension and reviews each import of such a source file instead.
Make a specifier that code computes, such as `import(path)`, end in the file's own extension too, which the shipped files leave to review.
Import a JavaScript file that the repository keeps, such as a vendored `./chart.js`, by its own name, and suppress that finding only as `code-lint-suppressions` allows.
Exempt generated files by a declared path pattern, but never a hand-written file that imports a generated one.

Violation: `jobs/run.ts` imports `./harness`, which a bundler resolves but a runtime that strips types cannot find.
Violation: `accounts/sync.ts` imports `./client.js`, a file that exists only after the build writes it.
Violation: `refunds/send.ts` imports `../orders`, a folder, instead of its entry point `../orders/index.ts`.
Allowed: `jobs/run.ts` imports `./harness.ts` and `../orders/index.ts`, and its package's compiler configuration enables `allowImportingTsExtensions` with `noEmit`.
Allowed: a package that the compiler builds imports `./client.ts` and enables `rewriteRelativeImportExtensions`, so its output imports `./client.js`.

## Checks

Run the repository's lint from the repository root, and confirm that it rejects `./harness`, `./orders`, and `./harness.js` and accepts `./harness.ts`, `./orders/index.ts`, and `./prices.json`.
For each compiler configuration a change adds or edits, does it enable `allowImportingTsExtensions` with `noEmit` or `emitDeclarationOnly`, or `rewriteRelativeImportExtensions` where it emits JavaScript?
Does each extension a change adds to the lint's accepted list name a kind of data or asset file rather than part of a source file's name?
For each dynamic import a change adds whose specifier code computes, does the computed path end in the imported file's own extension?
For each suppression of this rule a change adds, does the specifier name a JavaScript file that the repository keeps?
