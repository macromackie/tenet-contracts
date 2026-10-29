---
name: code-typescript-effect-absent-values
message: Type each TypeScript result and record field that may hold no value as an Effect `Option`, writing `null` and `undefined` only where a foreign format or signature requires them.
requires-tenet: 0.11.0
---

## Rules

Type every owned result and record field that may hold no value as `Option.Option<T>`, including an Effect's success value, such as `Effect.Effect<Option.Option<Invoice>, StoreUnavailable>`.
An empty collection or string is a value and keeps its own type, such as the `readonly Invoice[]` of a search that matches nothing.
Decide whether a missing result is a value or an expected failure as `code-typescript-effect-errors` does, and give only a value the `Option` type.

Turn a dependency's result that may be `null` or `undefined`, such as from `Map.get`, `Array.find`, `querySelector`, or a regular expression's `exec`, into an `Option` with `Option.fromNullishOr`.
Convert it where owned code returns it, stores it in a field, or passes it to an owned function, such as `return Option.fromNullishOr(found)` after `const found = invoices.get(id)`.
A local that the same function tests may keep the dependency's type, such as `if (!match) { continue; }` after `const match = PATTERN.exec(line)`, as `code-typescript-boolean-conditions` allows.

Write `null` only where a foreign format or signature requires it: the encoded side of a schema, a component that renders nothing, and a signature that a dependency declares.
Decode a foreign field written as `null` with `Schema.OptionFromNullOr`, one left out with `Schema.OptionFromOptionalKey`, and one either way with `Schema.OptionFromOptionalNullOr`, as `code-typescript-effect-schemas` decodes each boundary.
Never decode a field with `Schema.NullOr`, `Schema.UndefinedOr`, `Schema.NullishOr`, `Schema.Null`, `Schema.Undefined`, `Schema.optional`, or `Schema.optionalKey`, which leave `null` or `undefined` in the decoded type.
Return `null` from a component that renders nothing, and declare its return type, even when it is private, as the framework's type for anything it can render.
Annotate an owned function that implements a dependency's signature with that dependency's type, such as `const readSnapshot: SnapshotReader = ...`, never with a copy that writes `null`.

Use an `Option` in the form named below for each case, never `Option.match`, which nests each case in a callback, and never an `else` after `Option.isSome` or `Option.isNone`.
Take a default with `Option.getOrElse`, such as `Option.getOrElse(note, () => '')`, and derive an optional value with `Option.map`, such as `Option.map(dueAt, (date) => formatDate({ date }))`.
When the empty case leaves its function or loop body, as `code-guard-clauses` decides, test it first with a guard, such as `if (Option.isNone(found)) { return ...; }`, then read `found.value`.
Wrap code that runs only for a value, when the empty case carries on, in an `Option.isSome` test, and choose markup as `code-conditional-expressions` requires, such as `{Option.isSome(dueAt) && <DueDate dueAt={dueAt.value} />}`.
Give a dependency whose signature asks for `null` or `undefined` the value of `Option.getOrNull` or `Option.getOrUndefined`, whichever that signature names, where owned code passes it.

Never write `null` or `undefined` in a return type, a field type, or a type alias that owned code declares, such as `note: string | null`.
A dependency's type keeps its own `null` and `undefined`, such as a declaration file like `vendor.d.ts` that types the dependency.
Suppress a finding for a type argument that a dependency's type requires, such as the element type of a reference the framework fills, as `code-lint-suppressions` allows.
Never return, pass, or initialize with `undefined`, such as `return undefined` or an `= undefined` default, and leave a function that returns nothing early with a bare `return;`.

Mark a field `?:` only when a caller may leave it out of an owned function's argument object, never also as an `Option`, and default it as `code-typescript-function-arguments` requires.
Set every field of a record in the literal that creates it, and never assign one afterward except through a member key that `code-typescript-runtime-keyed-maps` allows.
Spread a condition into a literal, such as `...(Option.isSome(note) && { channel: note.value })`, only to leave out a `?:` field that the callee declares.

Configure the repository's lint to reject each type, value, schema constructor, field, assignment, and `Option` form forbidden above, and `return null` where no declared type decides it.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration, and suppress a finding only as `code-lint-suppressions` allows.

Violation: `function findOverdueInvoice({ invoices }: FindOverdueInvoiceInput): Invoice | undefined` returns the first overdue invoice, so every caller tests for `undefined`.
Violation: `type Invoice = { note: string | null }` writes `null` in a field type.
Violation: `type NotifyInput = { readonly channel?: Option.Option<string> }` marks an `Option` field optional.
Violation: `const draft: Draft = { id, note: Option.none() }` followed by `if (text !== '') { draft.note = Option.some(text); }` assigns a field after the literal.
Allowed: `function findOverdueInvoice({ invoices }: FindOverdueInvoiceInput): Option.Option<Invoice>` binds `const found = invoices.find((invoice) => isOverdue({ invoice }))` and returns `Option.fromNullishOr(found)`.
Allowed: a schema file declares `const Invoice = Schema.Struct({ id: Schema.String, note: Schema.OptionFromNullOr(Schema.String), replaces: Schema.OptionFromOptionalKey(Schema.String) })` with `type Invoice = typeof Invoice.Type`, and code returns `{ id, note, replaces: previous }`.
Allowed: a component that renders nothing, private or exported, declares the framework's node type and returns `null`.
Allowed: `const request: NotifyInput = { invoice, ...(Option.isSome(note) && { channel: note.value }) }`, then `notify(request)`, leaves out a `?:` field.
Violation: `Option.match(dueAt, { onNone: renderNoDueDate, onSome: renderDueDate })` chooses markup through `Option.match`, which nests each case in a callback.
Violation: `if (Option.isSome(found)) { sendReminder({ invoice: found.value }); } else { recordQuietRun({ account }); }` runs code for both cases behind an `else`.
Allowed: `const text = Option.getOrElse(note, () => '')`, and `{Option.isSome(dueAt) && <DueDate dueAt={dueAt.value} />}` shows a due date or nothing.
Allowed: `if (Option.isNone(found))` holds `recordQuietRun({ account });`, a blank line, and `return;`, and after another blank line `sendReminder({ invoice: found.value })` runs for a value.

## Checks

Run the repository's lint from the repository root, and confirm that it rejects `note: string | null`, `return undefined` in a typed function, and `replaces?: Option.Option<string>`.
Confirm also that it rejects `Schema.NullOr(Schema.String)`, `Option.match`, an `else` after `Option.isSome`, and `draft.note = Option.some(text)` after `const draft: Draft = { id, note: Option.none() }`.
From each affected package root, run the type check against effect 4.0.0 or later, so each declared `Option` type and each `return null` meets the type it must satisfy.
For each dependency's nullable result that a change returns, stores in a field, or passes to an owned function, is it converted with `Option.fromNullishOr` first?
For each `Option` a change adds, is an empty value a value rather than an expected failure, which `code-typescript-effect-errors` makes a tagged error?
For each `?:` field a change adds, may a caller leave it out of an owned function's argument, and does each conditional spread omit a callee's `?:` field?
For each `return null` and each `Option.getOrNull` or `Option.getOrUndefined` a change adds, does a component framework's type or a dependency's signature require `null` or `undefined` there?
