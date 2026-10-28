---
name: code-typescript-function-scoping
message: Declare a named TypeScript function inside another function only when it captures that function's scope, and move every other one to the top level of its file.
requires-tenet: 0.11.0
---

## Rules

Declare a named function other than a component inside another function only when it captures a parameter, a local, or the receiver, such as `this`, of an enclosing function.
Move every other named nested function to the top level of the same file, unexported, above its caller as `code-declaration-order` requires, and any nested component to its own file.
A named nested function is a function declaration, or a function bound to a variable, anywhere in another function's body, including inside a block.
This holds in every function, including a method, a component, a generator, a factory, and a test's callback.

Top-level names of the same file, imported names, the language's global names, and the function's own name are not captures, so a function that reads only them moves.
A type is not a capture either, so a function that names only an enclosing function's type parameter moves and declares that type parameter itself.
A call to another nested function captures the enclosing scope until that function moves, so check each of its callers again after a move.
A handler that a user interface component declares and that reads no props, state, or other local captures nothing, so it moves above the component.
A helper that a test's callback declares and that captures nothing moves to the top level of the test file, above the statements that register its cases.

A function written inline as a call's argument or a markup attribute's value, such as a callback passed to `map` or to a combinator, stays inline.
An event handler that needs a block is the exception, which `ui-react-typescript-jsx-attributes` moves into a named function.

Configure the repository's lint to report each named nested function that captures nothing, including in test code.
Where the repository's lint can load the configuration in this contract's `assets/` folder, extend it from the repository's own lint configuration.
The shipped file can miss a nested function that reads a top-level declaration of its file, or one declared directly in a component framework's hook callback.
Review covers each such function that a change adds.
The shipped file also reports an arrow function that captures nothing and that another function returns directly, so declare that one by name at the top level too.
Suppress a finding only as `code-lint-suppressions` allows, and exempt generated files by a declared path pattern.

Violation: `settleInvoice({ invoice })` declares `computeTotal`, which reads only its own argument and a top-level constant, inside its body.
Violation: an `InvoiceButton` component declares an `onClick` handler that reads no props or state, and a test's callback declares a `buildInvoice` helper that reads nothing from it.
Allowed: the file declares `computeTotal` at its top level, then the exported `settleInvoice`, which calls it.
Allowed: `scaleOrders({ factor, orders })` declares `scale`, which reads `factor`, and passes `(order) => scale({ order })` inline to `orders.map`.

## Checks

Run the repository's lint from the repository root, and confirm it reports a nested function reading only its arguments in a block, a method, a component, and a test.
For each named function that a change declares inside another function, which parameter, local, or receiver of an enclosing function does it read?
For each function that a change moves to the top level, is it unexported and declared above its caller?
Does a change turn the rule off, stop it checking functions bound to variables, or narrow the files it covers?
