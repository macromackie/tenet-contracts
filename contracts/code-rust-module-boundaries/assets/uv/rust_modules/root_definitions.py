"""Attribute explicit root associated paths to the matching method definitions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rust_modules.kinds import NodeKind
from rust_modules.model import read_node_text, require_field
from rust_modules.resolution import resolve
from rust_modules.syntax import read_path

if TYPE_CHECKING:
    from collections.abc import Iterator

    from tree_sitter import Node

    from rust_modules.model import Crate, RustPath


def read_impl_methods(*, node: Node, name: str) -> Iterator[Node]:
    """Read the one associated method named by an explicit source path."""
    body = require_field(node=node, name="body")
    for item in body.named_children:
        if item.type == NodeKind.FUNCTION_ITEM:
            declared = require_field(node=item, name="name")
            if read_node_text(node=declared) == name:
                yield item


def read_owned_impls(*, crate: Crate, target: RustPath) -> Iterator[Node]:
    """Find the impl blocks whose declared self type names the root owner."""
    root = crate.modules[()]
    for item in root.body:
        if item.type == NodeKind.IMPL_ITEM:
            declared = require_field(node=item, name="type")
            path = read_path(node=declared)
            owner = resolve(crate=crate, module=root, path=path, node=declared)
            if owner == target[:1]:
                yield item


def read_method_candidates(*, crate: Crate, target: RustPath, is_trait: bool) -> Iterator[Node]:
    """Read the named methods from inherent or trait impl blocks."""
    for item in read_owned_impls(crate=crate, target=target):
        has_trait = item.child_by_field_name("trait") is not None
        if has_trait == is_trait:
            yield from read_impl_methods(node=item, name=target[1])


def read_root_methods(*, crate: Crate, target: RustPath) -> Iterator[Node]:
    """Follow the named method, preferring inherent methods over trait methods."""
    inherent = list(read_method_candidates(crate=crate, target=target, is_trait=False))
    if inherent:
        yield from inherent
    else:
        yield from read_method_candidates(crate=crate, target=target, is_trait=True)


def read_alias_target(*, crate: Crate, node: Node, target: RustPath) -> RustPath | None:
    """Keep an associated suffix when a root type alias names another root type."""
    if node.type != NodeKind.TYPE_ITEM:
        return None

    declared = require_field(node=node, name="type")
    path = read_path(node=declared)
    owner = resolve(crate=crate, module=crate.modules[()], path=path, node=declared)
    if owner is None:
        return None

    return (*owner, *target[1:])


def read_root_definitions(
    *, crate: Crate, target: RustPath, visited_paths: frozenset[RustPath] = frozenset()
) -> Iterator[Node]:
    """Read a root item's definition and the particular associated method it references."""
    root = crate.modules[()]
    if target in visited_paths or target[0] not in root.items:
        return

    definition = root.items[target[0]]
    yield definition
    if len(target) > 1:
        yield from read_root_methods(crate=crate, target=target)
        alias = read_alias_target(crate=crate, node=definition, target=target)
        if alias is not None:
            yield from read_root_definitions(
                crate=crate, target=alias, visited_paths=visited_paths | {target}
            )
