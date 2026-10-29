---
name: library-contract-format
message: Write each library contract as a message, rules, and checks, one sentence per line.
---

## Rules

Store each contract at `contracts/<name>/CONTRACT.md`, and keep nothing else in its folder except tool configuration and data files under `assets/<tool>/`.
Start it with frontmatter holding `name`, `message`, and an optional `requires-tenet`, followed by `## Rules` and `## Checks` and no other headings.
Set `requires-tenet` to the minimum Tenet version that installs the contract's files, at least 0.11.0, whenever its folder holds `assets/`.
Write the message as one imperative sentence that states the requirement.
Write one sentence per line and never wrap a sentence, so line-based merges conflict only on a sentence both sides changed.
Separate groups of related rules with one blank line.

Give each contract one reviewable concern; split a contract whose rules a reviewer would check against unrelated code.
Write each rule as a plain imperative requirement that a reviewer could find violated in code, configuration, or history.
Give each rule one allowed form for each case it covers, never a choice between equivalent forms.
Allow two forms only for disjoint cases, and state the observable condition that tells them apart, such as a file extension.
Write a requirement in a form that a tool can check whenever such a form expresses the same decision.
Where a tool can check a rule, ship that tool's configuration under `assets/<tool>/`, and give the contract a check that runs the tool.
Turn a rule off in a shipped file only for a reason `code-lint-strictness` lists, never to scope that file's own test cases.
Leave a rule to review alone only when two reviewers would decide each case of it the same way.
Write each violation example so it breaks only the rule it illustrates, and each allowed example so it breaks no library contract that would govern it.
Do not number rules or use hedges such as "consider" or "where appropriate".
Keep a contract to at most 25 rules and 7 checks.
State each requirement once in the library; a contract that depends on another contract's rule names that contract instead of restating it.
Give each check a command with its working directory, a focused behavior check, or a concrete review question.
Do not require new checker scripts for subjective style.
Leave `## Local adaptations` out of library contracts; adopters add that heading to their copies.

## Checks

Run `uv run --script scripts/lint-contracts.py` from the repository root.
Install each changed contract into a scratch repository with `tenet contracts add`, then run `tenet validate` there.
For each changed rule, what code or history would violate it?
Does any changed rule repeat a requirement another library contract owns?
For each changed rule, does it name one allowed form per case, and does a shipped tool configuration check it wherever a tool can?
Does each changed violation example break only its own rule, and each changed allowed example no library contract that would govern it?
