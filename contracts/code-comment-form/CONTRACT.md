---
name: code-comment-form
message: Commit no task markers, commented-out code, or empty doc comments, and give doc comments and file summaries one lint-enforced layout.
---

## Rules

Apply these rules to comments and doc comments in maintained production code, tests, scripts, and examples, and not to generated or copied third-party source.
Never write a task marker, such as `TODO`, `FIXME`, `XXX`, or `HACK`, in a comment, in any letter case and at any position in the comment.
Record unfinished work in the task tracker instead of a comment.
A marker word that names a domain concept, such as the `todo` status of a task product, is allowed with the suppression that `code-lint-suppressions` describes.
Never commit commented-out code, such as a disabled statement, an earlier implementation, or an alternative kept for reference.
A code fragment inside a sentence that explains behavior, such as "`./src/a.rs` names `src/a.rs`", is prose and is allowed.
Never commit an empty doc comment.
Write a block doc comment that holds no tag and fits within the declared maximum line length on one line, such as `/** The run's deadline. */`.
Put the opening and closing markers of any longer or tagged block doc comment on lines of their own.
A block comment that holds only the type of the value that follows, such as `/** @type {Order} */`, is type syntax rather than a doc comment.
Write a file's summary as the file's first comment after any lines that must open the file, such as a shebang, a build constraint, or a license notice, and above its imports, in the language's doc comment form, such as `//!` or `/** ... */`.
Configure the repository's lint to reject each of these forms wherever a tool decides it.

Violation: `// TODO: retry on 429` above a fetch call, or `// const total = sum({ items });` left behind after a refactor.
Allowed: the retry is an open tracker issue, and the comment above the call reads `// The provider's 429 carries no retry-after, so the caller chooses when to retry.`

## Checks

Run the repository's lint from the repository root, and confirm that it rejects task markers, commented-out code, empty doc comments, short multi-line doc comments, text on the marker lines of a longer one, and a file summary below the imports, wherever a tool decides the form; read each changed comment for any form the lint does not reject.
For each suppression of a marker word that a change adds, does the word name a domain concept rather than unfinished work?
For each comment a change adds, is it free of disabled code that the lint's patterns miss, such as a statement inside a block comment?
