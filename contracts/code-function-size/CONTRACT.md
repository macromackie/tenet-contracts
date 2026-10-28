---
name: code-function-size
message: Keep every function within lint-enforced length, nesting, callback, markup depth, and complexity limits, and give each case of a branch on a closed set its own function.
requires-tenet: 0.11.0
---

## Rules

Declare a maximum function length in lines, counted without blank lines and comments, a maximum number of statements, a maximum block nesting depth, and a maximum callback nesting depth.
Count every statement in a function's body, including those inside its blocks, and leave each nested function to its own count.
Enforce all four limits with the repository's lint on every function, method, constructor, and closure, including test code.
Declare a maximum complexity per function in each measure that a language's lint computes, such as cyclomatic and cognitive complexity, and enforce it likewise.
Declare a maximum depth of elements nested inside one another in markup written in code, and enforce it with the repository's lint, including test code.
Leave a language without any of these limits only by declaring the language, the limit, and the reason beside the limits, such as that no lint counts statements.
Count an element's depth as the number of elements and fragments enclosing it, including through a condition, callback, call, local variable, or attribute value.
Move the markup past that depth into a child component, which starts its own count.
A repository may declare a different limit for one kind of function, with the reason beside the limits, such as a longer length for components that return markup.
A lint configuration may extend a file that this contract ships under `assets/`, and may override any limit that file sets.
That file allows 10 statements, a cyclomatic complexity of 10, and a cognitive complexity of 15 per function.
That file allows 60 lines for functions in `.tsx` and `.jsx` files, because a component's markup adds lines that hold no logic.
That file allows a markup depth of 6 through the markup plugin, which a repository whose code holds markup turns on in its own lint configuration.
Suppress a limit only as `code-lint-suppressions` allows, such as for a generated table.

When a function branches on the members of a closed set, such as a run's phase or an event's kind, give each case its own function, and keep the branching function to choosing the case.
Name each case's function for the operation it performs, such as `advanceSubmitted`; it is an independent operation even when the branching function is its only caller.
A case may stay inline when its only work is one value or one call whose arguments contain no function, such as `advanceStarting({ run })`.

Violation: under a declared maximum of 6, `OrderPage` renders each order's link 7 levels below its outermost element, inside the callback that maps the orders.
Allowed: that callback renders `<OrderLink key={order.id} order={order} />`, and `OrderLink` returns the list item and its link.
Violation: `advance({ run })` switches on the run's phase and holds 40 lines of work for each phase inline.
Allowed: `advance({ run })` switches on the run's phase and each case calls one function, such as `advanceStarting({ run })`.

## Checks

Run the repository's lint from the repository root.
For each call, callback, or local variable that a change places inside markup and that yields markup, does the depth counted through it stay within the declared maximum?
For each change to the lint configuration, does it keep every declared limit at its declared value?
Does each limit declared for one kind of function have its reason beside it?
For each language the repository lints, does its lint enforce each declared limit, or does a declaration beside the limits name the language, limit, and reason?
For each branch on a closed set that a change adds or grows, does every case either call its own function or hold only one value or one call without a function argument?
