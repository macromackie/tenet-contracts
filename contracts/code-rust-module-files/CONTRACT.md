---
name: code-rust-module-files
message: Name handwritten Rust files and module directories in lower_snake_case and resolve external modules by their declared names.
requires-tenet: 0.11.0
---

## Rules

Name each handwritten Rust file stem and every directory in its path below the Cargo package root in ASCII lower_snake_case, starting with a lowercase letter and separating nonempty lowercase alphanumeric words with single underscores.
Use the physical source path inside its crate without a symbolic-link alias.
Apply the naming rule to every handwritten Rust source, including build scripts, binary and library targets, tests, examples, benchmarks and conditionally compiled modules.
Resolve each external module through its declared name without a direct or conditional `path` attribute, including literal path attributes in handwritten macro token streams.

Declare a Rust module that has child modules in a file named for the module beside its folder, such as `invoices.rs` beside `invoices/parse.rs`.
A crate root, `src/lib.rs` or `src/main.rs`, declares its child modules itself.
Never write a `mod.rs` file under a crate's `src` folder, including for a module whose folder holds one child.
A file under a crate's `tests` folder may be a `mod.rs`, such as `tests/support/mod.rs` that several integration test files share, because Cargo builds each file directly in `tests` as its own test crate.
Deny Clippy's `mod_module_files` lint in the shared lint table that `code-rust-workspace-checks` requires, or in the crate's own `[lints.clippy]` table when the crate belongs to no workspace.
Never allow or expect `mod_module_files` with an attribute on an item or a crate or with a command-line flag, even in a form that `code-lint-suppressions` accepts; rename the file instead.

Violation: `src/invoices/mod.rs` declares `mod parse;` for `src/invoices/parse.rs`.
Allowed: `src/invoices.rs` declares `mod parse;` for `src/invoices/parse.rs`, and `tests/support/mod.rs` holds helpers that two integration tests share.

## Checks

Run the shipped `check-module-files.py` from the repository root with the handwritten source inventory for each crate, as its README describes.
Run the Clippy command that `code-rust-workspace-checks` names from each workspace root and from each crate that belongs to no workspace.
Does a change remove `mod_module_files` from a lint table, set it below deny, or add an attribute or flag that allows or expects it?
