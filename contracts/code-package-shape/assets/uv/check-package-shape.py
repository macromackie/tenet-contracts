#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Check each package's root entries, folder name, and source root against the declared shape."""

import argparse
import json
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

README_FILE = "README.md"
NAME_SEPARATOR = "/"
JSON_SUFFIX = ".json"


class ShapeRejected(ValueError):
    """The policy is malformed, or a package breaks the declared shape."""


@dataclass(frozen=True, kw_only=True)
class Policy:
    """The declared package folders, their fixed entries, and the limits of a source root."""

    patterns: tuple[str, ...]
    manifest: str
    source_folder: str
    entry_files: frozenset[str]
    role_files: frozenset[str]
    maximum_flat_modules: int
    deploy_entries: frozenset[tuple[str, str]]
    generated_entries: frozenset[str]


# jscpd:ignore-start -- duplication -- Standalone checkers must carry their own policy readers.
def _read_name(*, value: object) -> str:
    if not isinstance(value, str) or not value.strip() or PurePosixPath(value).is_absolute():
        message = f"read shape name {value!r}: expected a nonempty relative name"
        raise ShapeRejected(message)
    return value


def _read_generated_entry(*, value: object) -> str:
    match value:
        case {"name": str() as name, "reason": str() as reason, **unknown_fields} if (
            reason.strip() and not unknown_fields
        ):
            return _read_name(value=name)
        case _:
            message = f"read generated entry {value!r}: declare a name and its reason"
            raise ShapeRejected(message)


# jscpd:ignore-end


def _read_deploy_entry(*, value: object) -> tuple[str, str]:
    match value:
        case {
            "package": str() as package,
            "name": str() as name,
            "reason": str() as reason,
            **unknown_fields,
        } if reason.strip() and not unknown_fields:
            return _read_name(value=package), _read_name(value=name)
        case _:
            message = f"read deploy entry {value!r}: declare a package, a name, and its reason"
            raise ShapeRejected(message)


def read_policy(*, path: Path) -> Policy:
    """Require every field of the policy, and refuse a field that the policy does not define."""
    value: object = json.loads(path.read_text(encoding="utf-8"))
    match value:
        case {
            "packagePatterns": [*patterns],
            "manifest": manifest,
            "sourceFolder": source_folder,
            "entryFiles": [*entry_files],
            "roleFiles": [*role_files],
            "maximumFlatModules": int() as maximum_flat_modules,
            "deployEntries": [*deploy_entries],
            "generatedEntries": [*generated_entries],
            **unknown_fields,
        } if patterns and maximum_flat_modules >= 1 and not unknown_fields:
            return Policy(
                patterns=tuple(_read_name(value=pattern) for pattern in patterns),
                manifest=_read_name(value=manifest),
                source_folder=_read_name(value=source_folder),
                entry_files=frozenset(_read_name(value=name) for name in entry_files),
                role_files=frozenset(_read_name(value=name) for name in role_files),
                maximum_flat_modules=maximum_flat_modules,
                deploy_entries=frozenset(
                    _read_deploy_entry(value=entry) for entry in deploy_entries
                ),
                generated_entries=frozenset(
                    _read_generated_entry(value=entry) for entry in generated_entries
                ),
            )
        case _:
            message = (
                f"read shape policy {str(path)!r}: declare the package patterns, the manifest, "
                "the source folder, the entry files, the role files, a positive module limit, "
                "the deploy entries, and the generated entries"
            )
            raise ShapeRejected(message)


def _read_package_name(*, path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    document: object = json.loads(text) if path.suffix == JSON_SUFFIX else tomllib.loads(text)
    match document:
        case (
            {"name": str() as name}
            | {"package": {"name": str() as name}}
            | {"project": {"name": str() as name}}
        ):
            return name
        case _:
            message = f"read manifest {str(path)!r}: declare the package's name"
            raise ShapeRejected(message)


def _check_root(*, place: str, folder: Path, policy: Policy) -> list[str]:
    required_names = {README_FILE, policy.manifest, policy.source_folder}
    deployed_names = {name for package, name in policy.deploy_entries if package == place}
    names = {entry.name for entry in folder.iterdir()} - policy.generated_entries
    return [
        *(
            f"check package {place!r}: add {name!r} to the package root"
            for name in sorted(required_names - names)
        ),
        *(
            f"check package {place!r}: move {name!r} out of the package root, "
            "or declare it as a deploy entry with its reason"
            for name in sorted(names - required_names - deployed_names)
        ),
    ]


def _check_source_root(*, place: str, source: Path, policy: Policy) -> list[str]:
    entries = [entry for entry in source.iterdir() if entry.name not in policy.generated_entries]
    files = sorted(entry.name for entry in entries if entry.is_file())
    if any(entry.is_dir() for entry in entries):
        return [
            f"check source root {place!r}: move {name!r} into a folder, "
            "because only entry files and role files sit beside folders"
            for name in files
            if name not in policy.entry_files | policy.role_files
        ]
    if len(files) > policy.maximum_flat_modules:
        return [
            (
                f"check source root {place!r}: {len(files)!r} modules exceeds "
                f"{policy.maximum_flat_modules!r}; group the modules into folders"
            )
        ]
    return []


def _check_package(*, root: Path, folder: Path, policy: Policy) -> list[str]:
    place = folder.relative_to(root).as_posix()
    if not (folder / policy.manifest).is_file():
        return [f"check package {place!r}: add {policy.manifest!r} to the package root"]
    name = _read_package_name(path=folder / policy.manifest)
    errors = _check_root(place=place, folder=folder, policy=policy)
    if folder.name != name.rpartition(NAME_SEPARATOR)[2]:
        errors.append(
            f"check package {place!r}: name the folder "
            f"{name.rpartition(NAME_SEPARATOR)[2]!r}, the last segment of {name!r}"
        )
    source = folder / policy.source_folder
    if source.is_dir():
        errors.extend(
            _check_source_root(
                place=f"{place}/{policy.source_folder}", source=source, policy=policy
            )
        )
    return errors


def inspect_shape(*, root: Path, policy: Policy) -> list[str]:
    """Report every package whose root, folder name, or source root breaks the declared shape."""
    folders = sorted({
        folder for pattern in policy.patterns for folder in root.glob(pattern) if folder.is_dir()
    })
    if not folders:
        return [f"check package patterns {policy.patterns!r}: no folder matches"]
    return [
        error
        for folder in folders
        for error in _check_package(root=root, folder=folder, policy=policy)
    ]


def main() -> None:
    """Check the packages below the given root against the policy without changing any file."""
    # jscpd:ignore-start -- duplication -- Standalone checkers must carry their own argument parser.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="workspace root to inspect")
    parser.add_argument(
        "--config", required=True, help="policy path relative to the workspace root"
    )
    arguments = parser.parse_args()
    root = Path(arguments.root).resolve()
    # jscpd:ignore-end
    policy = read_policy(path=root / arguments.config)
    errors = inspect_shape(root=root, policy=policy)
    if errors:
        raise ShapeRejected("\n".join(errors))


if __name__ == "__main__":
    main()
