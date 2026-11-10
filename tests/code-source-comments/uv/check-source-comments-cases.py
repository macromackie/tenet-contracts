#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Run passing and failing example workspaces against the shipped source comment checker."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

GUIDANCE_PARENT_DEPTH = 3
CHECKER_PATH = "contracts/code-source-comments/assets/uv/check-source-comments.py"
CASE_TIMEOUT_SECONDS = 60
OUTPUT_CHARACTER_LIMIT = 6000
CHECKER_ARGUMENTS = ("--config", ".config/source-comments.json")


@dataclass(frozen=True, kw_only=True)
class Case:
    """One workspace as its changes to the passing files, with the diagnostic it must produce."""

    name: str
    files: tuple[tuple[str, str], ...] = ()
    removed: tuple[str, ...] = ()
    diagnostic: str = ""


POLICY = '{"maximumReasonComments": 2, "sourceRoots": ["src"]}\n'
TYPESCRIPT_MODULE = """export function settleInvoice(): void {
  // Why: the provider rejects a second capture within one second.
  wait();
}
"""
PYTHON_MODULE = """def settle_invoice() -> None:
    # Why: the provider rejects a second capture within one second.
    wait()
"""
RUST_MODULE = """fn settle_invoice() {
    // ast-grep-ignore: numeric-exit-statuses-rust -- the supervisor defines this status
    wait();
}
"""
PASSING_FILES = (
    (".config/source-comments.json", POLICY),
    ("src/settle-invoice.ts", TYPESCRIPT_MODULE),
    ("src/settle_invoice.py", PYTHON_MODULE),
    ("src/settle_invoice.rs", RUST_MODULE),
)
CASES = (
    Case(name="directives-and-counted-reasons-pass"),
    Case(
        name="doc-comment-is-rejected",
        files=(("src/settle-invoice.ts", "/** Settles the invoice. */\n" + TYPESCRIPT_MODULE),),
        diagnostic="check comment src/settle-invoice.ts:1: delete the prose comment",
    ),
    Case(
        name="docstring-is-rejected",
        files=(
            (
                "src/settle_invoice.py",
                PYTHON_MODULE.replace("    # Why", '    """Settle the invoice."""\n    # Why'),
            ),
        ),
        diagnostic="check comment src/settle_invoice.py:2: delete the prose comment",
    ),
    Case(
        name="directive-needs-its-reason",
        files=(
            (
                "src/settle_invoice.rs",
                RUST_MODULE.replace(" -- the supervisor defines this status", ""),
            ),
        ),
        diagnostic="check comment src/settle_invoice.rs:2: delete the prose comment",
    ),
    Case(
        name="reason-comments-stay-within-the-maximum",
        files=(
            (
                "src/settle_invoice.rs",
                RUST_MODULE.replace(
                    "    wait();", "    // Why: the ledger closes at noon.\n    wait();"
                ),
            ),
        ),
        diagnostic="3 reason comments exceeds 2",
    ),
    Case(
        name="source-root-must-exist",
        files=((".config/source-comments.json", POLICY.replace('"src"', '"sources"')),),
        diagnostic="scan source roots ['sources']: path does not exist",
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
        f"check source comment case {case.name!r}: expected diagnostic {case.diagnostic!r}, "
        f"received exit {result.returncode!r} with output {output!r}"
    )
    raise AssertionError(message)


def _check_case(*, checker: Path, case: Case) -> None:
    with TemporaryDirectory(prefix=f"check-source-comments-{case.name}-") as temporary:
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
