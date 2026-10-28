---
name: code-map-and-set-names
message: End every map's and set's name with a plural noun of what it holds, such as `orders` or `endedStates`, never a participle or adjective.
requires-tenet: 0.11.0
---

## Rules

A map or set is a value of a map or set type, such as `Map`, `ReadonlySet`, `WeakMap`, `dict[OrderId, Order]`, `frozenset`, `HashMap`, or `BTreeSet`.
Apply these rules to each variable, constant, parameter, field, class field, accessor, object key, schema key, and type member holding a map or set, in source, tests, and scripts.
End each such name with a plural noun of what the collection holds, in any case style, such as `orders`, `pendingJobs`, or `seen_order_ids`.
Never end a map's or set's name with a participle, an adjective, or a singular noun, such as `seen`, `pending`, `cache`, or `index`.
Name a set for its members, such as `seenOrderIds` rather than `seen`.
Name a map for the values it holds, and put any qualifier before the plural noun, such as `accountOrders` rather than `ordersByAccount`.
A mass noun, such as `evidence` or `data`, is not plural, and neither list holds it; name the collection for its countable members.

A name's last word is its part after its last underscore, its part from its last capital in camel case, or its whole name.
A last word is plural when it ends in `s` but not in `ss` or `ous`, such as `orders` but not `access` or `previous`.
Declare a list of irregular plurals that do not end in `s`, such as `children` and `people`, which count as plural.
Declare a list of singular nouns that end in a single `s`, such as `status` and `alias`, which never count as plural.
This contract's `assets/` folder ships both lists, and a repository may add words to either list in its copy.
Add a word to a list only when it is an irregular plural or a singular noun ending in `s`, never to let one name pass.

An object whose fields code reads by fixed names, such as a decoded request, is not a map, even when its type is a general mapping with untyped values.
An object whose type indexes it by key, such as `Record<OrderStatus, Delay>`, is not a map either.

Configure the repository's lint to report each map or set, known by its type annotation or the value that builds it, whose last word is not plural.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Review the name of each map or set that the lint cannot see, such as one that a call returns without an annotation.
Keep a name that another system fixes, such as a library option, a wire field, or an interface's member, and suppress its finding as `code-lint-suppressions` requires.
Give that suppression a reason that names the system.
Keep an owned stored or shipped field's external name, as `data-stored-and-shipped-formats` requires, through a serializer rename where one exists, and otherwise suppress its finding.
Exempt generated files and copied third-party source from these rules by a declared path pattern.

Violation: a function's `const seen = new Set<OrderId>()` and a class's `readonly #pending = new Map<JobId, Job>()` name a set with a participle and a map with an adjective.
Allowed: `const seenOrderIds = new Set<OrderId>()`, `readonly #pendingJobs = new Map<JobId, Job>()`, and `accountOrders` for a map from each account to its orders.

## Checks

Run the repository's lint from the repository root, and confirm it reports `const seen = new Set<OrderId>()` inside a function and a field `pending: ReadonlyMap<JobId, Job>`.
Does each map or set a change adds that the lint cannot see, such as a call's result, end its name with a plural noun?
Does each changed map's name end with a plural of its values, and each set's of its members, rather than its keys or a mass noun?
Is the last word of each changed map or set name that ends in `s` a plural noun, or should the singular list gain it, such as `bias`?
Does a change add a word to either list that is not an irregular plural or a singular noun ending in `s`?
For each suppression of these rules that a change adds, does its reason name the system that fixes the name?
Does a change widen the generated or third-party path pattern to cover source that the repository writes?
