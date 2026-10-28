---
name: code-declaration-order
message: Declare each function and class above the code that uses it, so each file reads from its helpers down to its exported function.
requires-tenet: 0.11.0
---

## Rules

Declare each function above every function and statement that uses it, so a reader meets each helper before its first use.
Declare each class above its uses in the same way, and treat a function bound to a constant as a function.
A use is any reference to the name, such as a call, a construction, a rendered component, a base class, a passed function, or an export list entry.
A reference inside a callback, a deferred task, or a lazily evaluated program is a use, even though it resolves only when that code runs.
Keep this order even where the language hoists a declaration or looks a name up only when the call runs.

A file that exports one function, as `code-module-file-roles` requires, therefore declares its private helpers above it, so the exported function follows every helper.
Apply the same order inside a function body, so a nested function sits above the statements that call it and a factory's inner functions sit above its return.
A function's call to itself follows the order, because the call sits below the function's name.
Members of one class, or of one block that implements a type's methods, may sit in any order within it.

Declarations that refer to each other, such as two functions that call each other, cannot all sit above their uses.
Declare them next to each other, put last the one that code outside them uses, and suppress each reference to a later one as `code-lint-suppressions` allows.

A program that yields a service key uses that key, so declare the key above the program, though the program runs later.

Put a file's top-level statements that run code below its declarations, so an executable file ends with the statement that `code-script-entry-points` allows to run its main program.
A test file declares its helper functions above the statements that register its cases and hooks.

Type declarations run nothing, so a type, an interface, or a type alias may sit above or below the code that names it.
A reference that names a class only as a type, such as in a parameter's annotation, is not a use either.

Enforce this order with the repository's lint in every language whose lint reports a use above its declaration, including test code.
Leave a language to review only by declaring that language and the reason in the lint configuration, such as that no lint for that language reports this order.
Where the repository's lint can load the configuration in this contract's `assets/` folder, extend it from the repository's own lint configuration.
The shipped file leaves to review a function constant that another function calls above its declaration, because its rule cannot tell function constants from other constants.
Exempt generated files by a declared path pattern, and suppress any other finding only as `code-lint-suppressions` allows.

Violation: `settleInvoice`, the file's exported function, calls `computeTotal`, which the file declares below it.
Violation: `notifyAll` calls `writeEvent`, a function constant declared below it, and the file's `await main();` sits above `main`.
Allowed: the file declares `computeTotal`, then `advanceStarting`, then the exported `settleInvoice`, which calls both.
Allowed: `isOdd` calls `isEven` below it through one suppression, and `isEven`, which code outside the pair calls, comes last.

## Checks

Run the repository's lint from the repository root, and confirm it reports calls, constructions, and same-scope uses of function constants above their declarations, inside function bodies too.
For each language the repository lints, does its lint enforce this order, or does the lint configuration name the language and the reason it has none?
In a language left to review, does each function and class that a change adds or moves sit above the code that uses it?
For each suppression of this order, do the declarations it joins refer to each other, and does the one that outside code uses come last?
Does each changed executable file end with the one statement that runs its main program, and each test file register its cases below its helpers?
Does a change turn the rule off, stop it checking functions or classes, or narrow the files it covers?
For each function constant a change adds, does it sit above every function that calls it?
