---
name: code-diagnostic-messages
message: Write each diagnostic as one clause that names the failed operation and its input, without a trailing period.
---

## Rules

A diagnostic is a line a program writes for a person about its run, such as an error, a refusal, a warning, or a progress line, and the message of any error it raises.
Prefix each diagnostic line that a command-line program writes once with the program's name and a colon, such as `deploy: `, where its output module writes the line, never inside the error message itself.
End each message without a period, and join its clauses with a colon or a semicolon instead of writing a second sentence.
Name the operation that failed and the input it failed on, such as a file, a record, or a command, and append the cause's own message after a colon, either in the message itself or through the error's cause chain that the output module prints, never both.
In a log or trace record that the program exports, record the cause as `telemetry-application-tracing` requires instead of appending its message.
When the reader can fix the failure, add the fix as an imperative clause after a semicolon, such as `; check out a clean v0.3.1`.
Enforce the trailing period with the repository's lint.

Violation: `Commit or stash every change first.` ends with a period and names neither the operation nor the uncommitted files.
Allowed: `tag v0.3.1: the working tree has 2 uncommitted files; commit or stash them` names the operation, its input, and the fix.

## Checks

Run the repository's lint and confirm that it rejects a diagnostic that ends with a period.
For each diagnostic a change adds, does it name the failed operation and its input?
Does any message a change adds also carry the program's prefix that its output module adds?
