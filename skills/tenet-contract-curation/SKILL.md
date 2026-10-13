---
name: tenet-contract-curation
description: Author or revise repository contracts and their examples when requested.
---

# Contract curation

Use a numbered `.contracts/001-name/CONTRACT.md` with `name` and `message` metadata. Names must be unique in the project.
Give each contract one reviewable concern and an identifiable violation. Inherit shared rules and name local exceptions.
Tenet asks one question about a whole contract per file, so a clause buried in a long contract can be missed. Enforce a
mechanical requirement, such as a required metadata field or an import rule, with a project script named under `Checks`.
A contract can govern code, configuration, tests, or documentation; state its scope in the body.
Write for someone reading the file without Tenet. Prefer `Rules` and `Checks`; keep exceptions and small examples inline.
Avoid mandatory subheadings or support files unless they make this particular contract easier to follow.

A contract installed from a shared library is recorded in `.tenet.lock`. Put local exceptions and additions under a
final `## Local adaptations` heading so `tenet contracts update` merges them cleanly. Edit an upstream sentence only
when a local requirement must replace it, and propose general improvements to the library.

Checks point to project-owned commands and state the working directory. Tenet does not execute them.
Keep exported requirements independent of private Factory commands. Remove obsolete rules and update affected code
and references when changing an adopted convention. A model finding is evidence to investigate, not permission to relax a rule.
Put behavior in prose, not just in a script. Keep production test assertions in project tests.

For model-sensitive requirements, keep short examples inline. Use the project's existing eval workflow when the
behavior needs live evaluation. Keep private rubrics and expected labels outside the inputs sent to the reviewer.
Avoid adding a second evaluation path solely for a contract.

Run `tenet validate` when Tenet is available and the repository's contract checks after edits. This checks document format, not compliance.
Use the existing eval runner for model behavior and review the code against every applicable contract.
A model assessment guides the review; it does not replace it.

## Improve an existing set

When asked to improve a codebase or its conventions, use the repository's tenet-code-curation and tenet-architecture-curation skills if available. If recurring reviews lack that guidance, recommend a small skill for the workflow and scoped contracts for adopted requirements. Do not scaffold a new governance system during an ordinary code review.

Work on one concrete concern, such as who owns retries or whether incomplete grades count as completed work:

1. Read the scoped code and its callers. State what would violate the requirement. Keep rules, short examples, and exceptions inline under `Rules` and `Checks`, with `name` and `message` metadata in `.contracts/001-name/CONTRACT.md`.
2. Run `tenet validate`, then a focused full check when adopting or changing a contract. Run the relevant project checks separately; commands in Markdown are not executed by Tenet.
3. Investigate flagged and unresolved results. Distinguish a code defect, an ambiguous rule, missing context, and a provider error. Add relevant context or use ev-grep to locate evidence. Review dependencies and callers together for architectural requirements.
4. Fix the code, or clarify an authorized convention change and its affected implementation. Preserve inherited obligations. Merge duplicate rules and remove obsolete requirements deliberately; never weaken a rule solely to obtain a favorable score.
5. Rerun the affected checks on stable inputs. Keep a representative failure and valid case in the existing eval suite when model behavior warrants it. Stop when the concrete concern is resolved and remaining uncertainty is explained, rather than retrying until every model answer is green.

Use a contract-maintenance meta-contract when ongoing curation needs durable rules: scope, inheritance, identifiable violations, and a useful verification path. Keep commands in the owning project and check references beside the rules. Avoid quotas for file size, package count, or number of contracts.

Record material findings and coverage limits in the project's normal review notes. Selected-file checks and ev-grep searches do not establish whole-repository compliance. Contract documents themselves may be excluded from assessment inputs: inspect their content directly as well as validating their format.
