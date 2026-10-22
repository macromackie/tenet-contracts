---
name: code-module-structure-and-control-flow
message: Keep modules focused and named for their behavior, with explicit inputs, results, and control flow.
---

## Rules

Give each module one understandable responsibility.
Name modules for the behavior or resource they own.
Name each function, type, and file, whether exported or not, and each stored or wire value, for the behavior or concept it stands for, never with a generic word alone such as `data`, `info`, `item`, `manager`, `handler`, or `script`.
A declared file role, such as `types` or `constants`, is not a generic name for a file that holds that role.
Do not create catch-all modules, such as `helpers`, `common`, or `misc`, that mix code of unrelated concerns.
A shared utilities module that holds only domain-free functions, one per file, as `code-shared-utilities` defines, is not a catch-all module.
Create a module only when it has an actual responsibility; do not add placeholder files.
Split a module when the split reduces the context needed to understand a change, and keep cohesive code together when splitting would obscure its invariants.
Keep a helper that depends on its module's domain private to that module until another caller needs it.

Extract a helper only when it names a real concept, collapses real duplication, or isolates an independent operation, never just to shorten a block.

Pass inputs and return results explicitly instead of relying on hidden side effects or ambient mutable state.
State that one module owns and changes only through its own functions, such as a cache, is not ambient state.
Name intermediate values when nested calls hide the sequence.
Name values for what they hold, and include the unit in the name of a limit or duration whose type does not carry it.

Never write by hand the parsing, validation, or provider integration that a maintained library provides; call the library and use its types.

## Checks

Read a representative changed call from entry to result: can its inputs, effects, result, error path, and owner be understood without following a chain of forwarding helpers?
Compare that call before and after the change and confirm the caller needs no more local context than before.
For each new module or helper, name the behavior it owns and the concept, duplication, or independent operation that justifies it.
Search changed paths for catch-all module names, generic names, and helpers with a single caller.
Run the repository's formatter, linter, and type checks; they establish layout and types, not readability.
