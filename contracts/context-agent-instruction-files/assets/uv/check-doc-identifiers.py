#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""
Check that each name a document gives in a code span still exists in the repository.

A file path with a folder names a file under the root, the document's folder, or a `--base` folder.
A bare file name names a file anywhere under the root, or appears in the code as a stored name.
An identifier in a case style that only code writes, alone or called, appears in the code as a word.
An identifier written "in" or "of" a file, as in "`readOrder` in `store.ts`", is in that file.
A package name such as `@scope/name` appears in the code as a whole name.
A kebab-case name is a declared name, a run of whole names in a path, or a whole name in the code.
A `mise run <task>` or `mise -C <folder> run <task>` command names a task that `--tasks` declares.
A limit written as a constant and its value, as in "`MAXIMUM_WORDS` (30)", is the constant's value.
A document after `--adapted` is an adopted contract, checked only under `## Local adaptations`.
"""

import argparse
import json
import re
import subprocess
import tomllib
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

SKIPPED_FOLDERS = frozenset({".git", "node_modules", "dist", "target", "__pycache__"})
"""The folders of version control, installed packages, and build output, which hold no names."""
DOCUMENT_SUFFIX = ".md"
RULE_SUFFIX = ".yml"
ROOT_FOLDER = "."
PAIR_SEPARATOR = "="
PATH_SEPARATOR = "/"
INLINE_CODE = re.compile(r"(`+)((?:(?!\1).)+)\1")
IDENTIFIER = re.compile(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*")
CALL = re.compile(rf"({IDENTIFIER.pattern})\(")
CODE_NAME = re.compile(
    r"[a-z0-9][A-Z]|^[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)*$"
    r"|^[A-Z][A-Z0-9]*_[A-Z0-9_]+$|^[a-z][a-z0-9]*_[a-z0-9_]+$"
)
"""A name in camelCase, PascalCase, SCREAMING_SNAKE_CASE, or snake_case, which only code writes."""
RULE_ID = re.compile(r"""^"?id"?:\s*["']?([\w-]+)["']?\s*$""", re.MULTILINE)
ADAPTATIONS = re.compile(r"^## Local adaptations\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
WORD = re.compile(r"[\w$]+")
FILE_PATH = re.compile(
    r"(?:\./)?((?:[\w@.-]+/)*\w[\w.-]*\."
    r"(?:cjs|cts|js|json|jsonc|jsonl|md|mjs|mts|py|rs|sh|toml|ts|tsx|txt|yaml|yml))"
)
PACKAGE = re.compile(r"@[\w-]+/[\w.-]+")
NAME_IN_FILE = re.compile(r"`(?P<name>[^`\s]+)` (?:in|of) (?:`?[\w@/-]+`?'s )?`(?P<token>[^`\s]+)`")
KEBAB_NAME = re.compile(r"[a-z][a-z0-9]*(?:[-.:/][a-z0-9]+)*[-:][a-z0-9]+(?:[-.:/][a-z0-9]+)*")
COMMAND = re.compile(r"mise (?:-C (\S+) )?run ([\w:-]+)(?: |$)")
LIMIT = re.compile(
    r"`(?P<name>[A-Za-z_$][\w$]*)` \((?P<value>\d[\d,_]*(?:\.\d+)?)(?: (?P<unit>[a-z]+))?\)"
)
LISTED_NAME = re.compile(r"^- `([a-z][a-z0-9-]*)`", re.MULTILINE)
NUMBERED_FOLDER = re.compile(r"\d+-(?P<name>.+)")
NAME_EDGE = r"[\w.@/-]"
"""The characters that continue a file or package name."""
KEBAB_EDGE = r"[\w-]"
"""The characters that continue a kebab-case name, which a dot, a slash, or a colon ends."""


class NamesRejected(ValueError):
    """A checked document gives a name that no longer exists, or a limit that changed."""


@dataclass(frozen=True, kw_only=True)
class Repository:
    """What a document may name: the files under the root, the code, declared names, and tasks."""

    root: Path
    bases: tuple[Path, ...]
    paths: tuple[str, ...]
    code: str
    words: frozenset[str]
    names: frozenset[str]
    tasks: dict[str, frozenset[str]]


def list_files(*, source: Path) -> list[Path]:
    """List every file under a folder, or the file itself, outside the skipped folders."""
    if source.is_file():
        return [source]

    files: list[Path] = []
    for folder, folders, names in source.walk():
        folders[:] = sorted(name for name in folders if name not in SKIPPED_FOLDERS)
        files.extend(folder / name for name in sorted(names) if (folder / name).is_file())
    return files


def read_rule_ids(*, folders: list[Path]) -> set[str]:
    """Read the id of every structural lint rule and utility under the folders."""
    return {
        str(name)
        for folder in folders
        for path in list_files(source=folder)
        if path.suffix == RULE_SUFFIX
        for name in RULE_ID.findall(path.read_text(encoding="utf-8"))
    }


def read_lint_rules(*, command: str) -> set[str]:
    """Read every rule the lint lists, alone and after its plugin, such as `plugin/no-shadow`."""
    listing = subprocess.run(
        [command, "--rules", "-f", "json"], check=True, capture_output=True, text=True
    )

    return {
        str(name)
        for rule in json.loads(listing.stdout)
        for name in (rule["value"], f"{rule['scope'].replace('_', '-')}/{rule['value']}")
    }


def read_installed_names(*, lock: Path) -> set[str]:
    """Read the name of each contract and skill that the lock installs."""
    installed = json.loads(lock.read_text(encoding="utf-8"))

    return {
        *(str(entry["contract"]) for entry in installed["contracts"].values()),
        *(str(entry["skill"]) for entry in installed["skills"].values()),
    }


def read_contract_names(*, folders: list[Path]) -> set[str]:
    """Read each contract folder's name, without the number an adopted folder starts with."""
    names = [path.parent.name for folder in folders for path in folder.glob("*/CONTRACT.md")]

    return {
        numbered["name"] if (numbered := NUMBERED_FOLDER.fullmatch(name)) else name
        for name in names
    }


def _read_task_names(*, source: Path) -> frozenset[str]:
    if source.is_dir():
        return frozenset(
            path.relative_to(source).as_posix().replace("/", ":")
            for path in list_files(source=source)
        )

    document = tomllib.loads(source.read_text(encoding="utf-8"))

    return frozenset(str(name) for name in document.get("tasks", {}))


def read_tasks(*, root: Path, pairs: list[str]) -> dict[str, frozenset[str]]:
    """Read the tasks of each `<folder>=<source>` pair, keyed by the folder a command names."""
    tasks: dict[str, frozenset[str]] = {}
    for pair in pairs:
        folder, separator, source = pair.partition(PAIR_SEPARATOR)
        if not separator:
            message = f"read tasks {pair!r}: write the folder, `=`, and its task file or folder"
            raise NamesRejected(message)
        key = PurePosixPath(folder).as_posix()
        tasks[key] = tasks.get(key, frozenset()) | _read_task_names(source=root / source)
    return tasks


def read_code(*, root: Path, sources: list[str], uncounted_folders: frozenset[str]) -> str:
    """Read every source file but documents and files under an uncounted folder."""
    return "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for source in sources
        for path in list_files(source=root / source)
        if path.suffix != DOCUMENT_SUFFIX
        and not uncounted_folders.intersection(path.relative_to(root).parts)
    )


def _is_name_in(*, name: str, text: str, edge: str) -> bool:
    escaped = re.escape(name)

    return re.search(rf"{escaped}(?<!{edge}{escaped})(?!{edge})", text) is not None


def _list_named_files(*, repository: Repository, document: Path, name: str) -> list[Path]:
    if PATH_SEPARATOR not in name:
        return [
            repository.root / path for path in repository.paths if PurePosixPath(path).name == name
        ]

    folders = (repository.root, document.parent, *repository.bases)

    return [folder / name for folder in folders if (folder / name).is_file()]


def _describe_path(*, repository: Repository, document: Path, token: str) -> str | None:
    name = FILE_PATH.fullmatch(token)
    if name is None:
        return None

    is_stored = PATH_SEPARATOR not in name[1] and _is_name_in(
        name=name[1], text=repository.code, edge=NAME_EDGE
    )
    is_named = bool(_list_named_files(repository=repository, document=document, name=name[1]))

    return None if is_named or is_stored else f"`{token}` names no file"


def _describe_task(*, repository: Repository, token: str) -> str | None:
    command = COMMAND.match(token)
    if command is None:
        return None

    folder = PurePosixPath(command[1] or ROOT_FOLDER).as_posix()
    if folder not in repository.tasks:
        return f"`{token}` names the folder `{folder}`, whose tasks `--tasks` does not declare"

    is_task = command[2] in repository.tasks[folder]

    return None if is_task else f"`{command[2]}` is no task of the folder `{folder}`"


def _describe_kebab_name(*, repository: Repository, token: str) -> str | None:
    is_path_run = any(f"/{token}/" in f"/{path}/" for path in repository.paths)
    is_named = (
        token in repository.names
        or is_path_run
        or _is_name_in(name=token, text=repository.code, edge=KEBAB_EDGE)
    )

    return None if is_named else f"`{token}` names no rule, task, contract, skill, path or code"


def _describe_identifier(*, repository: Repository, token: str) -> str | None:
    call = CALL.match(token)
    identifier = call[1] if call else token
    if not IDENTIFIER.fullmatch(identifier):
        return None

    missing = [
        part
        for part in identifier.split(".")
        if CODE_NAME.search(part) and part not in repository.words
    ]

    return f"`{'`, `'.join(missing)}` appears in no code" if missing else None


def describe_missing_name(*, repository: Repository, document: Path, token: str) -> str | None:
    """Describe a code span's name that no longer exists, or give None for any other span."""
    if FILE_PATH.fullmatch(token):
        return _describe_path(repository=repository, document=document, token=token)
    if PACKAGE.fullmatch(token):
        is_named = _is_name_in(name=token, text=repository.code, edge=NAME_EDGE)
        return None if is_named else f"`{token}` names no package"
    if COMMAND.match(token):
        return _describe_task(repository=repository, token=token)
    if KEBAB_NAME.fullmatch(token):
        return _describe_kebab_name(repository=repository, token=token)
    return _describe_identifier(repository=repository, token=token)


def describe_name_outside_file(
    *, repository: Repository, document: Path, name: str, token: str
) -> str | None:
    """Describe a name that is no word of the file its path names, or give None."""
    path = FILE_PATH.fullmatch(token)
    if not IDENTIFIER.fullmatch(name) or FILE_PATH.fullmatch(name) or path is None:
        return None

    named = _list_named_files(repository=repository, document=document, name=path[1])
    first = name.split(".", maxsplit=1)[0]
    is_named = not named or any(
        first in WORD.findall(file.read_text(encoding="utf-8")) for file in named
    )

    return None if is_named else f"`{name}` is not in `{token}`"


def _read_assigned_values(*, code: str, name: str) -> list[tuple[Decimal, str]]:
    escaped = re.escape(name)
    assigned = re.findall(
        rf"{escaped}(?<![\w$.]{escaped})['\"]?\s*(?:(?::[^=\n]*)?=|:)\s*"
        r"(?:([\w$.]+)\()?(\d[\d_]*(?:\.\d+)?)\b",
        code,
    )

    return list(
        dict.fromkeys(
            (Decimal(number.replace("_", "")), call.rpartition(".")[2]) for call, number in assigned
        )
    )


def describe_changed_limit(
    *, repository: Repository, name: str, value: str, unit: str | None
) -> str | None:
    """Describe a restated limit whose constant holds another value, or several, or give None."""
    values = _read_assigned_values(code=repository.code, name=name)
    stated = Decimal(re.sub(r"[,_]", "", value))
    found = ", ".join(f"{number} {call}".strip() for number, call in values) or "no number"
    if len(values) > 1:
        return f"`{name}` has several values in the code ({found}); restate one constant"

    is_held = any(
        number == stated and (unit is None or not call or call == unit) for number, call in values
    )
    shown = f"{value} {unit}" if unit is not None else value

    return None if is_held else f"`{name}` is {found} in the code, not {shown}"


def inspect_document(*, repository: Repository, document: Path, is_whole: bool) -> list[str]:
    """List each name and limit of a document's checked text that no longer holds."""
    text = document.read_text(encoding="utf-8")
    spans = [(match.start(1), match[1]) for match in ADAPTATIONS.finditer(text)]
    checks: list[tuple[re.Pattern[str], Callable[[re.Match[str]], str | None]]] = [
        (
            INLINE_CODE,
            lambda match: describe_missing_name(
                repository=repository, document=document, token=match[2]
            ),
        ),
        (
            NAME_IN_FILE,
            lambda match: describe_name_outside_file(
                repository=repository, document=document, **match.groupdict()
            ),
        ),
        (LIMIT, lambda match: describe_changed_limit(repository=repository, **match.groupdict())),
    ]
    found = sorted(
        (text.count("\n", 0, start + match.start()) + 1, problem)
        for start, span in ([(0, text)] if is_whole else spans)
        for pattern, describe in checks
        for match in pattern.finditer(span)
        if (problem := describe(match)) is not None
    )

    return list(dict.fromkeys(f"{document}:{line}: {problem}" for line, problem in found))


def _add_source_arguments(*, parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", required=True, help="repository root that holds every path")
    parser.add_argument(
        "--code", nargs="+", required=True, help="each source file or folder under the root"
    )
    parser.add_argument(
        "--base", nargs="+", default=[], help="each folder a path may also start from"
    )
    parser.add_argument(
        "--uncounted", nargs="+", default=[], help="each folder name whose files are no code"
    )
    parser.add_argument("--whole", nargs="+", default=[], help="each document checked whole")
    parser.add_argument(
        "--adapted", nargs="+", default=[], help="each contract checked under its adaptations"
    )


def _add_name_arguments(*, parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--rules", nargs="+", default=[], help="each folder whose structural lint rules give ids"
    )
    parser.add_argument("--lint", help="the lint executable that lists its rules as JSON")
    parser.add_argument(
        "--tasks", nargs="+", default=[], help="each `<folder>=<task file or folder>` pair"
    )
    parser.add_argument("--lock", help="the lock that names each installed contract and skill")
    parser.add_argument("--names", nargs="+", default=[], help="each file that lists names")
    parser.add_argument("--contracts", nargs="+", default=[], help="each folder of contracts")


def _read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    _add_source_arguments(parser=parser)
    _add_name_arguments(parser=parser)
    return parser.parse_args()


def read_names(*, root: Path, arguments: argparse.Namespace) -> frozenset[str]:
    """Read the kebab-case names that the rules, the lint, the lock, and the lists declare."""
    listed = (
        LISTED_NAME.findall((root / path).read_text(encoding="utf-8")) for path in arguments.names
    )

    return frozenset({
        *read_rule_ids(folders=[root / folder for folder in arguments.rules]),
        *(read_lint_rules(command=arguments.lint) if arguments.lint else ()),
        *(read_installed_names(lock=root / arguments.lock) if arguments.lock else ()),
        *read_contract_names(folders=[root / folder for folder in arguments.contracts]),
        *(str(name) for names in listed for name in names),
    })


def read_repository(*, arguments: argparse.Namespace) -> Repository:
    """Read what the documents may name from the root and the declared sources."""
    root = Path(arguments.root).resolve()
    tasks = read_tasks(root=root, pairs=arguments.tasks)
    code = read_code(
        root=root, sources=arguments.code, uncounted_folders=frozenset(arguments.uncounted)
    )

    return Repository(
        root=root,
        bases=tuple(root / base for base in arguments.base),
        paths=tuple(path.relative_to(root).as_posix() for path in list_files(source=root)),
        code=code,
        words=frozenset(WORD.findall(code)),
        names=read_names(root=root, arguments=arguments).union(*tasks.values()),
        tasks=tasks,
    )


def main() -> None:
    """Check every named document without changing any file."""
    arguments = _read_arguments()
    repository = read_repository(arguments=arguments)
    documents = [
        *((Path(path).resolve(), True) for path in arguments.whole),
        *((Path(path).resolve(), False) for path in arguments.adapted),
    ]
    errors = [
        error
        for document, is_whole in documents
        for error in inspect_document(repository=repository, document=document, is_whole=is_whole)
    ]
    if errors:
        raise NamesRejected("\n".join(errors))


if __name__ == "__main__":
    main()
