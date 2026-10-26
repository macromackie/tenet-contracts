# Recovery

Keep the owner of a lifecycle responsible for its deadlines, transitions, cancellation, and cleanup. Extract an
operation when it has a clear input and result, not simply because a coordinator has grown long.

For durable work, persist enough information to distinguish pending, completed, and failed stages. Save a completed
assessment before starting a separately retryable grade. A disconnected observer should reattach to the same work;
it should not reconstruct the run from terminal output or submit a second run.

Make repeated effects safe with stable identities or idempotent operations where supported. An interrupted external
request may already have succeeded or incurred a charge. Expose that uncertainty rather than claiming exactly-once
execution. Retry only a classified transient failure, within one overall deadline and attempt budget. Do not multiply
independent retries at each layer or turn an exhausted retry into an empty successful result.

Give cleanup an explicit owner. Cancellation stops new work and requests termination of active work; unfinished cleanup
must remain visible and retryable. Use durable coordination where this lifecycle needs it, and ordinary local state for
short-lived operations that can simply fail and be rerun.

Verify recovery by interrupting a real operation at the affected boundary, then inspect the resumed result and retained
errors. Keep a durable regression test when the behavior is important and easy to break; temporary fault injection and
manual evidence can provide additional confidence without becoming a second permanent harness.
