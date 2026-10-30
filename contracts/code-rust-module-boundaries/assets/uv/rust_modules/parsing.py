"""Discover Rust's declared module tree from parsed source files."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tree_sitter_rust
from tree_sitter import Language, Parser

from rust_modules.kinds import NodeKind
from rust_modules.model import Crate, Import, Module, format_location, read_node_text, require_field
from rust_modules.parsing_context import Declaration, ModuleContext
from rust_modules.parsing_paths import LEGACY_MODULE_FILE, read_module_file
from rust_modules.syntax import is_test_attribute, read_imports

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from tree_sitter import Node

LIBRARY_FILE = "lib.rs"
PROCEDURAL_MACRO_ATTRIBUTES = frozenset({
    "proc_macro",
    "proc_macro_attribute",
    "proc_macro_derive",
})
COMMENT_NODES = frozenset({NodeKind.LINE_COMMENT, NodeKind.BLOCK_COMMENT})
DISCARDED_IMPORT = "_"
LIBRARY_ROOT_ITEMS = frozenset({
    NodeKind.ATTRIBUTE_ITEM,
    NodeKind.INNER_ATTRIBUTE_ITEM,
    NodeKind.EXTERN_CRATE_DECLARATION,
    NodeKind.USE_DECLARATION,
    NodeKind.MOD_ITEM,
    NodeKind.LINE_COMMENT,
    NodeKind.BLOCK_COMMENT,
})


def parse_source(*, path: Path, parser: Parser) -> Node:
    """Parse an entire source file and reject incomplete syntax trees."""
    root = parser.parse(path.read_bytes()).root_node
    if root.has_error:
        message = f"parse Rust source {str(path)!r}: syntax tree contains an error"
        raise ValueError(message)

    return root


def read_declarations(*, node: Node) -> Iterator[Declaration]:
    """Pair each non-test declaration with the attributes that govern it."""
    attributes: list[Node] = []
    for child in node.named_children:
        if child.type == NodeKind.ATTRIBUTE_ITEM:
            attributes.append(child)
        elif child.type in COMMENT_NODES:
            yield Declaration(node=child, attributes=())
        else:
            if not any(is_test_attribute(node=attribute) for attribute in attributes):
                yield Declaration(node=child, attributes=tuple(attributes))

            attributes = []


def check_child_visibility(*, context: ModuleContext, node: Node, name: str) -> None:
    """Require a module below the crate root to remain private."""
    has_visibility = any(
        child.type == NodeKind.VISIBILITY_MODIFIER for child in node.named_children
    )
    if context.module.name and has_visibility:
        context.crate.diagnostics.append(
            f"{format_location(module=context.module, node=node)}: "
            f"child module {name!r} must be private"
        )


def read_child_context(*, context: ModuleContext, declaration: Declaration) -> ModuleContext:
    """Load the declared child source while preserving inline-module locations."""
    name = read_node_text(node=require_field(node=declaration.node, name="name"))
    check_child_visibility(context=context, node=declaration.node, name=name)
    body = declaration.node.child_by_field_name("body")
    if body is None:
        return read_external_child(context=context, declaration=declaration, name=name)

    child = Module(name=(*context.module.name, name), file=context.module.file, node=body)
    return ModuleContext(
        crate=context.crate,
        module=child,
        directory=context.directory / name,
        parser=context.parser,
    )


def read_external_child(
    *, context: ModuleContext, declaration: Declaration, name: str
) -> ModuleContext:
    """Parse an external module and choose the directory that owns its children."""
    path = read_module_file(context=context, name=name, attributes=declaration.attributes)
    body = parse_source(path=path, parser=context.parser)
    directory = path.with_suffix("")
    if path.name == LEGACY_MODULE_FILE:
        directory = path.parent

    child = Module(name=(*context.module.name, name), file=path, node=body)
    return ModuleContext(
        crate=context.crate, module=child, directory=directory, parser=context.parser
    )


def index_external_alias(*, module: Module, node: Node) -> None:
    """Resolve an explicit alias for this crate while leaving external crates separate."""
    if node.type != NodeKind.EXTERN_CRATE_DECLARATION:
        return

    name = require_field(node=node, name="name")
    alias = node.child_by_field_name("alias")
    if read_node_text(node=name) != NodeKind.SELF or alias is None:
        return

    local_name = read_node_text(node=alias)
    module.imports[local_name] = Import(name=local_name, path=(NodeKind.CRATE,), node=node)


def index_item(*, module: Module, declaration: Declaration) -> None:
    """Index a module's item, imported names, and source references together."""
    module.body.extend(declaration.attributes)
    module.body.append(declaration.node)
    index_external_alias(module=module, node=declaration.node)
    if declaration.node.type == NodeKind.USE_DECLARATION:
        for imported in read_imports(node=declaration.node):
            if imported.name != DISCARDED_IMPORT:
                module.imports[imported.name] = imported

    name = declaration.node.child_by_field_name("name")
    if name is not None:
        module.items[read_node_text(node=name)] = declaration.node


def is_procedural_macro_attribute(*, node: Node) -> bool:
    """Recognize a built-in procedural macro attribute by its parsed identifier."""
    attribute = node.named_children[0]
    name = attribute.named_children[0]
    return (
        name.type == NodeKind.IDENTIFIER
        and read_node_text(node=name) in PROCEDURAL_MACRO_ATTRIBUTES
    )


def is_procedural_macro(*, declaration: Declaration) -> bool:
    """Identify a procedural macro function whose declaration belongs at crate root."""
    return declaration.node.type == NodeKind.FUNCTION_ITEM and any(
        is_procedural_macro_attribute(node=attribute) for attribute in declaration.attributes
    )


def check_library_root(*, context: ModuleContext, declaration: Declaration) -> None:
    """Reject ordinary definitions at a library's package entry point."""
    if context.module.name or context.crate.root.name != LIBRARY_FILE:
        return

    if declaration.node.type in LIBRARY_ROOT_ITEMS or is_procedural_macro(declaration=declaration):
        return

    context.crate.diagnostics.append(
        f"{format_location(module=context.module, node=declaration.node)}: "
        "library root must contain declarations and re-exports only"
    )


def read_module(*, context: ModuleContext) -> None:
    """Index direct items and recursively discover each non-test child module."""
    for declaration in read_declarations(node=context.module.node):
        if declaration.node.type == NodeKind.MOD_ITEM:
            child = read_child_context(context=context, declaration=declaration)
            context.crate.modules[child.module.name] = child.module
            read_module(context=child)
        else:
            index_item(module=context.module, declaration=declaration)

        check_library_root(context=context, declaration=declaration)


def parse_crate(*, crate_root: Path) -> Crate:
    """Build the complete non-test module tree of one crate entry point."""
    parser = Parser(Language(tree_sitter_rust.language()))
    crate = Crate(root=crate_root)
    root = Module(name=(), file=crate_root, node=parse_source(path=crate_root, parser=parser))
    crate.modules[()] = root
    context = ModuleContext(crate=crate, module=root, directory=crate_root.parent, parser=parser)
    read_module(context=context)
    return crate
