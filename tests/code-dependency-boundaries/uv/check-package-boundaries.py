#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Run isolated system examples against the shipped package-boundary checker."""

import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

from constants import (
    CHECKER_PATH,
    FIXTURE_TIMEOUT_SECONDS,
    GUIDANCE_PARENT_DEPTH,
    MEMBERS,
    OUTPUT_CHARACTER_LIMIT,
    PROJECTION_PATH,
    SUPPORT_MANIFEST,
)
from read_fixtures import read_fixtures

if TYPE_CHECKING:
    from model import Fixture


def _read_package_policy(*, fixture: Fixture, manifest: str, name: str) -> dict[str, object]:
    is_test_support = manifest == SUPPORT_MANIFEST and fixture.is_test_support

    return {
        "builtins": [],
        "dependencies": [
            {"manifest": target, "testOnly": is_test_only}
            for source, target, is_test_only in fixture.declarations
            if source == manifest
        ],
        "manager": "npm",
        "manifest": manifest,
        "name": f"@fixture/{name}",
        "ownership": f"Owns fixture {name} behavior.",
        "testSources": ["tests/**"],
        "testSupport": is_test_support,
        "tsconfig": "",
    }


def _write_policy(*, root: Path, fixture: Fixture) -> None:
    policy: dict[str, object] = {
        "exclusions": [{"pattern": "**/node_modules/**", "reason": "Installed workspace links."}],
        "packages": [
            _read_package_policy(fixture=fixture, manifest=manifest, name=name)
            for manifest, name in MEMBERS
        ],
    }
    if fixture.has_unknown_policy_field:
        policy["allowUnknownPackages"] = True

    (root / "policy.json").write_text(json.dumps(policy), encoding="utf-8")


def _write_source_rules(*, root: Path) -> None:
    rules = {
        "forbidden": [
            {
                "from": {},
                "name": "acyclic-source-imports",
                "severity": "error",
                "to": {"circular": True},
            },
        ],
    }

    (root / "source-rules.json").write_text(json.dumps(rules), encoding="utf-8")


def _write_workspace(*, root: Path, fixture: Fixture) -> None:
    for relative, content in fixture.files:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    links = root / "node_modules/@fixture"
    links.mkdir(parents=True)

    for manifest, name in MEMBERS:
        (links / name).symlink_to((root / manifest).parent, target_is_directory=True)

    _write_policy(root=root, fixture=fixture)
    _write_source_rules(root=root)


def _inspect_result(*, fixture: Fixture, result: subprocess.CompletedProcess[str]) -> None:
    is_success = result.returncode == 0
    is_expected = is_success and fixture.diagnostic == ""
    if fixture.diagnostic:
        is_expected = not is_success and fixture.diagnostic in result.stderr

    if is_expected:
        return

    output = (result.stdout + result.stderr)[-OUTPUT_CHARACTER_LIMIT:]
    message = (
        f"check package fixture {fixture.name!r}: expected diagnostic {fixture.diagnostic!r}, "
        f"received exit {result.returncode!r} with output {output!r}"
    )
    raise AssertionError(message)


def _write_stale_projection(*, root: Path) -> None:
    path = root / PROJECTION_PATH
    value: object = json.loads(path.read_text(encoding="utf-8"))
    match value:
        case {"packages": [dict() as package]}:
            package["ownership"] = "Owns independently edited package behavior."
        case _:
            message = f"mutate package projection {str(path)!r}: expected one projected package"
            raise AssertionError(message)

    path.write_text(json.dumps(value), encoding="utf-8")


def _prepare_projection(*, arguments: list[str], root: Path, fixture: Fixture) -> None:
    arguments.extend(["--verify-projection", PROJECTION_PATH])
    subprocess.run(
        [*arguments, "--update-projection"],
        capture_output=True,
        check=True,
        text=True,
        timeout=FIXTURE_TIMEOUT_SECONDS,
    )
    if fixture.is_projection_stale:
        _write_stale_projection(root=root)


def _check_fixture(*, checker: Path, fixture: Fixture) -> None:
    with TemporaryDirectory(prefix=f"package-boundaries-{fixture.name}-") as temporary:
        root = Path(temporary)
        _write_workspace(root=root, fixture=fixture)
        arguments = [
            "uv",
            "run",
            "--script",
            str(checker),
            "--root",
            str(root),
            "--config",
            "policy.json",
        ]
        if fixture.has_source_rules:
            arguments.extend(["--source-rules", "source-rules.json"])
        if fixture.has_projection:
            _prepare_projection(arguments=arguments, root=root, fixture=fixture)

        result = subprocess.run(
            arguments,
            capture_output=True,
            check=False,
            text=True,
            timeout=FIXTURE_TIMEOUT_SECONDS,
        )
        _inspect_result(fixture=fixture, result=result)


def main() -> None:
    """Exercise real package discovery, manifest evidence, source edges, and optional rules."""
    guidance = Path(__file__).resolve().parents[GUIDANCE_PARENT_DEPTH]

    for fixture in read_fixtures():
        _check_fixture(checker=guidance / CHECKER_PATH, fixture=fixture)


if __name__ == "__main__":
    main()
