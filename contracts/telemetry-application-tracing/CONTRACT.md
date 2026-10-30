---
name: telemetry-application-tracing
message: Trace operations and write each log line as one JSON object with a declared event, without exposing secrets or letting diagnostics change results.
requires-tenet: 0.11.0
---

## Rules

Name each traced request by its registered route or operation template, never by its raw URL.
Map unknown methods and unmatched routes to fixed names instead of deriving names or attributes from request data.
Attach the deployed source revision and environment to every exported trace.
Propagate trace correlation across outbound requests, internal service calls, and queued or durable jobs.
Let the application that owns an operation name its spans and choose its sampling, export destinations, and deployment configuration; shared tracing libraries provide instrumentation, not that policy.

Apply these log-line rules to a command-line program's opt-in trace stream too.
Apply the log-line rules to every server and every process a host runs until it is stopped; a command-line program's lines for its user follow `cli-output-channels`.
Write each log line as one JSON object by passing the logger module's function one object literal whose `event` field names a member of that module's closed set.
Declare that set as `code-closed-value-sets` requires, such as `LogEvent`, with values of two snake case parts joined by a dot, and type the logger input's `event` field as it.
Hold every other value in its own field, such as `invoiceId`, never interpolated into a string.
Log a failure as an `error` field listing its cause chain outermost first, by each cause's error type or a generic error's safe error code, never the exception object.
Outside the logger module, never call a console method, a print function or macro, or a logging library's function, or open a handle to either standard stream.
Enforce the console and stream ban, the object literal, the named member, and the event's form with the repository's lint, and suppress a finding only as `code-lint-suppressions` allows.
Load this contract's `assets/` configuration where the lint can; it reads the function `log` in `logger/log`, the only file allowed console calls and stream handles, and the set `LogEvent`.
A repository may rename these, and adds to that allowance its command-line output module, as `cli-output-channels` requires, and its browser code, which these rules do not cover.

Export metadata only, never cookies, headers, authorization codes or state, credentials, signed capabilities, query text or parameters, request or response bodies, prompts, source code, or personal account data.
Redact query strings from every exported URL.
Record an error type or safe error code, never an exception message, and sanitize failures at service boundaries so unhandled storage and provider exceptions never reach exported telemetry.
Sanitize a custom span name or attribute where it is added; a shared tracing library cannot tell which values are sensitive.
Keep exporter credentials out of child process environments and browser assets, and production export destinations out of local and test runs.

Set sampling explicitly in configuration, change it only as a reviewed change, and never report sampled event counts as complete traffic totals.
Record waiting for a resource, such as acquiring a connection, separately from the work done with it.
Measure durations with a monotonic clock on one producer, and compare timestamps across hosts only with evidence of their clock offset.

Instrumentation must not change the order, count, or authority of the operations it measures.
A tracing or export failure must preserve the operation's result or exception, must not run the operation again, and must not block the request.
Export telemetry outside the request path; add no synchronous export call to application work.

Violation: a request handler calls `console.error(line)` outside the logger module, after `const line = JSON.stringify({ event: LogEvent.InvoiceSettleFailed, invoiceId })`.
Violation: `log({ error, event: LogEvent.InvoiceSettleFailed, invoiceId })` passes the exception object instead of its cause chain.
Allowed: `log({ error: causes, event: LogEvent.InvoiceSettleFailed, invoiceId })`, after `const causes = listCauseTags({ error })`, writes `"error":["InvoiceNotSettled","StoreUnavailable"]`.

## Checks

Run the repository's lint from its root and confirm it reports console calls outside the logger module, logger calls without an `event` object literal, and literal or malformed events.
For each log line a change adds, is every value other than its declared event its own field, and does a failure appear only as its cause chain?
Review the deployed export configuration for destinations, query-string redaction, sampling, and revision metadata.
Follow each changed span or attribute from where it is created to export and confirm that it carries no value from the redaction list.
Force a tracing or export failure and confirm that the operation runs once and returns its original result or exception.
Confirm that local and test configurations cannot reach a production export destination and that diagnostic fixtures use no real credentials.
After changing telemetry configuration, verify ingestion in the deployed environment; local checks do not prove it.
