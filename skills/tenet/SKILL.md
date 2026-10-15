---
name: tenet
description: Use Tenet to discover repository contracts, assess code and changes, and record a conclusion for each contract. Use when reviewing code governed by .contracts or working with the Tenet CLI.
---

# Tenet

Review against the complete English contracts, including scope and exceptions. You own the final judgment. Model answers and generated descriptions help investigate requirements; they do not replace them. Keep review within the requested scope.

## Review loop

These commands need Tenet 0.10.0 or later.

1. Run `tenet check --base BASE` with the actual comparison commit, or `tenet check` for the whole repository. It captures staged, unstaged, and untracked changes, asks the model, and appends a revision to `.tenet/`. The review stays on the commit `BASE` resolved to, so committing the change keeps it. After `tenet contracts add` or `update` changes a contract, check it with `tenet check --contract NAME` and no `--base`.
2. Run `tenet status`. It lists each contract as settled or pending, suggests the most likely violation to read first, and never calls a model or writes state.
3. For each pending contract, read `tenet show NAME`, or `tenet show --pending` for all of them with their shared change once: the model's answer, scoped files, earlier records, changes since an outdated one, the conclusions that fit, the complete contract, and the change. When `status` attributes a row to an earlier check's paths, pass them too: `tenet show NAME PATH ...`.
4. Investigate, then record what the code shows: `tenet record NAME --conclusion CONCLUSION --evidence PATH:START-END -m "what those lines show"`. Cite lines of the current files the check assessed. In a diff, a favorable conclusion must cite a line the change wrote or one beside it; `show` lists them. Disputing the model's `failed` requires evidence in a file it flagged.
5. Repeat until `tenet status` no longer exits 4.

With several pending contracts, give each to its own subagent with `tenet show NAME`; records for different contracts do not conflict. A favorable model conclusion settles a contract, but it is still a model judgment: read every contract in `tenet contracts list --base BASE --json`, including changed or removed contracts. Diff review assumes base compliance; a new or strengthened requirement needs review across its scope, so a contract the diff adds or edits stays pending as `contract_changed` until recorded. When the diff changed none of its files, `record` accepts a favorable conclusion only after `tenet check --contract NAME` is settled as `verified`.

A record is bound to the exact code it judged. Editing a scoped file makes its contract pending and `record` refuses it until the next `check`; then `show` gives the diff since the earlier record. When evidence stays unavailable, record `unresolved` and name the missing fact. Never record a conclusion only to stop a hook.

## Investigate

Follow responsibilities and relationships across the before and after source. For a change spanning owners, briefly identify what moved, its source locations, and any unknown premise. Inspect unchanged callers or implementations that determine the effect. Consider both which requirements the change affects and where each scoped requirement could be affected. A narrow negative answer cannot dismiss a broader relationship.

Use ordinary search, ast-grep, and deterministic checks where they answer the question. Before recording a failure, trace the reachable behavior and the violated clause. Read the caller, guard, transaction, or dependency semantics that could disprove it. Syntax and names alone do not establish identity, ordering, or authority. Preserve concrete defects and distinguish unavailable evidence from a demonstrated failure.

Ask the model again only for a question that remains useful after inspection. `tenet check --base BASE --contract NAME --context HELPER` adds supporting source to one contract within the same review, and `--context HELPER:START-END` supplies only those lines of a large file; positional paths narrow a check without replacing broader results for the same base. `--context` adds evidence without expanding the selected claim. An unchanged rerun reuses the earlier answer; `--fresh` samples the model again but adds no verification.

For external composition, `tenet export PATH --base BASE --context HELPER` exports source and contracts offline. Keep before/after references intact. Optional `ev-grep 'QUESTION' --state state.json --json` assesses one focused JSON value, limited to 64 KiB. Select the facts needed for that question; do not send an entire packet by default. Describe omissions and verify generated claims against source.

## Results

`check` and `status` exit 0 when every contract is settled without a violation, 1 for a recorded failure, 2 for input or execution errors, 3 for a recorded `unresolved`, and 4 while any contract is pending, including failed requests and uncertainty. When a request failed, rerun the check if its `failure` is `retryable`; the rerun sends only the failed requests. Exit 0 is favorable only within the reported scope and assumptions. `violation N%` is the model's estimate, not proof; a middling value does not identify its cause. Tenet skips empty, binary, non-UTF-8, and symlinked files, and a file `judged from its patch only` or a reduced combined input had less source to read. Inspect what was left out before relying on a favorable answer. A warning that a selected path is not checked means no contract assessed it, and `No contract governs` lists changed files no contract covers: review those yourself.

Report supported findings, source locations, consequences, and remaining gaps. Distinguish inspected code from executed checks with observed results. Markdown check commands do not execute themselves. Consult `tenet --help` for exact options.
