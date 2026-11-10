#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Run passing and failing example workspaces against the shipped tool configuration checker."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

GUIDANCE_PARENT_DEPTH = 3
CHECKER_PATH = "contracts/code-tool-configuration-folder/assets/uv/check-tool-configuration.py"
CASE_TIMEOUT_SECONDS = 60
OUTPUT_CHARACTER_LIMIT = 6000
CHECKER_ARGUMENTS = ("--config", ".config/tool-configuration.json")


@dataclass(frozen=True, kw_only=True)
class Case:
    """One workspace as its changes to the passing files, with the diagnostic it must produce."""

    name: str
    files: tuple[tuple[str, str], ...] = ()
    removed: tuple[str, ...] = ()
    diagnostic: str = ""


POLICY = """{
  "commandFiles": [".config/tasks.toml", ".config/hooks/*", "workflows/*.yml"],
  "configurationFolder": ".config",
  "generatedEntries": [{"name": "node_modules", "reason": "Installed dependencies."}],
  "rootEntries": [".config", ".gitignore", "package.json", "packages", "workflows"],
  "sharedSettings": ["compiler.json"],
  "tools": [{"command": "lint-orders", "flags": ["--config", "-c"]}]
}
"""
TASKS = """[tools]
"registry:lint-orders" = "1.0.0"

[tasks.lint]
description = "Run lint-orders on every package"
run = "lint-orders --config .config/lint-orders.json packages"

[tasks.versions]
run = "lint-orders --version"
"""
WORKFLOW = """jobs:
  check:
    steps:
      - name: Run lint-orders
        run: |
          node_modules/.bin/lint-orders \\
            -c=.config/lint-orders.json packages
"""
PASSING_FILES = (
    (".config/tool-configuration.json", POLICY),
    (".config/tasks.toml", TASKS),
    (".config/hooks/lint-edit.sh", '#!/bin/sh\nlint-orders -c .config/lint-orders.json "$1"\n'),
    (".config/lint-orders.json", "{}\n"),
    (".gitignore", "node_modules\n"),
    ("node_modules/lint-orders/compiler.json", "{}\n"),
    ("package.json", "{}\n"),
    ("packages/compiler.json", "{}\n"),
    ("packages/orders/index.ts", "export const total = 1;\n"),
    ("workflows/check.yml", WORKFLOW),
)
CASES = (
    Case(name="settings-stay-in-the-configuration-folder"),
    Case(
        name="unlisted-root-entry-is-rejected",
        files=(("lint-orders.json", "{}\n"),),
        diagnostic="check root entry 'lint-orders.json'",
    ),
    Case(
        name="task-passes-the-settings-path",
        files=((".config/tasks.toml", TASKS.replace(" --config .config/lint-orders.json", "")),),
        diagnostic="check tool call .config/tasks.toml:6: pass 'lint-orders' its settings",
    ),
    Case(
        name="hook-passes-the-settings-path",
        files=((".config/hooks/lint-edit.sh", '#!/bin/sh\nlint-orders "$1"\n'),),
        diagnostic="check tool call .config/hooks/lint-edit.sh:2: pass 'lint-orders' its settings",
    ),
    Case(
        name="workflow-passes-the-settings-path",
        files=(("workflows/check.yml", WORKFLOW.replace("-c=.config/lint-orders.json ", "")),),
        diagnostic="check tool call workflows/check.yml:7: pass 'lint-orders' its settings",
    ),
    Case(
        name="settings-path-stays-in-the-folder",
        files=(
            (".config/tasks.toml", TASKS.replace(".config/lint-orders.json", "lint-orders.json")),
        ),
        diagnostic="'lint-orders' reads 'lint-orders.json', which is outside '.config'",
    ),
    Case(
        name="package-settings-below-shared-settings-are-rejected",
        files=(("packages/orders/compiler.json", "{}\n"),),
        diagnostic="check settings file 'packages/orders/compiler.json': 'packages' already holds",
    ),
    Case(
        name="unknown-policy-field-is-rejected",
        files=(
            (
                ".config/tool-configuration.json",
                POLICY.replace("{\n", '{\n  "strict": false,\n', 1),
            ),
        ),
        diagnostic="read configuration policy",
    ),
)


def _write_workspace(*, root: Path, case: Case) -> None:
    files = {**dict(PASSING_FILES), **dict(case.files)}
    for relative, content in files.items():
        if relative in case.removed:
            continue
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _inspect_result(*, case: Case, result: subprocess.CompletedProcess[str]) -> None:
    is_success = result.returncode == 0
    is_expected = is_success and case.diagnostic == ""
    if case.diagnostic:
        is_expected = not is_success and case.diagnostic in result.stderr

    if is_expected:
        return

    output = (result.stdout + result.stderr)[-OUTPUT_CHARACTER_LIMIT:]
    message = (
        f"check tool configuration case {case.name!r}: expected diagnostic {case.diagnostic!r}, "
        f"received exit {result.returncode!r} with output {output!r}"
    )
    raise AssertionError(message)


def _check_case(*, checker: Path, case: Case) -> None:
    with TemporaryDirectory(prefix=f"check-tool-configuration-{case.name}-") as temporary:
        root = Path(temporary)
        _write_workspace(root=root, case=case)
        arguments = ["uv", "run", "--script", str(checker), "--root", str(root)]
        result = subprocess.run(
            [*arguments, *CHECKER_ARGUMENTS],
            capture_output=True,
            check=False,
            text=True,
            timeout=CASE_TIMEOUT_SECONDS,
        )
        _inspect_result(case=case, result=result)


def main() -> None:
    """Run the shipped checker on the passing workspace and on each workspace that must fail."""
    guidance = Path(__file__).resolve().parents[GUIDANCE_PARENT_DEPTH]

    for case in CASES:
        _check_case(checker=guidance / CHECKER_PATH, case=case)


if __name__ == "__main__":
    main()
