# Rust

Prefer a short sequence when it makes fallible work or data ownership easier to see. For example:

```rust
let source = read_source(path)?;
let candidate = validate_candidate(source)?;
let assessment = provider.assess(&candidate).await?;

report.record(candidate, assessment)?;
```

Keep iterators when they express a simple transformation. Use structs for related inputs and enums for alternatives;
avoid tuples and booleans whose meaning is only clear at the definition. Borrow when the caller retains ownership.

Keep an internal subsystem's modules private. Expose a narrow entry point with explicit names:

```rust
mod labels;
mod stream;

pub(crate) use labels::grade_labels;
pub(crate) use stream::interpret;
```

Use the repository's module naming convention. A split should separate responsibilities, not create a forwarding
function per implementation function. Keep error context where the operation's meaning is known. Let rustfmt own
mechanical layout; use blank lines to distinguish phases, not to separate every statement.
