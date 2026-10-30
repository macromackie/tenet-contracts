"""Decode explicit layout limits and justified data exclusions."""

import json
from pathlib import PurePosixPath
from typing import TYPE_CHECKING

from layout.constants import PARENT_COMPONENT
from layout.errors import LayoutRejected
from layout.types import LayoutPolicy

if TYPE_CHECKING:
    from pathlib import Path


def _read_path(*, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        message = f"read layout path {value!r}: expected a nonempty relative path"
        raise LayoutRejected(message)
    path = PurePosixPath(value)
    if path.is_absolute() or PARENT_COMPONENT in path.parts:
        message = f"read layout path {value!r}: expected a path inside the repository"
        raise LayoutRejected(message)
    return value


def _read_exclusion(*, value: object) -> str:
    match value:
        case {"pattern": str() as pattern, "reason": str() as reason, **unknown_fields} if (
            reason.strip() and not unknown_fields
        ):
            return _read_path(value=pattern)
        case _:
            message = f"read layout exclusion {value!r}: declare a pattern and its reason"
            raise LayoutRejected(message)


def _read_bound(*, value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        message = f"read layout bound {value!r}: expected a positive integer"
        raise LayoutRejected(message)
    return value


def _read_suffix(*, value: object) -> str:
    if (
        not isinstance(value, str)
        or not value.startswith(".")
        or PurePosixPath("source" + value).suffix != value
    ):
        message = f"read source suffix {value!r}: expected one file extension"
        raise LayoutRejected(message)
    return value


def read_layout(*, path: Path) -> LayoutPolicy:
    """Require positive shared bounds and explicit source-root and exclusion lists."""
    value: object = json.loads(path.read_text(encoding="utf-8"))
    match value:
        case {
            "maximumFilesPerExtension": maximum_files,
            "maximumFolderDepth": maximum_depth,
            "maximumSourceLines": maximum_source_lines,
            "sourceSuffixes": [*source_suffixes],
            "extensionlessSources": "shebang",
            "sourceFiles": [*files],
            "sourceRoots": [*roots],
            "exclusions": [*exclusions],
            **unknown_fields,
        } if roots and source_suffixes and not unknown_fields:
            return LayoutPolicy(
                roots=tuple(_read_path(value=root) for root in roots),
                exclusions=tuple(_read_exclusion(value=exclusion) for exclusion in exclusions),
                files=tuple(_read_path(value=file) for file in files),
                maximum_files=_read_bound(value=maximum_files),
                maximum_depth=_read_bound(value=maximum_depth),
                maximum_source_lines=_read_bound(value=maximum_source_lines),
                source_suffixes=tuple(_read_suffix(value=suffix) for suffix in source_suffixes),
            )
        case _:
            message = f"read layout policy {str(path)!r}: declare positive bounds and source roots"
            raise LayoutRejected(message)
