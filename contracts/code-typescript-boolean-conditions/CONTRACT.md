---
name: code-typescript-boolean-conditions
message: Give every TypeScript condition a boolean or a nullable object, compare strings, numbers, and lengths explicitly, and supply defaults with `??`, never `||`.
requires-tenet: 0.11.0
---

## Rules

Give every condition a boolean or a nullable object, meaning an object, array, or function type that may also be `null` or `undefined`, such as the result of `invoices.find((invoice) => isOverdue({ invoice }))`.
A condition is the test of an `if`, `while`, `do`, or `for` statement, or the operand of `!`.
The value that an array predicate returns, such as the callback of `filter` or `some`, is a condition too.
The left operand of `&&` or `||` is a condition, and so is its right operand when the whole expression is a condition.
A nullable object may be tested by its truthiness, such as `if (!match) { continue; }` after `const match = PATTERN.exec(line)`, because no object value is falsy.

Compare a string explicitly, such as `note === ''` or `note !== ''`, because the empty string is falsy.
Compare a number explicitly, such as `total === 0` or `total > 0`, because zero and `NaN` are falsy.
Compare an optional boolean with `true` or `false`, such as a dependency's `init.keepalive === true`, including one that an optional chain yields, such as `init?.keepalive === true`.
Compare an optional string, number, or enumeration member with `undefined` or `null`, and also with `''` or `0` when an empty value takes the same branch.
Never test a value whose type fixes the result, such as an object that cannot be absent, or a value typed `any`, which `code-typescript-type-assertions` treats as `unknown`.
Never coerce a string or number to a boolean, such as `Boolean(note)` or `!!note`, and compare it instead.

Test whether a collection is empty by comparing its `length` or `size` with zero, writing `=== 0` for empty and `> 0` for non-empty.
Never write those tests as `!items.length`, `items.length !== 0`, `items.length >= 1`, or `items.length < 1`.

Supply a default for a value that may be `null` or `undefined` with `??` or `??=`, such as `coupons.get(code) ?? 'none'`, never with `||` or `||=`.
An optional field of a function's argument object takes its default in the signature, as `code-typescript-function-arguments` requires.
An owned result or field that may hold no value follows `code-typescript-effect-absent-values`, and these rules cover every other absent value.
Default only a value whose absence the program expects; a value whose absence breaks an invariant follows `code-typescript-type-assertions`.
When a change replaces `||` with `??`, give an empty string or zero that must still take the default its own explicit test.
Inside a condition, `||` joining booleans or nullable objects tests them rather than supplying a default, so `if (cachedOwner || fallbackOwner)` is allowed.

Configure the repository's lint to reject a condition on a string, number, optional boolean, optional string, optional number, optional enumeration member, `any` value, or object that cannot be absent.
Configure it to reject `||` or `||=` on a value that may be absent outside a condition, and every length or size test that the rules above forbid.
Run that lint with type information, under the strict compiler settings that `code-typescript-compiler-strictness` requires, because its condition rules read each value's type.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `if (!lines.length)` tests a number's truthiness, and `const label = invoice.note || 'untitled'` gives an empty note the default without a test that shows it.
Violation: `if (version === KEEPALIVE_VERSION && init?.keepalive)` tests an optional boolean, and `const owner = owners.get(id) || guestOwner` defaults a nullable object with `||`.
Allowed: `if (lines.length === 0)`, `if (invoice.note === '')`, and `const coupon = coupons.get(code) ?? 'none'` compare and default explicitly.
Allowed: `if (!match) { continue; }` guards the nullable result of `PATTERN.exec(line)`, and `if (version === KEEPALIVE_VERSION && init?.keepalive === true)` compares an optional boolean.

## Checks

Run the repository's lint with type information from the repository root, and confirm that it reports no type configuration error, which makes its condition rules skip files.
Confirm that the lint rejects `if (!items.length)`, a condition on a string, a number, or an optional boolean, and `||` defaulting an optional value.
For each truthiness test a change replaces with a comparison, does the comparison keep every case the test covered, such as both `undefined` and the empty string?
For each `||` a change rewrites to `??`, does an empty string or zero that must still take the default get its own explicit test?
Search the change for `Boolean(` applied to a string or number, which the lint does not report.
For each condition in a file that no compiler configuration covers, does it test a boolean or a nullable object?
