---
name: code-typescript-doc-comment-coverage
message: Give every exported TypeScript function and class a doc comment, and fail checks when one is missing.
requires-tenet: 0.11.0
---

## Rules

Apply these rules to the functions and classes that a TypeScript module exports, in maintained source, tests, and scripts, and not in generated or copied third-party source.
Give a doc comment to every exported function, including an async or generator function, whether exported by its declaration, through an export list, or as the default export.
Treat an exported constant whose value is a function as an exported function, whether it binds a function expression, as `code-typescript-const-bindings` allows, or a function that a call returns.
Treat an exported component that returns markup as an exported function.
Give a doc comment to every exported class, including an error class and a service key class.
An exported schema class, such as one that `code-typescript-effect-schemas` describes, is an exported class and needs a doc comment.
Give an overloaded function one doc comment above its first signature; its other signatures and its implementation need none.

An exported type, interface, enum, or constant whose value is not a function, such as a schema constant, an object, or an effect, needs no doc comment.
A re-export needs no doc comment, because the module that declares the function or class documents it.

A doc comment that `code-comment-content` forbids, such as `/** Reads the invoice. */` above `readInvoice`, does not satisfy these rules.
Start each of these doc comments with its description, because a doc comment that holds only tags, such as `/** @internal */`, documents nothing.
Write each as a block doc comment directly above the declaration, with no blank line between, in the prose form and layout `code-comment-form` requires.
A line comment is not a doc comment.

Enforce these rules with the repository's lint over every package, and fail checks on each missing doc comment and each doc comment without a description.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
That configuration offers no autofix, because the only text that a tool can insert is the empty doc comment that `code-comment-form` forbids.
Review what that configuration cannot see: a declaration that an export list or default export names, and a function that a call returns, such as a wrapped component.
Exempt a declaration only with the suppression that `code-lint-suppressions` describes.

Violation: `export async function settleInvoice({ invoice }: SettleInvoiceInput): Promise<Receipt>` carries no doc comment, or carries `/** Settles the invoice. */`, which restates its name.
Allowed: `/** Marks the invoice paid, and fails with InvoiceRefunded when a refund already closed it. */` sits above it, and the exported `SettleInvoiceInput` type carries none.

## Checks

Run the repository's lint from the repository root, and confirm that it fails on an undocumented exported function and exported class.
Does each function or class that a change exports through an export list, a default export of a name, or a call's result carry a doc comment?
For each doc comment that a change adds to satisfy these rules, what does it tell callers that the name and signature do not?
For each change to the lint configuration, does it keep every declaration kind above required and skip no declaration by name?
