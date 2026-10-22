# TypeScript

Installed contracts decide argument shapes, conditional expressions, and closed value sets. These examples follow the
library's `code-typescript-function-arguments`, `code-conditional-expressions`, and `code-closed-value-sets`.

Make lifecycle decisions visible. Write a decision that accompanies state changes as ordinary branches, and compare
against the declared members of a closed set:

```ts
if (job.reviewed) {
  job.progress.stage = JobStage.Judging;
} else if (job.submission) {
  job.progress.stage = JobStage.Reviewing;
} else {
  job.progress.stage = JobStage.Preparing;
}

job.progress.lastEvent = Date.now();
```

Keep transport and environment lookup at composition boundaries. Pass the dependencies a function actually needs as
named fields of its object argument, rather than a service container or the entire application state.

When extracting trace processing, keep its redaction, size limit, sequence, and activity bookkeeping together. The
coordinator still owns when to accept an event and when to persist it. Avoid callbacks that conceal lifecycle changes.

Use declared package exports between packages, and export from a package only what another package imports. Add a
package README when it explains ownership and commands; ordinary files do not need their own instructions.
