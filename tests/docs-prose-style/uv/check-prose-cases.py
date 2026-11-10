#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Run passing and failing example documents against the shipped prose checker."""

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

GUIDANCE_PARENT_DEPTH = 3
CHECKER_PATH = "contracts/docs-prose-style/assets/uv/check-prose.py"
CASE_TIMEOUT_SECONDS = 60
OUTPUT_CHARACTER_LIMIT = 6000
UV = shutil.which("uv") or "uv"
GUIDE_FILE = "guide.md"
CONTRACT_FILE = "CONTRACT.md"
PASSING_ARGUMENTS = (GUIDE_FILE, "--adapted", CONTRACT_FILE)


@dataclass(frozen=True, kw_only=True)
class Case:
    """One folder of documents as its changes to the passing files, with its diagnostic."""

    name: str
    files: tuple[tuple[str, str], ...] = ()
    arguments: tuple[str, ...] = PASSING_ARGUMENTS
    diagnostic: str = ""


THIRTY_WORDS = (
    "A sentence counts each word, and an inline code span such as `mise run check` counts as "
    "one word, so this sentence of exactly thirty words stays well within the stated limit."
)
CODE_LINE = (
    "a code block is no prose, so the check counts none of its words, however many of them "
    "there are on one line, and this line holds more of them than the limit allows"
)
GUIDE = f"""---
title: Guide
---

# Guide

Run the check before each commit. It reads every guide that the task names. {THIRTY_WORDS}
It names each line over a limit. Fix the line and run it again.

- A list item is no paragraph. Its sentences count against the words alone. A third one.
  A fourth one. A fifth. A sixth.

```sh
echo "{CODE_LINE}"
```
"""
LONG_SENTENCE = THIRTY_WORDS.replace("stays well within", "is now just over")
CONTRACT = f"""---
name: guide-checks
---

## Rules

Run the check before each commit. {LONG_SENTENCE}

## Local adaptations

The repository runs the check in its lint task. It reads every guide.
"""
CASES = (
    Case(name="documents-within-both-maximums-pass"),
    Case(
        name="a-long-sentence-fails",
        files=((GUIDE_FILE, GUIDE.replace(THIRTY_WORDS, LONG_SENTENCE)),),
        diagnostic="guide.md:7: a sentence of 31 words exceeds 30",
    ),
    Case(
        name="a-long-paragraph-fails",
        files=((GUIDE_FILE, GUIDE.replace("Fix the line and", "Fix the line. Then")),),
        diagnostic="guide.md:7: a paragraph of 6 sentences exceeds 5",
    ),
    Case(
        name="a-declared-maximum-replaces-the-default",
        arguments=("--maximum-sentence-words", "29", GUIDE_FILE),
        diagnostic="guide.md:7: a sentence of 30 words exceeds 29",
    ),
    Case(
        name="a-contract-checked-whole-fails-above-its-adaptations",
        arguments=(CONTRACT_FILE,),
        diagnostic="CONTRACT.md:7: a sentence of 31 words exceeds 30",
    ),
    Case(
        name="a-long-sentence-in-the-adaptations-fails-at-its-line",
        files=((CONTRACT_FILE, f"{CONTRACT}\n{LONG_SENTENCE}\n"),),
        diagnostic="CONTRACT.md:13: a sentence of 31 words exceeds 30",
    ),
    Case(
        name="a-run-that-names-no-document-fails",
        arguments=(),
        diagnostic="name a document or an --adapted contract",
    ),
)
PASSING_FILES = ((GUIDE_FILE, GUIDE), (CONTRACT_FILE, CONTRACT))


def _inspect_result(*, case: Case, result: subprocess.CompletedProcess[str]) -> None:
    is_success = result.returncode == 0
    is_expected = is_success and case.diagnostic == ""
    if case.diagnostic:
        is_expected = not is_success and case.diagnostic in result.stderr

    if is_expected:
        return

    output = (result.stdout + result.stderr)[-OUTPUT_CHARACTER_LIMIT:]
    message = (
        f"check prose case {case.name!r}: expected diagnostic {case.diagnostic!r}, "
        f"received exit {result.returncode!r} with output {output!r}"
    )
    raise AssertionError(message)


def _check_case(*, checker: Path, case: Case) -> None:
    with TemporaryDirectory(prefix=f"check-prose-{case.name}-") as temporary:
        for relative, content in {**dict(PASSING_FILES), **dict(case.files)}.items():
            Path(temporary, relative).write_text(content, encoding="utf-8")
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
    """Run the shipped checker on the passing documents and on each change that must fail."""
    guidance = Path(__file__).resolve().parents[GUIDANCE_PARENT_DEPTH]

    for case in CASES:
        _check_case(checker=guidance / CHECKER_PATH, case=case)


if __name__ == "__main__":
    main()
