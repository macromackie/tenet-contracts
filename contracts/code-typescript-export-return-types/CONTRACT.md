---
name: code-typescript-export-return-types
message: Declare the return type of every exported TypeScript function and method, and let local functions and callbacks infer theirs.
requires-tenet: 0.11.0
---

## Rules

Declare the return type of every function and method a module exports, so that an edit inside one cannot silently change the module's contract.
This covers a function exported by its declaration, through an export list, or as the default export, and each function or method that an exported object holds.
It also covers each method, getter, and function-valued property of an exported class, whether public, protected, or static, but not a private one.
A constructor and a setter take no return type.
Treat an exported component that returns markup as an exported function, and declare the type of the element it returns.
Declare the return type of each overload signature and of the implementation that follows them.
Declare the type of each parameter of an exported function or method, except one whose default value supplies its type.

Declare the type that callers rely on, including each failure its result carries, such as an error union, and never widen it to `unknown` to avoid writing it out.

An exported constant annotated with a function type, such as `const writeEvent: EventSink = ...` as `code-typescript-const-bindings` requires, declares its return type through that annotation.
A function an exported object holds declares its return type in its own declaration or typed constant, because a `satisfies` clause on the object leaves callers the inferred type.
A function-valued property of an exported class takes its return type from the property's declared type.
A function the module does not export and a callback passed as an argument need no declared return type, except a component that renders nothing, as `code-typescript-effect-absent-values` requires.
A function nested in an exported function, including one it returns, needs none once the exported function declares its own.
A re-export of another module's function needs no annotation, because the module that declares the function declares its return type.

Configure the repository's lint to reject an exported function, method, or function-valued class property without a declared return type, and an exported function's parameter without a declared type.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
That configuration leaves an explicit `any` parameter to `code-typescript-type-assertions`, which rejects it.
Review what that configuration cannot see: a function that an exported object, list, or constant names by reference, such as `{ settleInvoice }`, or that a call returns.
That configuration also accepts a function written in an exported object that a `satisfies` clause types, so review that function's own return type.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `export async function readInvoice({ id }: ReadInvoiceInput) { ... }` leaves its result to inference, so an edit to its body changes every caller's type.
Violation: `export const settlers = { [PaymentKind.Card]: settleCard } as const` holds a `settleCard` function declared without a return type.
Allowed: `export async function readInvoice({ id }: ReadInvoiceInput): Promise<Invoice>`, whose local helpers and the callback it passes to `map` infer their return types.
Allowed: `export const writeEvent: EventSink = ({ event }) => log({ event })`, whose function type declares the return type.

## Checks

Run the repository's lint from the repository root, and confirm that it rejects an exported function, class method, and function-valued class property without a declared return type.
From each affected package root, run the type check, so the compiler checks each declared return type against its function's body.
Does each function a change exports, including one an exported object names by reference or a call returns, declare a return type itself or through its binding?
For each return type a change declares, does it name the result and each failure that callers handle, rather than widening them to `unknown`?
For each change to the lint configuration, does it still reject a higher-order export, a const assertion, and an overload implementation that lack a declared return type?
