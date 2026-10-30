"""The immutable source roots, bounds, and generated-data exclusions."""

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class LayoutPolicy:
    """Apply the same declared bounds to every first-party source root."""

    exclusions: tuple[str, ...]
    files: tuple[str, ...]
    roots: tuple[str, ...]
    maximum_files: int
    maximum_depth: int
    maximum_source_lines: int
    source_suffixes: tuple[str, ...]
