"""Carry module discovery state and a declaration's attached attributes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from tree_sitter import Node, Parser

    from rust_modules.model import Crate, Module


@dataclass(frozen=True)
class ModuleContext:
    """Own the inputs needed to discover one module's children."""

    crate: Crate
    module: Module
    directory: Path
    parser: Parser


@dataclass(frozen=True)
class Declaration:
    """Pair an item with the outer attributes that precede it."""

    node: Node
    attributes: tuple[Node, ...]
