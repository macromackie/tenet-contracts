---
name: docs-readme-structure
message: Open each README with what the project is and how to start, link out for depth, and keep status and history out.
---

## Rules

Apply these rules to every README in the governed scope.
Open the README with one sentence that says what the project is and what it does.
Put a command or example a reader can copy, such as an install command or a minimal usage example, before any section about design, internals, or contributing.
Write install steps as one code block with one command per line, and give alternatives as comment lines in the same block.
Name each section with a short noun phrase, such as Install, Usage, Documentation, or Contributing.
List features as one line each that starts with a bold term or a link.
Keep reference detail, runbooks, and long explanations in separate documents or a documentation site, and link to each one from a short README entry.
Declare a word budget for each README, and keep the README within it.
Never put status reports, history, release or deployment receipts, "last updated" stamps, continuous integration output, or roadmap checklists in a README, whether dated or not.
A badge that links to a live system, such as a build status or the latest version, is allowed.
Record status in release notes, the task tracker, or the continuous integration system, and link to them when readers need them.

Violation: a paragraph near the top reads "Deployment verified on 2026-03-02: 1.4.0-rc.1," followed by the steps an operator took.
Allowed: a Common tasks table pairs each task with its command and links the operator guide for details.

## Checks

Count the README's words and compare the count with the declared budget.
Does the README's first sentence say what the project is and what it does?
Does any line report a date, a deployment, a release status, or a check result?
For each section longer than its neighbors, could it move to a linked document without losing a first-time reader?
