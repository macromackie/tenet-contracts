---
name: contract-maintenance
message: Keep adopted contracts scoped, reviewable, and consistent with their implementation.
---

## Rules

Give each contract one reviewable concern, a clear scope, and an identifiable violation.
State adopted requirements and useful exceptions in the contract's own ordinary Markdown; a link may support a rule but must not replace it.
Keep short examples inline.
Contracts describe the agreed implementation baseline rather than an aspirational future architecture.

Define shared obligations once.
Nested contracts inherit their parents and add local ownership, concrete boundaries, or explicit exceptions.
Keep shared requirements usable without private tooling.
Keep numbered folders and indexes consistent; do not renumber unrelated rules.

Put local exceptions and additions to an adopted shared contract under a final `## Local adaptations` heading.
Edit an adopted upstream sentence only when a local requirement must replace it, and propose general improvements to the shared source.
Never overwrite local edits when updating an adopted contract; an upstream revision alone does not authorize changing local rules.

When a task authorizes a convention change, update the contract, affected implementation, callers, examples, and check references together.
Do not weaken a requirement merely to make a finding disappear.
Remove obsolete rules or merge redundant ones when their obligations are preserved elsewhere.
When an implementation change invalidates guidance, reconcile the affected contracts, context, skills, and references in the same change.
An unchanged document needs no edit; resolve conflicts against the intended requirement rather than automatically making it describe the current code.

Give each rule a verification path: a command with its working directory, a focused behavior check, or a concrete review question.
Formatting and document validation establish syntax, not compliance.
Do not require new checkers or tests for subjective style.

Skills describe how to work; contracts describe adopted requirements.
Keep tool-usage skills self-contained and separate from private development workflows.
When repeated review findings justify a curation change, investigate the cause, update authorized requirements and code together, then rerun focused checks.

## Checks

Read each changed contract without following its links, and confirm that its scope, obligations, and exceptions are stated in it.
Read changed contracts alongside their scoped code.
Identify what would violate each rule and how a reviewer would notice.
Check inherited requirements, exceptions, indexes, and commands for conflicts or duplication.
Validate documents with the repository's contract checks, confirm that each named command exists and runs from its stated working directory, then review actual behavior and run the affected project checks.
Inspect any obligation left to judgment rather than assuming that passing the mechanical portion closes the contract.
