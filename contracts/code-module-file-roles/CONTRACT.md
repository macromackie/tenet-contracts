---
name: code-module-file-roles
message: Give each source file one declared role and at most one exported function, keep types in a sibling types file, and make a module with several roles a folder.
requires-tenet: 0.11.0
---

## Rules

Declare the file roles the repository uses, such as types, constants, schemas, and behavior, and the file name that marks each role, such as `types` or `constants`.
Give each source file one role: a types file declares only types, a constants file only named constants, a schema file only validation schemas, and a behavior file only functions and classes.
Put a module's type declarations in a types file in the same folder as the code that uses them.
Put a module's named constants, such as limits, default values, and fixed lists, in a constants file in the same folder.
Keep functions out of a constants file, including functions stored as values in a named object or list.
A lookup table whose values are functions is behavior and belongs in a behavior file.
A type derived from a schema or a constant, such as a schema's decoded type or the union of a constant object's values, may stay beside it.
A type that a framework convention expects beside its implementation, such as a user interface component's props, may stay in the component's file.
Keep a type that several modules share in the types file of the module that owns the concept, never in one repository-wide types file.

When a module holds declarations of several roles, make it a folder named for the module with one file per role, such as `invoice-import/schemas`, `invoice-import/types`, and `invoice-import/parse-lines`.
Declare at most one exported function in each source file, so that operations other files call, such as building a command and parsing its output, sit in separate files.
An exported function is one that the file declares, or binds as a value to a name, for another file to import; re-exporting another file's function does not count.
A file may keep its exported function's private helpers, such as the function for one case of its branch, unexported beside it.
A namespace file, which an entry point re-exports under one namespace named for the file, may export several functions on that namespace's concept, such as `generate` and `validate`.
Exempt namespace files from the one-function limit by a declared path pattern that matches no other file.

Declare a maximum source file length in lines, and enforce it and the one-function limit with the repository's lint.
Leave a language's one-function limit to review only by declaring that language and the reason beside the declared length, such as that no lint counts its exported functions.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Suppress a finding only as `code-lint-suppressions` allows.
Exempt generated files from these rules by a declared path pattern.

Violation: one invoice import module declares four validation schemas, the importer, and the line parser that reads them.
Violation: the `invoice-import/import-invoices` file exports both `importInvoices` and `parseLines`.
Allowed: an `invoice-import` folder holds `schemas`, `types`, `import-invoices`, and `parse-lines` files, and each one holds only its role.
Allowed: `uuid/uuid` exports `generate` and `validate`, `uuid/index` re-exports it as the namespace `Uuid`, and the declared namespace pattern matches it.

## Checks

Run the repository's lint from the repository root and confirm that it enforces the declared length and reports a second exported function, except in a language left to review.
For each changed file, which declared role does it hold, and does any declaration in it belong to another role?
Does the change add a type, a named constant, or a schema to a behavior file?
For each function a change exports, including through an export list, a default export, or a call's result, is it its file's only one or in a namespace file?
For each path the declared namespace pattern matches, does an entry point re-export that file under one namespace named for the file?
