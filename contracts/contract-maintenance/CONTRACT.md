---
name: contract-maintenance
message: Keep adopted contracts scoped, reviewable, and consistent with their implementation.
---

## Rules

Give each contract one reviewable concern, a clear scope, and an identifiable violation.
State adopted requirements and useful exceptions in ordinary Markdown.
Keep short examples inline.
Put proposals and design rationale in .context; contracts describe the agreed implementation baseline rather than an aspirational future architecture.

Define shared obligations once.
Nested contracts inherit their parents and add local ownership, concrete boundaries, or explicit exceptions.
Fixture contracts are eval inputs, not repository policy.
Keep shared requirements usable without private tooling.
Keep numbered folders and indexes consistent; do not renumber unrelated rules.

Put local exceptions and additions to an adopted shared contract under a final `## Local adaptations` heading.
Edit an adopted upstream sentence only when a local requirement must replace it, and propose general improvements to the shared source.

When a task authorizes a convention change, update the contract, affected implementation, callers, examples, and check references together.
Do not weaken a requirement merely to make a finding disappear.
Remove obsolete rules or merge redundant ones when their obligations are preserved elsewhere.
When an implementation change invalidates guidance, reconcile the affected contracts, context, skills, and references in the same change.
An unchanged document needs no edit; resolve conflicts against the intended requirement rather than automatically making it describe the current code.

Give each rule a useful verification path: an existing tool, a focused behavior check, or a concrete review question.
Formatting and document validation establish syntax, not compliance.
Tenet/Jev can flag likely violations and missing context; the outer reviewer still owns the final judgment.
Do not require new checkers or tests for subjective style.

Skills describe how to work; contracts describe adopted requirements.
Keep tool-usage skills self-contained and separate from private development workflows.
When repeated review findings justify a curation change, investigate the cause, update authorized requirements and code together, then rerun focused checks.
Preserve errors and coverage limits; stop when the issue is understood and addressed rather than retrying until the model approves.

## Checks

Read changed contracts alongside their scoped code.
Identify what would violate each rule and how a reviewer would notice.
Check inherited requirements, exceptions, indexes, and commands for conflicts or duplication.
Validate documents with the repository's contract checks, then review actual behavior and run the affected project checks.
