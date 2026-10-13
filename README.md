# Tenet contracts

Shared contracts and agent skills for [Tenet](https://github.com/macromackie/tenet), which checks code against
Markdown contracts. A contract becomes a requirement only when a project installs it.

## Contracts

Install a contract into the scope it governs with Tenet 0.7.0 or later:

```sh
tenet contracts add tenet/data-and-apis --scope packages/api
tenet check --contract data-and-apis
```

Tenet copies it to the next numbered folder, such as `packages/api/.contracts/003-data-and-apis/CONTRACT.md`, and
records the release in `.tenet.lock`. Edit the copy freely; put local exceptions under `## Local adaptations`.
`tenet contracts update` takes later releases: unedited copies are replaced and edited copies merge three ways.
Installing the same contract in a second scope needs a distinct local name, such as `--name web-data-and-apis`.

### Names

Each name reads `<area>-[<technology>-]<subject>[-<aspect>]`, for example `security-api-key-lifecycle` or
`ui-react-interaction-ownership`.

- The area says what a reviewer checks. The list below is closed; a new area needs a release that defines it.
- A technology word, such as `react`, `typescript`, `fastapi`, or `postgres`, follows the area whenever any rule depends
  on it. A name without one applies to every language, framework, and vendor, so `ui-design-tokens` holds for any UI
  stack while `ui-react-interaction-ownership` applies only to React code.
- Reserved suffixes keep one form: `-boundaries`, `-apis`, `-checks`, `-lifecycle`, `-ownership`, and `-curation`.

| Area | Covers |
| --- | --- |
| `api` | HTTP and RPC interfaces: routes, wire schemas, and generated clients. |
| `ci` | Automated checks: reproducible inputs and what a result may be trusted for. |
| `code` | Source structure, boundaries, and comments in any language. |
| `context` | Durable repository notes for people and agents. |
| `contract` | Writing and maintaining adopted contracts. |
| `data` | Stored data, schemas, migrations, and object storage. |
| `eval` | Evaluating a system against curated cases. |
| `infra` | Provisioned infrastructure and its state. |
| `llm` | Systems that send requests to language models and act on the answers. |
| `release` | Building, publishing, and activating artifacts. |
| `security` | Authentication, authorization, credentials, and untrusted content. |
| `service` | Server-side writes, jobs, events, and their effects. |
| `telemetry` | Traces, logs, and metrics. |
| `test` | Test suites and what they keep. |
| `ui` | Presentation components and design systems. |
| `web` | Browser applications: routing, URLs, server rendering, and server data. |

### By area

The library has 73 contracts.

#### api

| Contract | Requirement |
| --- | --- |
| `api-fastapi-resource-layout` | Give each resource one folder of router, schema, query and service modules, and keep URLs fixed when code moves. |
| `api-fastapi-route-authorization` | Declare route admission as named shared dependencies and apply ownership in the statement, never after loading. |
| `api-fastapi-wire-schemas-and-errors` | Declare explicit wire models, keep secrets on mint responses only, and map each failure to one status and detail. |
| `api-openapi-generated-clients` | Generate the OpenAPI description from the live route registry, and publish pinned, framework-free clients from it. |

#### ci

| Contract | Requirement |
| --- | --- |
| `ci-check-trust` | Run complete required checks with explicit trust and no inherited cache or credential authority. |
| `ci-reproducible-checks` | Run the same declared checks locally and in CI with pinned tools and complete inputs. |

#### code

| Contract | Requirement |
| --- | --- |
| `code-comment-attribution` | Explain source behavior without attributing it to repository contracts or review tools. |
| `code-execution-lifecycle` | Bound work and preserve authoritative results through failure and interruption. |
| `code-module-structure-and-control-flow` | Keep modules focused and named for their behavior, with explicit control flow and established patterns. |
| `code-ownership-and-boundaries` | Give decisions and state one owner, with explicit dependency direction. |
| `code-python-client-injection` | Construct stateful Python clients at composition roots and inject them into consumers as abstract types. |
| `code-rust-source-structure` | Keep Rust entry points thin, alternatives as enums, and errors typed and propagated with context, never unwrapped in production. |
| `code-rust-workspace-checks` | Enforce rustfmt and deny-warnings Clippy, share dependencies and lints through the workspace, and commit Cargo.lock. |
| `code-typescript-compiler-strictness` | Type-check every TypeScript package under strict compiler settings that no file relaxes. |
| `code-typescript-file-names` | Use kebab-case source paths with dotted role suffixes; preserve tool-required names. |
| `code-typescript-function-arguments` | Use one named object argument for multiple, boolean, or optional inputs; keep externally defined signatures. |
| `code-typescript-module-boundaries` | Share code across source folders only through each folder's explicit named-export entry point. |
| `code-typescript-package-boundaries` | Consume TypeScript packages only through declared dependencies and explicitly exported entry points. |

#### context

| Contract | Requirement |
| --- | --- |
| `context-note-curation` | Keep context notes useful beyond a task, with dated, sourced evidence and execution tracking in the task tracker. |

#### contract

| Contract | Requirement |
| --- | --- |
| `contract-maintenance` | Keep adopted contracts scoped, reviewable, and consistent with their implementation. |

#### data

| Contract | Requirement |
| --- | --- |
| `data-alembic-revision-history` | Keep one Alembic head, never delete or re-identify a merged revision, and undo applied work with a new revision. |
| `data-and-apis` | Keep authoritative facts and explicit outcomes behind small, usable APIs. |
| `data-object-upload-lifecycle` | Reserve metadata before bytes, publish only after verified storage, and delete only unreferenced objects. |
| `data-postgres-schema-migrations` | Bound every DDL lock wait, build indexes concurrently, validate NOT VALID constraints, and read dependents from the catalog. |
| `data-sql-schema-rollouts` | Ship schema changes that the previous release and existing rows survive, in batches an interrupted deploy resumes. |
| `data-stored-and-shipped-formats` | Migrate every stored instance and keep what released clients read before narrowing a stored or shipped format. |

#### eval

| Contract | Requirement |
| --- | --- |
| `eval-case-curation` | Add only distinct, justified cases with clean controls and stated premises, and never edit cases to fit results. |
| `eval-experiment-comparisons` | Compare only frozen, equivalent experiments with a declared intervention, tuning on development cases and validating on holdout cases. |
| `eval-grading-isolation` | Keep expected outcomes from the assessed system, and condition, identity, and prior grades from the grader. |
| `eval-production-path` | Evaluate the shipped system through its public interface at pinned revisions without external effects. |
| `eval-run-lifecycle` | Freeze inputs before paid work, checkpoint results atomically, and resume only the same experiment. |
| `eval-score-accounting` | Report every score with its denominator, and never turn failures, unknowns, or missing cost into values. |

#### infra

| Contract | Requirement |
| --- | --- |
| `infra-terraform-apply-authority` | Apply infrastructure only from the exact reviewed source and saved plan, with narrowly scoped credentials. |
| `infra-terraform-state-ownership` | Keep one state owner per resource and preserve data and physical identities through ownership transfers. |

#### llm

| Contract | Requirement |
| --- | --- |
| `llm-assessment-inputs` | Capture bounded inputs once, reject rather than truncate, and keep selected, supporting, and omitted source distinct. |
| `llm-assessment-outcomes` | Keep pass, fail, uncertain, error, and incomplete outcomes distinct, and never let failed execution pass. |
| `llm-code-review-evidence` | Ground automated review conclusions in cited requirements, confirmed source, and observed execution receipts. |
| `llm-confidence-routing` | Keep raw model answers and confidence separate from routing, and never treat confidence as calibrated correctness. |
| `llm-request-lifecycle` | Retry transient model request failures within one owned budget, never to obtain a preferred answer. |
| `llm-response-validation` | Accept only complete, protocol-valid model responses that match exactly what was requested. |

#### release

| Contract | Requirement |
| --- | --- |
| `release-artifact-provenance` | Publish only verified bytes from a successful default-branch check, without rebuilding them. |

#### security

| Contract | Requirement |
| --- | --- |
| `security-api-key-lifecycle` | Store issued keys as hashes bound to owner, scope, and expiry, revoke them permanently, and fail with distinct unauthenticated errors. |
| `security-approved-external-actions` | Execute external writes only from an approved, exact, immutable request, once, and never replay uncertain outcomes. |
| `security-cli-credential-lifecycle` | Store CLI credentials owner-only and atomically, bound to their origin, and never print them or accept them as arguments. |
| `security-oauth-authorization-server` | Issue audience-bound tokens through PKCE, and never let a login confer authorization. |
| `security-oauth-browser-sessions` | Keep OAuth tokens server-side behind host-only HttpOnly cookies with exact-origin checks. |
| `security-resource-access-control` | Authorize every request on the server from current grants; logins, plain links, and caller-supplied facts grant nothing. |
| `security-server-secret-storage` | Encrypt held secrets bound to their record, keep keys outside the database, and never log secret values. |
| `security-user-content-serving` | Treat user content as untrusted; never execute markup, inline only verified passive formats, and serve the rest as downloads. |

#### service

| Contract | Requirement |
| --- | --- |
| `service-background-job-state` | Read job state only from its status, allow only declared transitions, and complete on the current attempt's verdict. |
| `service-event-records` | Keep events immutable, source-bound, and typed, with producer-owned retry and consumers that deduplicate by event identity. |
| `service-mutation-idempotency-keys` | Commit a caller-generated key's receipt with the mutation, return it on exact retries, and reject conflicting reuse. |
| `service-optimistic-revision-writes` | Write against the expected revision, reject a stale edit whole, and preserve the rejected draft. |
| `service-transaction-side-effects` | Emit best-effort effects after commit, and commit durable delivery intent with the state change. |

#### telemetry

| Contract | Requirement |
| --- | --- |
| `telemetry-application-tracing` | Trace operations consistently without exposing secrets or letting diagnostics change results. |

#### test

| Contract | Requirement |
| --- | --- |
| `test-curation` | Treat development tests as disposable and commit only checks that guard consequential regressions. |

#### ui

| Contract | Requirement |
| --- | --- |
| `ui-async-read-states` | Present pending, empty, failed, and refreshing reads truthfully, without false empties, flashing loaders, or displaced content. |
| `ui-control-accessibility` | Use semantic, named, keyboard-operable controls and managed overlays that contain, dismiss, and return focus. |
| `ui-design-tokens` | Name shared visual decisions as semantic tokens and expose named variants, not unrestricted style overrides. |
| `ui-deterministic-display-values` | Render identical display values from identical inputs everywhere, with explicit locale, time zone, zero, and missing values. |
| `ui-motion-lifecycle` | Keep animation interruptible, reduced-motion aware, pausable, paused when unseen, and released on removal. |
| `ui-presentation-boundaries` | Render supplied data and report intent; leave requests, routing, identity, and domain decisions to applications. |
| `ui-presentation-state` | Hold only ephemeral interaction state and unsaved drafts in presentation; receive application-owned state as inputs. |
| `ui-react-interaction-ownership` | Keep each interaction's state, transitions, subscriptions, and cleanup under one component or hook. |
| `ui-react-typescript-component-apis` | Encode supported component use in public prop types so unsupported combinations fail to compile. |
| `ui-storybook-component-checks` | Give every public component synthetic stories of its meaningful states and assert only consequential owned interactions. |
| `ui-time-series-charts` | Render application-prepared series faithfully and give pointer, touch, and keyboard users the same inspected values. |

#### web

| Contract | Requirement |
| --- | --- |
| `web-access-scoping` | Authorize every server entry point; scope private client data to its session and discard it on access change. |
| `web-development-fixtures` | Run presentation work against labeled synthetic responses without changing the production path or reaching production. |
| `web-public-page-server-rendering` | Render complete public content and real links in server HTML, and let hydration only add interaction. |
| `web-server-state-cache` | Keep server data in one client cache, keyed by every response-changing input and scoped to the viewer. |
| `web-url-search-state` | Validate URL search state in the destination route that owns it, and write only non-default choices. |
| `web-write-lifecycle` | Define each write once, show it saved only on acknowledgment, and retry only when the endpoint makes retries safe. |

## Skills

Start with `tenet` for CLI usage, `tenet-adoption` for adoption and updates, or one of the curation skills. Ask an agent
to adopt them with `tenet-adoption`, or use a skill installer such as
`npx skills add macromackie/tenet-contracts --skill tenet-adoption`.

## Contributing

Issues and pull requests are welcome. [.contracts](.contracts/index.md) holds the rules for this library's own
contracts and skills: area-first names, one sentence per line, no company or unnamed vendor content, and classified
releases. Run `python3 scripts/lint-contracts.py` before opening a pull request. Accepted changes ship in the next tag
and are credited in the changelog.

## Releases

Releases are `vX.Y.Z` tags. [CHANGELOG.md](CHANGELOG.md) classifies each change. A tightened or removed requirement is a
major release, so review the changelog before updating across one.

See https://tenet-contracts.com/docs/guidance for the full workflow.
