---
name: code-typescript-effect-errors
message: Carry each TypeScript failure that a caller can act on as a tagged error in an Effect's error type, and every other failure as a tagged defect.
requires-tenet: 0.11.0
---

## Rules

Treat a failure as expected when any caller or user could act differently because of it, such as a requested record that does not exist or a dropped request.
Treat every other failure as a defect, such as a record that the same object wrote now missing or corrupt, which means the code's own invariant broke.
An empty result, such as a search that matches nothing, is a value, but a lookup that finds no record for a caller's identifier is an expected failure.

Fail with a tagged error class for each expected failure, such as `class InvoiceNotFound extends Schema.TaggedError<InvoiceNotFound>()('InvoiceNotFound', { invoice: Schema.String }) {}`, and treat its tag as the failure's stable code.
Use `Effect.die`, `Effect.orDie`, or `throw` only for a defect, and give it a tagged error class with fields that locate it, such as `new InvoiceMissing({ invoice })`.
Give each tagged error the fields its handler needs, such as the invoice number or the provider's status, never only a message string.
Give each failure that a handler treats differently its own tag; a field may refine a tag only with a member of a closed set, such as a provider's refusal kind, never with a free-form code string.
Never build or extend a bare runtime error, such as `new Error(message)` or `class InvoiceError extends Error`, and never fail, die, or throw with a string or plain object.
A test fake that stands in for a dependency may throw what that dependency throws, such as the `TypeError` of a failed network request.

Pass an expected failure up in the error type, unchanged or wrapped in a higher-level tagged error, until the code that decides what happens next handles it by tag, such as with `Effect.catchTag`.
Never return `null`, `undefined`, `false`, or an `{ ok: false }` object for an expected failure, and never discard one, such as with `Effect.ignore`, `Effect.option`, or `Effect.orElseSucceed`.
A handler that catches every failure at once, such as `Effect.catch`, is allowed when it branches on each tag, such as by passing the error to a function that switches on its `_tag` with a case for every tag.

Wrap each foreign call that can throw or reject, such as `fetch`, JSON parsing, or a storage or library call, once where it is called, with `Effect.tryPromise` or `Effect.try`.
Map its failure in the `catch` option to a tagged error class that keeps the caught value as its `cause`, such as `RequestDropped` for a failed `fetch`.
Never write a `catch` clause or call a promise's `then`, `catch`, or `finally` method, though a `try` with only a `finally` clause may release a resource.
Declare every function that returns a promise `async`, even one without `await`, write `return await` for each promise it returns, and discard a promise only with `void`.

Run an Effect, such as with `Effect.runPromise`, only at an entry point that a framework or runtime calls, such as a request or click handler, and never build one in a bare statement, such as `Effect.fail(new InvoiceNotFound({ invoice }));`, which never runs it.
Map each tag to that entry point's response there, such as a 404 response for `InvoiceNotFound` or a retry prompt for a dropped request.
Elsewhere, compose Effects with `pipe` as `code-typescript-call-arguments` allows, and write the bound statements that it requires, such as `const invoice = yield* readInvoice({ id })`, in an anonymous generator that `Effect.gen` takes, or that `Effect.fn('name')` takes for a function whose calls a trace records, never with `Effect.withSpan` around the function's result.
Give each entry point one defect handler that records the defect and ends its unit of work, such as a server's 500 response or a command's error exit status.
Wrap each route of a user interface in an error boundary, and pass it the defects of that route's event handlers and asynchronous reads, which it cannot catch itself.
Catch a defect only in an entry point's defect handler, and never log a failure or defect and then continue, whether in a component or anywhere else.

Configure the repository's lint to reject bare runtime errors, thrown literals, `catch` clauses, inline `catch` handlers, the other promise forms above, and `Effect` calls written as bare statements, suppressing a finding only as `code-lint-suppressions` allows.
Keep off any lint rule that reports a tagged error class's declaration, such as one requiring `new` before each call whose name ends in `Error`.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.

Violation: `if (!response.ok) { throw new Error('the payment provider refused the refund'); }` turns a provider refusal into an untyped exception.
Violation: `Effect.orDie(refunding)` after `const refunding = refund({ invoice })` turns the provider's refusals and outages into defects.
Violation: `readInvoice({ invoice })` throws `new Error('invoice row missing')` for a row that the same object wrote, so the defect carries neither a tag nor the invoice number.
Violation: a component calls `readInvoice({ id }).catch(() => {})`, so a dropped request shows no retry and a defect never reaches the route's error boundary.
Violation: `function readInvoice(signal: Readonly<AbortSignal>) { return fetch(INVOICE_URL, { signal }).then((response) => response.json()) }` chains the promise with `then` and returns it from a function that is not `async`.
Violation: a click handler calls `save({ invoice })` as a statement, so the promise is discarded without `void`.
Violation: `Effect.fail(new InvoiceNotFound({ invoice }));` as a statement inside `Effect.gen` builds the failure and drops it, so the lookup succeeds.
Allowed: `return yield* new RefundRefused({ invoice, status })`, which the request handler handles with `Effect.catchTag('RefundRefused', ...)`.
Allowed: `throw new InvoiceMissing({ invoice })` inside `Effect.gen` for a row that the same object wrote, and `return yield* new InvoiceNotFound({ invoice })` for a number a caller supplied.
Allowed: `async function readInvoice(signal: Readonly<AbortSignal>): Promise<unknown> { const response = await fetch(INVOICE_URL, { signal }); return await response.json() }`, which `Effect.tryPromise({ catch: buildRequestDropped, try: readInvoice })` calls.

## Checks

Run the type check from each package root against effect 4.0.0 or later; an Effect's error type lists every tag it can fail with.
Run the repository's lint with type information from the repository root, and confirm that it reports no type configuration error and rejects each form the lint rule names.
For each failure a change adds, could any caller or user act differently because of it, and is it a tagged error if so and a tagged defect otherwise?
For each tagged error a change adds, which code handles it by tag, and does every Effect between them pass it up in its error type?
For each `Effect.ignore`, `Effect.option`, `Effect.orElseSucceed`, or catch-all handler a change adds, does it discard an expected failure or skip a tag?
For each foreign call a change adds, is it wrapped once where it is called, with its failure mapped to a tagged class that keeps the cause?
For each entry point a change adds, where is its one defect handler, and does the change run an Effect or catch a defect anywhere else?
