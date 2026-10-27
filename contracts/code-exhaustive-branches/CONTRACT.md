---
name: code-exhaustive-branches
message: Write an `else if` chain of equality tests on one value as a `switch`, and name every member of a declared closed set instead of a default or wildcard.
requires-tenet: 0.11.0
---

## Rules

Never follow an equality test on a value with an `else if` that tests the same value for equality; write those cases as a `switch` statement.
The requirement applies only where a `switch` accepts any expression as a case and compares it by strict equality, so the rewrite keeps behavior.
The requirement holds for an open set, such as a header value, as for a closed set, where the lint then checks that every member is named.
Comparisons of the value joined by a logical or form one equality test, and a test joined by a logical and is not an equality test.

When code branches on a closed set, as `code-closed-value-sets` defines it, that the repository declares, such as a union of states or an enumeration of event kinds, name every member in a case or arm.
Never cover a member of such a set with a default case, a wildcard arm, or a final `else`, such as `default: return 0` or `_ => None`, because a member added later would take that path unreviewed.
A test for one member whose other branch serves every remaining member, such as `if let Order::Paid(paid) = order` with an `else` or `let Order::Paid(paid) = order else`, is a wildcard too, although no lint reports it.
Group members that share one result in one case, such as `Order::Draft(_) | Order::Sent(_) => None`.
A lookup table that `code-conditional-expressions` allows is exhaustive only when its type requires every member as a key, such as `Record<OrderStatus, Delay>`.

A branch on an open set, such as a header value or an integer, ends with a default case that handles every remaining value.
A branch on a set declared outside the repository, such as a dependency's event kinds or the standard library's optional value, may cover the remaining members with a wildcard.
Where the lint reports such a wildcard, suppress it as `code-lint-suppressions` requires, with a reason that names the set.

Configure the repository's lint to reject an `else if` chain of equality tests on one value, wherever the lint supports that rule.
Configure the repository's lint to reject a branch on a union or enumeration that omits a member, covers members with a default or wildcard case, or covers a single remaining member with a wildcard.
Turn off each lint rule that requires a default case or final `else` on a branch over a closed set, or an `if` instead of a short `switch`.
Run the lint with the type information that its exhaustiveness rule needs.
Where the repository's lint can load the configuration in this contract's `assets/` folder, extend it from the repository's own lint configuration.

Violation: `if (order.status === OrderStatus.Draft)` is followed by `else if` tests for `OrderStatus.Paid` and for `OrderStatus.Refunded` or `OrderStatus.Cancelled`, so a new status passes the lint unhandled.
Allowed: `switch (order.status)` names `OrderStatus.Draft` and `OrderStatus.Paid` in their own cases and `OrderStatus.Refunded` and `OrderStatus.Cancelled` in one shared case, with no default, so a new status fails the lint.

## Checks

Run the repository's lint with type information from the repository root, and confirm that it reports no type configuration error, which makes its exhaustiveness rule skip files.
Confirm that the lint rejects an `else if` chain of equality tests on one value, a missing member, and a default or wildcard covering a member.
For each `else if` that a change adds and the lint does not report, does it test the same value for equality as the test before it?
For each chain of `if` and `else` that a change adds over a closed set's members, would a member added later fall into the final `else`?
For each pattern test with an `else` that a change adds over a closed set the repository declares, does the `else` serve every remaining member?
For each wildcard suppression a change adds, is the set declared outside the repository, and does the reason name it?
