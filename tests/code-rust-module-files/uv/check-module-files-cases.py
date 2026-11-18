#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["tree-sitter==0.25.2", "tree-sitter-rust==0.24.2"]
# ///
"""Exercise physical Rust paths and conditional source selection at the shipped CLI."""

import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

CHECKER = Path("contracts/code-rust-module-files/assets/uv/check-module-files.py").resolve()
CASES = (
    ("src/invoice_lines.rs", '#[cfg_attr(unix, doc = "path")] mod parse;', ""),
    ("tests/support/mod.rs", '// #[path="fixture.rs"]', ""),
    ("src/Invoice.rs", "", "lower_snake_case"),
    ("examples/Bad-Dir/main.rs", "", "lower_snake_case"),
    ("src/orders/mod.rs", "", "sibling file"),
    ("src/orders.rs", '#[path = "other.rs"] mod parse;', "path attribute"),
    (
        "tests/order_flow.rs",
        '#[cfg_attr(any(), cfg_attr(unix, r#path = "other.rs"))] mod data;',
        "path attribute",
    ),
    (
        "src/generated.rs",
        'macro_rules! declare { () => { #[path="other.rs"] mod data; } }',
        "path attribute",
    ),
)


def _check(*, root: Path, name: str, source: str, diagnostic: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, CHECKER, "--crate", root, name],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if diagnostic:
        if result.returncode != 1 or diagnostic not in result.stderr or name not in result.stderr:
            raise AssertionError((name, result.stderr))
    else:
        result.check_returncode()


def main() -> None:
    """Each invalid case must reject the named file for the expected rule."""
    with TemporaryDirectory() as temporary:
        for name, source, diagnostic in CASES:
            _check(root=Path(temporary), name=name, source=source, diagnostic=diagnostic)


if __name__ == "__main__":
    main()
