#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Run passing and failing example workspaces against the shipped package README checker."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

GUIDANCE_PARENT_DEPTH = 3
CHECKER_PATH = "contracts/docs-package-readme/assets/uv/check-package-readmes.py"
CASE_TIMEOUT_SECONDS = 60
OUTPUT_CHARACTER_LIMIT = 6000
CHECKER_ARGUMENTS: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class Case:
    """One workspace as its changes to the passing files, with the diagnostic it must produce."""

    name: str
    files: tuple[tuple[str, str], ...] = ()
    removed: tuple[str, ...] = ()
    diagnostic: str = ""


ORDERS_MANIFEST = '{"name": "@fixture/orders", "description": "Owns order totals."}\n'
INVOICES_MANIFEST = '{"name": "@fixture/invoices", "description": "Owns invoice numbers."}\n'
ORDERS_README = """# @fixture/orders

Owns order totals.

## Layout

- `src/totals/`: the modules that add up an order.

## Use

Import `readTotal` from the package.

## Never

- Never round a total before the last step.
"""
INVOICES_README = """# @fixture/invoices

Owns invoice numbers.

## Layout

- `src/`: the modules that issue a number.

## Use

Import `issueNumber` from the package.

## Never

- Never reuse a number.
"""
GROUP_README = """# billing

The packages that compute what a customer owes.

| Package             | Description           |
| ------------------- | --------------------- |
| `@fixture/invoices` | Owns invoice numbers. |
| `@fixture/orders`   | Owns order totals.    |
"""
PASSING_FILES = (
    ("pnpm-workspace.yaml", 'packages:\n  - "packages/*/*"\n'),
    ("packages/billing/README.md", GROUP_README),
    ("packages/billing/orders/package.json", ORDERS_MANIFEST),
    ("packages/billing/orders/README.md", ORDERS_README),
    ("packages/billing/orders/src/totals/read-total.ts", "export const total = 1;\n"),
    ("packages/billing/invoices/package.json", INVOICES_MANIFEST),
    ("packages/billing/invoices/README.md", INVOICES_README),
    ("packages/billing/invoices/src/issue-number.ts", "export const issued = 1;\n"),
)
CARGO_FILES = (
    ("Cargo.toml", '[workspace]\nmembers = ["packages/*/*"]\n'),
    (
        "packages/billing/orders/Cargo.toml",
        '[package]\nname = "@fixture/orders"\ndescription = "Owns order totals."\n',
    ),
    (
        "packages/billing/invoices/Cargo.toml",
        '[package]\nname = "@fixture/invoices"\ndescription = "Owns invoice numbers."\n',
    ),
)
CASES = (
    Case(name="every-readme-follows-its-form"),
    Case(
        name="toml-workspace-members-are-read",
        files=CARGO_FILES,
        removed=("pnpm-workspace.yaml",),
    ),
    Case(
        name="package-readme-is-required",
        removed=("packages/billing/orders/README.md",),
        diagnostic="check README 'packages/billing/orders/README.md': file does not exist",
    ),
    Case(
        name="group-readme-is-required",
        removed=("packages/billing/README.md",),
        diagnostic="check README 'packages/billing/README.md': file does not exist",
    ),
    Case(
        name="sentence-equals-the-manifest-description",
        files=(
            (
                "packages/billing/orders/README.md",
                ORDERS_README.replace("Owns order totals.", "Adds up orders."),
            ),
        ),
        diagnostic="and the one sentence 'Owns order totals.'",
    ),
    Case(
        name="sections-keep-their-order",
        files=(
            (
                "packages/billing/orders/README.md",
                ORDERS_README.replace("## Use", "## Never").replace(
                    "## Never\n\n- ", "## Use\n\n- "
                ),
            ),
        ),
        diagnostic="keep exactly the headings ## Layout, ## Use, ## Never, in that order",
    ),
    Case(
        name="layout-paths-exist",
        files=(
            (
                "packages/billing/orders/README.md",
                ORDERS_README.replace("src/totals/", "src/taxes/"),
            ),
        ),
        diagnostic="Layout path 'src/taxes/' does not exist",
    ),
    Case(
        name="package-readme-stays-within-its-lines",
        files=(
            (
                "packages/billing/orders/README.md",
                ORDERS_README + "- Never skip a line.\n" * 20,
            ),
        ),
        diagnostic="lines exceeds 30",
    ),
    Case(
        name="group-table-lists-every-package",
        files=(
            (
                "packages/billing/README.md",
                GROUP_README.replace("| `@fixture/orders`   | Owns order totals.    |\n", ""),
            ),
        ),
        diagnostic="with one row for each package",
    ),
    Case(
        name="workspace-file-is-required",
        removed=("pnpm-workspace.yaml",),
        diagnostic="read workspace",
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
        f"check package README case {case.name!r}: expected diagnostic {case.diagnostic!r}, "
        f"received exit {result.returncode!r} with output {output!r}"
    )
    raise AssertionError(message)


def _check_case(*, checker: Path, case: Case) -> None:
    with TemporaryDirectory(prefix=f"check-package-readmes-{case.name}-") as temporary:
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
