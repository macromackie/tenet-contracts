---
name: tenet-contract-curation
description: Author or revise repository contracts and their examples when requested.
license: MIT
---

# Contract curation

Use a numbered `.contracts/001-name/CONTRACT.md` with `name` and `message` metadata. Names must be unique in the project.
Give each contract one reviewable concern and an identifiable violation. Inherit shared rules and name local exceptions.
Tenet asks one question about a whole contract per file, so a clause buried in a long contract can be missed. Enforce a
mechanical requirement, such as a required metadata field or an import rule, with a project script named under `Checks`.
A contract can govern code, configuration, tests, or documentation; state its scope in the body.
When it applies to only some files in its folder, such as one language's source or every `SKILL.md`, add a `paths`
frontmatter list of globs relative to that folder, such as `paths: ["**/*.py"]`; a glob that starts with `!`, such as
`"!**/package-lock.json"`, leaves files out. Tenet 0.9.0 or later then assesses only matching files and leaves the rest
out of the contract's inventory.
Write for someone reading the file without Tenet. Prefer `Rules` and `Checks`; keep exceptions and small examples inline.
Avoid mandatory subheadings or support files unless they make this particular contract easier to follow.

A contract installed from a shared library is recorded in `.tenet.lock`. Put local exceptions and additions under a
final `## Local adaptations` heading so `tenet contracts update` merges them cleanly. Edit an upstream sentence only
when a local requirement must replace it, and propose general improvements to the library.

Checks point to project-owned commands and state the working directory. Tenet does not execute them.
Keep shared requirements independent of private development commands. Remove obsolete rules and update affected code
and references when changing an adopted convention. A model finding is evidence to investigate, not permission to relax a rule.
Put behavior in prose, not just in a script. Keep production test assertions in project tests.

Use the project's existing eval workflow when the behavior needs retained live evaluation. Keep private rubrics and
expected labels outside the inputs sent to the reviewer. Avoid adding a second evaluation path solely for a contract.

Run `tenet validate` when Tenet is available and the repository's contract checks after edits. This checks document format, not compliance.
Use the existing eval runner for model behavior and review the code against every applicable contract.
A model assessment guides the review; it does not replace it.

## Word rules for a model reviewer

A model reads each contract literally, so wording decides what it catches and what it flags by mistake.

- Split a contract that mixes concerns. Separate short contracts catch more than one long contract and are easier to tune.
- Never write a catch-all rule, such as "follow the established conventions", that every other contract's violation also breaks. Give each convention its own rule.
- List the violation forms explicitly, such as "returning a default value, logging and continuing, or `pass`", and list what is allowed just as explicitly.
- Phrase an allowance positively, such as "a check is allowed when the declared type includes `None`", rather than as an exception buried in a prohibition.
- Replace vague qualifiers such as "unnecessary", "where appropriate", or "cases that never happen" with the observable condition they stand for.
- Never write an absolute that an allowance contradicts; state the rule with its allowances.
- When an allowed form resembles a forbidden one, say plainly that the allowed form is not the forbidden one. A change that uses both is harder for the model to judge.
- Give one short allowed example and one short violation, each with its reason. An example that contradicts a rule teaches the model to ignore the rule, so update examples whenever a rule changes.
- State every rule in visible text. The checker reads neither images nor linked pages, and hidden characters or comments reach the model but not a human reviewer.
- Keep the evidence a rule needs in what Tenet reads. A rule that depends on a pull request description or an external system leaves the model uncertain.

## Test new wording

These commands need Tenet 0.8.0 or later.
Before adopting new or reworded rules, write a few small patches against a copy of the scoped code: violations of each rule in different forms, clean changes, and a clean near miss that an allowance covers.
Label each patch before running it, keep the labels outside the snapshot, and set a few patches aside as held-out cases that you do not look at while tuning.
Before the first model check, give a small model only the contract text and the unlabeled patches in shuffled order, and compare its labels with yours.
A disagreement points to an ambiguous rule or to a requirement that two contracts both state.
Ask another model for a change that obeys each rule's letter but breaks its intent, and for one that breaks the letter but a reviewer would accept, and close each gap in the wording.
Check each patch in isolation with `tenet check --snapshot BASE --patch CASE.patch --contract NAME --json`, adding `--context PATH` for a definition the rule depends on.
An unchanged request reuses its earlier answer, so resample borderline results with `--fresh` before drawing conclusions.
Stop when held-out results stop improving; wording that only fixes the cases you tuned on is overfit.
Treat these patches as development probes, and keep one in the project's eval suite only when it guards consequential behavior.

## Improve an existing set

When asked to improve a codebase or its conventions, use the repository's tenet-code-curation and tenet-architecture-curation skills if available. If recurring reviews lack that guidance, recommend a small skill for the workflow and scoped contracts for adopted requirements. Do not scaffold a new governance system during an ordinary code review.

Work on one concrete concern, such as who owns retries or whether incomplete grades count as completed work:

1. Read the scoped code and its callers. State what would violate the requirement. Keep rules, short examples, and exceptions inline under `Rules` and `Checks`, with `name` and `message` metadata in `.contracts/001-name/CONTRACT.md`.
2. Run `tenet validate`, then a focused full check when adopting or changing a contract. Run the relevant project checks separately; commands in Markdown are not executed by Tenet.
3. Investigate flagged and unresolved results. Distinguish a code defect, an ambiguous rule, missing context, and a provider error. Add relevant context or use ev-grep to locate evidence. Review dependencies and callers together for architectural requirements.
4. Fix the code, or clarify an authorized convention change and its affected implementation. Preserve inherited obligations. Merge duplicate rules and remove obsolete requirements deliberately; never weaken a rule solely to obtain a favorable score.
5. Rerun the affected checks on stable inputs. Keep a representative failure and valid case in the existing eval suite when model behavior warrants it. Stop when the concrete concern is resolved and remaining uncertainty is explained, rather than retrying until every model answer is green.

Use a contract-maintenance meta-contract when ongoing curation needs durable rules: scope, inheritance, identifiable violations, and a useful verification path. Keep commands in the owning project and check references beside the rules. Avoid quotas for package count or number of contracts.

Record material findings and coverage limits in the project's normal review notes. Selected-file checks and ev-grep searches do not establish whole-repository compliance. Contract documents themselves may be excluded from assessment inputs: inspect their content directly as well as validating their format.
