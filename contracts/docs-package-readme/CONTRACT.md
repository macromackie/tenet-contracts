---
name: docs-package-readme
message: Give every workspace package and every folder that groups packages a short README in one fixed form that a check reads beside the package manifest.
requires-tenet: 0.11.0
---

## Rules

Apply these rules to every member package of a workspace and to every folder that groups packages, which is a folder other than the workspace root that directly holds a member package.
The workspace root's README follows `docs-readme-structure` and is outside these rules.
Read the members from the workspace file that the package manager reads, never from a second list.
Give every member package a `description` in its manifest, written as one sentence that says what the package owns.
Give every member package a `README.md` in its root folder, and give every folder that groups packages a `README.md`.

Open a package README with a title that is the package's name from its manifest, a blank line, and that one description sentence, character for character.
Follow the sentence with exactly three sections, headed `## Layout`, `## Use`, and `## Never`, in that order, and write no other heading.
Write each line of Layout as a list item that opens with one path in backticks, relative to the package folder, followed by a colon and what the path holds, such as ``- `src/totals/`: the modules that add up an order.``
Name only paths that exist in Layout.
Write in Use how another package or a person uses the package, such as the import or the command.
Write in Never one list item for each thing a change to the package must never do.
Declare a maximum number of lines for a package README; the shipped checker sets 30, which a repository may override.

Open a group README with a title that is the folder's name, a blank line, and one sentence that says what its packages share.
Follow the sentence with one table of two columns, Package and Description, and nothing else.
Give the table one row for each member package directly inside the folder, in the order of their paths, with the package's name in backticks and its manifest's description.
Declare a maximum number of lines for a group README; the shipped checker sets 15, which a repository may override.
Change a package's description in its manifest and in both READMEs in the same change.
Keep longer explanation, such as design history or a runbook, in a separate document, as `docs-readme-structure` requires.

Violation: `packages/billing/orders/README.md` opens with "Order helpers." while the manifest's description reads "Owns order totals.", and its Layout lists `src/taxes/`, which was deleted.
Allowed: the README opens with `# @acme/orders` and "Owns order totals.", lists `src/totals/` under Layout, and `packages/billing/README.md` has a row for `@acme/orders` with the same sentence.

## Checks

Run the checker in this contract's `assets/` folder from the repository root with the workspace root as its `--root`, where its runtime can run.
For each changed Layout line, does its text say what the path holds today?
For each changed Never item, would a reviewer recognize a change that breaks it?
Does each changed Use section give an import or a command that works as written?
