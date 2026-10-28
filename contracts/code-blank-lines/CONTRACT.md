---
name: code-blank-lines
message: Separate a block's logical phases, control flow, returns, throws, calls, and multi-line declarations and expressions from neighboring code with one blank line.
requires-tenet: 0.11.0
---

## Rules

Separate the logical phases of a block, such as reading input, deciding, and producing a result, with one blank line.
Put one blank line before each control-flow statement, such as `if`, `for`, `while`, `switch`, `match`, or `try`, unless it is the first statement of its block.
Put one blank line after each control-flow statement, counted from its last line, unless it is the last statement of its block.
Space each `return`, `throw`, or `raise` statement like a control-flow statement.
Space each call or `await` statement, such as `notify({ order });`, `new Receipt({ order });`, `void flush();`, or `await save({ order });`, like a control-flow statement.
Space each multi-line declaration, such as a function, an interface, or an exported object constant, and each multi-line assignment or expression statement like a control-flow statement.

Consecutive call statements need no blank line between them, even when one spans several lines.
A function's overload signatures and its implementation need no blank lines between them.
A `break` or `continue` statement or a one-line assignment, such as `used += length;`, needs a blank line only where a neighboring statement requires one.
An import, a re-export, or a list of exported names needs a blank line only where a neighboring statement requires one, even when it spans several lines.
Apply these rules to a statement whose braced body holds one statement, such as `if (orders.length === 0) { return []; }`, as well as to a longer one.
Treat `else`, `catch`, and `finally` clauses and the cases of a `switch` or `match` as parts of their statement, which take no blank lines between them.

Put a comment that describes a statement directly above it, and put the blank line above the comment.
Where the repository's formatter requires more blank lines, such as two around a top-level function, keep its count.

Configure the repository's formatter or lint to enforce this spacing wherever a tool supports it.
Where the repository's lint can load the configuration in this contract's `assets/` folder, extend it from the repository's own lint configuration.

Violation: `const order = decode({ raw });` is directly followed by `notify({ order });`, which is directly followed by `return order;`.
Allowed: `const order = decode({ raw });`, a blank line, `notify({ order });` and `audit({ order });` on consecutive lines, another blank line, and `return order;`.

## Checks

Run the repository's formatter and lint from the repository root.
Does each control-flow, `return`, `throw`, `raise`, call, or `await` statement a change adds or moves have a blank line on each side, except at block edges and between calls?
Does each multi-line declaration, assignment, or expression statement a change adds or moves have a blank line on each side, except at block edges and between calls?
For each block a change adds or rewrites, does a blank line separate each of its logical phases?
