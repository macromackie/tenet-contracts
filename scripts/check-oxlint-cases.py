#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Exercise every shipped Oxlint fragment with rejected and accepted source files."""

import json
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import output

ROOT = Path(__file__).resolve().parent.parent
"""The library whose installed dependencies and shipped fragments the cases exercise."""
PARENT_PART = ".."
"""The path component that would leave a fixture project."""
RESERVED_PATH_PARTS = frozenset({"node_modules", "oxlint.json", "tsconfig.json"})
"""Path components owned by the runner, including its shared dependency symlink."""
SETTINGS_KEY = "settings"
"""The Oxlint settings key consumers copy because extends does not inherit it."""
CHECK_WORKERS = 4
"""Maximum independent fragment checks, each with one Oxlint worker thread."""
ASSETS = "contracts/*/assets/oxlint/*.json"
"""Every shipped Oxlint fragment, including optional runner-specific fragments."""
PLUGINS = (
    "eslint",
    "typescript",
    "unicorn",
    "oxc",
    "import",
    "jsdoc",
    "promise",
    "node",
    "react",
    "react-perf",
    "jsx-a11y",
    "vitest",
)
"""Built-in plugins whose names the fragments configure without repeating installation."""


@dataclass(frozen=True)
class Fixture:
    """A fragment's source path, expected rule, accepted code, rejected code, and modules."""

    filename: str
    rule: str
    valid: str
    invalid: str
    files: dict[str, str]


def read_relative_path(*, value: str, path: Path) -> str:
    """Reject fixture paths that leave the scratch source project."""
    target = Path(value)

    if target.is_absolute() or PARENT_PART in target.parts:
        message = f"{path}: source path leaves the scratch project: {value}"
        raise ValueError(message)

    if any(part.casefold() in RESERVED_PATH_PARTS for part in target.parts):
        message = f"{path}: source path names a runner-owned file or dependency: {value}"
        raise ValueError(message)

    return value


def check_source_paths(*, filename: str, files: dict[str, str], path: Path) -> None:
    """Require distinct source and companion paths on case-insensitive filesystems."""
    source_names: dict[str, str] = {}

    for name in (filename, *files):
        target = str(Path(name)).casefold()

        if target in source_names:
            message = f"{path}: source paths share a target: {source_names[target]} and {name}"
            raise ValueError(message)

        source_names[target] = name


def read_source_entry(*, name: object, content: object, path: Path) -> tuple[str, str]:
    """Validate the path and text of one companion source file."""
    if not isinstance(name, str) or not isinstance(content, str):
        message = f"{path}: files must map relative paths to source strings"
        raise TypeError(message)

    return (read_relative_path(value=name, path=path), content)


def read_files(*, value: object, path: Path) -> dict[str, str]:
    """Read companion modules confined to the scratch source project."""
    if not isinstance(value, dict):
        message = f"{path}: files must map relative paths to source strings"
        raise TypeError(message)

    return dict(
        read_source_entry(name=name, content=content, path=path) for name, content in value.items()
    )


def read_fixture(*, path: Path) -> Fixture:
    """Decode required source fields and optional companion modules."""
    document: object = json.loads(path.read_text(encoding="utf-8"))

    match document:
        case {
            "filename": str() as filename,
            "rule": str() as rule,
            "valid": str() as valid,
            "invalid": str() as invalid,
        }:
            files = read_files(value=document.get("files", {}), path=path)
            selected = read_relative_path(value=filename, path=path)
            check_source_paths(filename=selected, files=files, path=path)

            return Fixture(filename=selected, rule=rule, valid=valid, invalid=invalid, files=files)
        case _:
            message = f"{path}: supply filename, rule, valid, and invalid strings"
            raise ValueError(message)


def read_diagnostic(*, value: object, path: Path) -> str:
    """Read the stable rule identifier on one Oxlint diagnostic."""
    match value:
        case {"code": str() as code}:
            return code
        case _:
            message = f"{path}: diagnostic has no rule code"
            raise ValueError(message)


def read_diagnostics(*, text: str, path: Path) -> list[str]:
    """Read stable rule identifiers instead of diagnostic wording."""
    document: object = json.loads(text)

    match document:
        case {"diagnostics": list() as diagnostics}:
            return [read_diagnostic(value=value, path=path) for value in diagnostics]
        case _:
            message = f"{path}: Oxlint returned no diagnostic array"
            raise ValueError(message)


def read_config(*, asset: Path) -> dict[str, object]:
    """Extend a fragment and copy settings that Oxlint does not inherit."""
    document = json.loads(
        re.sub(r"^\s*//.*$", "", asset.read_text(encoding="utf-8"), flags=re.MULTILINE)
    )
    config: dict[str, object] = {"extends": [str(asset)], "plugins": list(PLUGINS)}

    if SETTINGS_KEY in document:
        config[SETTINGS_KEY] = document[SETTINGS_KEY]

    return config


def write_source(*, project: Path, name: str, content: str) -> Path:
    """Write one fixture module and create its owning folder."""
    target = project / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    return target


def write_project(*, project: Path, asset: Path, fixture: Fixture) -> None:
    """Use ordinary source paths so test-directory exemptions cannot hide violations."""
    options = {
        "jsx": "preserve",
        "module": "ESNext",
        "moduleResolution": "bundler",
        "noEmit": True,
        "strict": True,
        "target": "ES2024",
    }
    (project / "oxlint.json").write_text(json.dumps(read_config(asset=asset)), encoding="utf-8")
    (project / "tsconfig.json").write_text(
        json.dumps({"compilerOptions": options, "include": ["**/*.ts", "**/*.tsx", "**/*.mts"]}),
        encoding="utf-8",
    )
    (project / "node_modules").symlink_to(ROOT / "node_modules", target_is_directory=True)

    for name, content in fixture.files.items():
        write_source(project=project, name=name, content=content)


def check_source(*, project: Path, fixture: Fixture, source: str) -> list[str]:
    """Run the installed Oxlint with the unchanged shipped fragment."""
    target = write_source(project=project, name=fixture.filename, content=source)
    command = (
        str(ROOT / "node_modules/.bin/oxlint"),
        "--format=json",
        "--threads=1",
        "--deny-warnings",
        "--type-aware",
        "--config",
        str(project / "oxlint.json"),
        str(target),
    )
    process = subprocess.run(command, check=False, cwd=project, capture_output=True, text=True)

    if process.returncode not in {0, 1}:
        message = f"{fixture.filename}: Oxlint failed: {process.stderr}"
        raise RuntimeError(message)

    return read_diagnostics(text=process.stdout, path=target)


def check_fixture(*, asset: Path, path: Path) -> list[str]:
    """Require clean accepted code and the named diagnostic on rejected code."""
    fixture = read_fixture(path=path)

    with tempfile.TemporaryDirectory(prefix="oxlint-case-") as temporary:
        project = Path(temporary)
        write_project(project=project, asset=asset, fixture=fixture)
        valid = check_source(project=project, fixture=fixture, source=fixture.valid)
        invalid = check_source(project=project, fixture=fixture, source=fixture.invalid)

    return compare_diagnostics(path=path, fixture=fixture, valid=valid, invalid=invalid)


def compare_diagnostics(
    *, path: Path, fixture: Fixture, valid: list[str], invalid: list[str]
) -> list[str]:
    """Explain which accepted or rejected guarantee a case failed."""
    errors = []

    if valid:
        errors.append(f"{path.relative_to(ROOT)}: accepted code reports {', '.join(valid)}")

    if fixture.rule not in invalid:
        errors.append(
            f"{path.relative_to(ROOT)}: rejected code must report {fixture.rule}; got {invalid}"
        )

    return errors


def compare_inventory(*, expected_cases: dict[Path, Path], actual_paths: set[Path]) -> list[str]:
    """Find fragments without cases and cases without a shipped fragment."""
    return [
        *(
            f"{path.relative_to(ROOT)}: add a violation and allowed case"
            for path in expected_cases.keys() - actual_paths
        ),
        *(
            f"{path.relative_to(ROOT)}: no shipped fragment owns this case"
            for path in actual_paths - expected_cases.keys()
        ),
    ]


def check_available(*, expected_cases: dict[Path, Path], actual_paths: set[Path]) -> list[str]:
    """Check independent fragments concurrently and join every subprocess before returning."""
    with ThreadPoolExecutor(max_workers=CHECK_WORKERS) as executor:
        checks = [
            executor.submit(check_fixture, asset=asset, path=path)
            for path, asset in expected_cases.items()
            if path in actual_paths
        ]

        return [error for check in checks for error in check.result()]


def main() -> None:
    """Refuse missing or orphaned cases, then exercise every shipped fragment."""
    expected_cases = {
        ROOT / "tests" / asset.parts[-4] / "oxlint" / asset.name: asset
        for asset in sorted(ROOT.glob(ASSETS))
    }
    actual_paths = set(ROOT.glob("tests/*/oxlint/*.json"))
    errors = compare_inventory(expected_cases=expected_cases, actual_paths=actual_paths)

    errors.extend(check_available(expected_cases=expected_cases, actual_paths=actual_paths))

    output.report_findings(lines=errors)

    if errors:
        output.finish(status=output.ExitStatus.INVALID)

    output.report_summary(
        line=f"All {len(expected_cases)} Oxlint fragments reject and accept their cases"
    )


if __name__ == "__main__":
    main()
