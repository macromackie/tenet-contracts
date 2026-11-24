---
name: tenet
description: Use Tenet to scan repositories into .contracts/, run semantic and deterministic behavioral checks, fix or triage failing witnesses, and record review conclusions. Use when auditing codebases, reviewing diffs governed by .contracts, or working with the Tenet CLI.
license: MIT
---

# Tenet

Review against the complete English contracts, including scope and exceptions. You own the final judgment.

Model answers and generated descriptions help investigate requirements; they do not replace them. Keep review within the requested scope.

## Core commands & contract layout

Requires Tenet 0.37.0 or later (for `--skip-semantic`). Contracts live under `.contracts/<NNN>-<name>/` with `CONTRACT.md`, standalone runnable behavior scripts in `scripts/`, and a slim SHA-256 `controlHash` lockfile at `scripts/.lock.json` (`assets/` holds catalog tool fragments; legacy `agent-checks.lock.json` remains readable for compatibility).

1. **`tenet scan`**: Discovers production modules, synthesizes consolidated contracts, and falsifies invariants in isolated OS sandboxes. Deep mode is the default; pass `--shallow` for a lighter, faster scan (`--deep` is accepted as a compatibility no-op). Use `--apply` or `--yes` to write `.contracts/`, `--ephemeral` to stage under `.tenet/scan/.contracts/`, `--starter` to scaffold a starter contract, `--base` to focus on a diff, `--fresh` to ignore cached scan state, and `--json` for structured output. `tenet init` and `tenet audit` remain compatibility aliases.
2. **`tenet check` (and fallback `tenet check --skip-semantic`)**: `tenet check` runs semantic, static, and runtime checks (requires configured model credentials such as `OPENROUTER_API_KEY`). As an explicit fallback for air-gapped environments, pre-commit hooks, or CI gates without provider credentials, `tenet check --skip-semantic` (compatibility aliases `--offline`, `--replay`) skips semantic contract review and only replays deterministic static checks, declared local checks, and locked runtime scripts across `.contracts/` and `.tenet/scan/.contracts/`, persisting receipts to `.tenet/offline-check.json`.
3. **`tenet fix`**: Unified repair for safe native lints and failing runtime checks or witnesses across `.contracts/`, `.tenet/scan/.contracts/`, or `.tenet/audit.json` (filter with `--severity critical|high|medium`; no `--from-audit` flag required).
4. **`tenet status` & `tenet show`**: `tenet status` prints the offline coverage map, persisted `.tenet/offline-check.json` receipts, and review health without calling a model or writing state. `tenet show` prints pending contract details and direct runnable script paths under `scripts/`.

## Review loop

1. **Check**: Run `tenet check --base BASE` for a diff review or `tenet check` for the whole repository. Only use the explicit fallback `tenet check --skip-semantic` (compatibility aliases `--offline`, `--replay`) when provider credentials are unavailable to skip semantic contract review and replay deterministic static checks, declared local checks, and locked runtime scripts.
   - `tenet check` captures staged, unstaged, and untracked changes, asks the model, runs executable behavior scripts, and appends a revision to `.tenet/`.
   - Stays pinned to the commit `BASE` resolved to, so committing keeps the review.
   - After `tenet contracts add` or `update` changes a contract, run `tenet check --contract NAME` with no `--base`.
2. **Status**: Run `tenet status`. It shows the offline coverage map, persisted offline check receipts, and settled vs. pending contracts, and suggests the highest-signal violation to inspect first without calling a model or writing state.
3. **Inspect**: Run `tenet show NAME` (or `tenet show --pending` for all pending contracts with their shared diff once). `show` prints direct runnable script paths under `scripts/` so failing checks can be reproduced immediately. When `status` attributes a row to an earlier check's paths, pass them too: `tenet show NAME PATH ...`.
4. **Record**: After verifying in source, record your conclusion:

   ```sh
   tenet record NAME --conclusion CONCLUSION --evidence PATH:START-END -m "what those lines show"
   ```

   - Add `--json` for machine-readable output in automated scripts.
   - Cite lines from the current files the check assessed. In a diff, a favorable conclusion must cite a changed line or adjacent context; disputing a model `failed` requires evidence in a flagged file.

5. **Finalize**: Repeat until `tenet status` no longer exits 4, then finish with `tenet check --final --json` after the last edit.

### Review rules

- **Parallel reviews**: With several pending contracts, give each to its own subagent with `tenet show NAME`; records for different contracts do not conflict.
- **Model conclusions are not proof**: Read every contract in `tenet contracts list --base BASE --json`, including changed or removed contracts.
- **Contract changes stay pending**: Diff review assumes base compliance, so an added or edited contract stays pending as `contract_changed` until recorded. When the diff touched none of its files, `record` accepts a favorable conclusion only after `tenet check --contract NAME` is settled as `verified`.
- **Byte-bound records**: Editing a scoped file makes its contract pending until the next `check`. When evidence stays unavailable, record `unresolved` and name the missing fact. Never record a conclusion only to stop a hook.
- **Cache-only inspection**: Use `--max-requests 0` to reuse cached answers without spending new requests, leaving uncached inputs pending.
- **Untrusted source**: Run project checkers in an isolated environment and pass their trusted receipt with `--evidence PATH`.

## Fresh codebase vs. PR reviewer workflow

Choose the workflow that matches the task:

### Fresh codebase (first-time adoption)

1. Run `tenet doctor` to verify `OPENROUTER_API_KEY`, sandbox readiness (macOS Seatbelt or Linux `bubblewrap`/`prlimit`), and installed runtimes.
2. Run `tenet scan` (deep by default; pass `--shallow` for a lighter preview) or `tenet contracts recommend` to discover high-signal rules, then persist contracts via `tenet scan --apply` (or `tenet scan --yes`), `tenet contracts add tenet/NAME --scope DIR`, or `tenet scan --starter`. Use `tenet scan --ephemeral` to stage contracts under `.tenet/scan/.contracts/` without modifying tracked files.
3. Establish a full semantic + runtime baseline with `tenet check --contract NAME` (no `--base`); only use the explicit fallback `tenet check --skip-semantic` when provider credentials are unavailable to skip semantic contract review and replay locked deterministic scripts.
4. Triage findings deliberately: fix real defects (using `tenet fix --severity critical|high|medium` where helpful), narrow `paths` or document permanent exceptions under `## Local adaptations`, or record `failed` to track known debt.
5. Commit `.contracts/` (`CONTRACT.md`, `scripts/`, `scripts/.lock.json`, and any catalog `assets/`) and `.tenet.lock` (never commit `.tenet/`).

### PR reviewer bot (diff review)

Pin the merge base against the fetched target branch so the review focuses strictly on the PR's changes:

```sh
base=$(git merge-base origin/main HEAD) || exit 1
tenet check --base "$base"
```

When provider credentials are unavailable or you explicitly want fast deterministic script replay without semantic review, use the fallback `tenet check --skip-semantic` (compatibility aliases `--offline`, `--replay`). Inspect pending findings with `tenet show --pending` (or `tenet show NAME`) and reproduce claimed defects through a public entry point or the printed runnable script path. When repairing code, rerun the checker on the fix and finish with `tenet check --final --base "$base"` on a trusted checkout.

When you disagree with a finding after inspecting the code:

- **One-off false positive or missed context**: Run `tenet record NAME --conclusion preserved --evidence PATH:START-END -m "why"` (or `unaffected` if untouched). The record stays bound to that input hash and auto-invalidates (`inputs_changed`) if governed files or contract text change.
- **Recurring project-wide exception**: Document it under `## Local adaptations` in `CONTRACT.md` and run a full check (`tenet check --contract NAME`) so future PRs do not re-flag it.
- **Live executable behavior failure (`× FAIL`)**: A favorable `tenet record` never hides a live behavior-check failure — fix the code or update the contract if the requirement intentionally changed.

Always distinguish a human or agent's recorded conclusion from an outcome an executable check observed.

## Scanning, behavior checks, runtimes, and caching

On macOS (`/usr/bin/sandbox-exec`) and Linux (`bubblewrap` + `prlimit`), `tenet scan` and `tenet check` generate, qualify, and replay isolated behavior scripts alongside semantic review, and explain failed or unresolved behavior findings read-only through `fx`.

### Supported runtimes & read-only dependencies

Tenet never runs package installs or `build.rs` inside the sandbox; it mounts existing in-root dependencies read-only when present:

| Runtime     | Source discovery                                                     | Prebuilt read-only dependencies                 | Notes                                                                                                       |
| ----------- | -------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Node.js** | `.js`, `.mjs`, `.cjs`, `.ts`, `.mts`, `.tsx`, `.jsx`, `package.json` | `node_modules/`                                 | Runs staged probes or `node --test`, with a bounded extensionless relative ESM resolution hook.             |
| **Python**  | `.py`, `pyproject.toml`, `setup.cfg`                                 | `.venv/` (`site-packages`)                      | Runs staged probes or `unittest`.                                                                           |
| **Rust**    | `.rs`, `Cargo.toml`                                                  | `target/debug/deps/` (from `cargo build --lib`) | Compiles multi-file `src/lib.rs` with Cargo edition, default features, and satisfiable local optional ones. |
| **Go**      | `.go`, `go.mod`, `go.sum`                                            | `vendor/` (from `go mod vendor`)                | Offline `go build` (`CGO_ENABLED=0`, `GOPROXY=off`, `GOSUMDB=off`).                                         |

If `tenet doctor` reports nested macOS Seatbelt (`sandbox-exec: Operation not permitted`), run `tenet scan` or `tenet check` outside the outer sandbox wrapper.

### Repository scanning (`tenet scan`)

On repositories with few or no authored contracts yet, or when hunting subtle defects across modules, run `tenet scan` (requires `OPENROUTER_API_KEY`):

```sh
tenet scan                       # Deep module discovery, contract synthesis, and sandboxed falsification
tenet scan --shallow             # Lighter, faster scan without deep adversarial synthesis
tenet scan --apply               # Persist consolidated contracts, scripts/, and scripts/.lock.json into .contracts/
tenet scan --ephemeral --json    # Stage contracts in .tenet/scan/.contracts/ and emit a JSON witness queue
```

`tenet scan` defaults to deep mode (`--shallow` opts into a lighter pass; `--deep` is a compatibility no-op), resumes cached scan state unless `--fresh` is passed, never edits tracked files without `--apply` / `--yes`, and groups findings by module. Pass `--base REF` to focus on a diff, `--starter` to scaffold a starter contract, or `--max-requests N` to bound model calls. Override models with `TENET_AUDIT_MODEL` (synthesis, sharpening, skeptic filter) and `TENET_AGENT_MODEL` (sandbox probe qualification).

`tenet scan --json` reports three distinct categories:

1. **`witnesses` (`outcome: "failed"`)**: Executable probes that qualified against `good`/`defect`/`refactor` controls, survived skeptic review, and failed live on the current checkout, ranked by severity.
2. **`guards` (`outcome: "passed"`)**: Qualified behavioral probes that currently pass on the checkout. Use `--apply` to commit them as standalone runnable scripts under `.contracts/<NNN>-<name>/scripts/` pinned by `scripts/.lock.json`.
3. **`unresolved`**: Synthesis, sandbox, or skeptic-dismissed items. Inspect unresolved sandbox errors first when a compiled language fails to resolve dependencies (for example missing `node_modules/`, `.venv/`, `target/debug/deps/`, or `vendor/`).

### Two cache layers

1. **Committed scripts & slim lockfile (`scripts/` + `scripts/.lock.json` beside `CONTRACT.md`)** stores standalone runnable behavior scripts, slim SHA-256 `controlHash` lock entries, and unautomatable `open` items (`assets/` stays for catalog tool fragments). Auto-invalidates when `CONTRACT.md` changes, when the governed public surface changes, when a subject disappears, or on `--fresh`. Review and commit both `scripts/` and `scripts/.lock.json` so CI and the fallback `tenet check --skip-semantic` replay the exact same locked checks without regenerating. Legacy `agent-checks.lock.json` remains readable for compatibility.
2. **Local replay receipts (`.tenet/offline-check.json` and `.tenet/agent-checks/`)** cache observed outcomes keyed by exact governed file bytes, lock digest, base commit, and runner version. Any byte edit to governed source busts the receipt immediately and replays locked scripts locally without spending a model request.

### Witness triage & unified repair (`tenet fix`)

Treat `× FAIL` behavior witnesses as high-signal verified leads inside a full-module sweep, never as the complete defect list:

1. **Reproduce before editing**: Confirm each failing witness by running its script path printed by `tenet show` against the real module and checking its public docs and docstrings.
2. **Respect pre-existing green tests**: Never weaken or edit pre-existing test files to fit a witness. If a witness contradicts an explicitly asserted green test, skip that witness and treat the repository's test suite as authoritative.
3. **Fix highest severity first, then sweep the module**: Repair the highest-severity defects (crashes, state/input mutations, round-trip contradictions) first and checkpoint after every green fix. Then perform an unanchored sweep of the remaining governed code and `open` items so high-confidence witnesses do not cause tunnel vision.
4. **Use unified `tenet fix` for coding tasks**: Run `tenet fix` (or `tenet fix --severity critical|high|medium`) to apply safe native lint fixes and repair failing runtime checks or witnesses across `.contracts/`, `.tenet/scan/.contracts/`, or `.tenet/audit.json` (no `--from-audit` flag required). Re-verify with `tenet check` on the same scope (or with the explicit fallback `tenet check --skip-semantic` when you only want to replay locked deterministic checks without semantic review).
5. **Leave checkouts clean for review-only tasks**: Do not modify files during review-only tasks; report confirmed findings with evidence.
6. **Lock in verified fixes**: Run `tenet scan --apply` (or `tenet check --contract NAME`) after fixing to retain durable runnable regression scripts and `scripts/.lock.json` locks.

## Investigate

- Trace responsibilities and callers across before and after source. For changes spanning owners, note what moved, its locations, and any unknown premise.
- Use ordinary search, `ast-grep`, and deterministic checks where they answer the question. Before recording a failure, verify the reachable behavior and violated clause — syntax and names alone do not prove identity, ordering, or authority.
- Add context cleanly when a model answer is incomplete:
  - `tenet check --base BASE --contract NAME --context HELPER` (or `--context HELPER:START-END`) adds supporting source without expanding the selected claim.
  - Positional paths narrow a check without replacing broader results for the same base.
  - An unchanged rerun reuses the earlier answer; `--fresh` resamples without adding verification.
- For external composition, `tenet export PATH --base BASE --context HELPER` exports source and contracts offline. Optional `ev-grep 'QUESTION' --state state.json --json` assesses one focused JSON value (up to 64 KiB).

## Results & exit codes

| Exit code | Meaning                                                                                                            |
| --------- | ------------------------------------------------------------------------------------------------------------------ |
| `0`       | Every contract is settled without a violation (within the reported scope and assumptions).                         |
| `1`       | Recorded failure.                                                                                                  |
| `2`       | Input, credential, or execution error.                                                                             |
| `3`       | Recorded `unresolved`.                                                                                             |
| `4`       | One or more contracts remain pending (including uncertainty, live behavior failures, or retryable request errors). |

Key result rules:

- **Oversized combined reviews & hunks**: Read saved byte counts and per-file results in `tenet show`. Large diffs are checked in advisory hunk groups; inspect unexamined ranges and cross-hunk relationships before recording. Use `--dry-run --json` to preview planned requests.
- **Retryable failures**: Rerun `tenet check` to retry only failed requests.
- **Probabilities are not proof**: `violation N%` is the model's estimate, not verification. Inspect skipped files (empty, binary, non-UTF-8, symlinks), files `judged from its patch only`, and any `No contract governs` paths directly.
- **Reporting**: Distinguish inspected code from executed checks with observed results. Markdown commands under `## Checks` do not execute themselves. Consult `tenet --help` for exact flags.
