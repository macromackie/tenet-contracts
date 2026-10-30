"""Enforce an acyclic Rust top-level module graph and private child modules."""

from __future__ import annotations

from collections import defaultdict
from graphlib import CycleError, TopologicalSorter
from typing import TYPE_CHECKING

from rust_modules.model import format_location
from rust_modules.parsing import parse_crate
from rust_modules.resolution import read_uses, resolve
from rust_modules.root_definitions import read_root_definitions
from rust_modules.syntax import read_imports, read_references

if TYPE_CHECKING:
    from pathlib import Path

    from tree_sitter import Node

    from rust_modules.model import Crate, Module, RustPath


def read_node_paths(*, node: Node) -> list[tuple[RustPath, Node]]:
    """Read all references and imports belonging to one item's definition."""
    paths = list(read_references(node=node))
    for imported_node in read_uses(node=node):
        paths.extend(
            (imported.path, imported.node) for imported in read_imports(node=imported_node)
        )

    return paths


def read_paths(*, module: Module) -> list[tuple[RustPath, Node]]:
    """Collect every explicit import and every value, type, or macro reference."""
    paths: list[tuple[RustPath, Node]] = []
    for item in module.body:
        paths.extend(read_node_paths(node=item))

    return paths


def check_visibility(*, crate: Crate, module: Module, path: RustPath, node: Node) -> None:
    """Reject paths that explicitly enter another parent's private child module."""
    for length in range(1, len(path) + 1):
        prefix = resolve(crate=crate, module=module, path=path[:length], node=node)
        if prefix is not None and len(prefix) > 1 and prefix in crate.modules:
            parent = prefix[:-1]
            if module.name[: len(parent)] != parent:
                target = "::".join(prefix)
                crate.diagnostics.append(
                    f"{format_location(module=module, node=node)}: "
                    f"path enters private child module {target!r}"
                )


def read_owners(
    *,
    crate: Crate,
    module: Module,
    path: RustPath,
    node: Node,
    visited_paths: frozenset[RustPath] = frozenset(),
) -> set[str]:
    """Attribute root re-exports and root item references to their defining modules."""
    target = resolve(crate=crate, module=module, path=path, node=node)
    if target is None or not target or target in visited_paths:
        return set()

    if (target[0],) in crate.modules:
        return {target[0]}

    root = crate.modules[()]
    if target[0] not in root.items:
        return set()

    owners: set[str] = set()
    for definition in read_root_definitions(crate=crate, target=target):
        for reference, source in read_node_paths(node=definition):
            owners.update(
                read_owners(
                    crate=crate,
                    module=root,
                    path=reference,
                    node=source,
                    visited_paths=visited_paths | {target},
                )
            )

    return owners


def read_dependencies(*, crate: Crate) -> dict[str, set[str]]:
    """Build each top-level module's complete owned dependency set."""
    dependencies: dict[str, set[str]] = defaultdict(set)
    for name in crate.modules:
        if len(name) == 1:
            dependencies[name[0]] = set()

    for module in crate.modules.values():
        for path, node in read_paths(module=module):
            check_visibility(crate=crate, module=module, path=path, node=node)
            if module.name:
                owners = read_owners(crate=crate, module=module, path=path, node=node)
                dependencies[module.name[0]].update(owners - {module.name[0]})

    return dependencies


def check_crate(*, crate_root: Path) -> list[str]:
    """Check one crate entry file, such as src/lib.rs, and return source diagnostics."""
    crate = parse_crate(crate_root=crate_root)
    sorter = TopologicalSorter(read_dependencies(crate=crate))
    try:
        sorter.prepare()
    except CycleError as error:
        cycle = " -> ".join(error.args[1])
        crate.diagnostics.append(f"{crate_root}: top-level module cycle {cycle!r}")

    return sorted(set(crate.diagnostics))
