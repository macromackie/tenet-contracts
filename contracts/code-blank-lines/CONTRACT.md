---
name: code-blank-lines
message: Separate a block's logical phases, and each control-flow statement inside it, from neighboring code with one blank line.
requires-tenet: 0.11.0
---

## Rules

Separate the logical phases of a block, such as reading input, deciding, and producing a result, with one blank line.
Put one blank line before each control-flow statement, such as `if`, `for`, `while`, `switch`, `match`, or `try`, unless it is the first statement of its block.
Put one blank line after each control-flow statement, counted from its last line, unless it is the last statement of its block.
Apply these rules to a one-line statement, such as `if (!found) return [];`, as well as to a braced one.
A jump statement, such as `return`, `throw`, `break`, or `continue`, is not a control-flow statement under these rules.
Treat `else`, `catch`, and `finally` clauses and the cases of a `switch` or `match` as parts of their statement, which take no blank lines between them.
Put a comment that describes a statement directly above it, and put the blank line above the comment.
Configure the repository's formatter or lint to enforce this spacing wherever a tool supports it.
Where the repository's lint can load the configuration in this contract's `assets/` folder, extend it from the repository's own lint configuration.

Violation: `const order = decode({ raw });` is directly followed by `if (order === undefined) {`.
Allowed: `const order = decode({ raw });`, then a blank line, the `if` statement, another blank line, and `return order;`.

## Checks

Run the repository's formatter and lint from the repository root.
For each control-flow statement a change adds or moves, is there a blank line before it unless it opens its block, and after it unless it closes its block?
For each block a change adds or rewrites, does a blank line separate each of its logical phases?
