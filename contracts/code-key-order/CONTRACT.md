---
name: code-key-order
message: Write the keys of every object, struct, and configuration map in code point order, and keep another order only where order is behavior.
---

## Rules

Write keys in ascending code point order in every object literal, object type, interface, and struct or record definition and literal.
Write the keys of every map in a hand-written configuration file in the same order, such as a JSON object, a YAML map, or a TOML table.
Write the variants of an enumeration in the same order.
Compare two keys by the code points of their characters, without quotes, so `Total` sorts before `amount` and `line10` before `line9`.
Sort the keys between two spread elements as one group, and keep each spread element where its position decides which value wins.
A blank line or a comment between keys does not start a new group.
Where a format requires some entries before others, such as a TOML table's values before its sub-tables, sort each of those runs on its own.
Write a struct literal's fields in the order of its definition, which is sorted unless that definition's order is suppressed.

Where key order is behavior, such as a serialized field order or a constructor's argument order, keep that order and suppress the finding at that site.
Write that suppression as `code-lint-suppressions` allows, with a reason that names the behavior the order decides.
Where a file's format holds no comments, such as `package.json`, a key order that is behavior, such as the conditions of its `exports` map, needs no suppression.
Never suppress the order for a reader's preference alone, such as grouping related keys or putting an identifier first.
Sort keys with the lint's or formatter's autofix wherever it offers one, and by hand elsewhere.

This contract ships no files of its own; `code-lint-strictness` ships the lint and formatter configuration that sorts and checks keys in this order.
Review key order wherever no lint or formatter checks it, such as in JSON files, object types, interfaces, dictionary literals, class-based enumerations, and TOML table headers.
Review it as well across a comment or blank line between keys in TOML, which the formatter does not sort across.

Violation: `return { status: order.status, id: order.id };` writes `status` before `id`.
Allowed: `return { id: order.id, status: order.status };`.
Violation: a configuration file's job map lists `test` before `build`, and nothing reads the jobs in that order.
Allowed: a stored record type keeps `version` before `entries`, because readers parse the version first, with a site suppression whose reason names that format.

## Checks

Run the repository's lint and formatter checks from the repository root, and confirm they reject unsorted keys in an object literal, a struct, and a configuration map.
For each key order suppression a change adds, does its reason name the behavior that the order decides?
For each JSON file, object type, interface, or configuration map a change adds or edits that no lint or formatter checks, are its keys in code point order?
Does a change reorder the keys of a site whose order is behavior, such as a serialized record?
