---
name: docs-prose-style
message: Write documentation in short, direct sentences that lead with what the reader does or needs.
---

## Rules

Apply these rules to the prose of READMEs, guides, and reference pages in the governed scope, and not to code comments.
Declare a maximum sentence length in words and a maximum paragraph length in sentences, and keep prose within both.
Lead each section and paragraph with the action, answer, or fact the reader needs, and follow it with the reason.
Write each step a reader performs in the active voice and the imperative mood, such as "Run the check" instead of "The check can be run".
Replace grading words, such as fast, easy, robust, simple, or significantly, with the measurement they stand for, or delete them.
Never use filler phrases such as "it is important to note that", "in order to", or "please note".
Expand each acronym and internal name on first use, or link to its definition, unless it is a standard term of the reader's field, such as HTTP or JSON.
Use a numbered list for three or more steps that need prose, one code block for a run of commands, a bulleted list for three or more parallel items, and a table for items compared on several attributes.
Format every command, path, identifier, or code fragment a reader may copy as code, and put a multi-line one in a code block.
Give each paragraph one idea.

Violation: "It is important to note that the import is significantly faster now, so in order to use it you should run the sync first."
Allowed: "Run the sync before the import; the import takes 4 minutes for 10,000 invoices."

## Checks

Count the words in each changed sentence and the sentences in each changed paragraph, and compare them with the declared maximums.
Does each changed paragraph's first sentence state what the reader does or needs?
Search changed prose for grading words and filler phrases.
