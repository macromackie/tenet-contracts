---
name: code-boolean-names
message: Start every owned boolean's name with a declared predicate or option prefix and every boolean function's with a predicate prefix, and decode each external boolean name at the boundary.
requires-tenet: 0.11.0
---

## Rules

Declare a list of predicate prefixes, such as `is`, `has`, `can`, `should`, `was`, and `needs`, and a list of option prefixes, such as `include`, `allow`, `skip`, `keep`, and `use`.
Also declare a list of the boolean attribute names of markup elements, such as `disabled`, `open`, `checked`, and `readOnly`.
Start the name of every owned boolean variable, parameter, field, class field, and schema key with a listed prefix, such as `isPaid`, `hasPendingRefunds`, or `includeArchived`.
A component's prop for a listed attribute takes its bare name, such as `disabled`, never `isDisabled`, when the component forwards it to an element or a dependency's component.
Name the rest of a boolean or boolean function for the state it reports or the behavior it enables, never a generic word such as `flag` or `mode`.
Configure the repository's lint to reject a boolean, known by its type annotation, its schema, a boolean initial value, or a comparison, whose name starts with no listed prefix in any case style, such as `paid`, `archived`, or `json`.
That lint accepts a component's prop named on the attribute list, so the prop needs no suppression.

Start the name of every owned function and method that returns a boolean with a listed predicate prefix, such as `isOverdue` or `hasOpenRefunds`.
This covers a function whose boolean arrives through a promise, an effect, or a result that may fail.
Never start a boolean function's name with an option prefix such as `include` or `skip`, because an option names a setting that a caller passes, not a question.
An accessor, which reads as a property or only returns a field, as `code-module-structure-and-control-flow` defines one, is named as a field is.
Any function, method, or function-typed constant, field, or member named `on` and a capital letter, such as `onSubmit`, is an event handler and keeps that name, as `ui-react-typescript-jsx-attributes` requires.
Configure the repository's lint to reject a function, method, or function-typed constant, field, or member that declares such a return type and starts with no listed predicate prefix.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
That folder ships default lists of the predicate prefixes, option prefixes, and markup boolean attribute names as shared rules, one per list, that the language rules read.
A repository adds or removes entries in its own copy of a shared rule, which its lint configuration loads in place of the shipped one.
The shipped boolean rules check only the fields of a component's props type, such as `SaveButtonProps`, so configure every other form named above in the repository's own lint.
Review each boolean function that the lint cannot see, such as a local one whose return type is inferred or a constant typed by a named function type.

Decode a wire field or command-line flag that another system names without a prefix into a prefixed name at the boundary, such as reading an order's `paid` field into `isPaid`, and write the external name only in that mapping.
Map a field of a stored or shipped format that the repository owns the same way, so that its external name stays unchanged as `data-stored-and-shipped-formats` requires.
A serializer rename or a flag's declared long name that keeps the external name is the allowed mapping; an owned field that carries the bare external name is not.
Where a schema can declare an external field only under its external name, suppress that key's finding as `code-lint-suppressions` requires, with a reason that names the system, and decode the key into a prefixed field.
A boolean or boolean function whose name an interface, a trait, a framework, or the language fixes keeps that name, and its finding is suppressed the same way.
Exempt generated files and copied third-party source from this rule by a declared path pattern, and decode each external boolean they carry into a prefixed name where owned code first reads it.

Violation: `function settle({ invoice, capture }: SettleInput)` names its boolean with a bare verb, and an invoice row declares `paid: boolean`.
Allowed: `function settle({ invoice, shouldCapture }: SettleInput)`, and an invoice schema that decodes the wire's `paid` into `isPaid`.
Violation: `function checkOverdue({ invoice }: CheckOverdueInput): boolean` and `function allowRetry({ job }: AllowRetryInput): boolean` start boolean functions with a verb and an option prefix.
Allowed: `function isOverdue({ invoice }: IsOverdueInput): boolean` and `function canRetry({ job }: CanRetryInput): boolean`.
Violation: `type SaveButtonProps = { readonly busy: boolean }` names a component's boolean prop with a bare state word.
Allowed: `type SaveButtonProps = { readonly disabled: boolean; readonly isBusy: boolean }`, where `SaveButton` renders `<button disabled={disabled}>`.

## Checks

Run the repository's lint from the repository root, and confirm it reports `function allowRetry(): boolean`, a props field `busy: boolean`, and no changed name that this contract rejects.
For each boolean or boolean function the lint cannot see, does its name start with a listed prefix, and a function's with a predicate prefix?
After its prefix, does each changed boolean or boolean function name a state or a behavior rather than a generic word?
For each external boolean name, does it appear only in the mapping that decodes it, while owned code reads the prefixed name?
For each changed boolean prop named for a listed attribute, does it carry the bare name exactly when the component forwards it to an element or a dependency's component?
For each suppression of this rule that a change adds, does its reason name the system that fixes the name?
