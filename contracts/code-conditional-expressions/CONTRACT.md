---
name: code-conditional-expressions
message: Choose between values with statements, lookups, or pattern matching, never with a conditional operator.
---

## Rules

Never write a conditional operator expression, such as `ready ? total : 0` or `total if ready else 0`, whether it is nested or not and whether it spans one line or several.
Choose a value with an `if` statement that assigns or returns it, a lookup table keyed by a closed set of values, a `switch` or `match` statement, or a function that names the choice, such as `Math.min`.
Fill a lookup table only with values or functions, never with calls that run when the table is built.
A null-coalescing default, such as `name ?? 'anonymous'`, is not a conditional operator and is allowed.
Do not imitate a conditional operator with logical operators, such as `ready && total || 0`.
In a language without a conditional operator, an `if` or `match` expression whose branches are braced blocks is allowed.
Configure the repository's lint to reject the conditional operator wherever the lint supports that rule.

Violation: `const text = typeof content === 'string' ? content : content.map((part) => readText({ part })).join('\n')` puts a call chain in one branch of a conditional operator.
Allowed: `if (typeof content === 'string') { return content; }`, a blank line, and `return content.map((part) => readText({ part })).join('\n');` make each branch its own statement.

## Checks

Run the repository's lint from the repository root and confirm that it rejects the conditional operator.
Search the change for conditional operator expressions and for `&&` followed by `||` in one expression.
For each value a change chooses by condition, is the choice made by a statement, a lookup, a `switch` or `match`, or a null-coalescing default?
