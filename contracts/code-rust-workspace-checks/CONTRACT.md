---
name: code-rust-workspace-checks
message: Enforce rustfmt and deny-warnings Clippy, share dependencies and lints through the workspace, and commit Cargo.lock.
---

## Rules

Format all Rust code with rustfmt, and fail checks on unformatted code.
Run Clippy on every workspace member and target with warnings denied.
Scope each lint suppression to the smallest item that needs it, and state why in a `reason = "..."` argument or an adjacent comment.
Pin the Rust toolchain in `rust-toolchain.toml`, including the rustfmt and Clippy components.

Declare shared lint levels once in `[workspace.lints]`, and set `lints.workspace = true` in every member crate.
Declare each shared dependency's version once in `[workspace.dependencies]`, and reference it from member crates with `workspace = true`.
Commit `Cargo.lock`, and run builds, tests, and lints with `--workspace` and `--locked`, so that no member crate is skipped and the lock file is never rewritten.

Confine `unsafe` code to the crates that need it, and forbid it in every other crate.
Document the invariant that makes each `unsafe` block sound in a `// SAFETY:` comment, and give each `unsafe fn` a `# Safety` section.

Keep tests that need network access, credentials, or paid services out of the default `cargo test` run, and run them only through an explicit feature, an `#[ignore]` attribute with `--ignored`, or a separate command.

## Checks

Run `cargo fmt --all --check`.
Run `cargo clippy --workspace --all-targets --locked -- -D warnings`.
Run `cargo test --workspace --locked` with no credentials in the environment.
Inspect each member `Cargo.toml` for dependency versions or lint tables that bypass the workspace definitions.
Search for `unsafe` and confirm that each use sits in a crate that permits it and carries its safety comment, or enable `clippy::undocumented_unsafe_blocks` in those crates.
