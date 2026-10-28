# TypeScript

Installed contracts decide argument shapes, conditional expressions, bindings, and closed value sets. These examples
follow the library's `code-typescript-function-arguments`, `code-conditional-expressions`,
`code-typescript-const-bindings`, and `code-closed-value-sets`.

Make lifecycle decisions visible. Write a decision as ordinary branches in a function that returns a declared member of
a closed set, and build the new state from its result rather than changing the input:

```ts
function chooseNextStage({ job }: ChooseNextStageInput): JobStage {
  if (job.isReviewed) {
    return JobStage.Judging;
  }

  if (job.hasSubmission) {
    return JobStage.Reviewing;
  }

  return JobStage.Preparing;
}

function advanceJob({ job }: AdvanceJobInput): JobProgress {
  return { lastEventAtMs: Date.now(), stage: chooseNextStage({ job }) };
}
```

Keep transport and environment lookup at composition boundaries. Pass the dependencies a function actually needs as
named fields of its object argument, rather than a service container or the entire application state.

When extracting trace processing, keep its redaction, size limit, sequence, and activity bookkeeping together. The
coordinator still owns when to accept an event and when to persist it. Avoid callbacks that conceal lifecycle changes.

Use declared package exports between packages, and export from a package only what another package imports. Add a
package README when it explains ownership and commands; ordinary files do not need their own instructions.
