# Changelog

Each release lists every changed contract or skill under one class. A Tightened or Removed entry makes a major
release, an Added or Loosened entry a minor release, and Clarified entries alone a patch release.

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
