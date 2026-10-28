---
name: code-module-structure-and-control-flow
message: Keep modules focused and named for their behavior, start every lowercase function name with a declared verb, and keep inputs, results, and control flow explicit.
requires-tenet: 0.11.0
---

## Rules

Give each module one understandable responsibility.
Name modules for the behavior or resource they own.
Name each function, type, and file, whether exported or not, and each stored or wire value, for the behavior or concept it stands for, never with a generic word alone such as `data`, `info`, `item`, `manager`, `handler`, or `script`.
A declared file role, such as `types` or `constants`, is not a generic name for a file that holds that role.
Write a generic stored or wire name or value that another system fixes, or that a released format keeps as `data-stored-and-shipped-formats` requires, only in the mapping that reads or writes it, such as a serializer rename that decodes an order's `item` field into `lineItem` or an enumeration member `LineItem` whose value is `'item'`.
A serializer rename or an enumeration member's declared value that keeps the external name is the allowed mapping; an owned field, type, or member that carries the generic name is not.
Do not create catch-all modules, such as `helpers`, `common`, or `misc`, that mix code of unrelated concerns.
A shared utilities module that holds only domain-free functions, one per file, as `code-shared-utilities` defines, and a test support folder that holds one helper or fixture per file, as `test-support-modules` defines, are not catch-all modules.
Create a module only when it has an actual responsibility; do not add placeholder files.
Split a module when the split reduces the context needed to understand a change, and keep cohesive code together when splitting would obscure its invariants.
Keep a helper that depends on its module's domain private to that module until another caller needs it.

Extract a helper only when it names a real concept, collapses real duplication, or isolates an independent operation, never just to shorten a block.

Pass inputs and return results explicitly instead of relying on hidden side effects or ambient mutable state.
State that one object or closure owns and changes only through its own functions, such as a cache field, is not ambient state.
Name intermediate values when nested calls hide the sequence, in code that `code-typescript-call-arguments` does not govern.
Name values for what they hold.

Never write by hand the parsing, validation, or provider integration that a maintained library provides; call the library and use its types.

Declare a list of verbs, such as `read`, `create`, and `settle`, and start every owned function, method, function-typed member, and function-valued constant whose name begins in lowercase with one.
Match that first word in every case style, such as `settle` in `settleInvoice` and `settle_invoice`, and configure the repository's lint to reject any other first word.
The list also holds predicate prefixes from `code-boolean-names`, `on` for event handlers such as `onSubmit`, `use` for hooks, and per-language constructor and conversion prefixes such as `new` and `into`.
List only verbs and these prefixes, never a noun or adjective such as `total` or `pending`, and no word that `code-spelled-out-names` replaces.
The verb rule skips names that begin in capitals, such as components, names the language defines, such as constructors, and the `main` function of `code-script-entry-points`.
Name an accessor, which reads as a property or returns a field, and a test fixture for their values, and a test titled by its name for its behavior.
Keep a name that an interface or framework fixes, such as a platform's `alarm` method, and suppress its finding as `code-lint-suppressions` requires, with a reason naming that system.
This contract's `assets/` folder ships a default verb list and lint rules that hold it, and a repository may add or remove verbs in its copy.

Violation: `function total({ invoice }: TotalInput)` and `const finishedResults: ReadResults = ({ run }) => ...` name functions for the values they return.
Allowed: `computeTotal({ invoice })`, `readFinishedResults({ run })`, `isPaid({ invoice })`, `onSubmit`, `useInvoices`, an `InvoiceRow` component, and an accessor `get total()`.

## Checks

Read a representative changed call from entry to result: can its inputs, effects, result, error path, and owner be understood without following a chain of forwarding helpers?
Compare that call before and after the change and confirm the caller needs no more local context than before.
For each new module or helper, name the behavior it owns and the concept, duplication, or independent operation that justifies it.
Search changed paths for catch-all module names, generic names, and helpers with a single caller.
Run the repository's lint on changed files, confirm it reports no function off the verb list, and compare each language's rule and each predicate prefix with the list.
For each generic stored or wire name or value that another system or a released format fixes, does it appear only in the mapping that reads or writes it, while owned code uses a name for its concept?
Run the repository's formatter, linter, and type checks; they establish layout and types, not readability.
