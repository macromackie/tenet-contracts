---
name: code-typescript-effect-schemas
message: Decode every value that crosses a TypeScript boundary with an Effect Schema, reject unknown fields on owned shapes, and give each schema and its type one PascalCase name.
requires-tenet: 0.11.0
---

## Rules

Decode every value that crosses a boundary, such as a request body, a stored record, an environment variable, a message from another process, or a model's output, with an Effect Schema before code reads it.
Name each schema constant in PascalCase for the value it decodes, such as `Invoice`, never in camelCase or with a `Schema` suffix, such as `invoice` or `InvoiceSchema`.
Declare each schema once, and derive its type once, directly below it, in an alias that shares the schema's name, written `type Invoice = typeof Invoice.Type`.
Refer to that alias everywhere else, and never write a schema's derived type inline, such as `(input: typeof Invoice.Type)`, or under another name.
Never write a type by hand that repeats a schema's shape.
A schema built from a closed set's declaration may take its type from that declaration.
Write such a schema inline where a field or a decode uses it, such as `status: Schema.Enum(OrderStatus)`, so the set never needs a second name.
A schema class, such as `class Invoice extends Schema.Class<Invoice>('Invoice')({ ... }) {}`, is its own type and needs no alias.
A function built from a schema, such as a decoder or a guard, is not a schema and keeps a camelCase name, such as `decodeInvoice` or `const isInvoice = Schema.is(Invoice)`.
Never read a property of a value that a schema accepted as any value, such as `Schema.Unknown` or `Schema.Any`, until another schema decodes it.
Turn a decoding failure into the boundary's typed error, such as a rejected request or a failed job, and never into a default value.
When a framework accepts a common validator interface instead of its own schema type, pass the Effect schema through that interface instead of rewriting it in another library.
Use no other validation library, except one the repository declares for a named consumer that Effect Schema cannot serve, such as a generator that reads only that library's schemas.

An owned shape is one this repository declares for data it writes or accepts, such as its request bodies, stored records, settings files, and internal messages.
A foreign payload is one that another system declares and may extend, such as a provider's webhook or response, request headers, or the process environment.
Reject unknown fields on every decode by passing `{ onExcessProperty: 'error' }` beside the schema, such as `Schema.decodeUnknownEffect(Invoice, { onExcessProperty: 'error' })`.
Mark each foreign payload loose in its own schema by declaring its other fields with an index signature, such as a `Schema.StructWithRest` whose rest is `Schema.Record(Schema.String, Schema.Unknown)`.
Never mark an owned shape loose, so a misspelled or removed field fails its decode instead of disappearing.
When a framework or a common validator interface decodes a value for the code, give it the same option, such as `Schema.toStandardSchemaV1(Invoice, { parseOptions: { onExcessProperty: 'error' } })`.
Making an existing reader of stored or shipped data reject unknown fields narrows it, so ship that change only as `data-stored-and-shipped-formats` allows.

Configure the repository's lint to reject a schema constant whose name is not PascalCase, a derived type outside its alias, and a decode call without `onExcessProperty: 'error'`.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `const invoice = JSON.parse(body) as Invoice` trusts the body's shape.
Violation: `const invoiceSchema = Schema.Struct({ ... })` beside `type InvoiceRecord = typeof invoiceSchema.Type` gives one concept two names.
Violation: `Schema.decodeUnknownEffect(Settings)(file)` drops a misspelled `retrys` field, so the setting silently keeps its default.
Allowed: the handler decodes the parsed body with `Schema.decodeUnknownEffect(Invoice, { onExcessProperty: 'error' })` and reads only the decoded value, typed by `type Invoice = typeof Invoice.Type`.
Allowed: a webhook's `ProviderEvent` schema declares the one field code reads and a `Schema.Record(Schema.String, Schema.Unknown)` rest, and is decoded with `onExcessProperty: 'error'`.

## Checks

From the package directory, run the package's type check.
Run the repository's lint from the repository root, and confirm that it reports a camelCase schema constant, an inline `typeof Invoice.Type`, and a decode call without `onExcessProperty: 'error'`.
Search the change for imports of validation libraries other than Effect Schema, and confirm that each one serves a declared consumer.
For each boundary a change adds, which schema decodes it, and where is its type's one alias?
For each schema a change marks loose, does another system declare the payload, and for each one it leaves strict, does this repository own the shape?
For each existing reader of stored or shipped data that a change makes reject unknown fields, which migration or count shows that no stored instance carries one?
