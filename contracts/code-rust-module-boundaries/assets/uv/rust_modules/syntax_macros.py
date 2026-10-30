"""Read Rust path tokens inside macro arguments without inspecting strings."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rust_modules.kinds import NodeKind
from rust_modules.model import read_node_text
from rust_modules.syntax_names import NAME_NODES

if TYPE_CHECKING:
    from collections.abc import Iterator

    from tree_sitter import Node

    from rust_modules.model import RustPath

PATH_SEPARATOR = "::"


def _read_sequence(*, children: list[Node], start: int) -> tuple[RustPath, int]:
    segments = [read_node_text(node=children[start])]
    cursor = start + 1
    while cursor + 1 < len(children) and children[cursor].type == PATH_SEPARATOR:
        name = children[cursor + 1]
        if name.type not in NAME_NODES:
            break

        segments.append(read_node_text(node=name))
        cursor += 2

    return tuple(segments), cursor


def _read_nested_paths(*, node: Node) -> Iterator[tuple[RustPath, Node]]:
    if node.type == NodeKind.MACRO_INPUT:
        yield from read_macro_paths(node=node)


def read_macro_paths(*, node: Node) -> Iterator[tuple[RustPath, Node]]:
    """Read path token sequences from one macro argument tree."""
    children = node.children
    cursor = 0
    while cursor < len(children):
        child = children[cursor]
        cursor += 1
        if child.type in NAME_NODES:
            segments, cursor = _read_sequence(children=children, start=cursor - 1)
            yield segments, child

        yield from _read_nested_paths(node=child)
