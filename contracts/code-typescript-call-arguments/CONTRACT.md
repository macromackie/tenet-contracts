---
name: code-typescript-call-arguments
message: Bind to a name each nested call, `new`, `await`, and function written in an argument object or array, and each awaited or `yield*` value before reading a member.
requires-tenet: 0.11.0
---

## Rules

Never write a call, a `new` expression, or an `await` inside the arguments of another call or `new` expression; bind its result to a name and pass the name.
This holds through every expression in the arguments, such as an object field, an array element, a template, an operator, a spread, or a type assertion.
A call chain such as `invoices.listForAccount({ account }).findLatest()` is one call, and the calls on its receiver side are not arguments.
Inside a function, class, or embedded markup element written in the arguments, the rule starts afresh, so `orders.map((order) => computeTotal({ order }))` is allowed.
A tagged template is a template, not a call: passing one is allowed, and a call in its placeholders counts as inside the arguments that hold it.

A file with the schema or errors role the repository declares under `code-module-file-roles` may nest calls, `new` expressions, and `await` inside arguments, such as `Schema.Struct({ tags: Schema.Array(Schema.String) })` or the schema fields of a tagged error class.
The configuration under `assets/` exempts files named `schemas` and `errors`, the names the example in `code-module-file-roles` gives those roles.
A repository that declares another schema or errors file name copies that configuration into its own lint configuration with the name it declares.

Each direct argument of `pipe(...)` or of a `.pipe(...)` method may itself be one call, such as `amount.pipe(map((price) => applyDiscount({ price })), tap((price) => recordPrice({ price })))`, but never a `new` expression or an `await`.
The arguments of such a step follow the rules above, so `pipe(succeed(readAmount({ id })), map((price) => applyDiscount({ price })))` violates them.
When a step needs an earlier step's result other than its input, or chooses between paths, bind each step's result in a statement, such as `const amount = yield* readAmount({ id })`.
Leave a pipeline's line layout to the repository's formatter.

Bind the value of an `await` or `yield*` expression to a name before reading its members, such as `const invoice = await readInvoice({ id })`, then `invoice.status`.
Calling a method and indexing read a member too, and the rule holds through parentheses and type or non-null assertions, such as `((await read()) as Reply).result`.
Destructuring the value in the declaration that binds it, such as `const { status } = await readInvoice({ id })`, counts as binding it.

Bind to a name each function written as a field, method, or element of an object or array in the arguments of a call or `new` expression.
Objects and arrays nested inside one another count at any depth, but a function, class, call, or embedded markup element in between starts afresh.
A getter or setter is an accessor, not a function field, and stays where it is written.
A function passed directly as an argument stays inline, such as `orders.map((order) => order.id)` or `memoize(() => computeTotal({ lines }), [lines])`.
Bind each such function as `code-typescript-const-bindings` requires, such as `const writeEvent: EventSink = ...`.
A function bound to meet these rules is an independent operation under `code-module-structure-and-control-flow`, even when the call that receives it is its only use.

Configure the repository's lint to enforce these rules wherever a tool supports them, and suppress a finding only as `code-lint-suppressions` allows.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.

Violation: `send({ invoice: await readInvoice({ id }) })` nests an `await` and a call inside an argument.
Violation: `prepare({ onEvent: ({ event }) => log({ event }) })` writes a function as a field of an argument object.
Allowed: `const invoice = await readInvoice({ id })`, then `send({ invoice })`, and `prepare({ onEvent: writeEvent })` after `const writeEvent: EventSink = ({ event }) => log({ event })`.
Violation: `const status = (await readInvoice({ id })).status` and `(yield* readOrder({ id })).total` read a member of a value that no name holds.
Allowed: `const order = yield* readOrder({ id })`, then `order.total`, or `const { total } = yield* readOrder({ id })`.

## Checks

Run the repository's lint from the repository root and confirm that it rejects a nested call, a function in an argument object, and a member read from an `await`.
For each call a change adds or edits, does an argument hold a call, `new`, or `await` that is neither a direct pipeline step nor in a schema or errors file?
For each pipeline a change adds, does a step need an earlier step's result other than its input, or choose between paths, without bound statements?
For each object or array a change passes to a call, is every function written in it bound to a name?
For each member a change reads from an `await` or `yield*` expression, through parentheses or assertions, is the value bound to a name first?
