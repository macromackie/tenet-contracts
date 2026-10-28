---
name: code-rust-source-structure
message: Keep Rust entry points thin, alternatives as enums, and errors as derived types that callers match by variant, propagated with context and never unwrapped in production.
requires-tenet: 0.11.0
---

## Rules

Keep each binary's `main` function limited to process startup: parse arguments, build dependencies, call library code, and map the result to an exit status.
Follow Rust naming conventions: `snake_case` for functions, modules, and variables, `UpperCamelCase` for types and variants, and `SCREAMING_SNAKE_CASE` for constants and statics.

Represent mutually exclusive outcomes or states with an `enum`, not with several `Option` fields or boolean flags.
Group related values in a `struct` instead of passing them as parallel arguments or tuples.
Borrow inputs as `&T`, `&str`, or `&[T]` when the caller keeps ownership, and take ownership only when the function stores or consumes the value.

Return `Result` for recoverable failures, and panic only when an internal invariant is violated.
Propagate errors with `?`, and add context naming the failed operation and its input where the underlying error does not identify them.
A caller branches on a failure when it handles one kind differently from another, such as retrying a timeout or mapping a closed invoice to an exit status.
Return an error type the crate owns, such as `Result<Receipt, SettleError>`, from every function whose callers branch on its failure, in binary and library crates alike.
Inside a library crate, carry each expected failure as a variant of a typed error `enum` until code handles it, and never return an error as a bare string.
Use an opaque error type, such as `anyhow::Error`, only in a binary crate, and only for a failure that no caller branches on.
Derive each error type's `Display` and `std::error::Error` implementations with the one derive macro the repository declares, such as `thiserror`'s `#[derive(Error)]`, never by hand.
Give each error type its message in that derive's attribute, on a `struct` or each `enum` variant, such as `#[error("settle invoice {id:?}: the invoice is closed")]`, as `code-diagnostic-messages` requires.
Carry an underlying error in its `struct` or variant as the derive's source field, such as a field marked `#[source]` or `#[from]`, so the error's cause chain keeps it.
Never recover a type from an opaque error, a cause, or a `dyn Any` value with `downcast_ref`, `downcast_mut`, `downcast`, or `is`; match an `enum`'s variants instead.
When a dependency hands over only an opaque value, such as `Box<dyn Error>` or a panic payload, downcast it in the call that receives it, suppressed as `code-lint-suppressions` requires.
Configure the repository's lint to reject each downcast, each hand-written `std::error::Error` implementation, and each hand-written `Display` for a type that derives its `Error` implementation.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Do not call `unwrap` or `expect` in production code; test code may use them.
Do not leave `dbg!` or temporary debug printing in production code.
Bind each value a call returns, and handle each `#[must_use]` value, such as a `Result` with `?`.
Discard any other unused value only with a typed wildcard binding, such as `let _: Option<u64> = counts.insert(name, count);`.

Violation: `impl std::error::Error for SettleError {}` sits below a hand-written `impl fmt::Display for SettleError`.
Allowed: `#[derive(Debug, thiserror::Error)] enum SettleError { #[error("settle invoice {id:?}: the invoice is closed")] Closed { id: u64 } }` derives both.
Violation: `settle_invoice` returns `anyhow::Result<Receipt>`, and its caller branches with `error.downcast_ref::<SettleError>()`.
Allowed: `settle_invoice` returns `Result<Receipt, SettleError>`, and its caller matches `Err(SettleError::Closed { id })`.

## Checks

Run `cargo clippy --workspace --lib --bins -- -D clippy::unwrap_used -D clippy::expect_used -D clippy::dbg_macro`, which leaves test code out.
Run the repository's lint from the workspace root, and confirm that it rejects `error.downcast_ref::<SettleError>()` and `impl std::error::Error for SettleError {}`.
Read each binary's `main` function and confirm that it only parses arguments, builds dependencies, calls library code, and maps the result to an exit status.
Can any struct hold field values that contradict each other where an `enum` would make the invalid state unrepresentable?
Trace one error from its source to the top-level report, and confirm that the context identifies the failed operation without discarding the cause.
Search each crate's source for an opaque error type, such as `anyhow::Result`, and confirm that only binary crates use one, and only for failures no caller branches on.
For each function a change adds whose callers branch on its failure, does it return an error type the crate owns, and does each caller match its variants?
