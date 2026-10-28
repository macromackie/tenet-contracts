---
name: code-comment-content
message: Write comments that state what the code cannot show, never what it already says, what it used to do, or a shape that a declaration could carry.
---

## Rules

Apply these rules to comments and doc comments in maintained production code, tests, and scripts.
`code-comment-attribution` separately governs comments that name contracts or review tools.
`code-comment-form` governs task markers, commented-out code, step labels, and the form, placement, and layout of comments.
A doc comment that a framework publishes as interface text, such as a command's derived help line, is interface text rather than a code comment, and these rules leave it out.
Write a plain comment only for a reason, an external constraint, an invariant, or a consequence that the code and its names cannot show.
Write a declaration's doc comment for what callers rely on beyond its name, such as what it returns, accepts, guarantees, or refuses.
Never restate the code below a comment or the name a doc comment documents, such as `// Increment the retry count` above `retries += 1` or `/** The proxy base URL. */` above `proxyBaseUrl`.
Never narrate change history, such as what the code used to do or when it changed, and record that history in commit messages and release notes instead.
Commented-out code, including an earlier implementation kept for reference, is outside these rules, so judge only the prose comments beside it.
A comment may name an earlier stored format, schema revision, provider response, or release that current code, a migration, or a test still handles.
An example is "Revisions written before format 2 list their files in each assessment."
Citing an incident or issue as the reason for current behavior, which `code-comment-attribution` allows, is not change history.
Never describe a value's shape in a comment when a type or schema can declare it, and name that declaration instead, such as "JSON that `Publication` decodes"; `code-closed-value-sets` owns declaring a set of allowed values.
When a doc comment documents a field that may hold no value, say what its absence means, such as `/** Absent when the check sent no model request. */`.
When the field can be either omitted or null, say what each means.

Violation: `/** JSON {draft, maxFiles, maxBytes}. */` above an environment variable that the `Publication` schema decodes, which repeats the schema in prose that can drift from it.
Allowed: `// The provider allows ten minutes; the issue time sits a minute back to absorb clock drift.` inside the signing function explains the external limit and the offset.

## Checks

For each comment a change adds or edits, what reason, constraint, invariant, consequence, or caller reliance does it state that the code does not?
Does any changed comment describe what the code used to do, or a shape that a declaration could carry, outside the stored-format and incident allowances?
Does each changed doc comment on a field that may hold no value say what absence means, and for one that can be omitted or null, what each means?
