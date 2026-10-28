---
name: code-typescript-type-assertions
message: Narrow values with checks the compiler follows, annotate declared types unless code reads inferred ones, and never write type or non-null assertions, type predicates, return-only type parameters, or `any`.
requires-tenet: 0.11.0
---

## Rules

Never write a type assertion, such as `value as Invoice` or `<Invoice>value`, a non-null assertion, such as `rows[0]!` or `invoices.get(id)!.total`, or the `any` type.
Treat a value whose type is `any`, such as the result of `JSON.parse(body)` or an element of `value` after `Array.isArray(value)`, as `unknown`: never read its properties or call it, and never annotate, return, or pass it as a type other than `unknown`.
A const assertion, such as `['draft', 'sent'] as const`, is not a type assertion and is allowed.
Narrow a value with a check the compiler follows, such as a comparison with `undefined`, a discriminant test, or an `in` test, and decode each boundary value as `code-typescript-effect-schemas` requires.
Never write a type predicate, such as `invoice is PaidInvoice`, or an assertion signature, such as `asserts value is Invoice`, in any file, because the compiler never verifies them.
Test an `unknown` value against a schema with the guard that the schema library builds from that schema, named as `code-typescript-effect-schemas` requires, such as `isInvoice`.
TypeScript 5.5 and later infer a predicate from an inline callback's check, such as `orders.filter((order) => order.status === OrderStatus.Paid)`, so the callback narrows without a written one.
In tests and scripts, a dependency's assertion function that throws when its check fails, such as `assert.ok(row)`, narrows a value and is allowed.

When a constant or field must match a declared type, annotate it where it is declared, such as `const reminders: ReminderSchedule = { ... }`.
Write `satisfies` instead only where later code reads the narrower inferred type, and bind any other value that needs a declared type to an annotated constant.
Such reads include a story's `typeof meta`, a table's literal keys, an anonymous default export a runtime loads, and a module-level literal's `as const` type, as `code-typescript-module-state` requires.

When a field exists only in some of a record's states, such as an invoice's payment time, type each state as a union member that declares the field required, as `data-and-apis` requires for distinct outcomes, and read the field after a discriminant test.
Never replace an assertion with a default for a value whose absence is a broken invariant, such as `paymentTimes.get(invoice.id) ?? 0` for a paid invoice.
Narrow such a value instead, or read it through an accessor that fails.
Read a record whose absence breaks an invariant, such as a row this object wrote, through one accessor per record kind that fails as a defect naming the record.
A lookup by an id that a caller supplies is not a broken invariant, and `code-typescript-effect-errors` decides how its failure is returned.

Never declare a type parameter that only the return type uses, whether bare or inside another type, such as `parseJson<Value>({ text }: ParseJsonInput): Value`, `parseLines<Line>({ text }: ParseLinesInput): readonly Line[]`, or `request<Body>({ path }: RequestInput): Promise<Body>`.
Never pass a type argument to a function whose type parameter appears only in its return type, such as `db.exec<InvoiceRow>(query)`; decode the result instead.
A class may pass its own type to the base that it extends, such as the self type of the tagged error class that `code-typescript-effect-errors` requires.
A service key class may also pass the interface of its service, because the compiler checks each implementation that provides the service against that interface.
A call that creates an empty collection, such as a new queue, may take its member type, because the compiler checks each member that later enters it against that type.

Configure the repository's lint to reject type assertions, non-null assertions, explicit `any`, and each use of an `any` value other than as `unknown`, in source, scripts, and tests.
Configure it also to reject type predicates, assertion signatures, and a type parameter only a return type uses bare, such as `parseJson<Value>({ text }: ParseJsonInput): Value`, in those files.
Configure it also to list each `satisfies` expression for review without failing, because no lint can tell whether later code reads the inferred type.
Where the repository's lint can load this contract's `assets/` configuration, load it from the repository's own lint configuration, and suppress a finding only as `code-lint-suppressions` requires.

Violation: `const invoice = this.#invoices.get(this.#invoiceId)!;` asserts at each caller that the invoice row exists.
Allowed: `const invoice = this.#readInvoice();` fails once with an `InvoiceMissing` defect when the row that the object wrote is absent.
Violation: `orders.filter((order): order is PaidOrder => order.status === OrderStatus.Paid)` writes a predicate that the compiler never checks against the callback's body.
Allowed: `orders.filter((order) => order.status === OrderStatus.Paid)`, from which the compiler infers `order is PaidOrder`.
Violation: `const reminders = { invoiceId: invoice.id, sendDates } satisfies ReminderSchedule` in a function that reads `reminders` only as a `ReminderSchedule`.
Allowed: `const reminders: ReminderSchedule = { invoiceId: invoice.id, sendDates }` in that function.
Allowed: `type Story = StoryObj<typeof meta>` after `const meta = { component: InvoiceCard } as const satisfies Meta<typeof InvoiceCard>`.
Allowed: `layouts.compact` after `const layouts = { ... } as const satisfies Record<string, ColumnLayout>`.
Allowed: `export default { fetch: handleRequest } as const satisfies ExportedHandler<Bindings>`, so code that imports it reads `fetch` as present, where `ExportedHandler` declares it optional.

## Checks

Run the repository's type-aware lint from the repository root, and confirm it rejects type assertions, non-null assertions, explicit `any`, and each use of an `any` value except as `unknown`.
Confirm the same run rejects a type predicate, an assertion signature, and a type parameter that only a return type uses bare, such as `parseJson<Value>({ text }: ParseJsonInput): Value`.
For each `satisfies` the same run lists in changed code, does later code read the narrower type that the compiler infers, which the listing alone cannot decide?
For each type parameter a change declares, does a parameter's type use it, or does only the return type use it, such as inside an array or promise type?
For each assertion a change removes, does the replacement narrow the value, or does it hide the missing case behind a default value?
For each accessor a change adds that fails as a defect, did the same object write the record before any caller can read it?
For each type argument a change passes to a dependency's function, does that function's type parameter appear in its arguments, or does the type argument only declare the result?
