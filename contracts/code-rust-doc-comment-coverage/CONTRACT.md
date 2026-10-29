---
name: code-rust-doc-comment-coverage
message: Give every public item of a Rust library crate a doc comment, and fail checks when one is missing.
requires-tenet: 0.11.0
---

## Rules

Apply these rules to the items that a library crate exports, directly or through a re-export.
An item that a binary crate declares, or that a library crate declares without exporting, is outside these rules.
Give a doc comment to every exported struct, enum, trait, function, inherent method, method that a trait declares, type alias, constant, and static.
Give a doc comment as well to every exported module, union, and macro, and to every associated type and constant that an exported trait declares.
An item of a trait implementation needs no doc comment of its own, because the trait's doc comment documents it.
A field or variant of an exported type needs no doc comment of its own.
Write each doc comment in the prose form that `code-comment-form` requires.
Enforce these rules over every library crate with this contract's `assets/` configuration, loaded from the repository's own lint configuration, and fail checks on each missing doc comment.
Run that configuration over each library crate's folder and never over a binary crate, whose `pub` items it cannot tell from a library's.
Exempt an item only with the suppression that `code-lint-suppressions` describes.
Hiding an item from generated documentation so that the check passes, such as with `#[doc(hidden)]`, is a violation.

Violation: a library crate exports `pub fn compute_price(order: &Order) -> Money` with no doc comment above it.
Allowed: `/// The order's total after discounts, in the order's currency.` sits above it, and the fields of `Order` carry none.

## Checks

Run the repository's lint from the workspace root, and confirm that it fails on an undocumented public item of a library crate.
For each library crate or public module that a change adds, does the lint cover it?
For each change to the lint configuration, does it keep every item kind above required and skip no item by name?
Does any doc comment a change adds hold a section heading that `code-comment-form` bans?
