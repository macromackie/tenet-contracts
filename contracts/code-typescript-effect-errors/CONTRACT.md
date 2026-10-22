---
name: code-typescript-effect-errors
message: Carry each expected TypeScript failure as a tagged error in an Effect's error type until code handles it by tag, and throw or die only for broken invariants.
---

## Rules

An expected failure is one a correct program can meet, such as a rejected request, a missing record, invalid input, or a provider error.
Fail with a tagged error class for each expected failure, such as `class InvoiceNotFound extends Schema.TaggedError<InvoiceNotFound>()('InvoiceNotFound', { invoice: Schema.String }) {}`, and treat its tag as the failure's stable code.
Give each tagged error the fields its handler needs, such as the invoice number or the provider's status, never only a message string.
Give each failure that a handler treats differently its own tag; a field may refine a tag only with a member of a closed set, such as a provider's refusal kind, never with a free-form code string.
A result that may be empty, such as a search that matches nothing or an optional setting left unset, is a value, not a failure; a lookup by identity that finds no record is an expected failure.
Pass an expected failure up in the error type, unchanged or wrapped in a higher-level tagged error, until the code that decides what happens next handles it by tag, such as with `Effect.catchTag`.
Never `throw`, return `null`, `undefined`, `false`, or an `{ ok: false }` object, or log and continue for an expected failure.
Never discard an expected failure, such as with `Effect.ignore`, `Effect.option`, or `Effect.orElseSucceed`.
A handler that catches every failure at once, such as `Effect.catch`, is allowed when it branches on each tag, such as by passing the error to a function that switches on its `_tag` with a case for every tag.
Wrap a dependency's promise or throwing call with `Effect.tryPromise` or `Effect.try`, and map its failure to a tagged error in the `catch` option.
Use a defect, such as `Effect.die` or `Effect.orDie`, only for a broken invariant, such as a state the types already exclude.
Run an Effect, such as with `Effect.runPromise` or `Effect.runSync`, only at an entry point that a framework or runtime calls, such as a request handler or a scheduled alarm, and map each tag to that entry point's response there; everywhere else, compose Effects with `yield*` or `pipe`.

Violation: `if (!response.ok) throw new Error('the payment provider refused the refund')` turns a provider refusal into an untyped exception.
Violation: `refund({ invoice }).pipe(Effect.orDie)` turns the provider's refusals and outages into defects.
Allowed: `Effect.fail(new RefundRefused({ invoice, status }))`, which the request handler handles with `Effect.catchTag('RefundRefused', ...)`.

## Checks

Run the type check; an Effect's error type lists every tag it can fail with.
For each `throw`, `Effect.die`, `Effect.orDie`, `Effect.catch`, or `Effect.runPromise` a change adds, is it a broken invariant or an entry point, or an expected failure that needs a tagged error?
For each tagged error a change adds, which code handles it by tag, and does every Effect between them pass it up in its error type?
For each `Effect.ignore`, `Effect.option`, or `Effect.orElseSucceed` a change adds, does it discard an expected failure?
For each catch-all handler a change adds, does it branch on every tag?
