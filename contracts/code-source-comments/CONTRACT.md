---
name: code-source-comments
message: Write no prose comment in source except a tool directive with its reason and a counted allowance of reason comments inside function bodies.
requires-tenet: 0.11.0
---

## Rules

Apply these rules to maintained production code, tests, and scripts, and not to generated or copied third-party source.
This contract conflicts with the doc comment contracts, `code-typescript-doc-comment-coverage`, `code-python-doc-comment-coverage`, and `code-rust-doc-comment-coverage`, which require the doc comments that it forbids.
It also conflicts with the comment form contracts, `code-comment-form`, `code-comment-content`, and `code-comment-attribution`, which govern the comments that it forbids.
Adopt this contract or that family of six in one scope, never both.

Write no comment and no doc comment in source, in any comment syntax, and no string that stands alone as a statement to document code.
State what a declaration is in its name, its type, and its schema.
State what a package is, what its folders hold, and how to use it in the package's README.
State an invariant as a check, with its sentence in a contract or in the list of things a change must never do in the package's README.
State why a decision was made in the repository's decision notes, never beside the code.

A tool directive is a comment that a tool reads, such as a lint suppression, a copied-block marker, or a type checker's expected-error line.
Keep a tool directive, in the form its tool requires, with its reason inside it as `code-lint-suppressions` describes.
A directive whose tool reads no text there, such as a marker that ends a block, an interpreter line, or a script's metadata block, carries no reason.
A comment that a lint requires above an unsafe operation is a directive whose text is its reason.

A reason comment is the one prose comment allowed: a single line comment inside a function body that starts with `Why:` and states what the next line cannot show, such as an external constraint.
Write each reason comment as `Why:`, one space, and one sentence, and never write one outside a function body.
Declare the maximum number of reason comments for the whole scope; the shipped policy sets 10, which a repository may override.
Lower the maximum when reason comments are removed, and raise it only in a change whose description names the new comment.
Before adding a reason comment, try a name, a narrower type, or a named function that states the same fact, and add the comment only when none can.

Configure the repository's lint to reject every other comment, and load this contract's `assets/` configuration from it.
Suppress no finding of these rules; a comment that must stay is a directive or a reason comment.

Violation: `/** Settles the invoice. */` above `settleInvoice`, or `// The provider rejects a second capture within one second.` above a call inside it.
Allowed: the function is named `settleInvoice`, and the line above the call reads `// Why: the provider rejects a second capture within one second.`
Violation: `// Why: retries are capped by the provider.` above a module constant, outside every function body.
Allowed: the constant is named `PROVIDER_RETRY_MAXIMUM`, and the package's README says never to raise it above the provider's limit.

## Checks

Run the repository's lint from the repository root, and confirm that it loads this contract's rules for each language the scope holds.
Run the checker in this contract's `assets/` folder from the repository root with the repository's comment policy, where its runtime can run.
For each reason comment a change adds, could a name, a type, or a named function state the same fact?
For each comment a change deletes, does the fact it held still live in a name, a type, a README, a contract, or a decision note, or was it a restatement?
Does the scope adopt none of the six contracts that this contract conflicts with?
For each change to the declared maximum, does the change's description name the comment that needs it?
