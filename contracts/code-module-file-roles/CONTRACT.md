---
name: code-module-file-roles
message: Give each source file one declared role and at most one class, component, and exported function, export only components from markup files, and split multi-role modules into folders.
requires-tenet: 0.11.0
---

## Rules

Declare the file roles the repository uses, such as types, constants, schemas, errors, and behavior, and the file name that marks each role, such as `types` or `constants`.
Give each source file one role: a types file declares only types, a constants file only named constants, a schema file only validation schemas, and a behavior file only functions and classes.
Put a module's type declarations in a types file in the same folder as the code that uses them.
Put a module's named constants, such as limits, default values, and fixed lists, in a constants file in the same folder.
Keep functions out of a constants file: a named object, list, or lookup table whose values are functions is behavior and belongs in a behavior file.
A type derived from a schema or a constant, such as a schema's decoded type or the union of a constant object's values, may stay beside it.
A type that a framework convention expects beside its implementation, such as a user interface component's props, may stay in the component's file.
Keep a type that several modules share in the types file of the module that owns the concept, never in one repository-wide types file.

Declare at most one class and at most one user interface component in each source file, exported or not.
A module's error classes, such as tagged error classes, may share one declared errors file, and its schema classes one declared schemas file, each holding only those classes.
Export only user interface components, their props types, and declared framework names from a source file whose code holds markup, such as a `.tsx` or `.jsx` file.
Put the hooks, contexts, and constants that components share in source files without markup, so a development server can hot-swap a component file and keep its state.
Declare the names the repository's frameworks require a file to export, such as `generateMetadata` or `loader`, and count them toward neither the component-only nor the one-function limit.
A route, story, or test file, which a framework loads by its path, may keep its component unexported and export only what that framework loads, such as `Route`.
The shipped lint files list default framework names, skip `routes` folders and story and test files in the component-only lint, and a repository may add names and patterns.

When a module holds declarations of several roles, make it a folder named for the module with one file per role, such as `invoice-import/schemas`, `invoice-import/types`, and `invoice-import/parse-lines`.
Declare at most one exported function in each source file, so that operations other files call, such as building a command and parsing its output, sit in separate files.
An exported function is one that the file declares, or binds as a value to a name, for another file to import; re-exporting another file's function does not count.
A file may keep its exported function's private helpers, such as the function for one case of its branch, unexported beside it.
A namespace file, which an entry point re-exports under one namespace named for the file, may export several functions on that namespace's concept, such as `generate` and `validate`.
Exempt namespace files from the one-function limit by a declared path pattern that matches no other file.

Declare a maximum source file length in lines, and enforce it and the one-function, one-class, and one-component limits with the repository's lint.
Leave a language's limit on functions, classes, or components to review only by declaring the language and the reason beside the declared length.
Where the repository's lint can load this contract's `assets/` configuration, load it from the repository's own lint configuration, and turn on its markup plugin where code holds markup.
Suppress a finding only as `code-lint-suppressions` allows, and exempt generated files from these rules by a declared path pattern.

Violation: one invoice import module declares four validation schemas, the importer, and the line parser that reads them.
Violation: the `invoice-import/import-invoices` file exports both `importInvoices` and `parseLines`.
Allowed: an `invoice-import` folder holds `schemas`, `types`, `import-invoices`, and `parse-lines` files, and each one holds only its role.
Allowed: `uuid/uuid` exports `generate` and `validate`, `uuid/index` re-exports it as the namespace `Uuid`, and the declared namespace pattern matches it.
Violation: `use-invoice-dialog.tsx` exports only the `useInvoiceDialog` hook, which returns its open state and the markup of an unexported `InvoiceDialog` component.
Allowed: `use-invoice-dialog.ts` exports the `useInvoiceDialog` hook, which returns only its open state, and `invoice-dialog.tsx` exports only `InvoiceDialog`.
Violation: `invoice-list.tsx` declares the exported `InvoiceList` and an unexported `InvoiceRow` component that it renders.
Allowed: `invoice-row.tsx` holds `InvoiceRow`, and `invoice-import/errors.ts` declares both the `InvoiceRejected` and `InvoiceMissing` tagged error classes.

## Checks

Outside review-only languages, confirm the repository's lint run from its root reports an overlong file, a second exported function, and a second class outside errors and schemas files.
Run the repository's lint from the repository root and confirm that it reports a hook exported beside a component, and a second component, in a file with markup.
For each changed file, which declared role does it hold, and does any declaration in it belong to another role?
Does the change add a type, a named constant, or a schema to a behavior file?
For each function a change exports, including through an export list, a default export, or a call's result, is it its file's only one or in a namespace file?
For each path the declared namespace pattern matches, does an entry point re-export that file under one namespace named for the file?
Does each file with markup that a change touches export only components, their props types, and declared framework names?
