"""Read Rust lexical bindings without changing module path ownership."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rust_modules.kinds import NodeKind
from rust_modules.model import read_node_text
from rust_modules.syntax import read_imports

if TYPE_CHECKING:
    from collections.abc import Iterator

    from tree_sitter import Node

    from rust_modules.model import Import, Module

SCOPE_NODES = frozenset({NodeKind.BLOCK, NodeKind.DECLARATION_LIST, NodeKind.SOURCE_FILE})
PATTERN_CONTAINERS = frozenset({
    NodeKind.PARAMETER,
    NodeKind.FOR_EXPRESSION,
    NodeKind.MATCH_ARM,
    NodeKind.LET_CONDITION,
})
FUNCTION_NODES = frozenset({NodeKind.FUNCTION_ITEM, NodeKind.CLOSURE_EXPRESSION})


def read_ancestors(*, node: Node) -> Iterator[Node]:
    """Visit syntax parents from the immediate scope outwards."""
    parent = node.parent
    while parent is not None:
        yield parent
        parent = parent.parent


def read_identifiers(*, node: Node) -> set[str]:
    """Collect binding names from one pattern without interpreting expression text."""
    names: set[str] = set()
    if node.type == NodeKind.IDENTIFIER:
        names.add(read_node_text(node=node))

    for child in node.named_children:
        names.update(read_identifiers(node=child))

    return names


def has_pattern_name(*, node: Node, name: str) -> bool:
    """Test whether a grammar node binds one name in its pattern field."""
    pattern = node.child_by_field_name("pattern")
    return pattern is not None and name in read_identifiers(node=pattern)


def is_block_shadowing(*, block: Node, reference: Node, name: str) -> bool:
    """Read preceding let bindings and block-local item declarations."""
    for child in block.named_children:
        if child.type == NodeKind.LET_DECLARATION and child.end_byte <= reference.start_byte:
            if has_pattern_name(node=child, name=name):
                return True
        elif child.type == NodeKind.FUNCTION_ITEM:
            declared = child.child_by_field_name("name")
            if declared is not None and read_node_text(node=declared) == name:
                return True

    return False


def is_scope_shadowing(*, scope: Node, reference: Node, name: str) -> bool:
    """Read bindings introduced by one enclosing lexical scope."""
    if scope.type in PATTERN_CONTAINERS and has_pattern_name(node=scope, name=name):
        return True

    if scope.type in FUNCTION_NODES:
        parameters = scope.child_by_field_name("parameters")
        if parameters is not None:
            return any(
                has_pattern_name(node=child, name=name) for child in parameters.named_children
            )

    return scope.type == NodeKind.BLOCK and is_block_shadowing(
        block=scope, reference=reference, name=name
    )


def is_shadowed(*, name: str, node: Node, module: Module) -> bool:
    """Keep local bindings from resolving as identically named module imports."""
    if not any(scope.id == module.node.id for scope in read_ancestors(node=node)):
        return False

    for scope in read_ancestors(node=node):
        if scope.id == module.node.id:
            break

        if is_scope_shadowing(scope=scope, reference=node, name=name):
            return True

    return False


def read_scope_imports(*, node: Node) -> Iterator[Import]:
    """Read all imports declared directly in one lexical scope."""
    for child in node.named_children:
        if child.type == NodeKind.USE_DECLARATION:
            yield from read_imports(node=child)


def read_lexical_imports(*, module: Module, node: Node) -> Iterator[Import]:
    """Visit block-local bindings before the module's own import bindings."""
    if any(scope.id == module.node.id for scope in read_ancestors(node=node)):
        for scope in read_ancestors(node=node):
            if scope.id == module.node.id:
                break

            if scope.type in SCOPE_NODES:
                yield from read_scope_imports(node=scope)

    yield from module.imports.values()
