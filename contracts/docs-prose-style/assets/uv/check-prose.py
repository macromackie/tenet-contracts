#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""
Check each document's prose against a maximum of words per sentence and sentences per paragraph.

The prose is what remains after front matter, code blocks, headings, table rows, and comments.
An inline code span counts as one word and a link as its text.
A list item's sentences count against the word maximum only, since a list item is no paragraph.
A document after `--adapted` is an adopted contract: only the text under its
`## Local adaptations` heading is checked, and each finding keeps its line in the whole file.
"""

import argparse
import re
from dataclasses import dataclass, replace
from pathlib import Path

DEFAULT_SENTENCE_WORDS = 30
"""The words a sentence may hold unless the repository passes its declared maximum."""
DEFAULT_PARAGRAPH_SENTENCES = 5
"""The sentences a paragraph may hold unless the repository passes its declared maximum."""
SHOWN_CHARACTERS = 60
"""The opening characters of a long sentence that its finding shows."""
FRONT_MATTER_FENCE = "---"
FENCE = re.compile(r"^\s*(```|~~~)")
SKIPPED_PREFIXES = ("#", "|", "<!--")
"""The opening marks of a heading, a table row, and a comment, which hold no prose."""
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
QUOTE_MARKS = "> "
INLINE_CODE = re.compile(r"(`+)((?:(?!\1).)+)\1")
LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
SENTENCE_END = re.compile(r"(?<=[.!?])[\"')\]*_]*\s+")
WORD = re.compile(r"[\w$]")
ADAPTATIONS = re.compile(r"^## Local adaptations\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)


class ProseRejected(ValueError):
    """A sentence or a paragraph of a checked document is over its maximum."""


@dataclass(frozen=True, kw_only=True)
class Limits:
    """The declared maximum of words in a sentence and of sentences in a paragraph."""

    sentence_words: int
    paragraph_sentences: int


@dataclass(frozen=True, kw_only=True)
class Block:
    """One paragraph or list item of a document, with the number of its first line."""

    is_item: bool
    line: int
    text: str


def _read_prose_lines(*, text: str) -> list[str]:
    lines = text.splitlines()
    has_front_matter = bool(lines) and lines[0].strip() == FRONT_MATTER_FENCE
    start = lines.index(FRONT_MATTER_FENCE, 1) + 1 if has_front_matter else 0
    prose = [""] * start
    is_fenced = False
    for line in lines[start:]:
        is_fence = FENCE.match(line) is not None
        is_fenced = is_fenced != is_fence
        is_prose = not (is_fence or is_fenced or line.strip().startswith(SKIPPED_PREFIXES))
        prose.append(line if is_prose else "")
    return prose


def _read_opening(*, line: str, is_item: bool) -> str:
    return LIST_ITEM.sub("", line) if is_item else line.strip().lstrip(QUOTE_MARKS)


def list_blocks(*, text: str) -> list[Block]:
    """List each paragraph and list item of a Markdown text."""
    blocks: list[Block] = []
    is_open = False
    for number, line in enumerate(_read_prose_lines(text=text), start=1):
        stripped = line.strip()
        is_item = LIST_ITEM.match(line) is not None
        if stripped and is_open and not is_item:
            blocks[-1] = replace(blocks[-1], text=f"{blocks[-1].text} {stripped}")
        elif stripped:
            blocks.append(
                Block(is_item=is_item, line=number, text=_read_opening(line=line, is_item=is_item))
            )
        is_open = bool(stripped)
    return blocks


def split_sentences(*, text: str) -> list[str]:
    """Split prose into sentences at a full stop, question mark, or exclamation mark."""
    plain = LINK.sub(r"\1", INLINE_CODE.sub("code", text))

    return [sentence for sentence in SENTENCE_END.split(plain) if WORD.search(sentence)]


def count_words(*, sentence: str) -> int:
    """Count the space-separated tokens of a sentence that hold a letter or a digit."""
    return sum(1 for token in sentence.split() if WORD.search(token))


def read_adaptations(*, text: str) -> str:
    """Read a contract's local adaptations, with every other line left blank."""
    adaptations = ""
    previous = 0

    for match in ADAPTATIONS.finditer(text):
        start, end = match.span(1)
        adaptations += "\n" * text.count("\n", previous, start) + text[start:end]
        previous = end

    return adaptations


def inspect_document(*, path: Path, is_adapted: bool, limits: Limits) -> list[str]:
    """List each sentence and each paragraph of one document that is over its maximum."""
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for block in list_blocks(text=read_adaptations(text=text) if is_adapted else text):
        sentences = split_sentences(text=block.text)

        if not block.is_item and len(sentences) > limits.paragraph_sentences:
            errors.append(
                f"{path}:{block.line}: a paragraph of {len(sentences)} sentences "
                f"exceeds {limits.paragraph_sentences}"
            )

        errors.extend(
            f"{path}:{block.line}: a sentence of {count_words(sentence=sentence)} words "
            f"exceeds {limits.sentence_words}: {sentence[:SHOWN_CHARACTERS]}"
            for sentence in sentences
            if count_words(sentence=sentence) > limits.sentence_words
        )

    return errors


def _read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("documents", nargs="*", help="each Markdown document checked whole")
    parser.add_argument(
        "--adapted",
        nargs="+",
        default=[],
        help="each adopted contract whose local adaptations alone are checked",
    )
    parser.add_argument(
        "--maximum-sentence-words",
        type=int,
        default=DEFAULT_SENTENCE_WORDS,
        help="the declared maximum of words in a sentence",
    )
    parser.add_argument(
        "--maximum-paragraph-sentences",
        type=int,
        default=DEFAULT_PARAGRAPH_SENTENCES,
        help="the declared maximum of sentences in a paragraph",
    )
    arguments = parser.parse_args()
    if not arguments.documents and not arguments.adapted:
        parser.error("name a document or an --adapted contract")
    return arguments


def main() -> None:
    """Check every named document without changing any file."""
    arguments = _read_arguments()
    limits = Limits(
        sentence_words=arguments.maximum_sentence_words,
        paragraph_sentences=arguments.maximum_paragraph_sentences,
    )
    documents = [
        *((Path(path), False) for path in arguments.documents),
        *((Path(path), True) for path in arguments.adapted),
    ]
    errors = [
        error
        for path, is_adapted in documents
        for error in inspect_document(path=path, is_adapted=is_adapted, limits=limits)
    ]
    if errors:
        raise ProseRejected("\n".join(errors))


if __name__ == "__main__":
    main()
