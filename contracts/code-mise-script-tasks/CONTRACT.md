---
name: code-mise-script-tasks
message: Make every repository script a mise file task in the `mise-tasks/` folder of the root or package that owns it, and run repository work in CI only through `mise run`.
---

## Rules

This contract extends `ci-reproducible-checks`, which runs one declared check graph locally and in CI, and `code-script-entry-points`, which limits what each script's top level holds.
A repository script is a file that a person or CI runs to work on the repository, such as a check, a code generator, a smoke run, or a release step, and not a program the product ships or a file that a test runner loads.
Make every repository script a mise file task in the `mise-tasks/` folder of the repository root or of the package that owns its work, and keep scripts out of every other folder.
Exempt only the bootstrap that installs mise and a one-line shim that another program runs by path, such as a version-control hook that runs one task.
Put each module that only tasks import or start as a process, and that nobody runs as a task, in the `lib/` subfolder of that `mise-tasks/` folder.
Commit each task file with its executable bit set and every other file in a task folder without it, because mise lists only executable files as tasks on POSIX systems.
Keep `.toml` files, installed packages, and executable build outputs out of every task folder, because mise reads each `.toml` file there as task configuration and lists every executable file there as a task.

Declare a task in TOML only when it runs one command of one tool, only groups other tasks through `depends`, defines a task template, or extends one, and write every other task as a file task.
Never write a TOML task that runs a repository file by its path, such as an interpreter followed by a script's path; make that file a file task instead.
Make every CI step that runs repository work call `mise run`; only the steps that install mise and its pinned tools are exempt.

Violation: a TOML task `export-invoices` runs an interpreter on `tools/export-invoices`, and CI runs the same interpreter and path through `mise exec`.
Violation: the helper `mise-tasks/lib/invoice-totals` is executable, so `mise tasks ls` lists it as the task `lib:invoice-totals`.
Allowed: the executable `mise-tasks/invoices/export` imports the helper `mise-tasks/lib/invoice-totals`, and CI runs `mise run invoices:export 2026-10`.

## Checks

Run `mise tasks ls --hidden` from the repository root and from each package that holds a `mise-tasks/` folder, and confirm that the listings name every repository script and no helper module, installed package, or build output.
List the files that version control marks executable outside `mise-tasks/` folders, and confirm that each is the bootstrap, a one-line shim, a program the product ships, or a file that a test runner loads.
Search CI workflows for steps that run a script by its path, through an interpreter, or through `mise exec`, and confirm that each step that runs repository work calls `mise run` instead.
For each TOML task a change adds, does it run one command of one tool, only group tasks through `depends`, define a template, or extend one?
