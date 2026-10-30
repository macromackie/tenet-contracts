"""Count direct same-extension files and source-relative folder depth."""

from collections import Counter
from fnmatch import fnmatchcase
from pathlib import Path
from typing import TYPE_CHECKING

from layout.check_source_length import check_source_length

if TYPE_CHECKING:
    from layout.types import LayoutPolicy


def _is_excluded(*, path: Path, root: Path, policy: LayoutPolicy) -> bool:
    relative = path.relative_to(root).as_posix()
    return any(
        fnmatchcase(relative, pattern) or fnmatchcase(relative + "/", pattern)
        for pattern in policy.exclusions
    )


def _check_counts(*, relative: str, file_counts: Counter[str], policy: LayoutPolicy) -> list[str]:
    return [
        f"check folder {relative!r}: {count!r} files with extension {extension!r} "
        f"exceeds {policy.maximum_files!r}"
        for extension, count in sorted(file_counts.items())
        if count > policy.maximum_files
    ]


def _check_folder(
    *, path: Path, source: Path, filenames: list[str], root: Path, policy: LayoutPolicy
) -> list[str]:
    errors = []
    relative = path.relative_to(root).as_posix()
    depth = len(path.relative_to(source).parts)
    if depth > policy.maximum_depth:
        errors.append(
            f"check folder {relative!r}: depth {depth!r} exceeds {policy.maximum_depth!r} "
            f"below {source.relative_to(root).as_posix()!r}"
        )
    selected_names = tuple(
        name for name in filenames if not _is_excluded(path=path / name, root=root, policy=policy)
    )
    errors.extend(
        _check_counts(
            relative=relative,
            file_counts=Counter(Path(name).suffix for name in selected_names),
            policy=policy,
        )
    )
    errors.extend(
        error
        for name in selected_names
        for error in check_source_length(path=path / name, root=root, policy=policy)
    )
    return errors


def _inspect_source(*, source: Path, root: Path, policy: LayoutPolicy) -> list[str]:
    errors = []
    pending = [source]
    while pending:
        path = pending.pop()
        entries = tuple(path.iterdir())
        directories = [
            entry
            for entry in entries
            if entry.is_dir()
            and not entry.is_symlink()
            and not _is_excluded(path=entry, root=root, policy=policy)
        ]
        pending.extend(directories)
        filenames = [entry.name for entry in entries if entry.is_file()]
        errors.extend(
            _check_folder(path=path, source=source, filenames=filenames, root=root, policy=policy)
        )
    return errors


def _inspect_files(*, root: Path, policy: LayoutPolicy) -> list[str]:
    errors = []
    file_counts: dict[Path, Counter[str]] = {}
    for name in policy.files:
        source = root / name
        if not source.is_file():
            errors.append(f"check source file {name!r}: file does not exist")
            continue
        errors.extend(check_source_length(path=source, root=root, policy=policy))
        file_counts.setdefault(source.parent, Counter())[source.suffix] += 1
    for path, counts in file_counts.items():
        errors.extend(
            _check_counts(
                relative=path.relative_to(root).as_posix(), file_counts=counts, policy=policy
            )
        )
    return errors


def inspect_layout(*, root: Path, policy: LayoutPolicy) -> tuple[str, ...]:
    """Report every oversized or overdeep first-party folder without changing source files."""
    errors = _inspect_files(root=root, policy=policy)
    for name in policy.roots:
        source = root / name
        if not source.is_dir():
            errors.append(f"check source root {name!r}: folder does not exist")
            continue
        errors.extend(_inspect_source(source=source, root=root, policy=policy))
    return tuple(errors)
