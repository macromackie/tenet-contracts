---
name: telemetry-application-tracing
message: Trace operations consistently without exposing secrets or letting diagnostics change results.
---

## Rules

Name each traced request by its registered route or operation template, never by its raw URL.
Map unknown methods and unmatched routes to fixed names instead of deriving names or attributes from request data.
Attach the deployed source revision and environment to every exported trace.
Propagate trace correlation across outbound requests, internal service calls, and queued or durable jobs.
Let the application that owns an operation name its spans and choose its sampling, export destinations, and deployment configuration; shared tracing libraries provide instrumentation, not that policy.

Export metadata only, never cookies, headers, authorization codes or state, credentials, signed capabilities, query text or parameters, request or response bodies, prompts, source code, or personal account data.
Redact query strings from every exported URL.
Record an error type or safe error code instead of an exception message.
Sanitize failures at service boundaries so that unhandled storage and provider exceptions cannot reach exported logs or traces.
Sanitize a custom span name or attribute where it is added; a shared tracing library cannot tell which values are sensitive.
Keep exporter credentials out of child process environments and browser assets.
Keep local and test runs free of production export destinations.

Set sampling explicitly in configuration, and change it only as a reviewed change.
Never report sampled event counts as complete traffic totals.
Record waiting for a resource, such as acquiring a connection, separately from the work done with it.
Measure durations with a monotonic clock on one producer, and compare timestamps across hosts only with evidence of their clock offset.

Instrumentation must not change the order, count, or authority of the operations it measures.
A tracing or export failure must preserve the operation's result or exception, must not run the operation again, and must not block the request.
Export telemetry outside the request path; add no synchronous export call to application work.

## Checks

Review the deployed export configuration for destinations, query-string redaction, sampling, and revision metadata.
Follow each changed span or attribute from where it is created to export and confirm that it carries no value from the redaction list.
Force a tracing or export failure and confirm that the operation runs once and returns its original result or exception.
Confirm that local and test configurations cannot reach a production export destination and that diagnostic fixtures use no real credentials.
After changing telemetry configuration, verify ingestion in the deployed environment; local checks do not prove it.
