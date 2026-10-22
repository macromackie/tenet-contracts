---
name: code-typescript-type-assertions
message: Narrow TypeScript values with checks the compiler follows, never with type assertions, non-null assertions, return-only type parameters, or the any type.
---

## Rules

Never write a type assertion, such as `value as Invoice` or `<Invoice>value`, a non-null assertion, such as `rows[0]!` or `findInvoice({ id })!.total`, or the `any` type.
Treat a value whose type is `any`, such as the result of `JSON.parse(body)` or an element of `value` after `Array.isArray(value)`, as `unknown`: never read its properties or call it, and never annotate, return, or pass it as a type other than `unknown`.
A const assertion, such as `['draft', 'sent'] as const`, is not a type assertion and is allowed.
Give a value its declared type with an annotation or `satisfies`, such as `const statusText: Record<number, string> = { 404: 'not_found' }`, instead of an assertion.
Narrow a value with a check the compiler follows, such as a comparison with `undefined`, a discriminant test, or an `in` test, and decode each boundary value as `code-typescript-effect-schemas` requires.
Never write a type predicate as a function's return type, such as `invoice is PaidInvoice`, or, in source, an assertion signature, such as `asserts value is Invoice`, because the compiler does not check that the function's body proves the claim; write the check where the value is read, or let the compiler infer the predicate from that check.
In tests and scripts, an assertion function that throws when its check fails, such as `assert.ok(row)`, narrows a value and is allowed.

When a field exists only in some of a record's states, such as an invoice's payment time, type each state as a union member that declares the field required, as `data-and-apis` requires for distinct outcomes, and read the field after a discriminant test.
Never replace an assertion with a default for a value whose absence is a broken invariant, such as `invoice.paidAt ?? 0` for a paid invoice; narrow the value or read it through an accessor that fails.
When a record's absence is a broken invariant, such as a row that the same object wrote before any caller can read it, read the record through one accessor per record kind, such as `requireInvoice()`, that fails as a defect naming the record.
A lookup by an id that a caller supplies is not a broken invariant, and `code-typescript-effect-errors` decides how its failure is returned.

Never declare a type parameter that only the return type uses, whether bare or inside another type, such as `first<T>(query: string): T | undefined`, `all<T>(query: string): T[]`, or `request<T>(path: string): Promise<T>`.
Never pass a type argument to a function whose type parameter appears only in its return type, such as `db.exec<InvoiceRow>(query)`; decode the result instead.
A class may pass its own type to the base that it extends, such as the self type of the tagged error class that `code-typescript-effect-errors` requires.
A service key class may also pass the interface of its service, because the compiler checks each implementation that provides the service against that interface.
A call that creates an empty collection, such as a new queue, may take its member type, because the compiler checks each member that later enters it against that type.

Configure the repository's lint to reject type assertions, non-null assertions, explicit `any`, each use of an `any` value other than as `unknown`, and a type parameter that only a return type uses bare, such as `first<T>(query: string): T | undefined`, in source, scripts, and tests.
Suppress one of those findings only in the form that `code-lint-suppressions` requires.

Violation: `const invoice = this.#invoice()!;` asserts at each caller that the invoice row exists.
Allowed: `const invoice = this.#requireInvoice();` fails once with an `InvoiceMissing` defect when the row that the object wrote is absent.

## Checks

Run the repository's lint with type-aware rules from the repository root, and confirm that it rejects type assertions, non-null assertions, explicit `any`, each use of an `any` value other than as `unknown`, and a type parameter that only a return type uses bare, such as `first<T>(query: string): T | undefined`.
For each type parameter a change declares, does a parameter's type use it, or does only the return type use it, such as inside an array or promise type?
For each assertion a change removes, does the replacement narrow the value, or does it hide the missing case behind a default value?
For each accessor a change adds that fails as a defect, did the same object write the record before any caller can read it?
For each type argument a change passes to a dependency's function, does that function's type parameter appear in its arguments, or does the type argument only declare the result?
