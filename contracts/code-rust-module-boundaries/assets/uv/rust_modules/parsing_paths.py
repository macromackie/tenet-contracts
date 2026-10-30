"""Locate external Rust modules from declarations and explicit path attributes."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from rust_modules.kinds import NodeKind
from rust_modules.model import read_node_text

if TYPE_CHECKING:
    from pathlib import Path

    from tree_sitter import Node

    from rust_modules.parsing_context import ModuleContext

PATH_ATTRIBUTE = "path"
LEGACY_MODULE_FILE = "mod.rs"


def read_attribute_path(*, node: Node) -> str:
    """Decode a path attribute's string value without evaluating its contents."""
    literal = node.named_children[-1]
    if literal.type != NodeKind.STRING_LITERAL:
        message = (
            f"resolve Rust module path {read_node_text(node=node)!r}: expected a string literal"
        )
        raise ValueError(message)

    relative: object = json.loads(read_node_text(node=literal))
    if not isinstance(relative, str):
        message = (
            f"resolve Rust module path {read_node_text(node=node)!r}: expected a decoded string"
        )
        raise TypeError(message)

    return relative


def read_explicit_path(*, attributes: tuple[Node, ...]) -> str | None:
    """Read the source path named by an outer Rust path attribute."""
    for attribute in attributes:
        child = attribute.named_children[0]
        if read_node_text(node=child.named_children[0]) == PATH_ATTRIBUTE:
            return read_attribute_path(node=child)

    return None


def read_default_module_file(*, directory: Path, name: str) -> Path:
    """Require exactly one source file for an ordinary module declaration."""
    direct = directory / f"{name}.rs"
    legacy = directory / name / LEGACY_MODULE_FILE
    if direct.exists() == legacy.exists():
        message = (
            f"resolve Rust module {name!r} in {str(directory)!r}: expected exactly one source file"
        )
        raise ValueError(message)

    if direct.exists():
        return direct

    return legacy


def read_module_file(*, context: ModuleContext, name: str, attributes: tuple[Node, ...]) -> Path:
    """Locate a declared external module, including an explicit path attribute."""
    relative = read_explicit_path(attributes=attributes)
    if relative is not None:
        return context.module.file.parent / relative

    return read_default_module_file(directory=context.directory, name=name)
