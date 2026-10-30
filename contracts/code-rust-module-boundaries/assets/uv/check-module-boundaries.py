#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["tree-sitter==0.25.2", "tree-sitter-rust==0.24.2"]
# ///
"""Check Rust source module visibility and top-level dependency cycles."""

import argparse
import json
from pathlib import Path, PurePosixPath

from rust_modules import check_crate

PARENT_COMPONENT = ".."


class ModuleGraphRejected(ValueError):
    """The module policy or its production crates violate their declared boundaries."""


def _read_relative_path(*, value: object) -> PurePosixPath:
    if not isinstance(value, str) or not value.strip():
        message = f"read module policy path {value!r}: expected a nonempty relative file path"
        raise ModuleGraphRejected(message)

    relative = PurePosixPath(value)
    if relative.is_absolute() or PARENT_COMPONENT in relative.parts:
        message = (
            f"read module policy path {value!r}: expected a relative path without parent steps"
        )
        raise ModuleGraphRejected(message)

    return relative


def _read_relative_file(*, root: Path, value: object) -> Path:
    relative = _read_relative_path(value=value)
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root) or not resolved.is_file():
        message = f"read module policy path {value!r}: expected a file inside the repository"
        raise ModuleGraphRejected(message)

    return resolved


def _read_roots(*, root: Path, config: str) -> tuple[Path, ...]:
    path = _read_relative_file(root=root, value=config)
    value: object = json.loads(path.read_text(encoding="utf-8"))
    match value:
        case {"crateRoots": [*roots], **unknown_fields} if roots and not unknown_fields:
            return tuple(_read_relative_file(root=root, value=entry) for entry in roots)
        case _:
            message = f"read module policy {config!r}: declare a nonempty crateRoots list"
            raise ModuleGraphRejected(message)


def _check_roots(*, crate_roots: tuple[Path, ...]) -> None:
    errors: list[str] = []
    for crate_root in crate_roots:
        errors.extend(check_crate(crate_root=crate_root))

    if errors:
        message = "\n".join(errors)
        raise ModuleGraphRejected(message)


def main() -> None:
    """Check each explicitly declared crate entry file under the repository root."""
    # jscpd:ignore-start -- duplication -- Standalone checkers must carry their own argument parser.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="repository root to inspect")
    parser.add_argument(
        "--config", required=True, help="policy path relative to the repository root"
    )
    arguments = parser.parse_args()
    root = Path(arguments.root).resolve()
    # jscpd:ignore-end
    crate_roots = _read_roots(root=root, config=arguments.config)
    _check_roots(crate_roots=crate_roots)


if __name__ == "__main__":
    main()
