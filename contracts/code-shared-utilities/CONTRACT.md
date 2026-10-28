---
name: code-shared-utilities
message: Keep domain-free helpers in the application's one shared utilities module, one per file, and use the declared utility library first.
---

## Rules

A utility is a function whose behavior does not depend on its caller's domain, such as clipping text, grouping a list, retrying a call, or formatting a date.
Declare one shared utilities module for each application, and let every package or component of that application import it.
Put each utility in that module, in its own file named for its behavior, such as a `clip-text` file whose one export clips text.
Never declare a utility function outside the shared utilities module, whether in a domain module, beside its one caller, or in a utilities folder that belongs to one package.
A domain-free helper that only tests, smoke checks, and test scripts call belongs in the test support folder that `test-support-modules` declares, not in the shared utilities module.
Declare the utility library the repository uses, and write a utility only when that library lacks the behavior the caller needs.
Keep domain types, domain constants, and domain rules out of a utility, and let the caller pass domain values in as inputs.
A function that reads its module's own domain types, constants, or rules is domain code, not a utility, and stays in its module as `code-module-structure-and-control-flow` requires.
A type declared only for a function's own input or result does not make that function domain code.
A callback written inside the call that uses it, such as `orders.filter((order) => order.isPaid)`, is part of that call, not a utility.

Violation: an invoice export module declares `clip({ text })`, which cuts any string to a fixed length and reads nothing about invoices.
Allowed: the utilities module's `clip-text` file exports a function that takes the text and a maximum length, and the export module passes its own line limit.

## Checks

For each function a change adds outside the utilities module, does its body depend on its module's domain, or is it a utility in the wrong place?
For each utility a change adds, does the declared utility library already provide it?
Does the change add a module of domain-free functions, under any name, other than the declared utilities module?
