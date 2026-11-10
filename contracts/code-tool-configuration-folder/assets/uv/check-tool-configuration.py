#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Check a workspace's root entries, tool calls, and nested settings files against its policy."""

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

CONTINUATION = "\\"
WORD_PUNCTUATION = "\"',[](){};"
"""The quoting and list characters that surround a command's words in a task or workflow file."""
LABEL_PREFIXES = ("#", "//", "name:", "- name:", "description")
"""The starts of a comment line and of a line that labels a task or a step in prose."""
ASSIGNMENT_TOKENS = frozenset({"=", ":"})
INFORMATION_FLAGS = frozenset({"--version", "--help"})
"""The arguments that make a tool print its version or usage without reading any settings."""
VALUE_SEPARATOR = "="


class ConfigurationRejected(ValueError):
    """The policy is malformed, or the workspace breaks it."""


@dataclass(frozen=True, kw_only=True)
class Tool:
    """A command and the flags of which one must pass its settings path on every call."""

    command: str
    flags: tuple[str, ...]


@dataclass(frozen=True, kw_only=True)
class Policy:
    """The declared root entries, generated entries, tools, command files, and settings names."""

    folder: str
    root_entries: frozenset[str]
    generated_entries: frozenset[str]
    tools: tuple[Tool, ...]
    command_files: tuple[str, ...]
    shared_settings: frozenset[str]


# jscpd:ignore-start -- duplication -- Standalone checkers must carry their own policy readers.
def _read_name(*, value: object) -> str:
    if not isinstance(value, str) or not value.strip() or PurePosixPath(value).is_absolute():
        message = f"read configuration name {value!r}: expected a nonempty relative name"
        raise ConfigurationRejected(message)
    return value


def _read_generated_entry(*, value: object) -> str:
    match value:
        case {"name": str() as name, "reason": str() as reason, **unknown_fields} if (
            reason.strip() and not unknown_fields
        ):
            return _read_name(value=name)
        case _:
            message = f"read generated entry {value!r}: declare a name and its reason"
            raise ConfigurationRejected(message)


# jscpd:ignore-end


def _read_tool(*, value: object) -> Tool:
    match value:
        case {"command": str() as command, "flags": [*flags], **unknown_fields} if (
            flags and not unknown_fields
        ):
            return Tool(
                command=_read_name(value=command),
                flags=tuple(_read_name(value=flag) for flag in flags),
            )
        case _:
            message = f"read tool {value!r}: declare a command and the flags that pass its settings"
            raise ConfigurationRejected(message)


def read_policy(*, path: Path) -> Policy:
    """Require every list of the policy, and refuse a field that the policy does not define."""
    value: object = json.loads(path.read_text(encoding="utf-8"))
    match value:
        case {
            "configurationFolder": folder,
            "rootEntries": [*root_entries],
            "generatedEntries": [*generated_entries],
            "tools": [*tools],
            "commandFiles": [*command_files],
            "sharedSettings": [*shared_settings],
            **unknown_fields,
        } if root_entries and not unknown_fields:
            return Policy(
                folder=_read_name(value=folder),
                root_entries=frozenset(_read_name(value=entry) for entry in root_entries),
                generated_entries=frozenset(
                    _read_generated_entry(value=entry) for entry in generated_entries
                ),
                tools=tuple(_read_tool(value=tool) for tool in tools),
                command_files=tuple(_read_name(value=pattern) for pattern in command_files),
                shared_settings=frozenset(_read_name(value=name) for name in shared_settings),
            )
        case _:
            message = (
                f"read configuration policy {str(path)!r}: declare the configuration folder, "
                "the root entries, the generated entries, the tools, the command files, "
                "and the shared settings"
            )
            raise ConfigurationRejected(message)


def _check_root_entries(*, root: Path, policy: Policy) -> list[str]:
    allowed = policy.root_entries | policy.generated_entries
    return [
        f"check root entry {entry.name!r}: move it into {policy.folder!r} "
        "or declare it as an entry that its tool must find at the root"
        for entry in sorted(root.iterdir())
        if entry.name not in allowed
    ]


def _read_commands(*, text: str) -> list[tuple[int, list[str]]]:
    commands = []
    pending: list[str] = []
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith(LABEL_PREFIXES):
            continue
        tokens = [token.strip(WORD_PUNCTUATION) for token in stripped.split()]
        pending.extend(token for token in tokens if token and token != CONTINUATION)
        if not stripped.endswith(CONTINUATION):
            commands.append((number, pending))
            pending = []
    return commands


def _read_settings_path(*, tokens: list[str], tool: Tool) -> str | None:
    for index, token in enumerate(tokens):
        flag, separator, value = token.partition(VALUE_SEPARATOR)
        if flag in tool.flags and separator:
            return value
        if flag in tool.flags:
            return tokens[index + 1] if index + 1 < len(tokens) else ""
    return None


def _check_call(*, place: str, tokens: list[str], tool: Tool, folder: str) -> list[str]:
    settings = _read_settings_path(tokens=tokens, tool=tool)
    if settings is None:
        return [
            (
                f"check tool call {place}: pass {tool.command!r} its settings with "
                f"{' or '.join(tool.flags)}, so it never runs on its defaults"
            )
        ]
    if folder not in PurePosixPath(settings).parts:
        return [
            (
                f"check tool call {place}: {tool.command!r} reads {settings!r}, "
                f"which is outside {folder!r}"
            )
        ]
    return []


def _check_command(*, place: str, tokens: list[str], policy: Policy) -> list[str]:
    errors = []
    for index, token in enumerate(tokens):
        rest = tokens[index + 1 :]
        is_assigned = bool(rest) and rest[0] in ASSIGNMENT_TOKENS
        is_information = bool(rest) and rest[0] in INFORMATION_FLAGS
        if is_assigned or is_information:
            continue
        errors.extend(
            error
            for tool in policy.tools
            if PurePosixPath(token).name == tool.command
            for error in _check_call(place=place, tokens=tokens, tool=tool, folder=policy.folder)
        )
    return errors


def _check_command_files(*, root: Path, policy: Policy) -> list[str]:
    paths = sorted(
        path for pattern in policy.command_files for path in root.glob(pattern) if path.is_file()
    )
    return [
        error
        for path in paths
        for number, tokens in _read_commands(text=path.read_text(encoding="utf-8"))
        for error in _check_command(
            place=f"{path.relative_to(root).as_posix()}:{number}", tokens=tokens, policy=policy
        )
    ]


def _check_shared_settings(*, root: Path, policy: Policy) -> list[str]:
    holders: dict[str, list[Path]] = {}
    for folder, folder_names, file_names in os.walk(root):
        folder_names[:] = [name for name in folder_names if name not in policy.generated_entries]
        for name in policy.shared_settings.intersection(file_names):
            holders.setdefault(name, []).append(Path(folder))
    return [
        f"check settings file {(folder / name).relative_to(root).as_posix()!r}: "
        f"{ancestor.relative_to(root).as_posix()!r} already holds {name!r} for the folders below it"
        for name, folders in sorted(holders.items())
        for folder in sorted(folders)
        for ancestor in folders
        if ancestor in folder.parents
    ]


def inspect_configuration(*, root: Path, policy: Policy) -> list[str]:
    """Report each unlisted root entry, call without its settings, and nested settings file."""
    return [
        *_check_root_entries(root=root, policy=policy),
        *_check_command_files(root=root, policy=policy),
        *_check_shared_settings(root=root, policy=policy),
    ]


def main() -> None:
    """Check the workspace at the given root against its policy without changing any file."""
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
    errors = inspect_configuration(root=root, policy=policy)
    if errors:
        raise ConfigurationRejected("\n".join(errors))


if __name__ == "__main__":
    main()
