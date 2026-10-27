---
name: code-module-structure-and-control-flow
message: Keep modules focused and named for their behavior, with explicit inputs, results, and control flow.
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

## Checks

Read a representative changed call from entry to result: can its inputs, effects, result, error path, and owner be understood without following a chain of forwarding helpers?
Compare that call before and after the change and confirm the caller needs no more local context than before.
For each new module or helper, name the behavior it owns and the concept, duplication, or independent operation that justifies it.
Search changed paths for catch-all module names, generic names, and helpers with a single caller.
For each generic stored or wire name or value that another system or a released format fixes, does it appear only in the mapping that reads or writes it, while owned code uses a name for its concept?
Run the repository's formatter, linter, and type checks; they establish layout and types, not readability.
