---
name: code-spelled-out-names
message: Spell out every word of every declared name, with a repository word list and a one-character ban that lint enforces in every language.
---

## Rules

Apply these rules to every name a change declares: variables, parameters, callback parameters, fields, functions, methods, types, constants, enum members, and schema keys.
Exempt generated files and copied third-party source from these rules by a path pattern declared in the lint configuration, and apply the rules to the source that the repository writes as a generator's input.
Declare one list of word replacements for the repository, each mapping an abbreviation or a spelling variant to the one word that replaces it, such as `dir` to `directory`, `ctx` to `context`, `err` to `error`, and `colour` to `color`.
Keep that list in one place, and configure every language's lint from it, so that no language's lint misses a listed word.
Configure the repository's lint to reject a declared name that holds a listed word as any of its words, in any case style, such as `dir`, `orderDir`, `order_dir`, or `ORDER_DIR`.
When a language's lint cannot match a word inside a name, check that language's compound names in review.
Configure the lint to reject a declared name of one character, including a callback's parameters, such as `(a, b) => a.total - b.total`.
A type parameter of one capital letter, such as `T`, and `_` for a value that the code never reads are allowed.

Declare beside the list the acronyms that readers outside the repository know as words, such as `id`, `api`, `url`, `json`, and `utf8`, and leave them out of the list.
A word that a language itself defines, such as the name of a primitive type, is a word in that language, and that language's lint leaves it out.
Each unit suffix that the repository declares under `code-measured-value-names`, and the bound words `max` and `min` that it names, are words, and the list leaves them out.
Reading a name that another system declares, such as a base class's `this.ctx`, is not a declaration and is allowed.
Keep a declared name that another system fixes, such as an interface's method, a library option, a wire field, or a command-line flag, and suppress its finding as `code-lint-suppressions` requires, with a reason that names that system.
Keep the external name of a stored or shipped field that the repository owns, as `data-stored-and-shipped-formats` requires, through a serializer rename where one exists and otherwise with a suppressed finding.
Never remove a word from the list or exempt one name in the lint configuration to let a change pass; suppress that finding instead.

Violation: `const orderDir = join(root, 'orders')` abbreviates `directory`, and `orders.filter((o) => o.isPaid)` names an order with one letter.
Allowed: `const orderDirectory = join(root, 'orders')`, `orders.filter((order) => order.isPaid)`, and a constructor that names its parameter `state` and reads its base class's `this.ctx`.

## Checks

Run the repository's lint on the changed files, and confirm it reports no listed word and no one-character name.
Compare each language's lint configuration with the word list, and confirm each one holds every listed word that its language does not define.
For each compound name that a language's lint cannot split, does any of its words appear in the list?
Does a changed name use an abbreviation or spelling variant that the list lacks, and should the list gain it?
For each suppression of these rules that a change adds, does its reason name the system that fixes the name?
Does the change remove a word from the list or exempt a single name in the lint configuration?
