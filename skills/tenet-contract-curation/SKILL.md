---
name: tenet-contract-curation
description: Author or revise repository contracts and their examples when requested.
license: MIT
---

# Contract curation

Use a numbered `.contracts/001-name/CONTRACT.md` with `name` and `message` frontmatter. Names must be unique in the project.

Give each contract one reviewable concern and an identifiable violation. Tenet asks one question about a whole contract per file, so a clause buried in a long contract can be missed.

## Structure & scoping

- **Write for humans first**: Prefer `## Rules` and `## Checks`; keep exceptions and short examples inline. Avoid mandatory subheadings or support files unless they make this contract clearer.
- **Prefer existing tools for mechanical rules**: Enforce formatting, imports, or required metadata with the project's formatter, linter, or `ast-grep`. Name the command under `## Checks`, and write a custom script only when no tool can decide it.
- **Keep local adaptations cleanly separated**: Contracts installed from a shared library are tracked in `.tenet.lock`. Put local exceptions under a final `## Local adaptations` heading so `tenet contracts update` merges cleanly. Edit upstream text only when a local rule must replace it.
- **Local check recipes**: Use [local check recipes](./resources/local-checks.md) to bind a test or AST rule, qualify it on a representative mistake, and replay its evidence.
- **Prose stays primary**: Put the behavior in prose, not only in a script. Keep production test assertions in project tests, and keep shared contracts independent of private dev commands.

### Scoping large repos for behavior checks (`paths:`)

When a contract applies to only part of its folder, add a `paths` frontmatter list of relative globs (with `!` exclusions):

```yaml
paths:
  - "**/*.go"
  - "go.mod"
  - "!testdata/**"
  - "!**/*_test.go"
```

Scoping matters directly for both budget and behavior-check quality:

- **Exclude fixture and data trees** (`!testdata/**`, `!**/locales/**`, `!**/package-lock.json`) so file-level semantic checks do not exhaust `--max-requests` before behavior-check generation runs.
- **Exclude bulky test suites** (`!**/*_test.go`, `!**/tests/**`) from runtime-behavior contracts so production source fits comfortably inside the checker generation context window.
- **Target public entry points and concrete edge cases**: Executable behavior checks are strongest on real input/output invariants (parsing, formatting, timezone/boundary arithmetic, error propagation) where semantic-only review often under-calls subtle bugs.

## What makes a good contract

A good contract leaves one right way to write the code it covers, and a tool or behavior check catches most violations.

- **Look for a tool first**: Check the project's formatter, linter plugins, and structural search (`ast-grep`). Ship shared tool configs under `assets/<tool>/` and name the command under `## Checks`.
- **Keep rules decidable**: Leave to review only what two reviewers would decide alike ("name the operation that failed and its input" is decidable; "keep functions short" is not).
- **Remove arbitrary choices**: When two equivalent forms exist (such as `count++` vs. `count += 1`), allow one. When both stay, state the observable condition that selects one.
- **Choose on merits**: Write examples in each candidate form and pick the cleanest, most enforceable option with the fewest exceptions. Use code-change volume to plan rollout, never to pick the form.
- **Keep thresholds in config**: State the requirement in prose ("declare a maximum function length") and keep the number in tool configuration.
- **Validate examples against all contracts**: A violation example breaks only the rule it illustrates; an allowed example breaks none.
- **Split diverging concerns**: A single contract may combine executable behavior scripts (`scripts/` pinned by `scripts/.lock.json`; legacy `agent-checks.lock.json` remains readable for compatibility) and manual-review clauses (`open` items) when they share one concern and `paths` scope. Split into separate contracts when concerns or file scopes diverge so editing one rule does not invalidate unrelated behavior locks.

## Word rules for a model reviewer

A model reads each contract literally, so wording decides both recall and false positives:

- **One concern per contract**: Short, focused contracts catch more and tune faster than long catch-all contracts.
- **No catch-all clauses**: Never write "follow established conventions"; give each convention its own rule.
- **Enumerate violations and allowances explicitly**: List concrete violation forms ("returning a default value, logging and continuing, or `pass`") and phrase allowances positively ("allowed when the declared type includes `None`").
- **Replace vague qualifiers**: Swap "unnecessary", "where appropriate", or "cases that never happen" for the observable condition they mean.
- **Resolve contradictions upfront**: Never write an absolute rule that an allowance later contradicts; state the rule with its allowances. When an allowed form resembles a forbidden one, say plainly that the allowed form is not forbidden.
- **Pair short examples with reasons**: Give one concise allowed example and one concise violation, and update them whenever the rule changes.
- **Keep evidence visible and local**: State every rule in visible text (no images, linked pages, or hidden comments) and depend only on files Tenet reads (not PR descriptions or external services).

## Test new wording

Before adopting new or reworded rules:

1. Build small patches against a copy of scoped code: varied violations, clean changes, and clean near misses covered by allowances.
2. Label each patch beforehand, keep labels outside the snapshot, and hold a few patches out while tuning.
3. Run a blind check with a small model on the contract text plus shuffled unlabeled patches; disagreements expose ambiguous wording or overlapping contracts.
4. Probe adversarial edge cases (obeys letter / breaks intent, and vice versa) and close each wording gap.
5. Check each patch in isolation with `tenet check --snapshot BASE --patch CASE.patch --contract NAME --json` (adding `--context PATH` for external definitions; resample borderline cases with `--fresh`).
6. Stop when held-out results stop improving. Keep a case in the project's eval suite only when it guards consequential behavior; avoid creating a second evaluation harness solely for one contract.

Run `tenet validate` after edits (validates document format, not compliance).

## Improve an existing set

When asked to improve a codebase or its conventions, use the repository's `tenet-code-curation` and `tenet-architecture-curation` skills when available. Do not scaffold a new governance system during an ordinary code review.

Work on one concrete concern at a time:

1. Read the scoped code and callers; state what violates the requirement in `.contracts/001-name/CONTRACT.md`.
2. Run `tenet validate`, then a focused full check. Run project tools separately (`## Checks` commands are documentation).
3. Triage flagged and unresolved findings: distinguish code defects, ambiguous wording, missing context, and provider errors.
4. Repair the code, or clarify an authorized convention change. Merge duplicate rules and remove obsolete ones deliberately; never weaken a rule solely to get a green score.
5. Rerun affected checks on stable inputs and stop once the concern is resolved and remaining uncertainty is explained.

Use a `contract-maintenance` meta-contract for durable curation rules without setting arbitrary contract-count quotas. Record material findings and coverage limits in review notes, and inspect contract documents directly since they may be excluded from assessment inputs.
