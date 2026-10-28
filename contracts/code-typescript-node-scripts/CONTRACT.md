---
name: code-typescript-node-scripts
message: Write repository scripts as `.mts` files that the pinned Node runs directly without a loader or runner dependency, and type-check them for what Node's type stripping accepts.
requires-tenet: 0.11.0
---

## Rules

This contract extends `code-script-entry-points`, which limits what each script's top level holds, `code-typescript-compiler-strictness`, which type-checks scripts under strict settings, and `code-typescript-import-extensions`, which requires each relative import's own extension.
Apply this contract to the repository's own scripts, such as checks, code generators, smoke runs, and release steps, and to the helper modules that only scripts import, but not to programs the product ships.
Write each repository script in TypeScript, except a script for tooling already written in another language, which uses that language, and a shell script for the bootstrap that runs before the pinned Node is installed or for a one-line shim.
Give each script and each helper module the `.mts` extension, even inside a package marked as ECMAScript modules, because the compiler reads a `.ts` file outside such a package as CommonJS and, under `verbatimModuleSyntax`, rejects its imports.
Pin a Node version that strips types by default, and start each executable script with `#!/usr/bin/env node`, so that the pinned Node runs it without a loader, a flag, or a TypeScript runner.
Never add a dependency to run a script or to start its subprocesses, such as a loader, a TypeScript runner, or a shell or process helper library.
Call each Node function that has an asynchronous form in that form, such as `await readFile(path, 'utf-8')` from `node:fs/promises`, never `readFileSync` or `execFileSync`.
Configure the repository's lint to reject each synchronous Node call in scripts and their helper modules.
Where the repository's lint can load this contract's `assets/oxlint/oxlintrc.json`, load it from the repository's own lint configuration.

Type-check every folder of scripts with the TypeScript compiler under `module` and `moduleResolution` set to `nodenext`, `erasableSyntaxOnly`, `allowImportingTsExtensions`, and `noEmit`, beside the settings `code-typescript-compiler-strictness` requires.
Together they make the check fail where Node would, on syntax that type stripping rejects and on a type imported without `import type`.
A folder's compiler configuration may set these options by extending this contract's `assets/typescript/tsconfig.json`, listed after any base configuration it extends.

Violation: a change adds a process helper library so that `export-invoices.mts` can start `invoice-export`.
Allowed: `export-invoices.mts` opens with `#!/usr/bin/env node` and a summary of what it does and how to run it, imports `./invoice-totals.mts`, and starts the export with `execFile('invoice-export', [month])`.

## Checks

Run the repository's script type check and lint from the repository root, confirm the lint rejects `readFileSync` in a script, and run each changed script once.
For each folder of scripts, does the compiler's `--showConfig` output set `module` and `moduleResolution` to `nodenext` and enable `erasableSyntaxOnly`, `allowImportingTsExtensions`, and `noEmit`?
Does a change add a dependency that runs scripts or starts their subprocesses?
For each script a change adds in another language, is it for tooling already written in that language, the bootstrap, or a one-line shim?
