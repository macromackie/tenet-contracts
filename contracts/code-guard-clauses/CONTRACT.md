---
name: code-guard-clauses
message: Leave a block early with a guard instead of nesting its remaining work, and never write an `else` after a branch that leaves.
---

## Rules

When a condition means that the rest of a function or loop body does not apply, test it as soon as its value is known and leave with `return`, `throw`, `continue`, or `break`.
A guard may follow other statements once the value it tests is known, such as after an awaited read.
Declare a maximum number of statements for an `if` statement that has no `else` and ends a function.
Never end a function with an `if` statement that has no `else` and holds more statements than that maximum, counting every statement nested inside the `if` at any depth; invert its condition into a guard.

Never write an `else` after a branch that always ends with `return`, `throw`, `break`, or `continue`, whether the `else` holds a block or another `if`, and wherever that branch sits in an `else if` chain.
Never write an `if` statement as the only statement of an `else` block; write `else if`.
Never negate the whole condition of an `if` statement whose `else` holds a block, such as with `!` or a not-equal comparison; swap the branches instead.
Never end a loop body with a `continue` statement, and never write an `else` that holds only `continue`.
In a language with a statement that binds a pattern or leaves, such as `let Some(order) = found else { return Ok(None); };`, use it instead of a `match` or `if let` whose other branch only leaves, when the set is declared outside the repository; `code-exhaustive-branches` governs the sets the repository declares.
An `if` and `else` whose branches both continue the function, such as two different writes, are allowed and are not guards.

Configure the lint to reject an `else` after a branch that leaves, an `if` alone in an `else`, a negated condition with an `else`, a needless `continue`, a `match` that a pattern-binding statement replaces, and a trailing `if` over the declared maximum, wherever the lint supports each rule.

Violation: `if (order.isPaid) { return ship({ order }); } else { return hold({ order }); }` writes an `else` after a branch that returns.
Allowed: `if (order.lines.length === 0) return;`, a blank line, and the remaining work without nesting.

## Checks

Run the repository's lint from the repository root and confirm that it rejects an `else` after a `throw` and an `else if` after a `return`, wherever the lint supports each rule.
For each guard a change adds after other statements, does it test a value that those statements produced?
For each `if` a change adds that holds the rest of a loop body or function, would leaving early when its condition fails remove a level of nesting?
