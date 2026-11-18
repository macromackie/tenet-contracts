# Rust module files

Pass the directory containing a crate's Cargo manifest and the paths of its handwritten Rust files
relative to that directory. Include build scripts, library and binary targets, tests, examples,
benchmarks, and files excluded by the current compilation target. Use the repository's source
inventory so added files are included before compilation.

From the repository root, for a crate with the four source files shown here:

```bash
uv run --script .contracts/008-code-rust-module-files/assets/uv/check-module-files.py \
  --crate crates/order-service src/lib.rs src/orders.rs src/orders/parse.rs tests/order_flow.rs
```

The checker uses the Rust syntax tree to distinguish path attributes from comments, strings and
configuration predicates. It checks conditional attributes and literal attributes in macro templates.
