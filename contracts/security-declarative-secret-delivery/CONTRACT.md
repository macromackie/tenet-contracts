---
name: security-declarative-secret-delivery
message: Declare every deployment and runtime secret binding in one versioned manifest, deliver values directly from the central secret vault without plaintext scripts, and enforce manifest parity in CI.
requires-tenet: 0.11.0
---

## Rules

Declare every deployment environment and runtime host secret binding in one versioned manifest that maps each destination binding name to its authoritative secret identifier in the central secret vault.
Store only target identifiers, binding names, and vault secret references in the manifest, never secret values, encrypted blobs, or credential-bearing URLs.
Support both single-environment and multi-environment deployment targets explicitly in the manifest so every protected environment declares its own bindings.
Keep every binding name distinct within its deployment environment or runtime target.
Deliver secret values directly from the central secret vault to deployment environments and runtime hosts through an approved server-side sync flow, never through operator scripts that read plaintext values locally and push them over provider APIs.
Commit no ad-hoc secret synchronization script that reads plaintext credentials from local files or vaults and writes them to deployment or runtime targets.
Bind runtime secrets in infrastructure definitions by reference or inherited binding rather than passing secret values through infrastructure state or variables.
Keep every workflow secret reference and every inherited runtime secret binding declared in the manifest for its target, and remove retired bindings from both the manifest and live targets in the same change.
Run the repository's secret manifest checker on every change to verify manifest structure, workflow secret parity, runtime binding parity, and absence of ad-hoc sync scripts; a repository may use the checker under `assets/` with its declared policy.
Reconcile live deployment environments and runtime hosts against the manifest after every manifest or credential change, and prune undeclared live bindings rather than leaving orphaned secrets behind.

Violation: a deployment workflow reads `secrets.BILLING_API_KEY` without declaring `BILLING_API_KEY` in the repository's secret manifest, or a repository commits `scripts/sync-secrets.sh` to push plaintext values.
Allowed: `infra/secrets.manifest.json` declares every workflow and runtime secret binding by vault reference, CI verifies parity against every workflow and inherited runtime binding, and an approved server-side sync reconciles live targets.

## Checks

Run the checker in this contract's `assets/` folder from the repository root with the repository's secret delivery policy, where its runtime can run.
Inspect every deployment workflow and infrastructure definition to confirm that each secret reference and inherited runtime binding appears in the manifest and that no secret value enters infrastructure state.
Confirm that no committed script reads plaintext secrets to push them to deployment environments or runtime hosts, and that the manifest holds no secret values.
Confirm that every manifest or credential change reconciles live targets to zero missing and zero orphaned bindings.
