---
name: code-typescript-effect-scheduling
message: Sleep, bound, retry, poll, race, and fan out TypeScript work only with Effect's operators, never with hand-built promises, promise combinators, or timers.
requires-tenet: 0.11.0
---

## Rules

Sleep with `Effect.sleep`, such as `yield* Effect.sleep(POLL_INTERVAL)`, never with `setTimeout`, `setInterval`, or a runtime's promise timers module.
Bound a wait with `Effect.timeout` or one of its variants, such as `Effect.timeoutOrElse`, never with `AbortSignal.timeout`, `Promise.race`, or a timer that code clears later.
Retry with `Effect.retry` and a `Schedule`, and poll with `Effect.repeat`, a `Schedule`, and an `until` condition, never with a loop that sleeps between attempts.
End each retry and poll after a declared number of attempts or a declared duration, through its `Schedule` or `Effect.timeout`, within the budget that `code-execution-lifecycle` gives its one owner.
Work that repeats until its owner interrupts it, such as a queue consumer, may repeat on a `Schedule` without a bound.
A retry or deadline that a later invocation resumes from storage, such as a job's next attempt time, is a durable job, not an `Effect.retry` or `Effect.timeout`.

Run an Effect for each member of a collection with `Effect.forEach`, and pass it a numeric `concurrency` option, never `'unbounded'`.
Pass `{ concurrency: 1 }` to run the members in order, so that every `Effect.forEach` states its concurrency.
Combine with `Effect.all` only a fixed set of distinct Effects written out as its array or object argument, such as `Effect.all({ account, invoice })`.
A loop that runs its steps one at a time with `yield*`, such as paging through results by cursor, is not fan-out and stays a loop.
Race Effects with `Effect.race` or `Effect.raceFirst`, which interrupt the Effect that loses.

Never write `new Promise`, `Promise.withResolvers`, `Promise.all`, `Promise.allSettled`, `Promise.any`, or `Promise.race`, in any file, including tests and scripts.
Build an Effect from a callback API with `Effect.callback`, which hands the callback an `AbortSignal` and runs the cleanup Effect it returns when the wait is interrupted.
Wrap each foreign call that returns a promise once with `Effect.tryPromise`, as `code-typescript-effect-errors` requires, and bound and combine the wrapped Effects instead of their promises.
Pass the `signal` that `Effect.tryPromise` or `Effect.callback` hands its function to each foreign call in it that accepts one, so a timeout or lost race stops the call.
Where a foreign API takes a promise, such as a worker's `waitUntil`, pass it the promise that `Effect.runPromise` returns at the entry point that `code-typescript-effect-errors` allows.
A function that a foreign API calls and awaits, such as a test body, is such an entry point, is `async`, and returns `await Effect.runPromise(program)` for its Effect.
A user interface component that delays or repeats work, such as hiding a notice, runs the Effect with `Effect.runFork` when it mounts and interrupts that fiber in its cleanup.
A deadline that a library enforces on its own resource, such as a connection pool's acquire timeout or a test's time limit, stays in that library's configuration.
A retry that a library performs on its own requests, such as a model client's retry of a rate-limited call, stays in that library's configuration.
Never sleep, retry, poll, or limit concurrency through a helper that does not use these operators, such as a promise retry or pool package.

Configure the repository's lint to reject these promise forms, timers, deadline signals, `Effect.forEach` calls without a numeric concurrency, and loops that sleep, suppressing a finding only as `code-lint-suppressions` allows.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.

Violation: `await new Promise((resolve) => setTimeout(() => resolve(), RETRY_DELAY_MS))` sleeps through a hand-built promise that no interruption can cancel.
Violation: `const reminders = invoices.map((invoice) => sendReminder({ invoice }))`, then `await Promise.all(reminders)`, sends every reminder at once, with no bound, and keeps sending the rest after one fails.
Violation: a `for` loop reads a job, sleeps two seconds, and reads the job again until it finishes, with no deadline.
Allowed: `Effect.forEach(invoices, (invoice) => sendReminder({ invoice }), { concurrency: REMINDER_CONCURRENCY })`.
Allowed: `readJob({ job }).pipe(Effect.repeat({ schedule: pollSchedule, until: isFinished }), Effect.timeout(JOB_DEADLINE))`.
Allowed: `Effect.tryPromise({ catch: buildRequestDropped, try: readInvoice }).pipe(Effect.timeout(READ_DEADLINE))`, where `readInvoice` passes the `signal` it receives to `fetch`.

## Checks

From each package root, run the type check against effect 4.0.0 or later.
Run the repository's lint from the repository root, and confirm that it rejects `new Promise`, `Promise.all`, `setTimeout`, `AbortSignal.timeout`, an `Effect.forEach` without a numeric `concurrency`, and a loop that sleeps.
For each sleep, deadline, retry, poll, race, or concurrent step a change adds, including in tests and scripts, which Effect operator performs it?
For each retry or poll a change adds, what ends its `Schedule`, and does that bound fit its one owner's budget under `code-execution-lifecycle`?
For each foreign call a change wraps, does it receive the wrapped Effect's `signal` when it accepts one, so that a timeout or a lost race stops it?
For each `Effect.all` a change adds, does its argument write out a fixed set of distinct Effects rather than a collection?
Does a change sleep, retry, poll, or limit concurrency through a helper that does not use these operators, or hand a foreign API a promise that no Effect produced?
