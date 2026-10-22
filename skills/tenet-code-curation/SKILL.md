---
name: tenet-code-curation
description: Refactor or review implementation for clear ownership, focused modules, and consistent conventions during development and before committing.
---

# Code curation

Make behavior understandable with a small amount of local context. Prefer direct code and focused boundaries.

## During development

Read the nearest contracts and follow one representative call from entry point to result. Identify who owns state,
external effects, errors, and cleanup before moving code. Apply this workflow to touched code and related callers;
a broad cleanup request can justify a wider pass.

Before adding a rule or instruction for a recurring failure, identify its owner: implementation, an executable check,
an adopted requirement, missing context, or an agent decision. Ask which plausible mistake the new guidance prevents
and why existing guidance misses it. Fix that cause; consolidate instructions that lead to the same decision.

Make local control flow readable first. Use named steps and explicit branches for asynchronous work, retries, and
lifecycle decisions. Separate logical phases with blank lines. Keep related statements together. Slight verbosity
is useful when it makes ownership, units, or sequencing visible; do not expand straightforward expressions by habit.

Extract a coherent responsibility when it reduces what a reader must understand at once. Keep state with operations
that protect its invariants. Prefer a module or nested folder until a package boundary provides a concrete benefit.
Use the optional tenet-architecture-curation skill for ownership, package boundaries, data flow, and recovery.

Reuse established libraries rather than maintaining a second implementation of their behavior. Keep local helper
inputs and results explicit, and expose only what callers need.

## Before committing

Read the changed code as a caller. Can its inputs, effects, result, and failure path be understood without following
several forwarding helpers? Remove dead paths, stale comments, redundant wrappers, and speculative options.
Keep one execution path and consistent names, layout, error handling, and package commands across the affected area.
Inspect nearby implementations before introducing a new pattern; reuse the convention or update its affected callers.

Review large files for mixed responsibilities. Split a file along its responsibilities, never through the middle of
one lifecycle, and follow the file and function length limits and the file roles that installed contracts declare. Keep trivial glue inline. Choose visibility deliberately; a new helper need not become public.

Update contracts when this task authorizes changing conventions. Put concrete ownership and dependency rules at the
narrowest useful scope, inherit shared rules, and update affected callers, READMEs, exports, and indexes together.
Do not create a contract for every helper or repeat shared rules in every folder.

Use the optional tenet-test-curation skill to verify refactors and curate retained checks. In a behavior-preserving
refactor, preserve sequencing, cancellation, retry budgets, and serialized formats. For an intentional redesign,
identify the behavior being replaced and update its consumers and verification together.
Run the affected checks required by the repository instructions.
Report the behavior verified and any remaining uncertainty; formatting alone does not establish a good boundary.

Before finishing, reconcile the consequences of the change. Search for renamed or retired concepts through callers,
exports, options, dependencies, fixtures, and guidance; remove superseded paths and update their consumers together.
Keep implemented behavior in source and checks, requirements in contracts, decisions and evidence in context, workflows
in skills, and commands in owning docs. Link to each owner instead of repeating it. Investigate disagreements before
choosing which side to change; a code defect does not justify rewriting its requirement.

For a meaningful boundary change, start again from the repository entry point. Can the next reader find the owner,
trace the execution and authority, locate the relevant check, and distinguish the current design from a proposal?
Fix the particular gap. Use a short read-through and focused spot checks for routine curation; reserve controlled evals
for changes to model behavior or claims that need them. No additional agent or evaluation framework is required.

Ask what became easier to understand and what can now be removed. Scope this pass to affected behavior; an unchanged
document needs no edit. These are review prompts, not required reports, deletion quotas, or complexity scores.

Read [Rust](resources/rust.md) or [TypeScript](resources/typescript.md) for language-specific examples.
