---
name: code-typescript-named-types
message: Give every TypeScript object type a name instead of writing an object type literal inline.
---

## Rules

Declare every object type as a named `type` alias or `interface`.
Never write an object type literal inline in a parameter, return type, property, type argument, union member, intersection, or variable annotation.
Name each nested object type and refer to it by name, so a property that holds an object has a named type of its own.
A type built from named types by a type operator or a utility type, such as `Pick<Invoice, 'id'>` or `Record<OrderStatus, number>`, is allowed.
A type inferred from a value, such as `typeof defaults` or a schema's derived type, is allowed.

Violation: `command({ model, deadline }: { model: string; deadline: Date }): { argv: string[] }` declares two object types inline.
Allowed: `command({ model, deadline }: CommandInput): CommandLine` with `CommandInput` and `CommandLine` declared as named types.

## Checks

From the package directory, run the package's type check after renaming or extracting types.
Search the change for `{` in type positions: parameter annotations, return types, property types, type arguments, and unions.
For each object type literal the search finds, is it one of the allowed type operator, utility type, or inferred forms?
