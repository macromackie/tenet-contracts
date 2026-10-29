---
name: code-diagnostic-messages
message: Write each diagnostic as one clause that starts with a lowercase word, names the failed operation and its input, quotes every value it interpolates, and ends without a period.
requires-tenet: 0.11.0
---

## Rules

A diagnostic is a line a program writes for a person about its run, such as an error, a refusal, a warning, or a progress line, and the message of any error it raises.
Prefix each diagnostic line that a command-line program writes once with the program's name, a colon, and a space, such as `deploy:`, where its output module writes the line, never inside the error message itself.
End each message without a period, and join its clauses with a colon or a semicolon instead of writing a second sentence.
Name the operation that failed and the input it failed on, such as a file, a record, or a command.
Carry the cause's own message in the error's cause chain when the output module prints that chain, and otherwise append it to the message after a colon.
A log or trace record that the program exports is not a diagnostic; `telemetry-application-tracing` governs its fields and how it records a cause.
When the reader can fix the failure, add the fix as an imperative clause after a semicolon, such as `; check out a clean "v0.3.1"`.
Enforce the trailing period with the repository's lint.

Quote every value a diagnostic interpolates, whatever its type, with the language's form that prints a string literal with escapes, such as `JSON.stringify(value)`, `{value:?}`, or `{value!r}`.
Quote a number too, so that one form serves every value, and quote a `bigint`, which `JSON.stringify` throws on, as its text, such as `JSON.stringify(amountText)` after `const amountText = String(amount)`.
Never convert a value in a diagnostic another way, such as with `String(value)` outside that `bigint` form, and never wrap it in hand-written quotes or backticks.
A cause's own message after a colon is text, not a value, so write it unquoted in the language's message form: a `message` read, `{error:#}`, or `{error!s}`.
Enforce the quoting with the repository's lint, which reads each message an error carries, whether thrown, failed, declared by its type, or returned beside its code.
Write a line an output module receives unquoted after the program's prefix, since its caller composed that diagnostic; the lint leaves the module's lines to review.

Start each diagnostic with a lowercase word in every language, even one whose own errors start with a capital, so that it reads correctly after a colon.
Apply this to every message an error carries, including a message template that an error type declares and the context that a program adds to a cause.
Keep the spelling of a first word that is a proper noun, such as a product's name, or an identifier or code, such as `ENOENT`.
A diagnostic that starts with an interpolated value, such as a file path, starts with that value as it is.
Text that reproduces another program's message, such as a test fake's copy of a dependency's error, keeps that program's spelling.
Enforce this with the repository's lint, which reports a first word of one capital and only lowercase letters unless a declared list of proper nouns holds it.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
That folder also ships a default list of proper nouns as one shared rule.
A repository adds its own names in its own copy of that rule, which its lint configuration loads in place of the shipped one.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `Commit or stash every change first.` starts with a capital, ends with a period, and names neither the operation nor the uncommitted files.
Violation: `Cannot read "invoices/7.json"` starts with a capitalized common word, so it reads wrongly after a colon, as in `import: Cannot read "invoices/7.json"`.
Violation: `import: read "invoices/7.json": no such file` above a printed cause chain that ends in `no such file` shows the cause's message twice.
Violation: the message `` `read invoice ${path}` `` prints `read invoice` and a trailing space when `path` is empty, so the reader cannot see which value failed.
Allowed: `tag "v0.3.1": the working tree has "2" uncommitted files; commit or stash them` names the operation, its input, and the fix.
Allowed: where the output prints no cause chain, `` `read invoice ${JSON.stringify(path)}: ${error.message}` `` prints `read invoice "": no such file`, showing the empty path.
Allowed: `OrderStore.settle refused invoice "7": the invoice is closed` starts with an identifier spelled as the code spells it.

## Checks

Run the repository's lint from the repository root, and confirm that it rejects a trailing period, a capitalized common first word, and a bare interpolated value.
For each diagnostic a change adds, does it name the failed operation and its input?
For each error with a cause that a change adds, is the cause's message only in a printed chain, or after a colon when the output prints none?
For each diagnostic a change adds that starts with a capital, is its first word a proper noun or an identifier?
Does any message a change adds also carry the program's prefix that its output module adds?
For each line a change composes for the output module to write, is every value it interpolates quoted?
