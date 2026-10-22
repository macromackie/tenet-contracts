---
name: code-exhaustive-branches
message: Branch on a closed set that the repository declares by naming every member, never through a default or wildcard case, so that a new member fails the lint.
---

## Rules

When code branches on a closed set, as `code-closed-value-sets` defines it, that the repository declares, such as a union of states or an enumeration of event kinds, name every member in a case or arm.
Never cover a member of such a set with a default case, a wildcard arm, or a final `else`, such as `default: return 0` or `_ => None`, because a member added later would take that path unreviewed.
A test for one member whose other branch serves every remaining member, such as `if let Order::Paid(paid) = order` with an `else` or `let Order::Paid(paid) = order else`, is a wildcard too, although no lint reports it.
Group members that share one result in one case, such as `Order::Draft(_) | Order::Sent(_) => None`.
A lookup table that `code-conditional-expressions` allows is exhaustive only when its type requires every member as a key, such as `Record<OrderStatus, Delay>`.

A branch on an open set, such as a header value or an integer, ends with a default case that handles every remaining value.
A branch on a set declared outside the repository, such as a dependency's event kinds or the standard library's optional value, may cover the remaining members with a wildcard.
Where the lint reports such a wildcard, suppress it as `code-lint-suppressions` requires, with a reason that names the set.

Configure the repository's lint to reject a branch on a union or enumeration that omits a member, covers members with a default or wildcard case, or covers a single remaining member with a wildcard.

Violation: `switch (order.status)` names `OrderStatus.Draft` and `OrderStatus.Paid`, and its `default` case treats every other status as refunded.
Allowed: the same switch names `OrderStatus.Refunded` and `OrderStatus.Cancelled` in one shared case and has no default, so a new status fails the lint.

## Checks

Run the repository's lint from the repository root, with type information where its exhaustiveness rule needs it, and confirm that it rejects a missing member, a default case, and a wildcard arm on a closed set.
For each chain of `if` and `else` that a change adds over a closed set's members, would a member added later fall into the final `else`?
For each pattern test with an `else` that a change adds over a closed set the repository declares, does the `else` serve every remaining member?
For each wildcard suppression a change adds, is the set declared outside the repository, and does the reason name it?
