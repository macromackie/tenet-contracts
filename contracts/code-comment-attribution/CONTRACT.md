---
name: code-comment-attribution
message: Explain source behavior without attributing it to repository contracts or review tools.
---

## Rules

Apply these rules to maintained production code, tests, and examples, including their comments and inline documentation.
Keep requirements in guidance documents; source comments explain behavior and why it matters to callers.
Do not name a repository contract's number, name, or path as the reason for source behavior.
Do not name a review tool, automated reviewer, or review finding as the reason for source behavior.
Do not add attribution comments such as `// Contract 011: keep the session cookie host-only`, `# orders-retention-lifecycle: purge closed orders`, or `// See the route-paths contract`.
A comment that names a contract this way is an attribution even when it never uses the word contract and even when it also states a reason.

Explain the external constraint, failure consequence, or caller dependency that makes a behavior matter, for example `// A failed revocation returns focus to its invoker so the user can retry`.
When removing an attribution, keep the behavioral reason it carried, or remove the comment when the code already makes that reason clear.
A comment that explains behavior without naming a contract or review tool complies, including one that cites an incident, issue, or design specification as the source of that behavior.

Contract authoring, discovery, review, and check tooling may refer to contracts in its implementation, diagnostics, and fixtures when those references perform the tool's purpose.
Guidance documents, API or protocol contracts, and ordinary domain uses of the word "contract", such as a comment about the response contract that clients rely on, are outside these rules.
Generated and copied third-party source follows its own generation or copying policy.

## Checks

Search changed source for common attribution forms, such as a contract number, a contract folder path, or a review tool's name, and inspect each match against the tooling exception.
Read changed comments directly, because a search misses attributions written in other words.
Where an attribution was removed, does a behavioral explanation remain wherever the code alone does not make the reason clear?
Run the affected package checks after editing source.
