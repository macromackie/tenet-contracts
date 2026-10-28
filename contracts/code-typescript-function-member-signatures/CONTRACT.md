---
name: code-typescript-function-member-signatures
message: Declare each function member of a TypeScript type as a property with a function type, never as a method signature, so the compiler checks its parameters strictly.
requires-tenet: 0.11.0
---

## Rules

Declare each function member of an interface or object type as a property with a function type, such as `readonly settleInvoice: (input: SettleInvoiceInput) => Promise<Invoice>`.
Never declare it as a method signature, such as `settleInvoice(input: SettleInvoiceInput): Promise<Invoice>`, because the compiler checks a method's parameters bivariantly even under `strict`.
This holds for an optional, generic, or computed-key member, such as `readonly onProgress?: (input: OnProgressInput) => void` or `readonly [Symbol.iterator]: () => Iterator<Row>`.
It holds in every type the repository writes, including types in tests, scripts, and hand-written declaration files.
The compiler checks a property's parameters strictly only under `strictFunctionTypes`, which `strict` enables as `code-typescript-compiler-strictness` requires.

Write a function member's overloads as call signatures in a named type, such as `type ListInvoices = { (input: ListInvoicesByCustomerInput): Promise<readonly Invoice[]>; (input: ListInvoicesByPageInput): Promise<InvoicePage> }`.
Declare the member as a property of that type, such as `readonly listInvoices: ListInvoices`.
Never write overloads as repeated method signatures or as an intersection of function types, such as `readonly listInvoices: ByCustomerListing & ByPageListing`.
A call or construct signature, such as `(input: ListInvoicesByPageInput): Promise<InvoicePage>` or `new (input: RunnerInput): Runner`, is not a method signature.
A getter or setter signature, such as `get total(): number`, is an accessor, not a method signature.
A class body is not an object type, and `code-typescript-class-declarations` decides how a class declares its methods and their overload signatures.

An interface that augments a dependency's declaration, such as one inside `declare module` or `declare global`, follows these rules for each member it adds.
Only a method signature merges with a method that the dependency declares, so an augmentation may add an overload to that method as a method signature.
Suppress the lint finding on such an overload only as `code-lint-suppressions` allows, with a reason that names the dependency and the method it declares.
Exempt generated files and copied third-party source from these rules by a path pattern declared in the lint configuration.

Configure the repository's lint to reject every method signature in an interface or object type, and to accept accessor, call, and construct signatures.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Review what that configuration cannot see: overloads written as an intersection of function types.

Violation: `type InvoiceStore = { settleInvoice(input: SettleInvoiceInput): Promise<Invoice> }` compiles with an implementation that accepts only a paid invoice.
Allowed: `type InvoiceStore = { readonly settleInvoice: (input: SettleInvoiceInput) => Promise<Invoice> }`, which rejects that implementation.
Violation: `listInvoices(input: ListInvoicesByCustomerInput): Promise<readonly Invoice[]>;` followed by `listInvoices(input: ListInvoicesByPageInput): Promise<InvoicePage>;` declares overloads as method signatures.
Allowed: `readonly listInvoices: ListInvoices`, with the overloads as call signatures in `type ListInvoices`.

## Checks

Run the repository's lint from the repository root, and confirm that it rejects a method signature in an object type and accepts an accessor, call, and construct signature.
From each affected package root, run the type check after converting method signatures, so the compiler checks each implementation's parameters against the property types.
For each overloaded function member a change adds, are its overloads call signatures in a named type, rather than method signatures or an intersection of function types?
For each suppression of this rule a change adds, does the signature sit in an augmentation and add an overload to a method that the named dependency declares?
For each path pattern a change adds to exempt files from this rule, does it match only generated files or copied third-party source?
