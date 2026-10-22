---
name: code-closed-value-sets
message: Declare each closed set of values once and refer to its members by name, never by repeating their literal values.
---

## Rules

A closed set is a fixed list of values that code compares against, branches on, or offers as choices, such as an order's statuses or the kinds of event a parser reads.
Declare each closed set once, as a named type whose members code refers to by name, such as an enum or a constant object of named members.
Compare, branch on, and key maps by the set's members, such as `case OrderStatus.Refunded`, never by repeating a member's literal value, such as `case 'refunded'`.
Derive validation schemas, lookup tables, and lists of the set's values from that one declaration instead of repeating its values.
The declaration itself holds each literal value once, and a stored or wire value keeps its literal there.
A migration keeps the literal values it wrote, because it must not change when the set changes.
A comparison against a value that the language or a protocol defines, such as the result of a type-of operator or an HTTP status code, is allowed.
Give an open set of values, such as configured model or region identifiers that change without a code change, a named type instead of a closed declaration.
Declare a closed set for the members of an open set that code branches on, such as the models that need special handling.

Violation: `switch (order.status) { case 'refunded': ... }` repeats a stored value that the order schema already declares.
Allowed: `case OrderStatus.Refunded:` names the member, and `OrderStatus` is the one declaration that the schema and the switch both read.

## Checks

Search the change for `case` labels and equality comparisons against string or number literals, and name the closed set each one belongs to.
For each closed set the change touches, where is its one declaration, and do schemas and lookups derive from it?
Does the change branch on a configured identifier without a declared closed set for the values it handles?
