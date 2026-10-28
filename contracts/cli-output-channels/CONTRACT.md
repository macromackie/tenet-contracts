---
name: cli-output-channels
message: Write a command-line program's result to standard output and every other line to standard error through one output module, and end the process only from its entry point with a declared exit status.
---

## Rules

Apply these rules to command-line programs, scripts, eval runners, and test harnesses.
Lines that `telemetry-application-tracing` covers, such as a server's log lines, follow that contract instead of these rules.
Declare one output module for each program, and write to standard output and standard error only through it.
Never call a console method or a print macro, or open a handle to either standard stream, outside the output module.
A function that receives a writer from the output module may write to that writer.
Write the program's result, such as a report, the matches it found, or a machine-readable document, to standard output.
Write every other line, such as progress, warnings, errors, prompts, and the closing summary, to standard error, so that a reader of standard output receives only the result.
When the program writes a machine-readable document, write each error of the run as a record of that document, in the same envelope as its results.
Declare each machine-readable document's schema version once, as a named constant of the module that declares the document's schema, and have the output module write it from that constant.

End the process only from the program's entry point, by returning its exit status or by passing it to the output module's one exit function, such as `finish({ status })`.
Declare the program's exit statuses once, as a closed set whose member names say what each status means.
When the program has a command model, declare its exit statuses there, so that the generated command reference lists them.
A process exit status, including 0 and 130, is a value the program defines, not one a protocol defines, so `code-closed-value-sets` governs it like any other closed set.
Library code returns an outcome from a closed set, such as a review's overall status, and only the entry point maps each outcome to its exit status.

Enforce these rules with the repository's lint, which reports every console call, print macro, and stream handle outside the output module, every process exit outside the output module and the entry point, and every exit status written as a number outside the one declaration of the program's exit statuses.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: a deploy step calls `console.log('deploy: waiting for readiness')` and then `process.exit(1)` in the middle of the script.
Allowed: the deploy step calls the output module's `reportProgress({ line: 'waiting for readiness' })`, and the entry point passes `ExitStatus.Refused` to `finish`.

## Checks

Run the repository's lint from the repository root and confirm that it reports console calls, print macros, stream handles, process exits, and numeric exit statuses outside their declared paths.
For each line a change writes, is it the program's result on standard output or a diagnostic on standard error?
Does library code in the change compute a process exit status, such as a function that returns 2 or 130, instead of returning an outcome?
For each machine-readable document a change writes, does its schema version come from the one constant of the module that declares the document's schema?
