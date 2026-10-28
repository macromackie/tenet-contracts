---
name: code-typescript-collection-iteration
message: Iterate over TypeScript collections with `for...of`, keep a running total in a `let` that the loop advances, and never call `forEach` or `reduce` or write `for...in`.
requires-tenet: 0.11.0
---

## Rules

Visit the members of an array, `Set`, `Map`, iterator, or other iterable with a `for...of` loop.
Never call a `forEach`, `reduce`, or `reduceRight` method on any value, including an array, `Set`, `Map`, or iterator.
Keep a running total or other accumulated value, except a lookup, in a `let` that a `for...of` loop advances, as `code-typescript-const-bindings` allows.
Build a lookup from a collection, whether a map or a record, as `code-typescript-runtime-keyed-maps` requires, never by folding it.

Read a member's position with `for (const [index, order] of orders.entries())`.
Read a `Map`'s entries with `for (const [key, value] of prices)`, and its keys or values alone through its `keys()` or `values()`.
Read a plain object's own keys or entries with `for...of` over `Object.keys`, `Object.values`, or `Object.entries`.
Never write a `for...in` loop, which also visits inherited keys.

Never write a counting `for` loop whose counter only steps through one array's members in order; write it as `for...of`.
A counting `for` loop whose counter does more, such as an attempt number, a reverse walk, or a neighbor's position, is allowed.

`map`, `filter`, `flatMap`, `some`, `every`, and `find`, with their index and last-member forms, are allowed, because each returns a value.
Use the value each of those calls returns, and never make one a statement that discards it to run its callback's effects.
A function that a dependency's module namespace exports and that takes the collection as an argument, such as `Ledger.forEach(entries, (entry) => postEntry({ entry }))`, is not a collection's method.
Where `code-typescript-effect-scheduling` requires its operator for work over a collection, use that operator instead of a `for...of` loop.

Configure the repository's lint to reject these methods, `for...in` loops, discarded results, and counting loops that only step through an array, suppressing a finding only as `code-lint-suppressions` allows.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.

Violation: `const total = invoices.reduce((sum, invoice) => sum + invoice.amount, 0)` folds with a callback where a loop already sums.
Allowed: `let total = 0;` and then `for (const invoice of invoices) { total += invoice.amount; }`.
Violation: `orders.forEach((order, index) => ship({ index, order }))` runs a callback for each member.
Allowed: `for (const [index, order] of orders.entries()) { ship({ index, order }); }`.
Allowed: `const receipts = orders.filter((order) => order.isPaid).map((order) => createReceipt({ order }))` uses the arrays that `filter` and `map` return.

## Checks

Run the repository's lint from the repository root, and confirm that it rejects `orders.forEach((order) => ship({ order }))`, `orders.reduce((total, order) => total + order.amount, 0)`, a `for...in` loop, and a statement `orders.map((order) => ship({ order }))`.
Confirm that the same lint accepts `Ledger.forEach(entries, (entry) => postEntry({ entry }))`, a dependency namespace's function that takes the collection as an argument.
For each running total or other accumulated value except a lookup that a change adds, does a `let` that a `for...of` loop advances produce it?
For each counting `for` loop a change adds, does its counter do more than step through one array's members in order?
For each `map`, `filter`, `flatMap`, `some`, `every`, or `find` call a change adds, does the code use the value it returns?
For each `forEach`, `reduce`, or `reduceRight` call on a name that a change adds and no namespace import binds, is that name a module namespace rather than a collection?
