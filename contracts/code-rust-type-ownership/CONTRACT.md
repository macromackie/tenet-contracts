---
name: code-rust-type-ownership
message: Give each Rust type at most one impl block per file, make its fields all private or all public, give each shared counter its own type, and declare no global mutable state.
---

## Rules

Declare at most one inherent `impl` block for each self type in each file, and move a bound that only some methods need into those methods' `where` clauses.
`Order<Draft>` and `Order<Placed>` are two self types, but `impl<State> Order<State>` and `impl<State: Clone> Order<State>` share one.
Methods that serve one operation may live in that operation's file, beside the functions that use them.
Give a struct either private fields and the methods that read and change them, or public fields and no invariant on their values, never a mix of public and private fields.
Never give a field a scoped visibility, such as `pub(crate)` or `pub(super)`; make the field private behind a method, or make it public on a plain record.
Give a counter or limit that several functions change, such as a request budget, its own type that holds it in a private field and changes it only through a method for each change, such as `budget.try_spend()`.
That field may be a `Cell`, lock, or atomic, and several threads or structs may share a reference to the owning type, but never let several structs reference the same bare `Cell` or atomic, such as an `Arc<AtomicUsize>` that each worker holds.
Never declare global mutable state, such as a `static mut`, a `static` that holds a lock, cell, atomic, or lazily initialized value, or a thread-local value, except the `#[global_allocator]` item and a private `static`, never a `static mut`, that a function the platform calls without a context argument, such as an interrupt handler or a foreign callback, must reach.
Deny `multiple_inherent_impl`, `partial_pub_fields`, and `field_scoped_visibility_modifiers` in `[workspace.lints.clippy]`, or in a crate's own `[lints.clippy]` table when it belongs to no workspace.
Set `inherent-impl-lint-scope = "file"` in the `clippy.toml` at each workspace root and at the root of each crate that belongs to no workspace, and in every `clippy.toml` beneath those roots, which replaces the file above it rather than extending it, so `multiple_inherent_impl` counts blocks per file.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `orders.rs` declares `Order` and two `impl Order` blocks, one above the parsing functions and one below them.
Allowed: `Transport` keeps `cooldown: Mutex<Instant>` private and changes it only in its own `push_back` method.

## Checks

Run the Clippy command that `code-rust-workspace-checks` names from each workspace root and from each crate that belongs to no workspace.
Does a change declare a `static mut`, or a thread-local value or a `static` that holds a lock, cell, atomic, or lazy value, other than the global allocator or a private `static` that a function called without a context argument must reach?
For each counter, flag, or limit that a change shares between functions, which type owns it, and do callers change it only through that type's methods?
Does a change set one of the three Clippy lints weaker than deny, remove it from a lint table, change `inherent-impl-lint-scope`, or add a `clippy.toml` that does not set it to `"file"`?
