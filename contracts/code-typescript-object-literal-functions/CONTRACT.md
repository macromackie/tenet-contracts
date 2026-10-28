---
name: code-typescript-object-literal-functions
message: Declare each function a TypeScript object literal holds by name and list the name, such as `return { settleInvoice }`, instead of writing a method or function-valued property.
requires-tenet: 0.11.0
---

## Rules

Declare each function that an object literal holds by name, as `code-typescript-const-bindings` requires, and list that name in the literal, such as `return { settleInvoice }`.
Never write a method in an object literal, such as `parse({ line }) { ... }`, including an `async` or generator method.
Never write a function as the value of an object literal's property, such as `parse: ({ line }) => ...` or `parse: function ({ line }) { ... }`.
This holds when parentheses, an operator, an `as` assertion, or a `satisfies` expression stands between the function and the property, such as `onClose: (() => closeDialog())`.
A property whose value names a declared function, such as `{ fetch: handleRequest }`, holds that function by name.
A getter or setter is an accessor, not a method, and stays where it is written.

A function, class, call, or embedded markup element between a function and the literal starts afresh, so `{ paidInvoices: invoices.filter((invoice) => invoice.isPaid) }` holds the call's result.
A call that returns a function, such as `memoize(...)`, still gives the property a function, so bind its result by name and list that name.
A function written as an array element is not a property's value, even when the array is, such as `{ steps: [() => checkStock()] }`.
A class body is not an object literal, and `code-typescript-class-declarations` decides where a class and its methods may appear.
A function written in an object or array in the arguments of a call or `new` expression follows `code-typescript-call-arguments` instead, so the two contracts never judge one function twice.

An object that a runtime or framework reads functions from, such as an entry point's default export, a plugin, or a test fake, follows these rules too.
Type each function such an object holds as the runtime or framework declares it, with a typed constant or a declaration with those parameter and result types.
Such a constant is `const handleRequest: FetchHandler = ...`, listed in `export default { fetch: handleRequest } as const satisfies ExportedHandler<Bindings>`.
Suppress a finding only as `code-lint-suppressions` allows, such as for a method that calls `super`, which only method syntax allows.

Configure the repository's lint to reject each method and each function-valued property in an object literal outside a call's arguments, and to accept each accessor.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.

Violation: `return { settleInvoice: ({ id }) => settle({ id }) }` writes a function as a property's value.
Violation: `export default { async fetch(request: Request): Promise<Response> { ... } } as const satisfies ExportedHandler<Bindings>` writes a method in an object literal.
Allowed: `const settleInvoice: SettleInvoice = ({ id }) => settle({ id })`, then `return { settleInvoice }`, and `export default { fetch: handleRequest } as const satisfies ExportedHandler<Bindings>`.
Allowed: `const totals = { get total() { ... } }` writes an accessor.

## Checks

Run the repository's lint from the repository root and confirm that it rejects a method and an arrow property in an object literal and accepts a getter.
For each object literal a change adds or edits outside a call's arguments, is every function it holds declared by name and listed?
For each function a change moves out of an object literal for a runtime or framework, does its type match the type that runtime or framework declares?
For each suppression of this rule a change adds, does its reason name what requires method syntax, such as a call to `super`?
