# Changelog

Each release lists every changed contract or skill under one class. A Tightened or Removed entry makes a major
release, an Added or Loosened entry a minor release, and Clarified entries alone a patch release.

## v4.1.0

### Added

- Contract `code-domain-vocabulary`: a declared glossary gives each domain concept one word, which identifiers,
  comments, output, documentation, and interface text use instead of the words it replaced, and the lint denies each
  replaced word that has no ordinary sense as an identifier.

## v4.0.1

The `tenet` skill follows Tenet 0.10.0's review loop and needs Tenet 0.10.0 or later.

### Clarified

- `tenet`: a failed request leaves its contract pending, and a check with a `retryable` failure is rerun; `--context`
  accepts line ranges of a large file; changed files that no contract governs need the reviewer's own review.

## v4.0.0

The `tenet` skill follows Tenet 0.9.0's review loop and needs Tenet 0.9.0 or later.

### Tightened

- `tenet`: disputing a model `failed` cites a file the model flagged, and a contract the diff adds or edits stays
  pending until recorded. The skill reads `violation N%` instead of confidence, keeps a review across commits on its
  base, and inspects skipped files and source left out to fit the input limit before relying on a favorable answer.

### Added

- 5 contracts:
  - code: `code-python-exception-propagation`, `code-python-none-guards`.
  - context: `context-agent-instruction-files`.
  - security: `security-interpreter-injection`.
  - test: `test-assertion-integrity`.
- `scripts/lint-contracts.py` rejects invisible, bidirectional, and other hidden characters and HTML comments in
  Markdown files, and warns when a rule consists of an image or a link.

### Clarified

- `tenet-contract-curation` explains how to word rules for a model reviewer: one concern per contract, explicit
  violation forms and allowances, consistent examples, and no vague qualifiers. It also shows how to test new wording
  against labeled clean and violating patches, including held-out ones, with Tenet 0.8.0 or later.
- `tenet-contract-curation` suggests a `paths` frontmatter list for a contract that applies to only some files in its
  folder, such as one language's source, with `!` globs to leave files such as a lockfile out. Tenet 0.9.0 or later
  reads `paths`.
- `data-alembic-revision-history` states that it governs revision files and the migration runner, counts every revision
  the target branch already holds as merged, and names renaming to a new identifier and in-place edits, such as a
  changed column type, server default, index, or data statement, as the forms its rules forbid.
- `code-comment-attribution` shows that a bare contract name heading a comment is an attribution, and states that a
  behavioral comment citing an incident, issue, or design specification complies.
- `test-curation` states that a change touching no test, fixture, test report, or test-only dependency leaves it
  unaffected, and that removing or skipping a test, case, or assertion deletes coverage.
- `api-fastapi-wire-schemas-and-errors` applies its purity rule to the conversion function itself; the service that
  calls it may still call clients before or after, such as after its commit.

## v3.0.0

The `tenet` skill follows Tenet 0.8.0's review loop and needs Tenet 0.8.0 or later. No contract changed; installing
contracts still needs Tenet 0.7.0 or later.

### Tightened

- `tenet`: a review now ends only when `tenet status` stops exiting 4. Each pending contract is settled with
  `tenet record`, citing current lines; a review that only investigated findings no longer completes it. The skill
  reads contracts with `tenet show` and exports with `tenet export`, which replaces `tenet evidence`.

## v2.1.0

Two areas join the closed list: `agent`, for systems that give autonomous agents tools, credentials, memory, and
attributed activity, and `cli`, for command-line programs. Installing contracts still needs Tenet 0.7.0 or later.

### Added

- 14 contracts:
  - agent: `agent-activity-attribution`, `agent-shared-memory`, `agent-tool-authorization`.
  - cli: `cli-command-reference-generation`.
  - data: `data-metric-definitions`.
  - llm: `llm-code-review-publication`.
  - release: `release-public-source-export`.
  - security: `security-delegated-credential-vending`, `security-inbound-webhook-verification`.
  - ui: `ui-component-usage-guidance`, `ui-data-tables`, `ui-keyboard-shortcuts`, `ui-semantic-value-controls`.
  - web: `web-edge-gateway-routing`.

## v2.0.0

Contract names now start with an area, followed by every technology the rules depend on. A name without a technology
word applies to any stack; the README lists the areas. Installing contracts still needs Tenet 0.7.0 or later.

### Removed

- `execution-lifecycle`, renamed `code-execution-lifecycle`. The new contract also gives each request exactly one retry
  owner, records a required external effect's intent and operation identity before starting it, rejects identity reuse
  with different inputs, never replays an uncertain effect unless the external system deduplicates it, and keeps
  cleanup running when its caller fails.
- `ownership-and-boundaries`, renamed `code-ownership-and-boundaries`. The new contract also limits imports to declared
  dependencies and public entry points, consumes other repositories only through versioned artifacts or configured
  endpoints, and keeps test fixtures out of production builds.

To move an installed copy, move its `## Local adaptations` aside, run `tenet contracts remove PATH`, add the new name
with `tenet contracts add`, then restore the adaptations.

### Tightened

- `contract-maintenance`: a link may support a rule but must not replace it; each check names a command and its working
  directory; updates never overwrite local edits. Where proposals live moved to `context-note-curation`, the
  model-assessment and retry-until-approved rules moved to `llm-code-review-evidence`, and the fixture-contract rule
  was dropped.
- `data-and-apis`: keep the revisions that produced a value explicit; keep missing evidence, an unavailable provider,
  and an empty success distinct; never use another service's tables as an integration API. The model-assessment clause
  in its checks moved to `llm-code-review-evidence`.

### Added

- 69 contracts:
  - api: `api-fastapi-resource-layout`, `api-fastapi-route-authorization`, `api-fastapi-wire-schemas-and-errors`, `api-openapi-generated-clients`.
  - ci: `ci-check-trust`, `ci-reproducible-checks`.
  - code: `code-comment-attribution`, `code-module-structure-and-control-flow`, `code-python-client-injection`, `code-rust-source-structure`, `code-rust-workspace-checks`, `code-typescript-compiler-strictness`, `code-typescript-file-names`, `code-typescript-function-arguments`, `code-typescript-module-boundaries`, `code-typescript-package-boundaries`.
  - context: `context-note-curation`.
  - data: `data-alembic-revision-history`, `data-object-upload-lifecycle`, `data-postgres-schema-migrations`, `data-sql-schema-rollouts`, `data-stored-and-shipped-formats`.
  - eval: `eval-case-curation`, `eval-experiment-comparisons`, `eval-grading-isolation`, `eval-production-path`, `eval-run-lifecycle`, `eval-score-accounting`.
  - infra: `infra-terraform-apply-authority`, `infra-terraform-state-ownership`.
  - llm: `llm-assessment-inputs`, `llm-assessment-outcomes`, `llm-code-review-evidence`, `llm-confidence-routing`, `llm-request-lifecycle`, `llm-response-validation`.
  - release: `release-artifact-provenance`.
  - security: `security-api-key-lifecycle`, `security-approved-external-actions`, `security-cli-credential-lifecycle`, `security-oauth-authorization-server`, `security-oauth-browser-sessions`, `security-resource-access-control`, `security-server-secret-storage`, `security-user-content-serving`.
  - service: `service-background-job-state`, `service-event-records`, `service-mutation-idempotency-keys`, `service-optimistic-revision-writes`, `service-transaction-side-effects`.
  - telemetry: `telemetry-application-tracing`.
  - test: `test-curation`.
  - ui: `ui-async-read-states`, `ui-control-accessibility`, `ui-design-tokens`, `ui-deterministic-display-values`, `ui-motion-lifecycle`, `ui-presentation-boundaries`, `ui-presentation-state`, `ui-react-interaction-ownership`, `ui-react-typescript-component-apis`, `ui-storybook-component-checks`, `ui-time-series-charts`.
  - web: `web-access-scoping`, `web-development-fixtures`, `web-public-page-server-rendering`, `web-server-state-cache`, `web-url-search-state`, `web-write-lifecycle`.
- Repository contracts in `.contracts` for this library's own naming, format, generality, releases, and skills, and
  `scripts/lint-contracts.py`, which checks names, layout, and technology words.

### Clarified

- `tenet-adoption` explains area-first names and `--name` for a second scope.
- `tenet-architecture-curation` and `tenet-contract-curation` name no private directory or command.

## v1.0.0

First release. Installing contracts needs Tenet 0.7.0 or later.

### Added

- Contracts `contract-maintenance`, `data-and-apis`, `execution-lifecycle`, and `ownership-and-boundaries`, written
  one sentence per line so updates merge sentence by sentence.
- `contract-maintenance` asks for local exceptions under a final `## Local adaptations` heading.
- Skills `tenet`, `tenet-adoption`, `tenet-architecture-curation`, `tenet-code-curation`, `tenet-contract-curation`,
  and `tenet-test-curation`.
- `tenet-adoption` installs and updates contracts with `tenet contracts` and resolves update conflicts.
