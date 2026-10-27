---
name: code-typescript-call-arguments
message: Bind each nested call, `new`, `await`, and function written in an argument object or array to a name, and bind functions only as declarations or typed constants.
requires-tenet: 0.11.0
---

## Rules

Never write a call, a `new` expression, or an `await` inside the arguments of another call or `new` expression; bind its result to a name and pass the name.
This holds through every expression in the arguments, such as an object field, an array element, a template, an operator, a spread, or a type assertion.
A call chain such as `invoices.forAccount({ account }).latest()` is one call, and the calls on its receiver side are not arguments.
Inside a function, class, or embedded markup element written in the arguments, the rule starts afresh, so `orders.map((order) => total({ order }))` is allowed.
A tagged template is a template, not a call: passing one is allowed, and a call in its placeholders counts as inside the arguments that hold it.

A file with the schema role the repository declares under `code-module-file-roles` may nest calls, `new` expressions, and `await` inside arguments, such as `object({ name: string() })`.
The configuration under `assets/` exempts files named `schemas`, the name the example in `code-module-file-roles` gives that role.
A repository that declares another schema file name copies that configuration into its own lint configuration with the name it declares.

Each direct argument of `pipe(...)` or of a `.pipe(...)` method may itself be one call, such as `amount.pipe(map(double), tap(log))`, but never a `new` expression or an `await`.
The arguments of such a step follow the rules above, so `pipe(succeed(load({ id })), map(double))` violates them.
When a step needs an earlier step's result other than its input, or chooses between paths, bind each step's result in a statement, such as `const amount = yield* fetchAmount`.
Leave a pipeline's line layout to the repository's formatter.

Bind to a name each function written as a field, method, or element of an object or array in the arguments of a call or `new` expression.
Objects and arrays nested inside one another count at any depth, but a function, class, call, or embedded markup element in between starts afresh.
A getter or setter is an accessor, not a function field, and stays where it is written.
A function passed directly as an argument stays inline, such as `orders.map((order) => order.id)` or `memoize(() => total({ lines }), [lines])`.
Bind a function to a variable only as a function declaration or as a constant annotated with a function type, such as `const writeEvent: EventSink = ...`.
An annotation such as `any` or `unknown`, or a `satisfies` or `as` clause on the value, is not an annotation with a function type.
A function bound to meet these rules is an independent operation under `code-module-structure-and-control-flow`, even when the call that receives it is its only use.

Configure the repository's lint to enforce these rules wherever a tool supports them, and suppress a finding only as `code-lint-suppressions` allows.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.

Violation: `send({ invoice: await load({ id }) })` nests an `await` and a call inside an argument.
Violation: `prepare({ onEvent: ({ event }) => log({ event }) })` writes a function as a field of an argument object.
Allowed: `const invoice = await load({ id })`, then `send({ invoice })`, and `prepare({ onEvent: writeEvent })` after `const writeEvent: EventSink = ({ event }) => log({ event })`.

## Checks

Run the repository's lint from the repository root and confirm that it rejects a nested call, a function written in an argument object, and an unannotated function constant.
For each call a change adds or edits, does an argument hold a call, `new`, or `await` that is neither a direct pipeline step nor in a schema file?
For each pipeline a change adds, does a step need an earlier step's result other than its input, or choose between paths, without bound statements?
For each object or array a change passes to a call, is every function written in it bound to a name?
For each function a change binds to a variable, including an arrow that uses `this`, is it a function declaration or a constant annotated with a function type?
