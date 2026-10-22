---
name: code-boolean-names
message: Start every owned boolean's name with a declared predicate or option prefix that lint enforces, and keep an external boolean name only in the mapping that decodes it.
---

## Rules

Declare a list of predicate prefixes, such as `is`, `has`, `can`, `should`, `was`, and `needs`, and a list of option prefixes, such as `include`, `allow`, `skip`, `keep`, and `use`.
Start the name of every owned boolean variable, parameter, field, class field, and schema key with a listed prefix, such as `isPaid`, `hasPendingRefunds`, or `includeArchived`.
Name the rest of a boolean for the state it reports or the behavior it enables, never with a generic word such as `flag` or `mode`.
Configure the repository's lint to reject a boolean, known by its type annotation, its schema, a boolean initial value, or a comparison, whose name starts with no listed prefix in any case style, such as `paid`, `archived`, or `json`.

Decode a wire field or command-line flag that another system names without a prefix into a prefixed name at the boundary, such as reading an order's `paid` field into `isPaid`, and write the external name only in that mapping.
Map a field of a stored or shipped format that the repository owns the same way, so that its external name stays unchanged as `data-stored-and-shipped-formats` requires.
A serializer rename or a flag's declared long name that keeps the external name is the allowed mapping; an owned field that carries the bare external name is not.
Where a schema can declare an external field only under its external name, suppress that key's finding as `code-lint-suppressions` requires, with a reason that names the system, and decode the key into a prefixed field.
A boolean whose name an interface, a trait, or a framework fixes keeps that name, and its finding is suppressed the same way.
Exempt generated files and copied third-party source from this rule by a declared path pattern, and decode each external boolean they carry into a prefixed name where owned code first reads it.

Violation: `function settle({ invoice, capture }: SettleInput)` names its boolean with a bare verb, and an invoice row declares `paid: boolean`.
Allowed: `function settle({ invoice, shouldCapture }: SettleInput)`, and an invoice schema that decodes the wire's `paid` into `isPaid`.

## Checks

Run the repository's lint on the changed files, and confirm it reports no boolean without a listed prefix.
For each boolean that the lint cannot see, such as one assigned from a call, does its name start with a listed prefix?
After its prefix, does each changed boolean name a state or a behavior rather than a generic word?
For each external boolean name, does it appear only in the mapping that decodes it, while owned code reads the prefixed name?
For each suppression of this rule that a change adds, does its reason name the system that fixes the name?
