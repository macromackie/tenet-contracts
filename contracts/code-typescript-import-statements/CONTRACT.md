---
name: code-typescript-import-statements
message: Import modules at the top in sorted blocks without blank lines, once each and by name, test functions from the runner, listed libraries as namespaces, type-only names as `type`.
requires-tenet: 0.11.0
---

## Rules

This contract covers the position and form of the import statements in every TypeScript file, including tests, scripts, and `.tsx` files, while `code-typescript-import-extensions` governs their specifiers.

Sort each block of consecutive import statements into groups: runtime built-in modules, then packages, then path aliases and subpath imports, then relative paths, parent and sibling paths together.
Sort the statements of each group alphabetically by specifier, ignoring letter case, such as `@acme/money` before `order-kit` and `./orders.ts` before `./README.md`.
Sort a specifier whose scheme the runtime does not provide, such as `virtual:routes`, with packages.
Sort a path alias that the repository declares beside the subpath imports, such as `#config` and `~/orders.ts`, and list any other alias prefix in the formatter's settings.
Put a stylesheet imported as a value, such as `import { orderRow } from './orders.module.css'`, after the relative paths.
Sort an `import type` statement among the others by its specifier, as if `type` were absent, and leave the order of names inside any statement's braces to the writer.
Where alphabetical order leaves a tie open, such as for digits or punctuation, follow the order that the repository's formatter produces.
Write no blank line between the statements of an import block, including between its groups.

Write every import statement below the file's directives, such as `'use strict'`, and above every other statement, re-exports included, because imported modules run before the file's own code.
Keep each side-effect import, such as `import './reset.css'`, where its effect must run, first in its block when every other module depends on it.
Separate a comment that describes the whole file from the first import with one blank line, because a comment directly above an import moves with that import.

Mark each name the file uses only as a type, and write `import type` when every name a statement imports is one, such as `import type { Invoice }`.
Mark each type inline in a statement that also imports values, such as `import { type Invoice, settleInvoice } from './invoices.ts'`.
Never write a statement whose every name carries an inline `type`, because a compiler that keeps imports as written still loads that module at run time.
Import each module specifier in exactly one statement, merging its type and value names, where `./usage.md?raw` and `./usage.md?url` are different specifiers.

Declare the namespace libraries in the repository's lint configuration, replacing the shipped default list, and list only a package whose own documentation imports it as one namespace.
Write no namespace import of a module off that list, such as `import * as totals from './totals.ts'`, and import each name the file uses instead.
Import a runtime built-in module's names by name too, never through its default export, which is the whole module, such as `import { readFile } from 'node:fs/promises'`.
Import each test runner function a test calls, such as `expect`, by name from the runner's module, never as a global or from the runtime's test or assertion module.
Outside tests, import the runtime's assertion module only as `import { strict as assert } from 'node:assert'`, so that each call names the strict module, such as `assert.equal(total, expectedTotal)`.
Import a listed library only as one namespace, never by name, so that each call names its library, such as `chartKit.drawChart()`.
Name that namespace the camelCase form of the package's name without its scope, such as `import * as chartKit from '@acme/chart-kit'`, and never give it another name.

Fail the repository's formatter check on an unsorted import block, and fail its lint on each statement whose form breaks these rules.
Where the repository's formatter or lint can use the configuration in this contract's `assets/` folder, extend it or merge its settings into the repository's own configuration.

Violation: `orders/export.ts` imports `./totals.ts` above `node:path`, imports `Invoice` without `type` although it uses it only as a type, and imports `../invoices.ts` in two statements.
Allowed: `orders/export.ts` imports `node:path`, `@acme/money`, `import { type Invoice, settleInvoice } from '../invoices.ts'`, and `./totals.ts`, in that order with no blank lines.
Violation: with `@acme/chart-kit` on the namespace list, `orders/chart.ts` writes `import * as totals from './totals.ts'` and `import { drawChart } from '@acme/chart-kit'`.
Allowed: `orders/chart.ts` writes `import * as chartKit from '@acme/chart-kit'` and `import { sumTotals } from './totals.ts'`, binds `const totals = sumTotals({ orders })`, and calls `chartKit.drawChart({ totals })`.
Violation: `orders/export.test.ts` calls the runner's global `test` and imports `{ strict as assert }` from `node:assert`, and imports `./totals.ts` below its first declaration.
Allowed: `orders/export.test.ts` opens by importing `describe`, `expect`, and `test` by name from the test runner's module, then `import { sumTotals } from './totals.ts'`.

## Checks

Run the repository's formatter check from the repository root, and confirm that it fails on `./totals.ts` above `node:path` and on a blank line between groups.
Run the repository's lint from the repository root, and confirm it fails on an unmarked type-only name, a statement of only inline `type` names, and a module imported twice.
Run the lint and `assets/` rules from the repository root, confirming failures on an unlisted namespace import, a listed library imported by name, and a misnamed namespace.
Run the lint and `assets/` rules from the repository root, confirming failures on a built-in default import, globals, `node:test`, and `node:assert` in tests, `node:assert/strict` in scripts, and late imports.
For each side-effect import a change adds or moves, does it sit where its effect must run, first in its block when every other module depends on it?
Does one blank line separate each file comment a change adds from the first import below it?
For each library a change adds to the namespace list, does that library's own documentation import it as one namespace?
