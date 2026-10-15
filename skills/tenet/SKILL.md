---
name: tenet
description: Use Tenet to discover repository contracts, assess code and changes, and record a conclusion for each contract. Use when reviewing code governed by .contracts or working with the Tenet CLI.
---

# Tenet

Review against the complete English contracts, including scope and exceptions. You own the final judgment. Model answers and generated descriptions help investigate requirements; they do not replace them. Keep review within the requested scope.

## Review loop

These commands need Tenet 0.8.0 or later.

1. Run `tenet check --base BASE` with the actual comparison commit, or `tenet check` for the whole repository. It captures staged, unstaged, and untracked changes, asks the model, and appends a revision to `.tenet/`. After `tenet contracts add` or `update` changes a contract, check it with `tenet check --contract NAME` and no `--base`.
2. Run `tenet status`. It lists each contract as settled or pending and never calls a model or writes state.
3. For each pending contract, read `tenet show NAME`: the model's answer, scoped files, earlier records, changes since an outdated one, the conclusions that fit, the complete contract, and the change.
4. Investigate, then record what the code shows: `tenet record NAME --conclusion CONCLUSION --evidence PATH:START-END -m "what those lines show"`. Cite lines of the current files.
5. Repeat until `tenet status` no longer exits 4.

With several pending contracts, give each to its own subagent with `tenet show NAME`; records for different contracts do not conflict. A favorable model conclusion settles a contract, but it is still a model judgment: read every contract in `tenet contracts list --base BASE --json`, including changed or removed contracts. Diff review assumes base compliance; a new or strengthened requirement needs review across its scope.

A record is bound to the exact code it judged. Editing a scoped file makes its contract pending and `record` refuses it until the next `check`; then `show` gives the diff since the earlier record. When evidence stays unavailable, record `unresolved` and name the missing fact. Never record a conclusion only to stop a hook.

## Investigate

Follow responsibilities and relationships across the before and after source. For a change spanning owners, briefly identify what moved, its source locations, and any unknown premise. Inspect unchanged callers or implementations that determine the effect. Consider both which requirements the change affects and where each scoped requirement could be affected. A narrow negative answer cannot dismiss a broader relationship.

Use ordinary search, ast-grep, and deterministic checks where they answer the question. Before recording a failure, trace the reachable behavior and the violated clause. Read the caller, guard, transaction, or dependency semantics that could disprove it. Syntax and names alone do not establish identity, ordering, or authority. Preserve concrete defects and distinguish unavailable evidence from a demonstrated failure.

Ask the model again only for a question that remains useful after inspection. `tenet check --base BASE --contract NAME --context HELPER` adds supporting source to one contract within the same review; positional paths start a separate review. `--context` adds evidence without expanding the selected claim. An unchanged rerun reuses the earlier answer; `--fresh` samples the model again but adds no verification.

For external composition, `tenet export PATH --base BASE --context HELPER` exports source and contracts offline. Keep before/after references intact. Optional `ev-grep 'QUESTION' --state state.json --json` assesses one focused JSON value, limited to 64 KiB. Select the facts needed for that question; do not send an entire packet by default. Describe omissions and verify generated claims against source.

## Results

`check` and `status` exit 0 when every contract is settled without a violation, 1 for a recorded failure, 2 for input or execution errors, 3 for a recorded `unresolved`, and 4 while any contract is pending, including model failures and uncertainty. Exit 0 is favorable only within the reported scope and assumptions. Confidence is not proof; an uncertain choice or low score does not identify its cause.

Report supported findings, source locations, consequences, and remaining gaps. Distinguish inspected code from executed checks with observed results. Markdown check commands do not execute themselves. Consult `tenet --help` for exact options.
