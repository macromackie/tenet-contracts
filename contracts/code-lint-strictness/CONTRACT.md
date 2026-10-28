---
name: code-lint-strictness
message: Run every lint, type checker, compiler, and formatter at its strictest setting, and turn a rule off only for a listed reason named beside its entry.
requires-tenet: 0.11.0
---

## Rules

Run every lint, type checker, compiler, and formatter that the repository uses with every rule, rule group, and strictness option at error.
Include each rule group that its tool calls unstable, experimental, preview, or opt-in.
Run every checker that this contract ships a configuration for wherever the repository holds a file that checker reads.
Those checkers lint workflow, shell, configuration, and documentation files, audit workflows for security, check spelling, report unused files, exports, and dependencies, and reject disallowed dependencies.
Run a framework's rule group only on the files that framework loads, such as a test runner's rules on test files.

Turn a rule off only when it contradicts a contract's rule, contradicts another enabled rule, conflicts with the formatter, or reports code that a contract requires.
Write the reason in a comment on the line directly above each off entry, starting with its letters among C, R, F, and Q, in that order.
Follow the letter with its evidence: the contract and its rule, the other rule that stays on, the formatter's output, or a compliant sample the rule reports.
Give an entry that turns a rule off for a path pattern that a contract declares, such as test files or a settings module, the same comment.
Where an option chooses between forms, set the form a contract requires, or else the value under which the rule reports the most code.
Set each threshold to the value a contract declares, or else keep the tool's default as the repository's declared maximum.

Pin each checker, plugin, and formatter to one exact version, so a new rule arrives only through a reviewed upgrade.
Where the formatter's strictest configuration uses an option that only a nightly build accepts, pin the formatter alone to one dated nightly build.
Leave out a compiler lint that only a nightly compiler accepts until a stable release accepts it, and run the compiler on a stable release.
Never add a baseline file, a bulk suppression, or a lowered severity that lets existing findings pass.
Suppress a finding at one site only as `code-lint-suppressions` allows.

This contract ships each checker's strictest configuration under `assets/`, in a folder named for the checker.
Where a checker's strictest mode needs command options, run it with the command its shipped file's opening comment gives.
Where a checker's configuration can extend another file, extend the shipped file, listing it before every other contract's shipped file.
Where a checker reads only its own file, copy the shipped file to the path the checker reads.
Where a checker reads its settings from a package manifest, copy the shipped tables into the repository's root manifest.
Keep each copy equal to its shipped file apart from reasoned off entries and the repository's own entries in the lists and keys its opening comment names.
Give each entry the repository adds there, such as a license, a dependency source, an action, or a configuration variable, a comment naming what needs it.
Add the repository's own off entries and path scopes in its own configuration, after every shipped file, so they override the shipped entries.

Violation: a lint configuration turns the rule against empty functions off with no comment above the entry.
Allowed: the repository's lint configuration extends the shipped file first, which turns the rule against `continue` statements off with a `Q: code-guard-clauses` comment above the entry.

## Checks

Run each shipped checker from the repository root with the options its shipped file's opening comment gives, and confirm that each fails on a finding.
For each off entry or path scope a change adds, does the comment above it give the reason letters and their evidence?
Does each checker's configuration extend its shipped file first, or match its shipped copy apart from reasoned off entries and the entries its opening comment names?
Does the repository pin each checker's exact version, with a dated nightly build only for a formatter whose option needs one?
Does a change lower a severity, add a baseline file, or move a threshold away from its declared value?
For each file type that a shipped configuration checks, does the repository's check run that checker on every such file?
