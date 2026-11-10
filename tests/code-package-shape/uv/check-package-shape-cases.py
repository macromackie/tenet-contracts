#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Run passing and failing example workspaces against the shipped package shape checker."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

GUIDANCE_PARENT_DEPTH = 3
CHECKER_PATH = "contracts/code-package-shape/assets/uv/check-package-shape.py"
CASE_TIMEOUT_SECONDS = 60
OUTPUT_CHARACTER_LIMIT = 6000
CHECKER_ARGUMENTS = ("--config", ".config/package-shape.json")


@dataclass(frozen=True, kw_only=True)
class Case:
    """One workspace as its changes to the passing files, with the diagnostic it must produce."""

    name: str
    files: tuple[tuple[str, str], ...] = ()
    removed: tuple[str, ...] = ()
    diagnostic: str = ""


POLICY = """{
  "deployEntries": [
    {"package": "packages/orders", "name": "deploy.json", "reason": "The host reads it here."}
  ],
  "entryFiles": ["index.ts", "main.ts"],
  "generatedEntries": [{"name": "node_modules", "reason": "Installed dependencies."}],
  "manifest": "package.json",
  "maximumFlatModules": 3,
  "packagePatterns": ["packages/*"],
  "roleFiles": ["errors.ts"],
  "sourceFolder": "src"
}
"""
MODULE = "export const total = 1;\n"
PASSING_FILES = (
    (".config/package-shape.json", POLICY),
    ("packages/orders/README.md", "# @fixture/orders\n"),
    ("packages/orders/package.json", '{"name": "@fixture/orders"}\n'),
    ("packages/orders/deploy.json", "{}\n"),
    ("packages/orders/node_modules/dependency/index.js", "\n"),
    ("packages/orders/src/index.ts", MODULE),
    ("packages/orders/src/errors.ts", MODULE),
    ("packages/orders/src/totals/read-total.ts", MODULE),
    ("packages/invoices/README.md", "# invoices\n"),
    ("packages/invoices/package.json", '{"name": "invoices"}\n'),
    ("packages/invoices/src/index.ts", MODULE),
    ("packages/invoices/src/issue-number.ts", MODULE),
    ("packages/invoices/src/void-number.ts", MODULE),
)
CASES = (
    Case(name="packages-keep-the-declared-shape"),
    Case(
        name="package-root-holds-no-other-entry",
        files=(("packages/invoices/compiler.json", "{}\n"),),
        diagnostic="check package 'packages/invoices': move 'compiler.json' out of the package",
    ),
    Case(
        name="deploy-entry-is-declared-per-package",
        files=(("packages/invoices/deploy.json", "{}\n"),),
        diagnostic="check package 'packages/invoices': move 'deploy.json' out of the package root",
    ),
    Case(
        name="package-root-holds-a-readme",
        removed=("packages/invoices/README.md",),
        diagnostic="check package 'packages/invoices': add 'README.md' to the package root",
    ),
    Case(
        name="loose-module-beside-folders-is-rejected",
        files=(("packages/orders/src/read-tax.ts", MODULE),),
        diagnostic="check source root 'packages/orders/src': move 'read-tax.ts' into a folder",
    ),
    Case(
        name="flat-source-root-stays-within-its-limit",
        files=(("packages/invoices/src/read-number.ts", MODULE),),
        diagnostic="check source root 'packages/invoices/src': 4 modules exceeds 3",
    ),
    Case(
        name="folder-is-named-for-the-package",
        files=(("packages/invoices/package.json", '{"name": "@fixture/billing"}\n'),),
        diagnostic="check package 'packages/invoices': name the folder 'billing'",
    ),
    Case(
        name="unknown-policy-field-is-rejected",
        files=(
            (".config/package-shape.json", POLICY.replace("{\n", '{\n  "strict": false,\n', 1)),
        ),
        diagnostic="read shape policy",
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
        f"check package shape case {case.name!r}: expected diagnostic {case.diagnostic!r}, "
        f"received exit {result.returncode!r} with output {output!r}"
    )
    raise AssertionError(message)


def _check_case(*, checker: Path, case: Case) -> None:
    with TemporaryDirectory(prefix=f"check-package-shape-{case.name}-") as temporary:
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
