---
name: code-typescript-input-immutability
message: Never change a value that a TypeScript function received as a parameter or sort an array in place, and return a new value instead.
---

## Rules

Never assign to a parameter, or to a property at any depth of an object that a parameter holds, such as `order.status = status` or `order.totals.net = net`.
Never call a method that changes a collection a parameter holds at any depth, such as `push`, `splice`, `sort`, `reverse`, `set`, `add`, or `delete`, and never pass a parameter's value as the target of `Object.assign`.
Changing a field of `this` in the class's own method, such as `this.#cache.set(key, value)`, is not changing a parameter.
A collection or object that the function itself created may change before the function returns it, except through `sort` or `reverse`.
Sort or reverse an array with `toSorted` or `toReversed`, never with `sort` or `reverse`.

Configure the lint to reject assignment to a parameter or its properties, a changing method call or `Object.assign` whose target starts at a parameter, and in-place `sort` and `reverse`.

Violation: `function addLine({ order, line }: AddLineInput) { order.lines.push(line); }` changes a collection the caller passed in.
Allowed: `function addLine({ order, line }: AddLineInput) { return { ...order, lines: [...order.lines, line] }; }` returns a new order.

## Checks

Run the repository's lint from the repository root and confirm that it rejects `order.lines.push(line)` where `order` is a parameter.
For each value a change modifies in place, did the same function create it?
