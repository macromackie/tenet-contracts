---
name: code-typescript-effect-schemas
message: Decode every value that crosses a TypeScript boundary with an Effect Schema, and derive its type from that schema.
---

## Rules

Decode every value that crosses a boundary, such as a request body, a stored record, an environment variable, a message from another process, or a model's output, with an Effect Schema before code reads it.
Declare each schema once, and derive the value's type from it, such as `type Invoice = typeof Invoice.Type`.
Never write a type by hand that repeats a schema's shape.
A schema built from a closed set's declaration may take its type from that declaration.
Never read a property of a value that a schema accepted as any value, such as `Schema.Unknown` or `Schema.Any`, until another schema decodes it.
Never assert an unknown boundary value to a type with `as` or a non-null assertion instead of decoding it.
Turn a decoding failure into the boundary's typed error, such as a rejected request or a failed job, and never into a default value.
When a framework accepts a common validator interface instead of its own schema type, pass the Effect schema through that interface instead of rewriting it in another library.
Use no other validation library, except one the repository declares for a named consumer that Effect Schema cannot serve, such as a generator that reads only that library's schemas.

Violation: `const invoice = JSON.parse(body) as Invoice` trusts the body's shape.
Allowed: the handler decodes the parsed body with the `Invoice` schema and reads only the decoded value.

## Checks

From the package directory, run the package's type check.
Search the change for imports of validation libraries other than Effect Schema, and confirm that each one serves a declared consumer.
Search the change for `as` assertions and non-null assertions on parsed, fetched, or received values.
For each boundary a change adds, which schema decodes it, and where is its type derived?
