# Rust module check

Copy `module-policy.json` into the repository as `.config/rust-modules.json`. Set `crateRoots` to each production
crate's entry file, such as `src/lib.rs` or `src/main.rs`. Paths are relative to the repository root.

Run from that root, replacing the installed contract path:

```bash
uv run --script .contracts/013-code-rust-module-boundaries/assets/uv/check-module-boundaries.py --root . --config .config/rust-modules.json
```

The script requires Python 3.14 or later. Its inline metadata pins the syntax parser dependencies; `uv` installs
them in the script environment. `module-policy.schema.json` describes the policy.

The checker follows source module declarations, root re-exports, and source paths to report top-level dependency
cycles and access to private child modules. It leaves test modules out of the production dependency graph. Run the
repository's compiler separately for type resolution and other language checks.

The command reports every observed boundary violation and exits unsuccessfully. It changes no source files.
