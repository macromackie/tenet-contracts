#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Report each prose comment under the source roots, and count their reason comments."""

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

RULE_SET = "ast-grep/sgconfig.yml"
"""The rule set that this contract ships, relative to the contract's `assets/` folder."""
SCAN_COMMAND = ("ast-grep", "scan", "--json=stream", "--config")
PROSE_RULE_PREFIX = "prose-comments-"
REASON_RULE_PREFIX = "reason-comments-"
PARENT_COMPONENT = ".."


class CommentsRejected(ValueError):
    """The policy is malformed, or the source roots break it."""


@dataclass(frozen=True, kw_only=True)
class Policy:
    """The declared source roots and the most reason comments that they may hold together."""

    roots: tuple[str, ...]
    maximum_reason_comments: int


@dataclass(frozen=True, kw_only=True)
class Finding:
    """One report of a shipped rule, with the line that the scan numbers from zero."""

    rule: str
    file: str
    line: int


def _read_root(*, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        message = f"read source root {value!r}: expected a nonempty relative path"
        raise CommentsRejected(message)
    path = PurePosixPath(value)
    if path.is_absolute() or PARENT_COMPONENT in path.parts:
        message = f"read source root {value!r}: expected a path inside the repository"
        raise CommentsRejected(message)
    return value


def read_policy(*, path: Path) -> Policy:
    """Require the source roots and a maximum count, and refuse any other field."""
    value: object = json.loads(path.read_text(encoding="utf-8"))
    match value:
        case {
            "sourceRoots": [*roots],
            "maximumReasonComments": int() as maximum,
            **unknown_fields,
        } if roots and maximum >= 0 and not isinstance(maximum, bool) and not unknown_fields:
            return Policy(
                roots=tuple(_read_root(value=root) for root in roots),
                maximum_reason_comments=maximum,
            )
        case _:
            message = (
                f"read comment policy {str(path)!r}: declare the source roots "
                "and the maximum number of reason comments"
            )
            raise CommentsRejected(message)


def _read_finding(*, value: object) -> Finding:
    match value:
        case {
            "ruleId": str() as rule,
            "file": str() as file,
            "range": {"start": {"line": int() as line}},
        }:
            return Finding(rule=rule, file=file, line=line)
        case _:
            message = f"read scan finding {value!r}: expected a rule, a file, and a start line"
            raise CommentsRejected(message)


def scan_sources(*, root: Path, policy: Policy) -> list[Finding]:
    """Run the shipped rule set over the declared roots, and read each finding it prints."""
    missing = [name for name in policy.roots if not (root / name).exists()]
    if missing:
        message = f"scan source roots {missing!r}: path does not exist"
        raise CommentsRejected(message)
    rule_set = Path(__file__).resolve().parents[1] / RULE_SET
    scan = subprocess.run(
        [*SCAN_COMMAND, str(rule_set), *policy.roots],
        capture_output=True,
        check=False,
        cwd=root,
        text=True,
    )
    if scan.stderr.strip() and not scan.stdout.strip():
        message = f"scan source roots {policy.roots!r}: {scan.stderr.strip()}"
        raise CommentsRejected(message)
    return [_read_finding(value=json.loads(line)) for line in scan.stdout.splitlines() if line]


def inspect_comments(*, findings: list[Finding], policy: Policy) -> list[str]:
    """Report each prose comment, and each reason comment once their count passes the maximum."""
    reasons = [finding for finding in findings if finding.rule.startswith(REASON_RULE_PREFIX)]
    errors = [
        f"check comment {finding.file}:{finding.line + 1}: delete the prose comment, "
        "or state its fact in a name, a type, a README, or a contract"
        for finding in findings
        if finding.rule.startswith(PROSE_RULE_PREFIX)
    ]
    if len(reasons) > policy.maximum_reason_comments:
        errors.extend(
            f"check reason comment {finding.file}:{finding.line + 1}: {len(reasons)!r} reason "
            f"comments exceeds {policy.maximum_reason_comments!r}"
            for finding in reasons
        )
    return errors


def main() -> None:
    """Check the declared source roots without changing any file."""
    # jscpd:ignore-start -- duplication -- Standalone checkers must carry their own argument parser.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="repository root to inspect")
    parser.add_argument(
        "--config", required=True, help="policy path relative to the repository root"
    )
    arguments = parser.parse_args()
    root = Path(arguments.root).resolve()
    # jscpd:ignore-end
    policy = read_policy(path=root / arguments.config)
    errors = inspect_comments(findings=scan_sources(root=root, policy=policy), policy=policy)
    if errors:
        raise CommentsRejected("\n".join(errors))


if __name__ == "__main__":
    main()
