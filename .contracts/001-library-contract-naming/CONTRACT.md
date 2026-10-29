---
name: library-contract-naming
message: Name each library contract area first, followed by every technology its rules depend on.
---

## Rules

Name every library contract `<area>-[<technology>-]<subject>[-<aspect>]` in lowercase kebab case.
Start with one area from the closed list in the README's naming guide, and add an area only through a changelog entry that defines it.
Choose the area by the concern a reviewer checks, not by the directory or team that first wrote the contract.
A name without a technology word promises rules that hold in every language, framework, and vendor.
Add a technology word after the area when any rule depends on that technology, such as `ui-react-` or `api-fastapi-`.
When rules depend on several technologies, name each of them.
Name the subject for the concern being checked, never for a virtue such as quality, conventions, or best practices.
End with a reserved suffix in its fixed form when one fits: `-boundaries`, `-apis`, `-checks`, `-lifecycle`, `-ownership`, or `-curation`.
Prefer a longer explicit name to an abbreviation; abbreviate only established acronyms such as api, ci, llm, sql, and ui.
Keep each contract's folder name identical to its `name` field.

Rename a published contract only in a major release, and name its replacement in the changelog.
Never reuse a removed contract's name for a different requirement.

## Checks

Run `uv run --script scripts/lint-contracts.py` from the repository root.
Could a reader predict a new contract's concern and stack from its name alone?
Does every technology a changed contract's rules mention appear in its name?
Does the changelog name the replacement for each renamed or removed contract?
