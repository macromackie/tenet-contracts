---
name: code-typescript-runtime-keyed-maps
message: Hold each TypeScript lookup that code fills at run time or builds from a collection in a `Map`, and create each record whole.
requires-tenet: 0.11.0
---

## Rules

A record is an object whose type is a `Record`, has an index signature, or maps its keys, such as `Record<string, number>` or `{ [accountId: string]: number }`.
Hold a lookup that code adds keys to after creating it in a `Map`, such as `const accountTotals = new Map<AccountId, number>()`, and add each entry with `set`.
Hold in a `Map` each record that code rebuilds from a spread of itself plus a computed key, such as `totals = { ...totals, [key]: amount }`.
Build a lookup from a collection with `new Map(entries)`, such as `const invoices = new Map(invoiceEntries)`.
Call `Object.fromEntries` only for a plain object that a dependency or a written format takes, such as a field of a JSON document.
Create every other record whole, as one object literal that writes every entry, such as `{ accept: 'application/json', [TRACE_HEADER]: traceId }`.
Never create a record as an empty object, `{}`, in a binding, a class field, or an `as` or `satisfies` expression, because code then fills or replaces it.
Never assign through a key that is not a literal, such as `totals[accountId] = amount`, except to a closed-set record that the writing function declares.

A closed-set record is a `const` annotated `Record<Set, Value>`, where `Set` is a closed set that `code-closed-value-sets` declares, such as `Record<CheckState, number>`.
Its literal keys one entry for each member by that member, such as `{ [CheckState.Failed]: 0, [CheckState.Passed]: 0 }`, so the compiler requires each one.
Hold a per-member tally or other value that a function updates in a closed-set record it declares, and update it through a member key, such as `counts[check.state] += 1`.

An array variable is a `const` or `let` that has an array type or is built by an array literal, `Array.from`, `Array.of`, `new Array`, or a typed array constructor.
A function may write by index to an array variable that it declares, such as `words[index] = word` after `const words = new Uint32Array(WORD_COUNT)`.
Hold any other array that a function writes by index in such a variable, such as `const fields: string[] = line.split(SEPARATOR)`, because the lint recognizes no other array.
`get` on a `Map` returns `undefined` for a missing key, so convert its result where `code-typescript-effect-absent-values` requires, and otherwise test it or default it with `??`.
Name each map as `code-map-and-set-names` requires, such as `accountTotals` rather than `totalsByAccount`.

Configure the repository's lint to report `{}` where a binding's or class field's annotation, `satisfies`, or an assertion gives it a record type.
Configure it also to report each assignment, compound assignment, increment, and decrement through a key that is not a literal, except on a declared array or closed-set record.
Configure it as well to report each variable that code rebuilds from a spread of itself plus a computed key.
Configure it to report every `Object.fromEntries` too, and mark each boundary call with a suppression whose reason names the dependency or format, as `code-lint-suppressions` allows.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Suppress a finding only as `code-lint-suppressions` allows.
Review each record write that the lint cannot see, such as a record typed through an alias, a field of another literal, or an entry that `Object.assign` adds.

Violation: `const totals: Record<string, number> = {}` followed by `totals[invoice.accountId] = invoice.amount` in a loop fills an empty record.
Allowed: `const accountTotals = new Map<AccountId, number>()` followed by `accountTotals.set(invoice.accountId, invoice.amount)` in the loop.
Violation: `const totals: Record<string, number> = { [DEFAULT_ACCOUNT]: 0 }` followed by `totals[invoice.accountId] = invoice.amount` writes a whole record through a run-time key.
Allowed: `const counts: Record<CheckState, number> = { [CheckState.Failed]: 0, [CheckState.Passed]: 0 }` followed by `counts[check.state] += 1` in a loop over checks.
Violation: `const invoiceIndex = Object.fromEntries(invoiceEntries)` builds a lookup that only owned code reads.
Allowed: `const invoices = new Map(invoiceEntries)`, and `const headers = { accept: 'application/json', [TRACE_HEADER]: traceId }` creates a record whole.
Allowed: `const exportPaths = Object.fromEntries(exportEntries)` fills a JSON manifest's `exports` field, under a suppression whose reason names that manifest format.

## Checks

Run the repository's lint from the repository root, and confirm that it reports `const totals: Record<string, number> = {}`, its `let` form, and `{} satisfies Record<string, number>`.
Confirm that the same lint reports `totals[accountId] = amount` and `Object.fromEntries(entries)`, and accepts `words[index] = word` after `const words = new Uint32Array(WORD_COUNT)`.
Confirm that it accepts `counts[check.state] += 1` after `const counts: Record<CheckState, number> = { [CheckState.Failed]: 0, [CheckState.Passed]: 0 }` in the same function.
Confirm that the same lint reports `totals = { ...totals, [key]: amount }` and a write to an array that the writing function does not declare.
For each lookup a change writes after creating it, is it a `Map` that gains entries through `set`, or a closed-set record when its keys form a closed set?
For each record a change creates through a type alias or inside another literal, is it written whole and never assigned through a run-time key afterward?
For each `Object.fromEntries` suppression a change adds, does its reason name a dependency or written format that takes the plain object?
