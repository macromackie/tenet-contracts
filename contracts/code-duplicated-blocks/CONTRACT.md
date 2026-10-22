---
name: code-duplicated-blocks
message: Fail checks on every copied block that the repository's copy detector reports, and remove the copy by calling one declaration.
---

## Rules

Declare one copy detector, its minimum clone size in tokens and in lines, and the path patterns it skips, in one configuration file beside each root check command, including the root check command of an exported product.
Run the detector over every file in each programming language the repository checks, including tests and scripts, and fail checks when it reports any clone at or above the minimum size.
Configure the detector to read files of every length, because a detector that skips long files misses the copies in them.
Skip only generated files, build output, copied third-party source, and test input files, such as recorded responses and fixture projects, that tests read rather than import or start, each by a declared path pattern.
Adding a skip pattern to hide one clone, raising the minimum size, and setting any other detector option that narrows which clones it reports, such as one that ignores copies within one folder, are violations.

Remove a reported clone by keeping one declaration and calling it from every place that held a copy, placed as `code-module-structure-and-control-flow` and `code-shared-utilities` require.
A copy at or above the minimum size that keeps the same steps under renamed identifiers is a clone even when the detector does not report it.
Suppress a clone only with the start and end markers that `code-lint-suppressions` requires for a finding that spans a block.
The reason in a start marker states why both copies must stay, such as two shipped migrations that must keep the steps they ran.
Repeated code shorter than the declared minimum size, repeated configuration files, and copies between repositories, which `code-cross-repository-copies` covers, are outside this contract.

Violation: a second smoke script adds a 9-line copy of the first script's worker startup instead of calling it.
Allowed: both smoke scripts call `startWorker({ port, log })` from the module that declares it.

## Checks

From each directory that holds a root check command, run the copy detector with its configuration, and confirm that it reads files of every length and fails on a single clone.
From the same directory, run the repository's checks, and confirm that they fail on a start marker without a reason, on markers around a whole file, and on markers around a block that no longer has a copy.
Does the change add a skip pattern, raise the minimum size, or set any other detector option that narrows which clones the detector reports?
For each block the change adds, does it repeat the steps of an existing block under renamed identifiers?
