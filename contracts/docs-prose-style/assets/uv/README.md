# Prose check

Run from the repository root, replacing the installed contract path and naming each governed document:

```bash
uv run --script .contracts/012-docs-prose-style/assets/uv/check-prose.py README.md docs/*.md
```

The script requires Python 3.14 or later and has no package dependencies. It sets 30 words for a sentence and 5
sentences for a paragraph. Pass the repository's declared maximums with `--maximum-sentence-words` and
`--maximum-paragraph-sentences`.

The checker reads prose only. It skips front matter, code blocks, headings, table rows, and comments. An inline code
span counts as one word and a link as its text. A list item's sentences count against the word maximum only.

Name an adopted contract after `--adapted` to check only the text under its `## Local adaptations` heading. Each
finding keeps its line number in the whole file.

The command reports every sentence and paragraph over its maximum and exits unsuccessfully. It changes no files.
