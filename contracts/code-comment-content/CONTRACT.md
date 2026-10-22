---
name: code-comment-content
message: Write comments that state what the code cannot show, never what it already says, what it used to do, or a shape that a declaration could carry.
---

## Rules

Apply these rules to comments and doc comments in maintained production code, tests, and scripts; `code-comment-attribution` separately governs comments that name contracts or review tools, and `code-comment-form` governs task markers, commented-out code, and doc comment layout.
A doc comment that a framework publishes as interface text, such as a command's derived help line, is interface text rather than a code comment, and these rules leave it out.
Write a plain comment only for a reason, an external constraint, an invariant, or a consequence that the code and its names cannot show.
Write a declaration's doc comment for what callers rely on beyond its name, such as what it returns, accepts, guarantees, or refuses.
Never restate the code below a comment or the name a doc comment documents, such as `// Increment the retry count` above `retries += 1` or `/** The proxy base URL. */` above `proxyBaseUrl`.
Never narrate change history, such as what the code used to do or when it changed, and record that history in commit messages and release notes instead.
Commented-out code, including an earlier implementation kept for reference, is outside these rules, so judge only the prose comments beside it.
A comment that names an earlier stored format, schema revision, provider response, or release that current code, a migration, or a test still handles is allowed, such as "revisions written before format 2 list their files in each assessment".
Citing an incident or issue as the reason for current behavior, which `code-comment-attribution` allows, is not change history.
Never describe a value's shape in a comment when a type or schema can declare it, and name that declaration instead, such as "JSON that `Publication` decodes"; `code-closed-value-sets` owns declaring a set of allowed values.
When a doc comment documents an optional or nullable field, say what the field's absence means, such as "absent when the check sent no model request", and when the field can be either omitted or null, say what each means.

Violation: `/** JSON {draft, maxFiles, maxBytes}. */` above an environment variable that the `Publication` schema decodes, which repeats the schema in prose that can drift from it.
Allowed: `// The provider allows ten minutes; the issue time sits a minute back to absorb clock drift.` above the token's issue time, which gives the external limit and the reason for the offset.

## Checks

For each comment a change adds or edits, what reason, constraint, invariant, consequence, or caller reliance does it state that the code does not?
Does any changed comment describe what the code used to do, or a shape that a declaration could carry, outside the stored-format and incident allowances?
For each optional or nullable field a change documents, does its doc comment say what absence means, and for a field that can be either omitted or null, what each means?
