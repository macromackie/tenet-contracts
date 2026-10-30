#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Check repository source lengths, same-extension file counts, and folder depths."""

import argparse
from pathlib import Path

from layout import inspect_layout, read_layout
from layout.errors import LayoutRejected


def main() -> None:
    """Check the declared repository roots without changing any source files."""
    # jscpd:ignore-start -- duplication -- Standalone checkers must carry their own argument parser.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="repository root to inspect")
    parser.add_argument(
        "--config", required=True, help="policy path relative to the repository root"
    )
    arguments = parser.parse_args()
    root = Path(arguments.root).resolve()
    # jscpd:ignore-end
    policy = read_layout(path=root / arguments.config)
    errors = inspect_layout(root=root, policy=policy)
    if errors:
        raise LayoutRejected("\n".join(errors))


if __name__ == "__main__":
    main()
