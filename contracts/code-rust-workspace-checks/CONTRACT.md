---
name: code-rust-workspace-checks
message: Enforce the rustfmt and Clippy settings that code-lint-strictness ships, share dependencies and lints through the workspace, and commit Cargo.lock.
---

## Rules

Format all Rust code with rustfmt and the `rustfmt.toml` that `code-lint-strictness` ships, and fail checks on unformatted code.
Run Clippy on every workspace member and target with the lint tables and `clippy.toml` that `code-lint-strictness` ships, and fail checks on every finding.
Suppress a Clippy or compiler lint only as `code-lint-suppressions` allows, with an outer `#[expect(lint, reason = "...")]` attribute on the smallest item or statement that silences it, never with `#[allow]` or an inner attribute that covers a whole module.
Pin the Rust toolchain in `rust-toolchain.toml`, including the Clippy component.
Pin one dated nightly toolchain with its rustfmt component in the repository's check task, such as `cargo +nightly-2026-10-27 fmt`, and format and check formatting only with that rustfmt.

Declare shared lint levels once in `[workspace.lints]`, and set `lints.workspace = true` in every member crate except one that needs `unsafe` code.
A crate that needs `unsafe` code copies that table into its own `[lints]` table with `unsafe_code` at deny, and changes nothing else in it.
Declare each shared dependency's version once in `[workspace.dependencies]`, and reference it from member crates with `workspace = true`.
Commit `Cargo.lock`, and run builds, tests, and lints with `--workspace` and `--locked`, so that no member crate is skipped and the lock file is never rewritten.

Confine `unsafe` code to the crates that need it, and forbid it in every other crate.
Document the invariant that makes each `unsafe` block sound in a `// SAFETY:` comment, and give each `unsafe fn` a `# Safety` section.

Keep tests that need network access, credentials, or paid services out of the default `cargo test` run, and run them only through an explicit feature, an `#[ignore]` attribute with `--ignored`, or a separate command.

## Checks

Run `cargo +<pinned nightly> fmt --all --check` from the workspace root.
Run `cargo clippy --workspace --all-targets --all-features --locked` from the workspace root, and confirm that it fails on a finding.
Run `cargo doc --workspace --no-deps --all-features --locked` from the workspace root, and confirm that it fails on a rustdoc finding.
Run `cargo test --workspace --locked` with no credentials in the environment.
Inspect each member `Cargo.toml` for dependency versions or lint tables that bypass the workspace definitions, apart from an `unsafe` crate's copied table that differs only in `unsafe_code`.
Search for `unsafe` and confirm that each use sits in a crate that permits it and carries its safety comment, or enable `clippy::undocumented_unsafe_blocks` in those crates.
