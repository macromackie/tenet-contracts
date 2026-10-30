"""Enforce the declared total line limit on source files and shebang tasks."""

from typing import TYPE_CHECKING

from layout.constants import SHEBANG_PREFIX

if TYPE_CHECKING:
    from pathlib import Path

    from layout.types import LayoutPolicy


def _is_source_file(*, path: Path, policy: LayoutPolicy) -> bool:
    if path.suffix in policy.source_suffixes:
        return True
    if path.suffix:
        return False
    with path.open("rb") as source:
        return source.read(len(SHEBANG_PREFIX)) == SHEBANG_PREFIX


def check_source_length(*, path: Path, root: Path, policy: LayoutPolicy) -> list[str]:
    """Count every line, including comments and blanks, in declared source files."""
    if not _is_source_file(path=path, policy=policy):
        return []
    lines = len(path.read_text(encoding="utf-8").splitlines())
    if lines <= policy.maximum_source_lines:
        return []
    relative = path.relative_to(root).as_posix()
    return [
        f"check source file {relative!r}: {lines!r} lines exceeds {policy.maximum_source_lines!r}"
    ]
