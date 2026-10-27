---
name: code-closed-value-sets
message: Declare each closed set of values once, HTTP methods and status codes included, and refer to its members by name, never by repeating their literal values.
requires-tenet: 0.11.0
---

## Rules

A closed set is a fixed list of values that code compares against, branches on, or offers as choices, such as an order's statuses or the kinds of event a parser reads.
Declare each closed set once, as a named type whose members code refers to by name, such as an enum or a constant object of named members.
Compare, branch on, and key maps by the set's members, such as `case OrderStatus.Refunded`, never by repeating a member's literal value, such as `case 'refunded'`.
Derive validation schemas, lookup tables, and lists of the set's values from that one declaration instead of repeating its values.
The declaration itself holds each literal value once, and a stored or wire value keeps its literal there.
A migration keeps the literal values it wrote, because it must not change when the set changes.
A comparison against a value that the language or a protocol defines, such as a type-of operator's result, is allowed, except an HTTP method or status code.
An error's tag, which its error class declares once, is allowed as a literal in a tag comparison or a tag handler's argument when the type checker rejects a tag outside the error type.
Give an open set of values, such as configured model or region identifiers that change without a code change, a named type instead of a closed declaration.
Declare a closed set for the members of an open set that code branches on, such as the models that need special handling.

Name each HTTP method and status code through a declared closed set whose members hold the protocol's values, such as `HttpMethod.Post` and `HttpStatus.MethodNotAllowed`.
Use those members wherever code writes, passes, or compares a method or status code, such as `{ status: HttpStatus.NotFound }` instead of `{ status: 404 }`.
Derive any type of methods or status codes from the set's declaration, never from a literal union that repeats its values, such as `'GET' | 'POST'`.
Put each set's declaration in a module that holds only that declaration, unless the standard library or a dependency already exports the set with named members.
A status code is also a numeric literal under `code-numeric-literals`, and its named constant is the status set's member, never a second constant such as `NOT_FOUND = 404`.
Test files, matched by a declared path pattern, may write HTTP methods and status codes as literals, because a test states the exact values it sends and expects.

Configure the repository's lint to report each HTTP method literal outside the declaring modules and the test files.
Configure it also to report, in the same files, each status code under a status name that the lint of `code-numeric-literals` skips, such as `{ status: 404 }`.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Its path patterns, which a repository may override, find the declaring modules by the file names `http-method` and `http-status`, and test files by common folders and suffixes.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `switch (order.status) { case 'refunded': ... }` repeats a stored value that the order schema already declares.
Violation: `fetch(url, { method: 'POST' })` writes the method as a literal, which compiles even when misspelled as `'POTS'`, because the request's method is a plain string.
Allowed: `case OrderStatus.Refunded:` names the member, and `OrderStatus` is the one declaration that the schema and the switch both read.
Allowed: `fetch(url, { method: HttpMethod.Post })` and `if (response.status === HttpStatus.NotFound)` name members of the declared sets.

## Checks

Run the repository's lint from the repository root, and confirm that it reports a method literal and a numeric status property outside the declaring modules and tests.
Search the change for `case` labels and equality comparisons against string or number literals, and name the closed set each one belongs to.
For each closed set the change touches, where is its one declaration, and do schemas and lookups derive from it?
Does the change write an HTTP method or status code without its set's member, such as in a local constant, a `code` property, or a longer string?
Does the change branch on a configured identifier without a declared closed set for the values it handles?
