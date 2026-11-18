#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["tree-sitter==0.25.2", "tree-sitter-rust==0.24.2"]
# ///
"""Check physical Rust paths and module path attributes in handwritten source files."""

import argparse
import re
from itertools import pairwise
from pathlib import Path
from typing import TYPE_CHECKING

import tree_sitter_rust
from tree_sitter import Language, Parser

if TYPE_CHECKING:
    from collections.abc import Iterator

    from tree_sitter import Node

SNAKE_CASE = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*")
ATTRIBUTE = "attribute"
GROUP = "token_tree"
HASH = "#"
BANG = "!"
OPEN_BRACKET = "["
EQUALS = "="
COMMA = ","
PARENT = ".."
RUST_SUFFIX = ".rs"
SOURCE = "src"
LEGACY = "mod.rs"
COMMENTS = {"block_comment", "line_comment"}


def _has_path_attribute(*, parts: list[Node]) -> bool:
    match parts:
        case [name, equals, *_] if name.text in {b"path", b"r#path"} and equals.type == EQUALS:
            return True
        case [name, group] if name.text in {b"cfg_attr", b"r#cfg_attr"}:
            arguments: list[list[Node]] = [[]]
            for token in group.children[1:-1]:
                if token.type == COMMA:
                    arguments.append([])
                elif token.type not in COMMENTS:
                    arguments[-1].append(token)
            return any(_has_path_attribute(parts=argument) for argument in arguments[1:])
        case _:
            return False


def _find_macro_overrides(*, node: Node) -> Iterator[int]:
    tokens = [part for part in node.children if part.type not in COMMENTS and part.type != BANG]
    for prefix, group in pairwise(tokens):
        if prefix.type == HASH and group.type == GROUP and group.children[0].type == OPEN_BRACKET:
            parts = [part for part in group.children[1:-1] if part.type not in COMMENTS]
            if _has_path_attribute(parts=parts):
                yield group.start_point.row + 1


def _find_overrides(*, tree: Node) -> Iterator[int]:
    pending = [tree]
    while pending:
        node = pending.pop()
        if node.type == ATTRIBUTE:
            if _has_path_attribute(
                parts=[part for part in node.children if part.type not in COMMENTS]
            ):
                yield node.start_point.row + 1
        elif node.type == GROUP:
            yield from _find_macro_overrides(node=node)
        pending.extend(reversed(node.named_children))


def _check_path(*, root: Path, path: Path) -> str | None:
    if path.is_absolute() or PARENT in path.parts or path.suffix != RUST_SUFFIX:
        return f"{path}: supply a crate-relative Rust source file"
    if (root / path).resolve() != root / path:
        return f"{path}: use the physical Rust path inside its crate"
    if any(not SNAKE_CASE.fullmatch(part) for part in (*path.parent.parts, path.stem)):
        return f"{path}: use lower_snake_case for Rust filenames and module directories"
    if path.parts[0] == SOURCE and path.name == LEGACY:
        return f"{path}: declare the module in the sibling file named for it"
    return None


def _check_file(*, root: Path, path: Path, parser: Parser) -> Iterator[str]:
    if (error := _check_path(root=root, path=path)) is not None:
        yield error
        return
    tree = parser.parse((root / path).read_bytes()).root_node
    if tree.has_error:
        yield f"{path}: could not parse handwritten Rust"
    for line in _find_overrides(tree=tree):
        yield f"{path}:{line}: resolve the module by its declared name without a path attribute"


def main() -> None:
    """Check each supplied file relative to the directory containing its Cargo manifest."""
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("--crate", required=True, type=Path)
    arguments.add_argument("files", nargs="+", type=Path)
    options = arguments.parse_args()
    root = options.crate.resolve()
    parser = Parser(Language(tree_sitter_rust.language()))
    errors = [
        error
        for path in options.files
        for error in _check_file(root=root, path=path, parser=parser)
    ]
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
