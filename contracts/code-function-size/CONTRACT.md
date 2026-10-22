---
name: code-function-size
message: Keep every function within lint-enforced length, nesting, and callback limits, and give each case of a branch on a closed set its own function.
---

## Rules

Declare a maximum function length in lines, counted without blank lines and comments, a maximum block nesting depth, and a maximum depth of callbacks nested inside one another.
Enforce all three limits with the repository's lint on every function, method, constructor, and closure, including test code.
Suppress a limit only as `code-lint-suppressions` allows, such as for a generated table.

When a function branches on the members of a closed set, such as a run's phase or an event's kind, give each case its own function, and keep the branching function to choosing the case.
Name each case's function for the operation it performs, such as `advanceSubmitted`; it is an independent operation even when the branching function is its only caller.
A case may stay inline when its only work is one value or one call whose arguments contain no function, such as `advanceStarting({ run })`.

Violation: `advance({ run })` switches on the run's phase and holds 40 lines of work for each phase inline.
Allowed: `advance({ run })` switches on the run's phase and each case calls one function, such as `advanceStarting({ run })`.

## Checks

For each change to the lint configuration, does it keep all three declared limits at their declared values?
For each branch on a closed set that a change adds or grows, does every case either call its own function or hold only one value or one call without a function argument?
