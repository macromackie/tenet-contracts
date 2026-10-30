"""Hold parsed Rust modules and their lexical import bindings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from tree_sitter import Node

type RustPath = tuple[str, ...]


@dataclass(frozen=True)
class Import:
    """Bind a local name to a parsed use-tree path."""

    name: str
    path: RustPath
    node: Node


@dataclass(frozen=True)
class Module:
    """Own one Rust module's source and direct declarations."""

    name: RustPath
    file: Path
    node: Node
    imports: dict[str, Import] = field(default_factory=dict)
    items: dict[str, Node] = field(default_factory=dict)
    body: list[Node] = field(default_factory=list)


@dataclass(frozen=True)
class Crate:
    """Index the module tree and accumulated source diagnostics."""

    root: Path
    modules: dict[RustPath, Module] = field(default_factory=dict)
    diagnostics: list[str] = field(default_factory=list)


def read_node_text(*, node: Node) -> str:
    """Read the UTF-8 text retained by a parsed syntax node."""
    content = node.text
    if content is None:
        message = "read Rust syntax: parser did not retain source bytes"
        raise ValueError(message)

    return content.decode()


def require_field(*, node: Node, name: str) -> Node:
    """Read a field required by the Rust grammar."""
    child = node.child_by_field_name(name)
    if child is None:
        message = f"read Rust syntax {node.type!r}: required field {name!r} is absent"
        raise ValueError(message)

    return child


def format_location(*, module: Module, node: Node) -> str:
    """Identify a diagnostic's source path and one-based line."""
    return f"{module.file}:{node.start_point.row + 1}"
