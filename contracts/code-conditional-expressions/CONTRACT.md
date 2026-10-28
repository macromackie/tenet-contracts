---
name: code-conditional-expressions
message: Choose values with statements, lookups, pattern matching, or named functions, and markup with extracted components, not conditional operators, complementary pairs, or immediately invoked functions, within a declared logical-operator maximum.
requires-tenet: 0.11.0
---

## Rules

Never write a conditional operator expression, such as `isReady ? total : 0` or `total if is_ready else 0`, whether it is nested or not and whether it spans one line or several.
Choose a value with an `if` statement, a lookup table keyed by a closed set of values, a `switch` or `match` statement, or a function that names the choice, such as `Math.min`.
Fill a lookup table only with values or functions, never with calls that run when the table is built.
A null-coalescing default, such as `name ?? 'anonymous'`, is not a conditional operator and is allowed.
Do not imitate a conditional operator with logical operators, such as `isReady && total || 0`.
In a language without a conditional operator, an `if` or `match` expression whose branches are braced blocks is allowed.

Choose between branches of markup in a component whose `if` statements, or `switch` cases for a closed set, each return one branch, extracted from any larger markup.
Never write sibling children on a condition and its negation, such as `{isPaid && <Receipt />}` beside `{!isPaid && <PaymentForm />}`.
Show one piece of markup or nothing with one `&&` child where it is rendered, such as `{isPaid && <Receipt />}`.
Give a component a visibility prop, such as `isVisible`, only when it stays mounted while hidden to keep its elements' state, such as scroll position, or to animate out.
That component hides itself with styles while it stays mounted.
Never return nothing from a component when a boolean prop alone, or its negation, decides it, such as `if (!isVisible) { return null; }`.

Never compute a value with an immediately invoked function, a function expression called where it is written, such as `const shippingDays = (() => { ... })()`.
A value that needs statements comes from a named function called by name, such as `const shippingDays = chooseShippingDays({ order })`.
When that function chooses the value, it only chooses and returns it.
A function written to replace an immediately invoked function is an independent operation under `code-module-structure-and-control-flow`, even when it has one caller.
A callback passed to an array method, a memoizing hook, or any other call is not an immediately invoked function, even when that call runs it at once.

Declare a maximum number of logical operators in one expression, counting `&&`, `||`, and `??`, or words such as `and` and `or`, together.
Count every logical operator nested inside a chain of logical operators with that chain, so `!(isPaid && isShipped) && isOpen` and `name ?? alias ?? 'anonymous'` each hold two.
A call's callee and arguments, an object literal's values, a `function` expression's body, and a named markup element's attributes and children start their own count.
An arrow function's body, a `new` expression's arguments, an array element, a template placeholder, and a markup fragment's children count with the chain around them.
Split a longer expression into named booleans, guard clauses, or a named predicate, never a call that only restarts the count, like `Boolean(isOpen && isShipped) && isPaid && isReady`.

Configure the repository's lint to reject the conditional operator, an immediately invoked function, and an expression over the logical-operator maximum, wherever the lint supports each rule.
Configure it also to reject sibling children on a condition and its negation, and a component that returns nothing when a boolean prop alone decides it.
Where the repository's lint can load a file in this contract's `assets/` folder, load it from the repository's own lint configuration, which may override the file's maximum.

Violation: `const text = typeof content === 'string' ? content : content.map((part) => readText({ part })).join('\n')` puts a call chain in one branch of a conditional operator.
Violation: `{isPaid && <Receipt />}` beside `{!isPaid && <PaymentForm />}` chooses between two branches of markup with sibling children on a condition and its negation.
Violation: `function ShippingBanner({ isVisible, carrier }: ShippingBannerProps)` declares the framework's node type and starts with `if (!isVisible) { return null; }`, so the component decides whether its caller shows it.
Violation: `const shippingDays = (() => { ... })()` holds `if (order.isRush) { return RUSH_DAYS; }`, a blank line, and `return STANDARD_DAYS;`, so it computes a value with an immediately invoked function.
Violation: `if (order.isPaid && order.isShipped && order.isOpen && !order.isRefunded)` holds three logical operators against a declared maximum of two.
Allowed: `if (typeof content === 'string') { return content; }`, a blank line, and `return content.map((part) => readText({ part })).join('\n');` make each branch its own statement.
Allowed: `function InvoiceAction({ isPaid }: InvoiceActionProps)` holds `if (isPaid) { return <Receipt />; }`, a blank line, and `return <PaymentForm />;`, and the invoice's markup renders `<InvoiceAction isPaid={invoice.isPaid} />`.
Allowed: a caller writes `{isVisible && <ShippingBanner carrier={carrier} />}`, and a document preview that keeps its scroll position while hidden takes `isVisible` and hides itself with styles.
Allowed: `const shippingDays = chooseShippingDays({ order })` calls a named function that only chooses and returns the shipping days.
Allowed: `const isDeliverable = order.isPaid && order.isShipped` and `if (isDeliverable && order.isOpen && !order.isRefunded)` each hold at most two logical operators.

## Checks

Where the lint supports each rule, run it from the repository root to confirm it rejects each form that this contract configures it to reject.
Search the change for conditional operator expressions and for `&&` followed by `||` in one expression.
For each value a change chooses by condition, is the choice made by a statement, a lookup, a `switch` or `match`, a named function, or a null-coalescing default?
For each change to the lint configuration, does it keep the logical-operator maximum at its declared value?
For each expression a change adds that the lint does not count, such as in a language without the rule, does it stay within the declared maximum?
For each call a change wraps around part of a condition, does the call do more than restart the logical-operator count?
Is each markup choice in a change one `&&` child, a branch an extracted component returns, or a component mounted while hidden to keep element state or animate out?
