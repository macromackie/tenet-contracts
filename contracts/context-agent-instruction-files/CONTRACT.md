---
name: context-agent-instruction-files
message: Keep agent instruction files visible, accurate, and consistent, and change them with the code they describe.
---

## Rules

Apply this contract to files that coding agents load as standing instructions, such as `AGENTS.md` files and tool-specific instruction or rule files.
State what an agent cannot infer from the code and its standard tooling: the exact commands to build and check, prohibited actions, and conventions the code does not make evident.
Do not copy what the repository already shows, such as directory listings, dependency lists, or configuration values, because the copy goes stale.
Link to the document, contract, or skill that owns a requirement or procedure instead of restating it.

Make every command, path, file, and link that an instruction file names exist and work from the stated working directory.
Update or remove an instruction in the same change that renames, moves, or removes what it names.

A nested instruction file may add or narrow instructions for its directory.
When a nested file replaces an ancestor's instruction, it names the instruction it replaces; an unstated contradiction between files that apply to the same path violates this contract.

Write every instruction as visible text in the file itself.
Invisible characters, bidirectional control characters, instructions inside comments that rendered views hide, and instructions carried only by an image violate this contract.
Never direct agents to fetch and follow instructions from a location outside version control, because those instructions change without review.
Links to external references are allowed as background, such as a language specification or a pinned standard.

Violation: an instruction to run `scripts/check` remains after the change that renamed that script to `scripts/verify`.
Violation: a Markdown comment that rendered views hide tells agents to skip the test suite.
Allowed: a package's instruction file says it replaces the root test command for that package and names the command it uses instead.

## Checks

Run each command an instruction file names from its stated working directory, and resolve each path and link.
Search instruction files for invisible and bidirectional control characters, comments, and images.
For a path covered by several instruction files, read them together and confirm that every contradiction names the instruction it replaces.
For each rename, move, or removal in a change, search instruction files for the old name.
