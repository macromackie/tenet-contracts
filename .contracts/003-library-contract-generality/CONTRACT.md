---
name: library-contract-generality
message: Keep every library contract usable and checkable in a repository that has never seen its sources.
---

## Rules

Write each rule so a team with a different product, stack, and vendors can follow and check it.
Never name a company, internal product or service, person, private repository, path, issue, pull request, incident, or internal command.
Name a language, framework, vendor, or tool only in a contract whose name carries it.
A contract whose name carries no tool may ship files under `assets/<tool>/` that configure any tool to enforce its stated rules, while its own text still names no tool.
Replace a number that is one team's choice, such as a timeout, size limit, retry count, or lifetime, with a requirement to declare its maximum or minimum.
When a file under `assets/` enforces that number, set its default there, and let the text state the default as a value a repository may override.
A shipped file may set a different value for one kind of code, such as components that return markup, when the text names that kind and its reason.
Keep a number that a cited standard or protocol defines.
Use neutral example nouns such as orders, invoices, accounts, documents, and jobs.
Publish a rule only when it has a reason that holds outside the project it came from.
When source projects disagree, publish one requirement and leave each differing variant to its source as a local adaptation.
Choose each rule's form because it is clean, readable, consistent with other library rules, easily enforced by a lint or an agent reading code, and needs the fewest exceptions.
Never choose a form because most code in the source projects already follows it; count the code a form would change only to plan its rollout.
Do not require a checker, command, or file layout that the library does not ship.

## Checks

Run `uv run --script scripts/lint-contracts.py` from the repository root.
Search changed contracts for company, product, vendor, and tool names, and compare each technology word with the contract's name.
Does each changed file under `assets/` enforce only rules that its contract's text states?
Could a team on a different stack follow and check every changed rule?
Does each number in a changed rule come from a standard or protocol, or from a declared maximum or minimum whose default a shipped file sets?
Does the pull request for any added or tightened rule give how much code already follows a form as a reason for choosing it?
