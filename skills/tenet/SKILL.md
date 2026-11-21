---
name: tenet
description: Use Tenet to discover repository contracts, assess code and changes, and record a conclusion for each contract. Use when reviewing code governed by .contracts or working with the Tenet CLI.
license: MIT
---

# Tenet

Review against the complete English contracts, including scope and exceptions. You own the final judgment.

Model answers and generated descriptions help investigate requirements; they do not replace them. Keep review within the requested scope.

## Review loop

Requires Tenet 0.20.0 or later (`tenet check` always requires configured model credentials such as `OPENROUTER_API_KEY`).

1. **Check**: Run `tenet check --base BASE` for a diff review, or `tenet check` for the whole repository.
   - Captures staged, unstaged, and untracked changes, asks the model, runs executable behavior checks, and appends a revision to `.tenet/`.
   - Stays pinned to the commit `BASE` resolved to, so committing keeps the review.
   - After `tenet contracts add` or `update` changes a contract, run `tenet check --contract NAME` with no `--base`.
2. **Status**: Run `tenet status`. It lists settled vs. pending contracts and suggests the highest-signal violation to inspect first without calling a model or writing state.
3. **Inspect**: Run `tenet show NAME` (or `tenet show --pending` for all pending contracts with their shared diff once). When `status` attributes a row to an earlier check's paths, pass them too: `tenet show NAME PATH ...`.
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
2. Run `tenet init` (or `tenet contracts recommend`) to inspect high-signal catalog rules, then adopt 1–3 contracts via `tenet init --yes`, `tenet contracts add tenet/NAME --scope DIR`, or `tenet init --starter`.
3. Establish a baseline with a full check (`tenet check --contract NAME`, no `--base`).
4. Triage findings deliberately: fix real defects, narrow `paths` or document permanent exceptions under `## Local adaptations`, or record `failed` to track known debt.
5. Commit `.contracts/`, `.tenet.lock`, and reviewed `agent-checks.lock.json` files (never commit `.tenet/`).

### PR reviewer bot (diff review)

Pin the merge base against the fetched target branch so the review focuses strictly on the PR's changes:

```sh
base=$(git merge-base origin/main HEAD) || exit 1
tenet check --base "$base"
```

Inspect pending findings with `tenet show --pending` (or `tenet show NAME`) and reproduce claimed defects through a public entry point. When repairing code, rerun the checker on the fix and finish with `tenet check --final --base "$base"` on a trusted checkout.

When you disagree with a finding after inspecting the code:

- **One-off false positive or missed context**: Run `tenet record NAME --conclusion preserved --evidence PATH:START-END -m "why"` (or `unaffected` if untouched). The record stays bound to that input hash and auto-invalidates (`inputs_changed`) if governed files or contract text change.
- **Recurring project-wide exception**: Document it under `## Local adaptations` in `CONTRACT.md` and run a full check (`tenet check --contract NAME`) so future PRs do not re-flag it.
- **Live executable behavior failure (`× FAIL`)**: A favorable `tenet record` never hides a live behavior-check failure — fix the code or update the contract if the requirement intentionally changed.

Always distinguish a human or agent's recorded conclusion from an outcome an executable check observed.

## Behavior checks, runtimes, and caching

On macOS (`/usr/bin/sandbox-exec`) and Linux (`bubblewrap` + `prlimit`), `tenet check` automatically generates, qualifies, and replays isolated behavior checks alongside semantic review, and explains failed or unresolved behavior findings read-only through `fx`.

### Supported runtimes & read-only dependencies

Tenet never runs package installs or `build.rs` inside the sandbox; it mounts existing in-root dependencies read-only when present:

| Runtime     | Source discovery                                                     | Prebuilt read-only dependencies                 | Notes                                                                                                       |
| ----------- | -------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Node.js** | `.js`, `.mjs`, `.cjs`, `.ts`, `.mts`, `.tsx`, `.jsx`, `package.json` | `node_modules/`                                 | Runs staged probes or `node --test`, with a bounded extensionless relative ESM resolution hook.             |
| **Python**  | `.py`, `pyproject.toml`, `setup.cfg`                                 | `.venv/` (`site-packages`)                      | Runs staged probes or `unittest`.                                                                           |
| **Rust**    | `.rs`, `Cargo.toml`                                                  | `target/debug/deps/` (from `cargo build --lib`) | Compiles multi-file `src/lib.rs` with Cargo edition, default features, and satisfiable local optional ones. |
| **Go**      | `.go`, `go.mod`, `go.sum`                                            | `vendor/` (from `go mod vendor`)                | Offline `go build` (`CGO_ENABLED=0`, `GOPROXY=off`, `GOSUMDB=off`).                                         |

If `tenet doctor` reports nested macOS Seatbelt (`sandbox-exec: Operation not permitted`), run `tenet check` or `tenet audit` outside the outer sandbox wrapper.

### On-demand module audits (`tenet audit`)

On repositories with few or no authored contracts yet, run `tenet audit` (requires `OPENROUTER_API_KEY`):

```sh
tenet audit                       # Discover production modules, synthesize contracts, falsify in sandbox
tenet audit src/ --deep --json    # Add adversarial edge-case synthesis and emit a JSON witness queue
tenet audit --save                # Persist verified contracts and pre-qualified pins into .contracts/
```

`tenet audit` resumes from `.tenet/audit.json` unless `--fresh` is passed, never edits tracked files without `--save`, and groups findings by module so you can repair one module at a time without losing context.

### Two cache layers

1. **Committed pin (`agent-checks.lock.json` beside `CONTRACT.md`)** stores qualified checks, concrete controls, and unautomatable `open` items. Auto-invalidates when `CONTRACT.md` changes, when the governed public surface changes, when a subject disappears, or on `--fresh`. Review and commit it so CI replays the exact same checks without regenerating.
2. **Local replay receipt (`.tenet/agent-checks/`)** caches observed outcomes keyed by exact governed file bytes, pin digest, base commit, and runner version. Any byte edit to governed source busts the receipt immediately and replays frozen checks locally without spending a model request.

### Using witnesses in broad audits

Treat `× FAIL` behavior witnesses as verified starting points, not the complete defect list:

- Fix and re-verify every `× FAIL` witness first, then perform an unanchored sweep of the remaining governed code and `open` items so high-confidence witnesses do not cause tunnel vision.
- For coding tasks, run `tenet fix` to apply supported tool fixes, repair remaining behaviors, and rerun `tenet check` with the same scope.
- For review-only tasks, leave the checkout untouched and report confirmed findings.

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
