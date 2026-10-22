---
name: code-typescript-class-declarations
message: Declare a TypeScript class only where a runtime or library requires one, write every other unit that holds dependencies or state as a factory function, and give each class field a readonly private name.
---

## Rules

Declare a class only where a runtime or library requires one: a class the runtime instantiates, such as a stateful actor, a container, or a worker entry point; a tagged error class that `code-typescript-effect-errors` requires; or a service key class with an empty body that an effect or dependency-injection library requires to name a service.
Write every other unit that holds dependencies or state, such as a store, a client, or a driver, as a factory function that returns named functions that close over them, such as `createInvoiceStore({ sql })` returning `{ settleInvoice }`.
Keep a factory's storage handle and other dependencies in its closure, and never return them beside its functions.
A plain record that holds values and no storage handle, such as `type InvoiceAccount = { apiUrl: string; token: string }` passed as `requestInvoices({ account, path })`, is data and needs no factory.
Extend only the base class that the runtime or library requires, and never extend an owned class or declare an `abstract` class.
Declare each field of a class `readonly` with a private name, such as `readonly #storage: Storage`, and never use the `private`, `protected`, or `public` keywords or constructor parameter properties.
A field that the runtime base class declares for subclasses to set, such as a container's `defaultPort`, keeps the name the base class gives it and carries the `override` modifier, such as `override readonly defaultPort = 8080`.
A `readonly` field may hold a collection that the class changes, such as `readonly #tokens = new Map<Purpose, Token>()`.
Read `this` in every method of a class except an `override` of a method that the runtime or library base class declares; any other method that reads nothing from the instance is a function.
Enable `erasableSyntaxOnly`, which rejects parameter properties, and `noImplicitOverride`, which requires `override` on each field and method that the base class declares, in every package's compiler configuration.
Enforce the other rules with the repository's lint, and suppress a finding only as `code-lint-suppressions` allows, such as for an exported subclass that only passes a dependency to a runtime class.

Violation: `class InvoiceApi { readonly #settings: Settings; constructor({ settings }: InvoiceApiInput) { this.#settings = settings; } }` holds a client's dependencies in an owned class.
Allowed: `createInvoiceApi({ settings })` returns `{ requestInvoices }`, and `class InvoiceObject extends RuntimeObject` is a class the runtime instantiates.

## Checks

Run the repository's lint from the repository root and each package's type check from its package root.
Does a change remove `erasableSyntaxOnly` or `noImplicitOverride` from a compiler configuration, or a class rule from the lint configuration?
For each class a change adds, which runtime or library instantiates or requires it?
For each factory a change adds, does its result hold only named functions, with the storage handle and other dependencies left in the closure?
For each suppression of these rules, does its reason name the runtime or library that requires the exception?
