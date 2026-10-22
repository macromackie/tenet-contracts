---
name: code-rust-source-structure
message: Keep Rust entry points thin, alternatives as enums, and errors typed and propagated with context, never unwrapped in production.
---

## Rules

Keep each binary's `main` function limited to process startup: parse arguments, build dependencies, call library code, and map the result to an exit status.
Follow Rust naming conventions: `snake_case` for functions, modules, and variables, `UpperCamelCase` for types and variants, and `SCREAMING_SNAKE_CASE` for constants and statics.

Represent mutually exclusive outcomes or states with an `enum`, not with several `Option` fields or boolean flags.
Group related values in a `struct` instead of passing them as parallel arguments or tuples.
Borrow inputs as `&T`, `&str`, or `&[T]` when the caller keeps ownership, and take ownership only when the function stores or consumes the value.

Return `Result` for recoverable failures, and panic only when an internal invariant is violated.
Propagate errors with `?`, and add context naming the failed operation and its input where the underlying error does not identify them.
Return errors from library APIs as types that implement `std::error::Error` and let callers distinguish the failures they handle, never as bare strings.
Inside a library crate, carry each expected failure as a variant of a typed error `enum` until code handles it; use an opaque error type, such as `anyhow::Error`, only in a binary crate.
Do not call `unwrap` or `expect` in production code; test code may use them.
Do not leave `dbg!` or temporary debug printing in production code.

## Checks

Run `cargo clippy --workspace --lib --bins -- -D clippy::unwrap_used -D clippy::expect_used -D clippy::dbg_macro`, which leaves test code out.
Read each binary's `main` function and confirm that it only parses arguments, builds dependencies, calls library code, and maps the result to an exit status.
Can any struct hold field values that contradict each other where an `enum` would make the invalid state unrepresentable?
Trace one error from its source to the top-level report, and confirm that the context identifies the failed operation without discarding the cause.
Search each library crate's source for an opaque error type, such as `anyhow::Result`, and confirm that only binary crates use one.
