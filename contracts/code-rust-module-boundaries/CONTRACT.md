---
name: code-rust-module-boundaries
message: Keep a Rust crate's top-level modules acyclic and its child modules private.
requires-tenet: 0.11.0
---

## Rules

Keep the dependency graph between a crate's top-level modules acyclic.
Count as an edge every `use` declaration and every path in a type, an expression, or a macro argument, and attribute an import through a crate-root re-export to the module it re-exports from.
Attribute a path to an item defined at the crate root, such as a function beside a binary's `main`, to each module that the item's definition uses, directly or through other items defined there.
A test module, such as one under `#[cfg(test)]`, may use any module of its crate, including through the crate root, and its imports are not edges of that graph.
Keep a library crate's root to module declarations, re-exports, `extern crate` declarations, and procedural-macro functions that delegate to a module, and define every other item in a module.
Declare every child module below the crate root private with `mod name;`, and re-export from its parent module the items that code outside that parent uses or re-exports.
A `pub mod`, `pub(crate) mod`, `pub(super) mod`, or `pub(in ...) mod` below the crate root is a violation, and so is a path from outside a module into one of its children, such as `crate::orders::pricing::Discount` in `invoices.rs`.
A library crate's root may declare `pub mod` for a module that callers outside the crate use as part of its API.
Enforce the cycle and visibility rules with the repository's checks, and suppress a finding only as `code-lint-suppressions` allows.
A repository may use the checker under `assets/`, whose policy names each crate's root source file explicitly.

Violation: `invoices.rs` adds `use crate::MAX_LINES;`, a constant that `orders` defines and the crate root re-exports, while `orders` already uses `invoices`.
Allowed: the limit moves into `invoices`, the module that owns it, and `orders` reads `crate::invoices::MAX_LINES`.

## Checks

Run the repository's checks from the workspace root, and confirm that they fail on a cycle between top-level modules and on a child module that is not private.
For the shipped checker, follow its usage instructions under `assets/`, declare each crate root in the repository's policy, and run it from the repository root.
For each re-export a change adds to a parent module, does code outside that parent use or re-export the item?
Does a cycle fix move the item into the module that owns its concept, not into a forwarding layer that `code-ownership-and-boundaries` rejects?
