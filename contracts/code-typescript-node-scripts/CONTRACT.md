---
name: code-typescript-node-scripts
message: Write repository scripts as `.mts` files that the pinned Node runs directly without a loader or runner dependency, and type-check them for what Node's type stripping accepts.
requires-tenet: 0.11.0
---

## Rules

This contract extends `code-script-entry-points`, which limits what each script's top level holds, and `code-typescript-compiler-strictness`, which type-checks scripts under strict settings.
Apply this contract to the repository's own scripts, such as checks, code generators, smoke runs, and release steps, and to the helper modules that only scripts import, but not to programs the product ships.
Write each repository script in TypeScript, except a script for tooling already written in another language, which uses that language, and a shell script for the bootstrap that runs before the pinned Node is installed or for a one-line shim.
Give each script and each helper module the `.mts` extension, even inside a package marked as ECMAScript modules, because the compiler reads a `.ts` file outside such a package as CommonJS and, under `verbatimModuleSyntax`, rejects its imports.
Pin a Node version that strips types by default, and start each executable script with `#!/usr/bin/env node`, so that the pinned Node runs it without a loader, a flag, or a TypeScript runner.
Never add a dependency to run a script or to start its subprocesses, such as a loader, a TypeScript runner, or a shell or process helper library.
Write each relative import with the imported file's own name and extension, because the compiler also accepts its output's name, such as `.mjs` for an `.mts` file, which Node cannot load.

Type-check every folder of scripts with the TypeScript compiler under `module` and `moduleResolution` set to `nodenext`, `erasableSyntaxOnly`, `verbatimModuleSyntax`, `allowImportingTsExtensions`, and `noEmit`, so that the check fails where Node would, on syntax that type stripping rejects and on a type imported without `import type`.
A folder's compiler configuration may set these options by extending this contract's `assets/typescript/tsconfig.json`, listed after any base configuration it extends.

Violation: `export-invoices.mts` imports `./invoice-totals.mjs`, which the compiler resolves to `invoice-totals.mts` and Node cannot find.
Violation: a change adds a process helper library so that `export-invoices.mts` can start `invoice-export`.
Allowed: `export-invoices.mts` starts with `#!/usr/bin/env node`, imports `./invoice-totals.mts`, and starts the export with `execFile('invoice-export', [month])`.

## Checks

Run the repository's script type check and lint from the repository root, and run each changed script once.
For each folder of scripts, does the compiler's `--showConfig` output set `module` and `moduleResolution` to `nodenext` and enable `erasableSyntaxOnly`, `verbatimModuleSyntax`, `allowImportingTsExtensions`, and `noEmit`?
Search scripts for relative imports that name a `.js` or `.mjs` file that does not exist.
Does a change add a dependency that runs scripts or starts their subprocesses?
For each script a change adds in another language, is it for tooling already written in that language, the bootstrap, or a one-line shim?
