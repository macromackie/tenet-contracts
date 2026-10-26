# Rust examples

Keep the result a caller depends on. Exact wording usually belongs in manual output review.

```rust
// Brittle: a copy edit breaks the test.
assert_eq!(stderr, "Review finished in 0.12s: 2 findings\n");
```

```rust
// Keep: execution failure remains distinguishable from a successful assessment.
assert_eq!(output.status.code(), Some(2));
assert!(records.iter().any(|record| record["type"] == "error"));
```

Source locations, protocol labels, and exit codes are interfaces. Keep exact assertions when changing the value
would break a consumer. Avoid asserting the same coordinates in a parser test, renderer test, and several CLI tests
unless each boundary introduces a different risk.

For resume behavior, remove the mock CLI after checkpointing and resume. Successful completion proves the runner
reused the assessment. This is stronger than checking that a private helper was called, and it survives refactoring.

Use a pending response or explicit gate to hold asynchronous work. Wait for an observable checkpoint, then release
or cancel it. Avoid assuming that a checkpoint appears before an arbitrary 350ms response delay expires.

Similar-looking inputs can protect different failures. For half-up rounding, `2.665 -> 2.67` catches half-even
rounding while `2.675 -> 2.68` catches a binary-float implementation. A separate positivity assertion for either
exactly checked result adds no protection. Check the counterexample before calling an assertion redundant.
