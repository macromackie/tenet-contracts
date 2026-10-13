---
name: library-contract-generality
message: Keep every library contract usable and checkable in a repository that has never seen its sources.
---

## Rules

Write each rule so a team with a different product, stack, and vendors can follow and check it.
Never name a company, internal product or service, person, private repository, path, issue, pull request, incident, or internal command.
Name a language, framework, vendor, or tool only in a contract whose name carries it.
Replace a number that is one team's choice, such as a timeout, size limit, retry count, or lifetime, with a requirement to declare a bounded value.
Keep a number that a cited standard or protocol defines.
Use neutral example nouns such as orders, invoices, accounts, documents, and jobs.
Publish a rule only when it has a reason that holds outside the project it came from.
When source projects disagree, publish one requirement and leave each differing variant to its source as a local adaptation.
Do not require a checker, command, or file layout that the library does not ship.

## Checks

Run `python3 scripts/lint-contracts.py` from the repository root.
Search changed contracts for company, product, vendor, and tool names, and compare each technology word with the contract's name.
Could a team on a different stack follow and check every changed rule?
Does each number in a changed rule come from a standard or protocol rather than one team's choice?
