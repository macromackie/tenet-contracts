#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["markdown-it-py==4.0.0", "mdit-py-plugins==0.5.0", "PyYAML==6.0.3"]
# ///
"""
Check that each tracked guidance document's local links resolve and its frontmatter is complete.

Run `uv run --locked --script check-guidance.py PATH... [--require PATTERN=FIELD,...]` from the
repository root. It reads each Markdown file that Git tracks under the given paths. Each `--require`
names the frontmatter fields, each a nonempty string, that a document matching its pattern needs.
The first matching pattern applies, so an empty field list exempts the documents it matches from
the patterns after it. It skips external and site-root links, heading fragments, code, and raw
HTML, and it cannot tell whether a document is current.
"""

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin

import output

if TYPE_CHECKING:
    from urllib.parse import SplitResult

    from markdown_it.token import Token

GIT_FILES = ("git", "ls-files", "-z", "--")
"""The command that lists each tracked file under the paths after it, separated by NUL."""
FENCE = "---"
"""The line that opens YAML frontmatter."""
FENCE_ENDS = frozenset({"---", "..."})
"""The lines that may close YAML frontmatter."""
MARKDOWN_SUFFIX = ".md"
SKIPPED_PATH_STARTS = frozenset({"", "/"})
"""How a link path starts when it leaves the repository's files: empty, or at the site root."""


@dataclass(frozen=True)
class Requirement:
    """The frontmatter fields that each document matching a path pattern needs."""

    pattern: str
    fields: tuple[str, ...]


@dataclass(frozen=True)
class Settings:
    """The decoded arguments of one run."""

    root: Path
    paths: tuple[str, ...]
    requirements: tuple[Requirement, ...]


class GuidanceRejectedError(Exception):
    """A guidance document whose frontmatter or a link destination cannot be read."""

    def __init__(self, *, path: PurePosixPath, reason: str) -> None:
        """Name the document and why it cannot be read."""
        super().__init__(f"{path}: {reason}")


def read_requirement(*, text: str) -> Requirement:
    """Decode one `PATTERN=FIELD,...` argument; an empty field list requires nothing."""
    pattern, _, fields = text.partition("=")

    return Requirement(pattern=pattern, fields=tuple(field for field in fields.split(",") if field))


def read_settings() -> Settings:
    """Decode the paths to check and the frontmatter that each kind of document needs."""
    parser = argparse.ArgumentParser(description="Check guidance links and frontmatter.")
    parser.add_argument("paths", nargs="+", help="the files and folders whose documents to check")
    parser.add_argument(
        "--require",
        action="append",
        default=[],
        help="PATTERN=FIELD,... : the frontmatter fields that matching documents need",
    )
    arguments = parser.parse_args()

    return Settings(
        root=Path.cwd(),
        paths=tuple(arguments.paths),
        requirements=tuple(read_requirement(text=text) for text in arguments.require),
    )


def read_mapping(*, path: PurePosixPath, text: str) -> dict[str, object]:
    """Load frontmatter text as a YAML mapping."""
    try:
        metadata = yaml.safe_load(text)
    except yaml.YAMLError as error:
        raise GuidanceRejectedError(path=path, reason=f"invalid frontmatter: {error}") from error

    if not isinstance(metadata, dict):
        raise GuidanceRejectedError(path=path, reason="write the frontmatter as a YAML mapping")

    return {str(key): value for key, value in metadata.items()}


def read_frontmatter(*, path: PurePosixPath, text: str) -> tuple[dict[str, object], str]:
    """Split a document into its frontmatter and its body, keeping the body's line numbers."""
    lines = text.splitlines(keepends=True)

    if not lines or lines[0].strip() != FENCE:
        return {}, text

    end = next(
        (index for index, line in enumerate(lines[1:], 1) if line.strip() in FENCE_ENDS),
        len(lines),
    )

    if end == len(lines):
        raise GuidanceRejectedError(path=path, reason="close the YAML frontmatter")

    metadata = read_mapping(path=path, text="".join(lines[1:end]))
    # Blank lines stand in for the frontmatter, so the body's line numbers stay the document's.
    body = "\n" * (end + 1) + "".join(lines[end + 1 :])

    return metadata, body


def read_destination(*, token: Token) -> str:
    """Read a link's or an image's destination, or an empty string for any other token."""
    match token.type:
        case "link_open":
            return str(token.attrGet("href") or "")
        case "image":
            return str(token.attrGet("src") or "")
        case _:
            return ""


def read_destinations(*, body: str, parser: MarkdownIt) -> list[tuple[int, str]]:
    """Read each link's and image's destination with the line its block starts on."""
    return [
        (block.map[0] + 1 if block.map else 1, destination)
        for block in parser.parse(body)
        for token in block.children or []
        if (destination := read_destination(token=token))
    ]


def read_link(*, path: PurePosixPath, destination: str) -> SplitResult:
    """Split a link destination into its parts."""
    try:
        return urlsplit(destination)
    except ValueError as error:
        raise GuidanceRejectedError(path=path, reason=f"invalid link: {destination}") from error


def check_links(*, root: Path, path: PurePosixPath, body: str, parser: MarkdownIt) -> list[str]:
    """Report each relative link or image whose target is missing."""
    errors = []

    for line, destination in read_destinations(body=body, parser=parser):
        link = read_link(path=path, destination=destination)

        # Site-root links and external URLs belong to their publishing surface.
        if link.scheme or link.netloc or link.path[:1] in SKIPPED_PATH_STARTS:
            continue

        if not (root / path.parent / unquote(link.path)).exists():
            errors.append(f"{path}: line {line}: missing link target: {destination}")

    return errors


def check_fields(
    *, path: PurePosixPath, metadata: dict[str, object], requirements: tuple[Requirement, ...]
) -> list[str]:
    """Report each field that the first requirement matching the document names and it lacks."""
    fields = next((item.fields for item in requirements if path.full_match(item.pattern)), ())

    return [
        f"{path}: frontmatter requires nonempty string: {field}"
        for field in fields
        if not isinstance(value := metadata.get(field), str) or not value.strip()
    ]


def check_document(*, settings: Settings, path: PurePosixPath, parser: MarkdownIt) -> list[str]:
    """Report each missing link target and missing frontmatter field of one document."""
    text = (settings.root / path).read_text(encoding="utf-8")
    metadata, body = read_frontmatter(path=path, text=text)

    return [
        *check_fields(path=path, metadata=metadata, requirements=settings.requirements),
        *check_links(root=settings.root, path=path, body=body, parser=parser),
    ]


def read_documents(*, settings: Settings) -> list[PurePosixPath]:
    """List each Markdown file that Git tracks under the settings' paths and that still exists."""
    listed = subprocess.run(
        [*GIT_FILES, *settings.paths],
        capture_output=True,
        check=True,
        cwd=settings.root,
        text=True,
    )

    # An unstaged deletion is checked through the references that remain.
    return sorted(
        PurePosixPath(name)
        for name in listed.stdout.split("\0")
        if name.endswith(MARKDOWN_SUFFIX) and (settings.root / name).exists()
    )


def check_documents(*, settings: Settings, documents: list[PurePosixPath]) -> list[str]:
    """Report each missing link target and missing frontmatter field of every document."""
    parser = MarkdownIt("commonmark").use(footnote_plugin)

    return [
        error
        for path in documents
        for error in check_document(settings=settings, path=path, parser=parser)
    ]


def main() -> output.ExitStatus:
    """Check every tracked guidance document, and return whether any fails."""
    settings = read_settings()
    documents = read_documents(settings=settings)

    try:
        errors = check_documents(settings=settings, documents=documents)
    except GuidanceRejectedError as error:
        output.report_findings(lines=[str(error)])

        return output.ExitStatus.INVALID

    output.report_findings(lines=errors)
    output.report_summary(line=f"Checked {len(documents)} guidance documents: {len(errors)} errors")

    if errors:
        return output.ExitStatus.INVALID

    return output.ExitStatus.VALID


output.finish(status=main())
