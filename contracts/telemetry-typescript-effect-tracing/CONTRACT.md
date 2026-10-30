---
name: telemetry-typescript-effect-tracing
message: Name traced TypeScript Effects with literal operation names and compose telemetry once at the application entry point.
requires-tenet: 0.11.0
---

## Rules

Apply these rules to TypeScript code that uses effect 4.0.0 or later, including TypeScript with markup.
Declare a function whose calls a trace records with `Effect.fn('invoice.read')(function* ({ id }: ReadInvoiceInput) { return yield* store.read({ id }); })`, with an anonymous generator and a nonempty string literal operation name.
Use `Effect.withSpan` for a child span that ends with its Effect, and `Effect.withSpanScoped` for a child span that ends with its enclosing scope.
Give each child span a nonempty string literal name at that call.
Outside a pipeline, pass the Effect as the call's first argument; inside a pipeline, pass the curried call to `.pipe`.
Keep the operation name at its declaration or span call, never in an identifier, template string, interpolation, or computation.

Compose the logger and tracer layers once for each application runtime at the framework entry point that owns that runtime.
Reuse that runtime for its operations and dispose of its telemetry resources with the runtime's lifecycle.
Follow `telemetry-application-tracing` for logging, correlation, metadata, export ownership, and diagnostic failures.
Load this contract's structural lint configuration and suppress a finding only as `code-lint-suppressions` allows.

Violation: `Effect.fn(operationName)(function* () { return yield* readInvoice({ id }); })` derives the operation name from a value.
Violation: `Effect.withSpan(reading, operationName)` adds a dynamic span name.
Allowed: `Effect.withSpan(reading, 'invoice.read')` adds a child span outside a pipeline.
Allowed: `reading.pipe(Effect.withSpan('invoice.read'))` adds a child span inside a pipeline.

## Checks

Run the repository's structural lint from its root with this contract's configuration and confirm it reports dynamic or empty names at `Effect.fn`, `Effect.withSpan`, and `Effect.withSpanScoped`.
For each changed child span, is its call effect-first outside a pipeline and curried inside one?
Run the package's TypeScript check against its pinned effect version.
For each newly traced function, is its name declared by `Effect.fn` with an anonymous generator and a nonempty string literal?
Follow runtime creation and disposal and confirm that logger and tracer layers are composed once per runtime at its owning framework entry point.
Follow a span through the shared export configuration and confirm that exporting runs outside the operation as `telemetry-application-tracing` requires.
