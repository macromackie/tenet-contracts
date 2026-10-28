---
name: code-comment-form
message: Write comments as capitalized sentences without task markers, commented-out code, step labels, license notices, or empty doc comments, and declaration comments and file summaries as lint-enforced prose doc comments.
requires-tenet: 0.11.0
---

## Rules

Apply these rules to comments and doc comments in maintained production code, tests, scripts, and examples, and not to generated or copied third-party source.
Never write a task marker, such as `TODO`, `FIXME`, `XXX`, or `HACK`, anywhere in a comment in any case, and record unfinished work in the task tracker.
A marker word that names a domain concept, such as the `todo` status of a task product, is allowed with the suppression that `code-lint-suppressions` describes.
Never commit commented-out code, such as a disabled statement or an earlier implementation; a code fragment inside a sentence that explains behavior is prose.
Never number or letter a step in a comment, such as `// 4.` or `// (g)`, and give each step a function named for what it does instead.
A numbered list inside a doc comment is documentation and is allowed.

Write every comment as one or more sentences that start with a capital letter; line comments on consecutive lines form one comment.
Put a code identifier that opens a comment in backticks, such as ``// `retryAfter` is absent.``, so the comment opens with no letter, which the lint skips.
The lint skips a comment that opens with a type annotation, such as `@type`, or a directive word that the lint, the shipped configuration, or a repository's copy lists.

Never commit an empty doc comment, and write a tagless block doc comment that fits the declared maximum line length on one line, such as `/** The run's deadline. */`.
Put the opening and closing markers of any longer or tagged block doc comment on lines of their own.
A block comment that holds only the type of the value that follows, such as `/** @type {Order} */`, is type syntax rather than a doc comment.
Write every doc comment in every language as prose, stating in sentences what callers need about its parameters, result, yielded values, errors, and panics.
Never write a section or tag for those or for usage examples, such as `@param`, `@throws`, `Returns:`, `# Errors`, or `# Examples`; `# Safety` is the only section allowed.

Outside a function body, write each comment above or beside a declaration, a class, type, interface, or enum member, or module constant as a doc comment directly above it.
Where a language has both line and block doc comments, write the line form, such as `///`.
Write a comment inside a function body as a plain line comment, such as `//`.
Where the language's doc comment is a string, such as a docstring, make it the first statement of the function's or class's body.
In such a language, document a module constant or a class field with a string directly below its assignment, never with a comment above it.
A tool's directive, such as a lint suppression, and the reason line that `code-lint-suppressions` puts above one keep the form their tool requires.

Write a file's summary as a doc comment, such as `//!` or `/** */`, above its imports, after only required opening lines, such as a shebang.
Never write a copyright or license notice, such as a `Copyright` line or `SPDX-License-Identifier: MIT`, in a source file, because the repository's `LICENSE` file states it once.
Open every file that `code-script-entry-points` covers, the files the repository executes directly, with a summary that says what it does and how to run it, such as its command.

Configure the repository's lint to reject each of these forms wherever a tool decides it, and suppress a finding only as `code-lint-suppressions` allows.
Load this contract's `assets/` configuration from the repository's lint, replacing its executable path patterns, `scripts/` and `bin/` folders, with the declared ones in rule copies.

Violation: `// TODO: retry on 429` above a fetch call, or `// Receipts.send({ order });` left behind after a refactor.
Allowed: the retry is an open tracker issue, and the comment above the call reads `// The provider's 429 carries no retry-after, so the caller chooses when to retry.`
Violation: `// Workflow sleeps must not hold a connection.` sits above the module's private `function openConnection({ pool }: OpenConnectionInput): Connection`, so its callers never see it.
Allowed: `/** Opens a connection that no workflow sleep may hold. */` sits directly above that function.
Violation: `main` in `scripts/migrate-orders.mts` labels its work `// (b) Copy the rows.` and copies the rows inline.
Allowed: `main` calls `copyRows({ source, target })`, and `scripts/migrate-orders.mts` opens with a doc comment that says what it migrates and gives the command `./scripts/migrate-orders.mts --month <month>`.
Violation: `// retryAfter is absent on a 429, so the caller waits.` opens with a lowercase identifier.
Allowed: ``// `retryAfter` is absent on a 429, so the caller waits.``
Violation: the doc comment above `settleInvoice` ends with `@returns The receipt.` and `@throws InvoiceRefunded`, or a file opens with `// SPDX-License-Identifier: MIT`.
Allowed: `/** Returns the receipt, and fails with InvoiceRefunded when a refund already closed the invoice. */` above `settleInvoice`, and no notice in any source file.

## Checks

Run the repository's lint from the repository root, and confirm that it rejects each form these rules name wherever a tool decides it, such as a step label.
Read each changed comment for any form the lint does not reject.
For each suppression of a marker word that a change adds, does the word name a domain concept rather than unfinished work?
For each comment a change adds, is it free of disabled code that the lint's patterns miss, such as a statement inside a block comment?
For each file a change adds that the repository executes directly, does its summary say what it does and how to run it?
Is each comment a change adds whole sentences, and does each one the lint skips open with a backticked identifier, a type annotation, a directive, or a continued sentence?
