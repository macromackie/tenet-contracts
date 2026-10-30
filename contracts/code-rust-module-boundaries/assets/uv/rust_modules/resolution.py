"""Resolve module paths through lexical imports and crate-root re-exports."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rust_modules.kinds import NodeKind
from rust_modules.scope_bindings import is_shadowed, read_lexical_imports

if TYPE_CHECKING:
    from collections.abc import Iterator

    from tree_sitter import Node

    from rust_modules.model import Crate, Import, Module, RustPath

GLOB_IMPORT_NAME = "*"


def resolve_import(
    *,
    crate: Crate,
    module: Module,
    imported: Import,
    seen_bindings: frozenset[tuple[RustPath, str]],
) -> RustPath | None:
    """Follow one import through its source scope while breaking import alias loops."""
    key = (module.name, imported.name)
    if key in seen_bindings:
        return None

    return resolve(
        crate=crate,
        module=module,
        path=imported.path,
        node=imported.node,
        seen_bindings=seen_bindings | {key},
    )


def resolve_named(
    *,
    crate: Crate,
    module: Module,
    path: RustPath,
    node: Node,
    seen_bindings: frozenset[tuple[RustPath, str]],
) -> RustPath | None:
    """Resolve an ordinary name through imports or its module's declarations."""
    first, *remaining = path
    for imported in read_lexical_imports(module=module, node=node):
        if imported.name == first and (module.name, first) not in seen_bindings:
            target = resolve_import(
                crate=crate, module=module, imported=imported, seen_bindings=seen_bindings
            )
            if target is None:
                return None

            return resolve_from(
                crate=crate,
                owner=target,
                path=tuple(remaining),
                node=node,
                seen_bindings=seen_bindings | {(module.name, first)},
            )

    if (*module.name, first) in crate.modules or first in module.items:
        return resolve_from(
            crate=crate,
            owner=(*module.name, first),
            path=tuple(remaining),
            node=node,
            seen_bindings=seen_bindings,
        )

    return resolve_external_alias(
        crate=crate, module=module, path=path, node=node, seen_bindings=seen_bindings
    )


def resolve_external_alias(
    *,
    crate: Crate,
    module: Module,
    path: RustPath,
    node: Node,
    seen_bindings: frozenset[tuple[RustPath, str]],
) -> RustPath | None:
    """Resolve a crate-root self alias that enters Rust's extern prelude."""
    root = crate.modules[()]
    imported = root.imports.get(path[0])
    if imported is not None and imported.node.type == NodeKind.EXTERN_CRATE_DECLARATION:
        target = resolve_import(
            crate=crate, module=root, imported=imported, seen_bindings=seen_bindings
        )
        if target is not None:
            return resolve_from(
                crate=crate, owner=target, path=path[1:], node=node, seen_bindings=seen_bindings
            )

    return resolve_globs(
        crate=crate, module=module, path=path, node=node, seen_bindings=seen_bindings
    )


def resolve_glob(
    *,
    crate: Crate,
    module: Module,
    imported: Import,
    path: RustPath,
    seen_bindings: frozenset[tuple[RustPath, str]],
) -> RustPath | None:
    """Resolve a name exposed by one owned glob import."""
    target = resolve_import(
        crate=crate, module=module, imported=imported, seen_bindings=seen_bindings
    )
    if target is None:
        return None

    return resolve_from(
        crate=crate,
        owner=target,
        path=path,
        node=imported.node,
        seen_bindings=seen_bindings | {(module.name, imported.name)},
    )


def resolve_globs(
    *,
    crate: Crate,
    module: Module,
    path: RustPath,
    node: Node,
    seen_bindings: frozenset[tuple[RustPath, str]],
) -> RustPath | None:
    """Follow owned glob imports while leaving external crate globs external."""
    for imported in read_lexical_imports(module=module, node=node):
        if imported.name == GLOB_IMPORT_NAME:
            resolved = resolve_glob(
                crate=crate,
                module=module,
                imported=imported,
                path=path,
                seen_bindings=seen_bindings,
            )
            if resolved is not None:
                return resolved

    return None


def resolve(
    *,
    crate: Crate,
    module: Module,
    path: RustPath,
    node: Node,
    seen_bindings: frozenset[tuple[RustPath, str]] = frozenset(),
) -> RustPath | None:
    """Resolve a source path to an owned module or item, separating external crates."""
    if not path:
        return module.name

    first, *remaining = path
    if first == NodeKind.CRATE:
        return resolve_from(
            crate=crate, owner=(), path=tuple(remaining), node=node, seen_bindings=seen_bindings
        )

    if first == NodeKind.SELF:
        return resolve_from(
            crate=crate,
            owner=module.name,
            path=tuple(remaining),
            node=node,
            seen_bindings=seen_bindings,
        )

    if first == NodeKind.SUPER:
        return resolve_from(
            crate=crate,
            owner=module.name[:-1],
            path=tuple(remaining),
            node=node,
            seen_bindings=seen_bindings,
        )

    if len(path) == 1 and is_shadowed(name=first, node=node, module=module):
        return None

    return resolve_named(
        crate=crate, module=module, path=path, node=node, seen_bindings=seen_bindings
    )


def resolve_from(
    *,
    crate: Crate,
    owner: RustPath,
    path: RustPath,
    node: Node,
    seen_bindings: frozenset[tuple[RustPath, str]],
) -> RustPath | None:
    """Continue resolution after an explicit crate, self, super, or imported prefix."""
    if not path:
        return owner

    if owner not in crate.modules:
        return (*owner, *path)

    return resolve(
        crate=crate, module=crate.modules[owner], path=path, node=node, seen_bindings=seen_bindings
    )


def read_uses(*, node: Node) -> Iterator[Node]:
    """Find module and block-local imports without entering a different module."""
    if node.type == NodeKind.MOD_ITEM:
        return

    if node.type == NodeKind.USE_DECLARATION:
        yield node
        return

    for child in node.named_children:
        yield from read_uses(node=child)
