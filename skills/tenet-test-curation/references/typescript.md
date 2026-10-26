# TypeScript examples

Prefer the observable result over intermediate call sequences.

```ts
// Brittle: ties the test to private formatting and update steps.
assert.equal(output, "⠸ reviewing 0.1s\n");
assert.equal(renderCalls, 4);
```

```ts
// Keep: redirected output includes the completed result without terminal controls.
assert.match(output, /example\/plain\s+100%/);
assert.doesNotMatch(output, /\x1b/);
```

Inspect colors, wrapping, spacing, and animation in a real terminal during development. Do not retain a snapshot of
every frame. A fixed machine-readable format warrants stronger checks than cosmetic terminal output.

For a stale async result, hold the response, finish the review, then resolve it. Assert that it cannot reopen the
completed row. Do not enumerate every intermediate spinner or pin the number of streaming callbacks.

For websites, use a browser to check layout, navigation, and copy buttons. Keep small automated checks for broken
installer URLs or missing published documents. Avoid DOM assertions that merely repeat component markup.
