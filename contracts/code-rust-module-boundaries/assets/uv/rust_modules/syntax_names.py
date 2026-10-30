"""Identify the Rust tokens that may form a path segment."""

from rust_modules.kinds import NodeKind

NAME_NODES = frozenset({
    NodeKind.IDENTIFIER,
    NodeKind.TYPE_IDENTIFIER,
    NodeKind.CRATE,
    NodeKind.SUPER,
    NodeKind.SELF,
})
