---
name: code-rust-numeric-conversions
message: Convert Rust numbers with From and TryFrom instead of as, and declare each limit, count, or size in the type its consumers take.
---

## Rules

Never convert between numeric types with `as`, such as `len as u64`, `jobs as usize`, or `count as f64`.
Convert with `From` where the standard library implements it for the pair, such as `u64::from(count_u32)` or `f64::from(count_u32)`, and with `TryFrom` and `?` for every other integer pair, such as `usize::try_from(jobs)?`.
Convert a `usize` or `isize` to a fixed-width integer type with `TryFrom`, such as `u64::try_from(text.len())?`, because its width depends on the target and the standard library implements no `From` for it.
Reinterpret the bits of a hash, a bit-flag set, or another value whose magnitude means nothing as the same-width integer of the other signedness with `cast_unsigned` or `cast_signed` instead of `TryFrom`, and never reinterpret a quantity this way, such as a count, size, index, limit, amount, or timestamp.
Compute a count or an index with integer arithmetic, such as `len.div_ceil(2)`, never by converting a floating-point result back to an integer.

Declare a limit, count, or size in the type its consumers take, such as `const MAX_FILE_BYTES: u64` for a reader's `take`, or a command-line count parsed as `usize`, instead of converting it at each use.
Compute a ratio or mean of counts in one function placed as `code-shared-utilities` requires.
That function converts its counts with `f64::from` from `u32`, or suppresses both `clippy::as_conversions` and `clippy::cast_precision_loss` as `code-lint-suppressions` requires, with a reason that names the precision it gives up.

Deny the `as_conversions`, `cast_possible_truncation`, `cast_sign_loss`, `cast_possible_wrap`, and `cast_precision_loss` Clippy lints in the workspace lint table that `code-rust-workspace-checks` requires.

Violation: `let jobs = metadata["jobs"].as_u64().context("missing jobs")? as usize;` truncates silently on a 32-bit target.
Allowed: `let jobs = usize::try_from(saved.jobs).context("saved jobs exceed usize")?;` fails with context instead.

## Checks

Run `cargo clippy --workspace --all-targets --locked -- -D warnings` from each workspace root, and confirm that the workspace lint table denies the five conversion lints.
For each limit, count, or size a change declares or converts, does its declared type match the type its consumers take?
For each suppression of a conversion lint a change adds, does it sit in the one ratio function, and does its reason name the precision it gives up?
For each floating-point value a change turns into a count or an index, could integer arithmetic compute it instead?
For each `cast_signed` or `cast_unsigned` a change adds, is the value it reinterprets one whose magnitude means nothing, such as a hash or a bit-flag set?
