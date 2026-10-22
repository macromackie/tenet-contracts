---
name: code-module-file-roles
message: Give each source file one declared role, keep types in a sibling types file, and turn a module with several roles into a folder.
---

## Rules

Declare the file roles the repository uses, such as types, constants, schemas, and behavior, and the file name that marks each role, such as `types` or `constants`.
Give each source file one role: a types file declares only types, a constants file only named constants, a schema file only validation schemas, and a behavior file only functions, classes, and the module state they own, such as a cache.
Put a module's type declarations in a types file in the same folder as the code that uses them.
Put a module's named constants, such as limits, default values, and fixed lists, in a constants file in the same folder.
Keep functions out of a constants file, including functions stored as values in a named object or list.
A lookup table whose values are functions is behavior and belongs in a behavior file.
A type derived from a schema or a constant, such as a schema's decoded type or the union of a constant object's values, may stay beside it.
A type that a framework convention expects beside its implementation, such as a user interface component's props, may stay in the component's file.
Keep a type that several modules share in the types file of the module that owns the concept, never in one repository-wide types file.

When a module holds declarations of several roles, make it a folder named for the module with one file per role, such as `invoice-import/schemas`, `invoice-import/types`, and `invoice-import/parse-lines`.
Put independent operations of a behavior module, such as building a command and parsing its output, in separate files of that folder.
Declare a maximum source file length in lines, and enforce it with the repository's lint.
Exempt generated files from these rules by a declared path pattern.

Violation: one invoice import module declares four validation schemas, the importer, and the line parser that reads them.
Allowed: an `invoice-import` folder holds `schemas`, `types`, `import-invoices`, and `parse-lines` files, and each one holds only its role.

## Checks

Run the repository's lint from the repository root and confirm that it enforces the declared file length.
For each changed file, which declared role does it hold, and does any declaration in it belong to another role?
Does the change add a type, a named constant, or a schema to a behavior file?
