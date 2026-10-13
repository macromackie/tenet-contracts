# TypeScript

Make lifecycle decisions visible. A nested conditional such as `reviewed ? "judging" : submitted ? "reviewing" :
"preparing"` is easier to extend as ordinary branches when it accompanies state changes:

```ts
if (job.reviewed) {
  job.progress.stage = "judging";
} else if (job.submission) {
  job.progress.stage = "reviewing";
} else {
  job.progress.stage = "preparing";
}

job.progress.lastEvent = Date.now();
```

Keep transport and environment lookup at composition boundaries. Pass the dependencies a function actually needs,
rather than a service container or the entire application state. Use named object fields for several related values.

When extracting trace processing, keep its redaction, size limit, sequence, and activity bookkeeping together. The
coordinator still owns when to accept an event and when to persist it. Avoid callbacks that conceal lifecycle changes.

Use declared package exports between packages. Internal helpers stay private to the package. Add a package README
when it explains ownership and commands; ordinary files do not need their own instructions.
