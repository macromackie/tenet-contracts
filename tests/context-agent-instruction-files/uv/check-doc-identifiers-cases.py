#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Run passing and failing example repositories against the shipped document name checker."""

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

GUIDANCE_PARENT_DEPTH = 3
CHECKER_PATH = "contracts/context-agent-instruction-files/assets/uv/check-doc-identifiers.py"
CASE_TIMEOUT_SECONDS = 60
OUTPUT_CHARACTER_LIMIT = 6000
UV = shutil.which("uv") or "uv"
GUIDE_FILE = "AGENTS.md"
CONTRACT_FILE = "contracts/001-order-limits/CONTRACT.md"
LIMITS_FILE = "src/billing/limits.ts"
RULE_FILE = "rules/seeded-totals.yml"
TASK_FILE = ".config/mise.toml"
PASSING_ARGUMENTS = (
    "--root",
    ".",
    "--code",
    "src",
    "--rules",
    "rules",
    "--tasks",
    f".={TASK_FILE}",
    "packages/billing=packages/billing/tasks",
    "--contracts",
    "contracts",
    "--whole",
    GUIDE_FILE,
    "--adapted",
    CONTRACT_FILE,
)


@dataclass(frozen=True, kw_only=True)
class Case:
    """One repository as its changes to the passing files, with the diagnostic it must produce."""

    name: str
    files: tuple[tuple[str, str], ...] = ()
    arguments: tuple[str, ...] = PASSING_ARGUMENTS
    diagnostic: str = ""


GUIDE = """# Guide

The `seeded-totals` rule keeps `readOrderTotal` on the order's seed, as `order-limits` requires.
Run `mise run lint` before each commit, and `mise -C packages/billing run totals:check` after it.
An order holds at most `MAXIMUM_ORDER_LINES` (30) lines, which `src/billing/limits.ts` declares.
`readOrderTotal` in `limits.ts` reads the total.
"""
CONTRACT = """---
name: order-limits
---

## Rules

Name `retiredFunction` here, above the adaptations, where the check does not read.

## Local adaptations

The repository declares `MAXIMUM_ORDER_LINES` in `src/billing/limits.ts`.
"""
LIMITS = """export const MAXIMUM_ORDER_LINES = 30;

export function readOrderTotal(): number {
  return MAXIMUM_ORDER_LINES;
}
"""
PASSING_FILES = (
    (GUIDE_FILE, GUIDE),
    (CONTRACT_FILE, CONTRACT),
    (LIMITS_FILE, LIMITS),
    (RULE_FILE, "id: seeded-totals\n"),
    (TASK_FILE, '[tasks.lint]\nrun = "true"\n'),
    ("packages/billing/tasks/totals/check", "#!/bin/sh\n"),
)
CASES = (
    Case(name="names-that-exist-pass"),
    Case(
        name="a-renamed-rule-fails",
        files=((RULE_FILE, "id: seeded-sums\n"),),
        diagnostic="AGENTS.md:3: `seeded-totals` names no rule, task, contract, skill, path",
    ),
    Case(
        name="a-renamed-function-fails",
        files=((LIMITS_FILE, LIMITS.replace("readOrderTotal", "readTotal")),),
        diagnostic="AGENTS.md:3: `readOrderTotal` appears in no code",
    ),
    Case(
        name="a-removed-task-fails",
        files=((TASK_FILE, '[tasks.check]\nrun = "true"\n'),),
        diagnostic="AGENTS.md:4: `lint` is no task of the folder `.`",
    ),
    Case(
        name="a-folder-without-declared-tasks-fails",
        arguments=tuple(
            argument for argument in PASSING_ARGUMENTS if not argument.startswith("packages/")
        ),
        diagnostic="names the folder `packages/billing`, whose tasks `--tasks` does not declare",
    ),
    Case(
        name="a-path-that-starts-below-the-root-fails",
        files=((GUIDE_FILE, GUIDE.replace("`src/billing/limits.ts`", "`billing/limits.ts`")),),
        diagnostic="AGENTS.md:5: `billing/limits.ts` names no file",
    ),
    Case(
        name="a-declared-base-folder-starts-a-path",
        files=((GUIDE_FILE, GUIDE.replace("`src/billing/limits.ts`", "`billing/limits.ts`")),),
        arguments=(*PASSING_ARGUMENTS, "--base", "src"),
    ),
    Case(
        name="a-changed-limit-fails",
        files=((LIMITS_FILE, LIMITS.replace("= 30", "= 40")),),
        diagnostic="AGENTS.md:5: `MAXIMUM_ORDER_LINES` is 40 in the code, not 30",
    ),
    Case(
        name="a-name-moved-out-of-its-file-fails",
        files=(
            (LIMITS_FILE, LIMITS.replace("readOrderTotal", "readTotal")),
            ("src/billing/totals.ts", "export const readOrderTotal = 1;\n"),
        ),
        diagnostic="AGENTS.md:6: `readOrderTotal` is not in `limits.ts`",
    ),
    Case(
        name="a-stale-name-in-the-adaptations-fails",
        files=((CONTRACT_FILE, CONTRACT.replace("MAXIMUM_ORDER_LINES", "MAXIMUM_LINES")),),
        diagnostic="CONTRACT.md:11: `MAXIMUM_LINES` appears in no code",
    ),
)


def _inspect_result(*, case: Case, result: subprocess.CompletedProcess[str]) -> None:
    is_success = result.returncode == 0
    is_expected = is_success and case.diagnostic == ""
    if case.diagnostic:
        is_expected = not is_success and case.diagnostic in result.stderr

    if is_expected:
        return

    output = (result.stdout + result.stderr)[-OUTPUT_CHARACTER_LIMIT:]
    message = (
        f"check document names case {case.name!r}: expected diagnostic {case.diagnostic!r}, "
        f"received exit {result.returncode!r} with output {output!r}"
    )
    raise AssertionError(message)


def _check_case(*, checker: Path, case: Case) -> None:
    with TemporaryDirectory(prefix=f"check-doc-identifiers-{case.name}-") as temporary:
        for relative, content in {**dict(PASSING_FILES), **dict(case.files)}.items():
            path = Path(temporary, relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        result = subprocess.run(
            [UV, "run", "--script", str(checker), *case.arguments],
            capture_output=True,
            check=False,
            cwd=temporary,
            text=True,
            timeout=CASE_TIMEOUT_SECONDS,
        )
        _inspect_result(case=case, result=result)


def main() -> None:
    """Run the shipped checker on the passing repository and on each change that must fail."""
    guidance = Path(__file__).resolve().parents[GUIDANCE_PARENT_DEPTH]

    for case in CASES:
        _check_case(checker=guidance / CHECKER_PATH, case=case)


if __name__ == "__main__":
    main()
