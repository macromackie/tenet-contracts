---
name: code-typescript-const-bindings
message: Declare TypeScript variables with `const`, give every `let` its first value where it is declared, and choose a value with a function rather than by assigning in each branch.
---

## Rules

Declare every TypeScript variable that is never reassigned with `const`, and never declare one with `var`.
Give every `let` its first real value in its declaration, never no initializer, `null`, or `undefined` to fill in later.
Reassign a `let` only inside a loop that carries its value from one pass to the next, such as a counter, a running total, or a polled value.

Never choose a value by assigning a variable in each branch of an `if`, `switch`, or `try` statement; return it from a function instead, as `code-conditional-expressions` allows.
A function that only chooses and returns a value is an independent operation even when it has one caller.
Never take a value from a call that can throw by assigning a variable inside a `try` block; when the function making that call handles the call's failure, take the value through a call that returns the value or a typed failure, such as a schema decode.

Suppress the `let` rule only as `code-lint-suppressions` requires.
Configure the lint to reject `var`, a `let` that is never reassigned, and a `let` with no initializer or with a `null` or `undefined` initializer.

Violation: `let label; if (order.isPaid) { label = paidLabel; } else { label = draftLabel; }` declares a `let` without a value and assigns it in each branch.
Allowed: `const label = orderLabel({ order })`, where `orderLabel` returns a label from each branch, and `let total = 0` that a loop over line items advances.

## Checks

Run the repository's lint from the repository root and confirm that it rejects a `let` with no initializer.
For each function a change adds to choose a value, does it only choose and return that value?
For each `let` a change adds, does a loop advance it from a real first value, rather than a branch filling it in?
For each `let` suppression a change adds, does it meet `code-lint-suppressions`?
