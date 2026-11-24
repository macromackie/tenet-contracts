# Secret delivery manifest check

Copy `secret-delivery.json` into the repository as `.config/secret-delivery.json` and declare the repository's own
paths and patterns. Run from the repository root, replacing the installed contract path:

```bash
uv run --script .contracts/001-security-declarative-secret-delivery/assets/uv/check-secret-manifest.py \
  --root . --config .config/secret-delivery.json
```

The script requires Python 3.14 or later and has no package dependencies. `secret-delivery.schema.json` describes the
policy:

- `manifestPath` names the versioned secret manifest file relative to the repository root, such as
  `infra/secrets.manifest.json`.
- `workflowPatterns` lists path patterns for deployment workflow files whose secret references must match the manifest.
- `runtimeBindingPatterns` lists path patterns for infrastructure files whose inherited runtime bindings must match the
  manifest.
- `bannedScriptPatterns` lists path patterns for ad-hoc secret sync scripts that must not exist in the repository.
- `builtinWorkflowSecrets` lists platform-supplied workflow secrets, such as a default job token, that do not belong in
  the manifest.
- `allowedUnusedManifestSecrets` lists declared deployment secrets that are intentionally consumed outside scanned
  workflow files, each with a reason.

The checker validates version 1 single-environment (`environment` and `secrets`) and multi-environment (`environments`)
deployment targets, runtime worker targets, duplicate binding names, forbidden plaintext fields, workflow secret parity,
inherited runtime binding parity, and banned sync scripts.

The command reports every finding and exits unsuccessfully. It changes no files.
