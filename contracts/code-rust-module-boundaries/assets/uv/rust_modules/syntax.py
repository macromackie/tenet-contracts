"""Decode Rust paths and use trees from Tree-sitter's Rust grammar."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rust_modules.kinds import NodeKind
from rust_modules.model import Import, read_node_text, require_field
from rust_modules.syntax_macros import read_macro_paths
from rust_modules.syntax_names import NAME_NODES

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from tree_sitter import Node

    from rust_modules.model import RustPath

PATH_NODES = frozenset({NodeKind.SCOPED_IDENTIFIER, NodeKind.SCOPED_TYPE_IDENTIFIER})
COMMENT_NODES = frozenset({NodeKind.LINE_COMMENT, NodeKind.BLOCK_COMMENT})
REFERENCE_NODES = frozenset({NodeKind.IDENTIFIER, NodeKind.TYPE_IDENTIFIER})
OWNER_NODES = frozenset({NodeKind.MOD_ITEM, NodeKind.USE_DECLARATION})
SELF_SEGMENT = NodeKind.SELF
TEST_ATTRIBUTE = "#[cfg(test)]"
GLOB_IMPORT = "*"


def _read_scoped_path(*, node: Node) -> RustPath:
    parent = node.child_by_field_name("path")
    prefix: RustPath = ()
    if parent is not None:
        prefix = read_path(node=parent)

    name = require_field(node=node, name="name")
    return (*prefix, read_node_text(node=name))


def read_path(*, node: Node) -> RustPath:
    """Decode the segments of an identifier or scoped path."""
    if node.type in NAME_NODES:
        return (read_node_text(node=node),)

    if node.type in PATH_NODES:
        return _read_scoped_path(node=node)

    if node.type == NodeKind.GENERIC_TYPE:
        return read_path(node=require_field(node=node, name="type"))

    message = f"decode Rust path {read_node_text(node=node)!r}: unsupported syntax {node.type!r}"
    raise ValueError(message)


def _read_declaration(*, node: Node, prefix: RustPath) -> Iterator[Import]:
    yield from read_imports(node=require_field(node=node, name="argument"), prefix=prefix)


def _read_scoped_imports(*, node: Node, prefix: RustPath) -> Iterator[Import]:
    path = node.child_by_field_name("path")
    segments = prefix
    if path is not None:
        segments = (*prefix, *read_path(node=path))

    yield from read_imports(node=require_field(node=node, name="list"), prefix=segments)


def _read_import_list(*, node: Node, prefix: RustPath) -> Iterator[Import]:
    for child in node.named_children:
        yield from read_imports(node=child, prefix=prefix)


def _read_renamed_import(*, node: Node, prefix: RustPath) -> Iterator[Import]:
    path = require_field(node=node, name="path")
    name = require_field(node=node, name="alias")
    yield Import(name=read_node_text(node=name), path=(*prefix, *read_path(node=path)), node=node)


def _read_glob_import(*, node: Node, prefix: RustPath) -> Iterator[Import]:
    segments = prefix
    for child in node.named_children:
        segments = (*segments, *read_path(node=child))

    yield Import(name=GLOB_IMPORT, path=segments, node=node)


def _read_named_import(*, node: Node, prefix: RustPath) -> Iterator[Import]:
    if node.type in COMMENT_NODES:
        return

    segments = (*prefix, *read_path(node=node))
    if segments[-1] == SELF_SEGMENT:
        segments = segments[:-1]

    yield Import(name=segments[-1], path=segments, node=node)


IMPORT_READERS: dict[str, Callable[..., Iterator[Import]]] = {
    NodeKind.USE_DECLARATION: _read_declaration,
    NodeKind.SCOPED_USE_LIST: _read_scoped_imports,
    NodeKind.USE_LIST: _read_import_list,
    NodeKind.USE_AS_CLAUSE: _read_renamed_import,
    NodeKind.USE_WILDCARD: _read_glob_import,
}


def read_imports(*, node: Node, prefix: RustPath = ()) -> Iterator[Import]:
    """Flatten grouped and renamed Rust imports without losing their source nodes."""
    reader = IMPORT_READERS.get(node.type, _read_named_import)
    yield from reader(node=node, prefix=prefix)


def is_test_attribute(*, node: Node) -> bool:
    """Identify an explicit test-only conditional attribute."""
    return (
        node.type == NodeKind.ATTRIBUTE_ITEM
        and "".join(read_node_text(node=node).split()) == TEST_ATTRIBUTE
    )


def _has_qualified_prefix(*, node: Node) -> bool:
    if node.type == NodeKind.BRACKETED_TYPE:
        return True

    child = node.child_by_field_name("path")
    if node.type == NodeKind.GENERIC_TYPE:
        child = node.child_by_field_name("type")

    return child is not None and _has_qualified_prefix(node=child)


def _read_type_arguments(*, node: Node) -> Iterator[tuple[RustPath, Node]]:
    for child in node.named_children:
        if child.type == NodeKind.TYPE_ARGUMENTS:
            yield from read_references(node=child)
        else:
            yield from _read_type_arguments(node=child)


def _read_scoped_references(*, node: Node) -> Iterator[tuple[RustPath, Node]]:
    if _has_qualified_prefix(node=node):
        prefix = require_field(node=node, name="path")
        yield from read_references(node=prefix)
    else:
        yield read_path(node=node), node
        yield from _read_type_arguments(node=node)


def read_references(*, node: Node) -> Iterator[tuple[RustPath, Node]]:
    """Walk paths while leaving nested modules to their own owner."""
    if node.type in OWNER_NODES:
        return

    if node.type in PATH_NODES:
        yield from _read_scoped_references(node=node)
        return

    if node.type == NodeKind.MACRO_INPUT:
        yield from read_macro_paths(node=node)
        return

    if node.type in REFERENCE_NODES:
        yield (read_node_text(node=node),), node

    for child in node.named_children:
        yield from read_references(node=child)
