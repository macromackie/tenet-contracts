---
name: code-domain-vocabulary
message: Name each domain concept with its one glossary word in code, output, documentation, and interface text, and never with a word it replaced.
---

## Rules

Apply these rules to identifiers, comments, command and log output, documentation, and user interface text.
Declare a glossary that gives each domain concept one word, states what the word means, and lists the words it replaced.
Keep the glossary in one place that reviewers read beside this contract, such as the copy's local adaptations or a contract that extends this one.

Name each glossary concept with its word, and give no second word to the same concept.
Never use a replaced word for the concept it was replaced for: after `invoice` replaces `bill`, an identifier, field, command, log line, heading, label, or comment that calls an invoice a bill violates this rule.
A replaced word keeps its ordinary sense, so a linked list keeps its `head` after `owner` replaces `head` for an account's owner.
Build compound names from glossary words, so an invoice's total is `invoiceTotal`, never `billTotal`.
Give a collection one name in every message, API, and output that carries it, such as `lineItems` for an invoice's lines everywhere, never `items` in one response and `lines` in another.

Configure the repository's lint to reject every identifier named exactly a replaced word that has no ordinary sense as an identifier.
Leave a replaced word that has an ordinary sense as an identifier, such as the `head` of a linked list or a regular expression's `match`, off that denylist, and check its uses in review.

## Checks

Run the repository's lint and confirm its identifier denylist holds every replaced word that has no ordinary sense as an identifier.
Search the governed files for each replaced word, including compounds, comments, and documentation, and confirm each match uses the word in its ordinary sense.
For each changed name, comment, message, or label, does a replaced word that the denylist leaves out stand for its glossary concept?
Does each concept a change introduces have a glossary word, and does each compound name the change adds use glossary words?
