---
name: code-rust-numeric-conversions
message: Convert Rust numbers with From and TryFrom instead of as, and declare each limit, count, or size in the type its consumers take.
---

## Rules

Never convert between numeric types with `as`, such as `len as u64`, `jobs as usize`, or `count as f64`.
Convert with `From` where the standard library implements it for the pair, such as `u64::from(count_u32)` or `f64::from(count_u32)`, and with `TryFrom` and `?` for every other integer pair, such as `usize::try_from(jobs)?`.
Convert a `usize` or `isize` to a fixed-width integer type with `TryFrom`, such as `u64::try_from(text.len())?`, because its width depends on the target and the standard library implements no `From` for it.
Reinterpret the bits of a hash, a bit-flag set, or another value whose magnitude means nothing as the same-width integer of the other signedness with `cast_unsigned` or `cast_signed` instead of `TryFrom`, and never reinterpret a quantity this way, such as a count, size, index, limit, amount, or timestamp.
Compute a count or an index with integer arithmetic, such as `item_count.div_ceil(ITEMS_PER_PAGE)`, never by converting a floating-point result back to an integer.
Suffix each numeric literal whose type nothing else fixes, after an underscore, such as `let mut retry_count = 0_u32;`, so its type never falls back to `i32` or `f64`.
Compute each integer sum, difference, product, quotient, remainder, and negation with a `checked_*` method that returns `Option`, never with an operator that can overflow or panic.
Clamp with a `saturating_*` method instead only a quantity that stops at its type's bound by design, such as a remaining budget that stops at zero.
Wrap with a `wrapping_*` method only a value whose magnitude means nothing, such as a hash.

Declare a limit, count, or size in the type its consumers take, such as `const MAX_FILE_BYTES: u64` for a reader's `take`, or a command-line count parsed as `usize`, instead of converting it at each use.
Compute a ratio or mean of counts in one function placed as `code-shared-utilities` requires.
That function converts its counts with `f64::from` from `u32`, or suppresses both `clippy::as_conversions` and `clippy::cast_precision_loss` as `code-lint-suppressions` requires, with a reason that names the precision it gives up.
That function also suppresses `clippy::float_arithmetic` as `code-lint-suppressions` requires, with a reason that names the ratio it computes.

Keep every Clippy conversion and arithmetic lint denied, such as `as_conversions` and `arithmetic_side_effects`, as the lint table that `code-lint-strictness` ships denies them, and turn none off locally.

Violation: `let jobs = metadata["jobs"].as_u64().context("missing jobs")? as usize;` truncates silently on a 32-bit target.
Allowed: `let jobs = usize::try_from(saved.jobs).context("saved jobs exceed usize")?;` fails with context instead.
Violation: `let total_bytes = used_bytes + reserved_bytes;` panics in a debug build and wraps in a release build when the sum overflows.
Allowed: `let total_bytes = used_bytes.checked_add(reserved_bytes).context("total bytes exceed u64")?;` fails with context instead.

## Checks

Run the Clippy check that `code-rust-workspace-checks` requires, and confirm that the repository's lint table leaves the conversion and arithmetic lints denied.
For each limit, count, or size a change declares or converts, does its declared type match the type its consumers take?
For each suppression of a conversion lint a change adds, does it sit in the one ratio function, and does its reason name the precision it gives up?
For each `clippy::float_arithmetic` suppression a change adds, does it sit in the one ratio function, and does its reason name the ratio it computes?
For each floating-point value a change turns into a count or an index, could integer arithmetic compute it instead?
For each `cast_signed` or `cast_unsigned` a change adds, is the value it reinterprets one whose magnitude means nothing, such as a hash or a bit-flag set?
