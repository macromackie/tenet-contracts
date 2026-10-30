---
name: telemetry-rust-tracing
message: Centralize Rust tracing, keep entered spans out of suspended futures, and install exporters only in application binaries.
requires-tenet: 0.11.0
---

## Rules

Follow `telemetry-application-tracing` for event records, correlation, metadata, redaction, sampling, and exporter isolation.
Construct spans and record events only through a crate's telemetry module; its functions own the tracing macros.
Load this contract's structural lint rules and keep their telemetry file allowance aligned with the module that owns these calls.
Review imported or renamed tracing macros to confirm they do not bypass that ownership, because structural lint cannot resolve a macro alias to its defining crate.

Attach a span to its future with `Instrument::instrument` instead of holding `tracing::span::Entered` or `EnteredSpan` across an await.
Load the span-guard restrictions from `code-lint-strictness`'s shared assets.
When using the instrumentation attribute, write `#[instrument(skip_all)]` and name each permitted field explicitly.
Map each `LogEvent` member to its serialized value in a `name` method whose match arms return literals; follow `telemetry-application-tracing` for the event's spelling.

Let only application binary packages depend directly on `tracing-subscriber` or `opentelemetry_sdk`; libraries record through the tracing facade and install no exporter.
Fill the exporter dependency restrictions in `code-lint-strictness`'s shared assets with the application binary packages' exact package names.
Require each allowed package to expose no library target, because a dependency restriction by package name cannot distinguish a binary target from a library target in the same package.

Violation: `#[instrument]` on `settle_invoice(invoice: Invoice)` records its argument by default.
Allowed: `#[instrument(skip_all)]` on that function records no argument by default.
Violation: a request handler calls `tracing::info!(event = "invoice.finished")` outside the telemetry module.
Allowed: the handler calls `telemetry::record_finished()` and that function owns the event macro.

## Checks

Run the repository's lint from its root over every production and test target; confirm that a tracing macro outside the telemetry module, an instrumentation attribute without `skip_all`, and a malformed event name report.
Compile an asynchronous function that holds an entered span across an await and confirm that the configured span-guard restriction reports it.
Run the dependency checks and inspect package metadata to confirm that each allowed exporter consumer is an application binary package with no library target.
Inspect tracing macro imports and aliases, and follow each call to the module that owns its span or event.
