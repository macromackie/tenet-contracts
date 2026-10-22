---
name: code-script-entry-points
message: Keep the top level of every file the repository executes directly to declarations and one statement that runs its main program.
---

## Rules

Apply this contract to every file the repository executes directly, such as automation scripts, smoke and qualification checks, fixture servers started as processes, development tools, and command entry points; `code-function-size` then limits all of their work.
Hold only imports, type declarations, function and class declarations, constant declarations, and one statement that runs the main program at the top level of an executable file.
Running the main program means one call to the main function, awaited or not, one call that hands the main program to its runtime's entry function, or one call that ends the process and whose only argument is one of those calls.
A guard that runs the main program only when the file is executed directly, such as comparing the module's path with the process's first argument, is part of that statement when its body holds only that call.
Declare the calls that may initialize a top-level constant, such as resolving a directory from the module's location or building a validation schema, and initialize each top-level constant only from literals, functions, other constants, the module's location, and those calls.
A top-level statement or constant that awaits, starts a process, opens a server, reads or writes a file, reads the process's arguments or environment, branches, loops, or wraps the rest of the file in a `try` block is a violation.
Attaching an error handler to the main call at the top level is a violation; the main function or the runtime's entry function handles its own failure.
A test file that registers cases, groups of cases, and setup and teardown hooks with the test runner, at its top level or as the only statements inside a group, such as `test("a replayed order creates no second invoice", ...)`, holds declarations and is allowed; a loop or branch that registers cases is a violation.
Keep functions that other modules import out of an executable file, so that no file is both an entry point and a library.
Enforce these rules with the repository's lint over every executable file, declared by path pattern, and suppress a finding only as `code-lint-suppressions` allows.

Violation: `check-orders` creates its temporary directory, starts the server, and runs forty checks inside one top-level `try` block.
Allowed: `check-orders` ends with `await main()`, and `main` starts the environment, runs each scenario function, and stops the environment.

## Checks

Run the repository's lint from the repository root and confirm that it reports top-level work in every declared executable file.
For each call a change adds to the declared calls that may initialize a top-level constant, does it compute its value without an effect?
For each file a change adds that the repository executes directly, does a declared path pattern cover it?
For each executable file a change touches, does any other module import from it?
