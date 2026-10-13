---
name: tenet
description: Use Tenet to discover repository contracts, assess code and changes, and investigate contract findings. Use when reviewing code governed by .contracts or working with the Tenet CLI.
---

# Tenet

Review against the complete English contracts, including scope and exceptions. You own the final judgment. Model answers and generated descriptions help investigate requirements; they do not replace them. Keep review within the requested scope.

Start offline: inspect the change and contract inventory with `tenet contracts list --base BASE --json`, then read each scoped document with `tenet contracts view NAME`. Use the actual comparison commit or supplied snapshot. Include untracked files and inspect changed or removed contracts. Diff review assumes base compliance; a new or strengthened requirement needs review across its scope. After `tenet contracts add` or `update` changes a contract, check it with `tenet check --contract NAME` and no `--base`.

Follow responsibilities and relationships across the before and after source. For a change spanning owners, briefly identify what moved, its source locations, and any unknown premise. Inspect unchanged callers or implementations that determine the effect. Consider both which requirements the change affects and where each scoped requirement could be affected. A narrow negative answer cannot dismiss a broader relationship.

Use ordinary search, ast-grep, and deterministic checks where they answer the question. Before asserting a defect, trace the reachable behavior and the violated clause. Read the caller, guard, transaction, or dependency semantics that could disprove it. Syntax and names alone do not establish identity, ordering, or authority. Preserve concrete defects and distinguish unavailable evidence from a demonstrated failure.

Use model assessments only for a question that remains useful after inspection. A focused `tenet check PATH --contract NAME --base BASE --context HELPER --json` can provide another assessment. Preflight it with `--dry-run`; omit options that do not fit the review. `--context` adds evidence without expanding the selected claim. Preserve reports and inspect selected, supporting, and omitted files. Repeating the same request adds no verification.

For external composition, optional `tenet evidence PATH --base BASE --context HELPER` exports source and contracts offline. Keep before/after references intact. Optional `ev-grep 'QUESTION' --state state.json --json` assesses one focused JSON value, limited to 64 KiB. Select the facts needed for that question; do not send an entire evidence packet by default. Describe omissions and verify generated claims against source.

Read nonzero reports: Tenet exits 1 for failures, 2 for input/execution errors, and 3 for uncertainty or incomplete checks. Exit 0 is favorable only within the reported scope and assumptions. Confidence is not proof; an uncertain choice or low score does not identify its cause. Resolve a concrete missing fact when possible, then stop when evidence settles the question or remains unavailable.

Report supported findings, source locations, consequences, and remaining gaps. Distinguish inspected code from executed checks with observed results. Markdown check commands do not execute themselves. Consult `tenet --help` for exact options.
