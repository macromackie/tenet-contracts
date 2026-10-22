---
name: code-rust-visibility
message: Give every Rust item the narrowest visibility its users need, and fail checks on a public item that the crate root does not export.
---

## Rules

This contract applies `code-export-consumers` to Rust and extends `code-rust-workspace-checks` to the visibility of every item in every crate, binaries included.
Treat a library's crate root as its package entry point, whose exports are the `pub` items that other crates can reach through it, and treat `pub(crate)`, `pub(in ...)`, and `pub(super)` items as exports to the crate's other modules.
Make checks fail on the `unreachable_pub` lint in every crate, through `[workspace.lints]` or, for a crate outside a workspace, its own `[lints]` table.
An item that the crate root does not export is `pub(crate)`, `pub(in ...)`, `pub(super)`, or private, except a child module, which `code-rust-module-boundaries` keeps private, and a field, whose visibility `code-rust-type-ownership` sets.
Give such an item the narrowest of these visibilities that reaches every module using it, such as `pub(super)` for an item of `orders/pricing.rs` that only code inside `orders` uses, and never `pub`, even inside a private module, so leave the Clippy `redundant_pub_crate` lint off.
A type that an exported item's signature uses counts as used by that item's consumers, so the crate root may export it although no other crate names it.
A link in a doc comment is not a use of the item it names, so never widen an item's visibility only so that a doc comment can link to it.

Violation: a library's crate root re-exports `DEFAULT_SOURCE` with `pub use`, and only its own `lock` module reads it.
Allowed: a library's crate root exports a `Routing` type that no other crate names, because an exported function returns it.

## Checks

Confirm that every crate's lint table, including a crate outside any workspace, makes `unreachable_pub` fail and leaves `redundant_pub_crate` off.
For each `pub(crate)`, `pub(in ...)`, or `pub(super)` item a change adds, does another module use it, and is it the narrowest of these forms that reaches every module that uses it?
For each item a change adds to a crate root's exports, does another crate name it from production code, such as the package's own binary, or from tests when the exporting crate is a test support package, or does an exported signature use it?
