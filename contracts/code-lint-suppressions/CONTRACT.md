---
name: code-lint-suppressions
message: Suppress a lint or check finding only at the one site it reports, with the rule's name and a reason, and fail checks on every suppression that suppresses nothing.
---

## Rules

A suppression is any comment, attribute, tag, marker, or configuration entry that makes a lint, a compiler, or a repository check accept a finding that its rule reports.
Apply these rules to every suppression in source, tests, scripts, and check configuration, whichever tool reads it.
A contract may forbid suppressing one of its rules, and then no form below passes that rule.

Suppress a finding only at the site the tool reports: the reported line, the smallest statement or item that the tool honors there, or the one declaration, block, or path that the finding names.
Name every rule that a suppression silences, and never write a suppression that names no rule or silences every rule; a directive whose tool accepts no rule's name, such as a compiler's expected-error comment, names its rule by stating in its reason the one finding it accepts.
Give each suppression a reason that says why this site cannot follow the rule and names the system or source that keeps it from doing so, such as the provider that names a wire field, the dependency that declares a set, or the generator that writes a table.
Write the reason as behavior, never as a contract's name or a review tool's finding, as `code-comment-attribution` requires, and never as a promise of a later fix.

Write the reason inside the directive or attribute when the tool accepts text there, such as after two hyphens with a space on each side, or in a reason argument.
When a tool's directive accepts no text after the rule's name, write the reason on its own comment line directly above the directive.
Use the expectation form, which fails once its finding is gone, instead of the allow form wherever the language offers both.
When the tool reports a block, such as a copied block, surround only that block with the tool's start and end markers, and write the reason on the start marker.
When the finding concerns a declaration's consumers, such as an export that only another repository imports, mark that declaration with the tool's documentation tag, and write the reason on the tag's own line.
When the finding reports no line, such as a folder over its file limit, add a configuration entry that names that one path and carries its reason in a comment beside it.
When a tool honors no suppression at a site it reports, the site follows the rule, and a configuration entry that skips that site by name is a violation.
Spell the directive of every check that the repository owns one way: the check's name followed by `-allow`, the rule's name, two hyphens with a space on each side, and the reason, on the line above the reported line.

A suppression that covers a whole file, module, or package, a rule turned off, a lowered severity, and an option or limit changed so that one site passes are violations.
A rule turned off with one of the reasons that `code-lint-strictness` lists, named in the comment above its entry, is not a violation.
A path pattern that a contract declares in the lint configuration, such as a settings module, generated files, or test fixtures, scopes a rule and is not a suppression, and widening it to admit one site is a violation.
Configure every tool to fail on a suppression that no longer suppresses a finding, wherever the tool supports it.
Make every check that the repository owns fail on its own directive once that directive suppresses nothing.
Configure the lint to reject a suppression that names no rule or gives no reason, in every directive spelling that the tool honors, wherever a lint rule can decide it.

Violation: `// lint-disable-next-line -- legacy` above a long function names no rule, and its reason does not say why that function needs the exception.
Allowed: a directive above a generated function names the function-length rule and gives the reason after a space and two hyphens: `-- the generator writes one case per status code that the provider documents`.

## Checks

From the repository root, run each lint and check with its unused-suppression setting, and confirm that a stale suppression fails.
For each suppression a change adds, does it sit at the reported site, name each rule it silences, and give a reason that names the system or source that keeps the site from following the rule?
For a tool that cannot report a stale suppression, does each suppression that a change keeps still cover a finding?
For each configuration entry or path pattern a change adds or widens, does it name one path with a reason, or scope a rule as a contract declares?
Does a change turn a rule off without a reason that `code-lint-strictness` lists, lower its severity, or change an option or limit so that one site passes?
