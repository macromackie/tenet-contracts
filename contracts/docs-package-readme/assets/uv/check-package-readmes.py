#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Check the README of every workspace package and of every folder that groups packages."""

import argparse
import json
import re
import tomllib
from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path

README_FILE = "README.md"
PNPM_FILE = "pnpm-workspace.yaml"
CARGO_FILE = "Cargo.toml"
PYPROJECT_FILE = "pyproject.toml"
NODE_MANIFEST = "package.json"
INSTALLED_FOLDER = "node_modules"
NEGATION_PREFIX = "!"
PNPM_SECTION = re.compile(r"^packages:(?P<body>[^\n]*(?:\n(?:[ \t-][^\n]*)?)*)", flags=re.MULTILINE)
"""The `packages` key with its value: the rest of its line and each indented or list line below."""
PNPM_ITEM = re.compile(
    r"""(["'])(?P<quoted>[^"'\n]+)\1|^[ \t]*-[ \t]+(?P<bare>[^\s"'#\[][^\n#]*?)[ \t]*(?:#.*)?$""",
    flags=re.MULTILINE,
)
"""One member pattern, quoted in a block or flow list, or bare in a block list."""
JSON_SUFFIX = ".json"
DESCRIPTION_FIELD = "description"
TWO_SENTENCES = re.compile(r"[.!?] +[A-Z`]")
FENCE = "```"
HEADING_PREFIX = "#"
SECTION_HEADINGS = ("## Layout", "## Use", "## Never")
LAYOUT_ENTRY = re.compile(r"^- `(?P<path>[^`]+)`: \S")
TABLE_HEADER = ("Package", "Description")
TABLE_RULE = re.compile(r"^\|(?:[ \t]*:?-+:?[ \t]*\|)+$")
TABLE_EDGE = "|"
SENTENCE_INDEX = 2
INTRODUCTION_LINES = 4
"""The title, a blank line, the one sentence, and a blank line that open every README."""


class ReadmesRejected(ValueError):
    """The workspace file is missing or unreadable, or a README breaks its declared form."""


@dataclass(frozen=True, kw_only=True)
class Workspace:
    """The member patterns of one workspace file and the manifest that each member holds."""

    manifest: str
    patterns: tuple[str, ...]
    exclusions: tuple[str, ...]


@dataclass(frozen=True, kw_only=True)
class Package:
    """One workspace member with the name and description that its manifest declares."""

    folder: Path
    name: str
    description: str


@dataclass(frozen=True, kw_only=True)
class Limits:
    """The declared maximum number of lines of a package README and of a group README."""

    package_lines: int
    group_lines: int


def _read_pnpm_patterns(*, path: Path) -> tuple[str, ...]:
    section = PNPM_SECTION.search(path.read_text(encoding="utf-8"))
    patterns = tuple(
        str(item["quoted"] or item["bare"])
        for item in PNPM_ITEM.finditer(section["body"] if section is not None else "")
    )
    if not patterns:
        message = f"read workspace file {path.name!r}: list each member pattern under `packages`"
        raise ReadmesRejected(message)
    return patterns


def _read_pnpm_workspace(*, path: Path) -> Workspace:
    patterns = _read_pnpm_patterns(path=path)
    return Workspace(
        manifest=NODE_MANIFEST,
        patterns=tuple(pattern for pattern in patterns if not pattern.startswith(NEGATION_PREFIX)),
        exclusions=tuple(
            pattern.removeprefix(NEGATION_PREFIX)
            for pattern in patterns
            if pattern.startswith(NEGATION_PREFIX)
        ),
    )


def _read_toml_workspace(*, path: Path) -> Workspace | None:
    document: object = tomllib.loads(path.read_text(encoding="utf-8"))
    match document:
        case {"workspace": {"members": [*members], **settings}}:
            pass
        case {"tool": {"uv": {"workspace": {"members": [*members], **settings}}}}:
            pass
        case _:
            return None
    return Workspace(
        manifest=path.name,
        patterns=tuple(str(member) for member in members),
        exclusions=tuple(str(excluded) for excluded in settings.get("exclude", [])),
    )


def read_workspace(*, root: Path) -> Workspace:
    """Read the member patterns from the first workspace file that the root holds."""
    if (root / PNPM_FILE).is_file():
        return _read_pnpm_workspace(path=root / PNPM_FILE)
    for name in (CARGO_FILE, PYPROJECT_FILE):
        workspace = _read_toml_workspace(path=root / name) if (root / name).is_file() else None
        if workspace is not None:
            return workspace
    message = (
        f"read workspace {str(root)!r}: expected {PNPM_FILE}, a {CARGO_FILE} with `[workspace]`, "
        f"or a {PYPROJECT_FILE} with `[tool.uv.workspace]`"
    )
    raise ReadmesRejected(message)


def _read_manifest_table(*, path: Path) -> object:
    text = path.read_text(encoding="utf-8")
    if path.suffix == JSON_SUFFIX:
        return json.loads(text)
    match tomllib.loads(text):
        case {"package": table} | {"project": table}:
            return table
        case _:
            return {}


def _read_package(*, folder: Path, workspace: Workspace) -> Package:
    match _read_manifest_table(path=folder / workspace.manifest):
        case {"name": str() as name, "description": str() as description} if name:
            return Package(folder=folder, name=name, description=description)
        case {"name": str() as name, **fields} if name and DESCRIPTION_FIELD not in fields:
            return Package(folder=folder, name=name, description="")
        case _:
            message = (
                f"read manifest {str(folder / workspace.manifest)!r}: "
                "declare the name and the description as strings in the manifest itself"
            )
            raise ReadmesRejected(message)


def read_packages(*, root: Path, workspace: Workspace) -> list[Package]:
    """Read every member below the root that holds a manifest, without installed copies."""
    folders = {
        folder
        for pattern in workspace.patterns
        for folder in root.glob(pattern)
        if (folder / workspace.manifest).is_file()
        and folder != root
        and INSTALLED_FOLDER not in folder.relative_to(root).parts
        and not any(
            fnmatchcase(folder.relative_to(root).as_posix(), excluded)
            for excluded in workspace.exclusions
        )
    }
    return [_read_package(folder=folder, workspace=workspace) for folder in sorted(folders)]


def _read_headings(*, lines: list[str]) -> list[str]:
    headings = []
    is_fenced = False
    for line in lines:
        if line.lstrip().startswith(FENCE):
            is_fenced = not is_fenced
        elif not is_fenced and line.startswith(HEADING_PREFIX):
            headings.append(line)
    return headings


def _check_frame(
    *, place: str, lines: list[str], title: str, sentence: str, maximum: int
) -> list[str]:
    errors = []
    if lines[:INTRODUCTION_LINES] != [f"# {title}", "", sentence, ""]:
        errors.append(
            f"check README {place!r}: open with the title `# {title}`, a blank line, "
            f"and the one sentence {sentence!r}"
        )
    if not sentence.endswith(".") or TWO_SENTENCES.search(sentence):
        errors.append(
            f"check README {place!r}: write {sentence!r} as one sentence that ends with a period"
        )
    if len(lines) > maximum:
        errors.append(f"check README {place!r}: {len(lines)!r} lines exceeds {maximum!r}")
    return errors


def _check_layout(*, place: str, package: Package, lines: list[str]) -> list[str]:
    start = lines.index(SECTION_HEADINGS[0]) + 1
    end = lines.index(SECTION_HEADINGS[1])
    errors = []
    for line in lines[start:end]:
        entry = LAYOUT_ENTRY.match(line)
        if entry is None and line.strip():
            errors.append(
                f"check README {place!r}: write each Layout line as "
                f"`- `path`: what it holds`, not {line!r}"
            )
        elif entry is not None and not (package.folder / entry["path"]).exists():
            errors.append(f"check README {place!r}: Layout path {entry['path']!r} does not exist")
    return errors


def _check_package_readme(*, root: Path, package: Package, maximum: int) -> list[str]:
    path = package.folder / README_FILE
    place = path.relative_to(root).as_posix()
    if not path.is_file():
        return [f"check README {place!r}: file does not exist"]
    lines = path.read_text(encoding="utf-8").splitlines()
    errors = _check_frame(
        place=place,
        lines=lines,
        title=package.name,
        sentence=package.description,
        maximum=maximum,
    )
    if tuple(_read_headings(lines=lines)[1:]) != SECTION_HEADINGS:
        headings = ", ".join(SECTION_HEADINGS)
        return [
            *errors,
            f"check README {place!r}: keep exactly the headings {headings}, in that order",
        ]
    return [*errors, *_check_layout(place=place, package=package, lines=lines)]


def _read_table_cells(*, line: str) -> tuple[str, ...]:
    return tuple(cell.strip() for cell in line.strip().strip(TABLE_EDGE).split(TABLE_EDGE))


def _check_group_readme(
    *, root: Path, folder: Path, packages: list[Package], maximum: int
) -> list[str]:
    path = folder / README_FILE
    place = path.relative_to(root).as_posix()
    if not path.is_file():
        return [f"check README {place!r}: file does not exist"]
    lines = path.read_text(encoding="utf-8").splitlines()
    rows = [
        _read_table_cells(line=line)
        for line in lines[INTRODUCTION_LINES:]
        if line.strip() and not TABLE_RULE.match(line.strip())
    ]
    errors = _check_frame(
        place=place,
        lines=lines,
        title=folder.name,
        sentence=lines[SENTENCE_INDEX] if len(lines) > SENTENCE_INDEX else "",
        maximum=maximum,
    )
    if rows != [TABLE_HEADER, *((f"`{member.name}`", member.description) for member in packages)]:
        errors.append(
            f"check README {place!r}: after the sentence, keep only a table of "
            f"{' and '.join(TABLE_HEADER)} with one row for each package in manifest path order, "
            "its name in backticks and its manifest's description"
        )
    return errors


def inspect_readmes(*, root: Path, packages: list[Package], limits: Limits) -> list[str]:
    """Report every missing or malformed README of a package or of a folder that groups them."""
    groups: dict[Path, list[Package]] = {}
    for package in packages:
        if package.folder.parent != root:
            groups.setdefault(package.folder.parent, []).append(package)
    return [
        *(
            error
            for package in packages
            for error in _check_package_readme(
                root=root, package=package, maximum=limits.package_lines
            )
        ),
        *(
            error
            for folder, members in sorted(groups.items())
            for error in _check_group_readme(
                root=root, folder=folder, packages=members, maximum=limits.group_lines
            )
        ),
    ]


def _read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="workspace root to inspect")
    parser.add_argument(
        "--maximum-package-lines", type=int, default=30, help="line limit of a package README"
    )
    parser.add_argument(
        "--maximum-group-lines", type=int, default=15, help="line limit of a group README"
    )
    return parser.parse_args()


def main() -> None:
    """Check each member of the workspace at the given root without changing any file."""
    arguments = _read_arguments()
    root = Path(arguments.root).resolve()
    errors = inspect_readmes(
        root=root,
        packages=read_packages(root=root, workspace=read_workspace(root=root)),
        limits=Limits(
            package_lines=arguments.maximum_package_lines,
            group_lines=arguments.maximum_group_lines,
        ),
    )
    if errors:
        raise ReadmesRejected("\n".join(errors))


if __name__ == "__main__":
    main()
