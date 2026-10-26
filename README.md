# Tenet contracts

Shared contracts and agent skills for [Tenet](https://github.com/macromackie/tenet), which checks code against
Markdown contracts. A contract becomes a requirement only when a project installs it.

## Contracts

Install a contract into the scope it governs with Tenet 0.7.0 or later, or 0.11.0 or later for a contract that ships
tool files under `assets/`:

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
| `agent` | Systems that give autonomous agents tools, credentials, memory, and attributed activity. |
| `api` | HTTP and RPC interfaces: routes, wire schemas, and generated clients. |
| `ci` | Automated checks: reproducible inputs and what a result may be trusted for. |
| `cli` | Command-line programs: command definitions, published references, output, and exit status. |
| `code` | Source structure, boundaries, and comments in any language. |
| `context` | Durable repository notes for people and agents. |
| `contract` | Writing and maintaining adopted contracts. |
| `data` | Stored data, schemas, migrations, and object storage. |
| `docs` | Documentation that people read: READMEs, guides, and reference pages. |
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

The library has 143 contracts.

#### agent

| Contract | Requirement |
| --- | --- |
| `agent-activity-attribution` | Attribute activity to individual agents without letting attribution grant access or change outcomes. |
| `agent-shared-memory` | Let one writer edit agent memory, and give readers verified immutable snapshots identified by digest. |
| `agent-tool-authorization` | Let agents discover and call only reviewed, explicitly selected tools through one assigned backend. |

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

#### cli

| Contract | Requirement |
| --- | --- |
| `cli-command-reference-generation` | Declare each command once in a model that drives both the CLI parser and its published reference. |
| `cli-output-channels` | Write a command-line program's result to standard output and every other line to standard error through one output module, and end the process only from its entry point with a declared exit status. |

#### code

| Contract | Requirement |
| --- | --- |
| `code-blank-lines` | Separate a block's logical phases, and each control-flow statement inside it, from neighboring code with one blank line. |
| `code-boolean-names` | Start every owned boolean's name with a declared predicate or option prefix that lint enforces, and keep an external boolean name only in the mapping that decodes it. |
| `code-closed-value-sets` | Declare each closed set of values once and refer to its members by name, never by repeating their literal values. |
| `code-comment-attribution` | Explain source behavior without attributing it to repository contracts or review tools. |
| `code-comment-content` | Write comments that state what the code cannot show, never what it already says, what it used to do, or a shape that a declaration could carry. |
| `code-comment-form` | Commit no task markers, commented-out code, or empty doc comments, and give doc comments and file summaries one lint-enforced layout. |
| `code-conditional-expressions` | Choose between values with statements, lookups, or pattern matching, never with a conditional operator. |
| `code-cross-repository-copies` | Keep each file that several repositories use in one source repository, and consume it from a release or as a locked copy whose hash checks verify. |
| `code-dependency-boundaries` | Declare which packages each package may depend on once, in configuration that checks enforce, and keep that declaration acyclic and exact. |
| `code-diagnostic-messages` | Write each diagnostic as one clause that names the failed operation and its input, without a trailing period. |
| `code-domain-vocabulary` | Name each domain concept with its one glossary word in code, output, documentation, and interface text, and never with a word it replaced. |
| `code-duplicated-blocks` | Fail checks on every copied block that the repository's copy detector reports, and remove the copy by calling one declaration. |
| `code-environment-settings` | Read a program's environment only in its settings module, decode it once there, and pass decoded settings to the code that needs them. |
| `code-execution-lifecycle` | Bound work and preserve authoritative results through failure and interruption. |
| `code-exhaustive-branches` | Branch on a closed set that the repository declares by naming every member, never through a default or wildcard case, so that a new member fails the lint. |
| `code-export-consumers` | Give every export, source file, and dependency a production consumer, and let the repository's dead-code check prove it. |
| `code-folder-size` | Keep every source folder within lint-enforced limits on its file count and depth, and name and justify each exempt folder in the lint configuration. |
| `code-function-size` | Keep every function within lint-enforced length, nesting, callback, and complexity limits, and give each case of a branch on a closed set its own function. |
| `code-guard-clauses` | Leave a block early with a guard instead of nesting its remaining work, and never write an `else` after a branch that leaves. |
| `code-lint-suppressions` | Suppress a lint or check finding only at the one site it reports, with the rule's name and a reason, and fail checks on every suppression that suppresses nothing. |
| `code-measured-value-names` | End the name of every numeric limit, duration, and bound with a declared unit, counted noun, or unitless measure that the repository's lint enforces. |
| `code-mise-script-tasks` | Make every repository script a mise file task in the `mise-tasks/` folder of the root or package that owns it, and run repository work in CI only through `mise run`. |
| `code-module-file-roles` | Give each source file one declared role, keep types in a sibling types file, and turn a module with several roles into a folder. |
| `code-module-structure-and-control-flow` | Keep modules focused and named for their behavior, with explicit inputs, results, and control flow. |
| `code-ownership-and-boundaries` | Give decisions and state one owner, with explicit dependency direction. |
| `code-python-client-injection` | Construct stateful Python clients at composition roots and inject them into consumers as abstract types. |
| `code-python-exception-propagation` | Let Python exceptions propagate; catch one only to re-raise it, translate it with its cause, retry it, or record a failed unit of work. |
| `code-python-none-guards` | Trust non-optional Python annotations, and check for None only where the checked value's type includes None. |
| `code-python-uv-scripts` | Run each Python repository script with `uv run --script`, and declare its dependencies in its own PEP 723 inline metadata block. |
| `code-rust-doc-comment-coverage` | Give every public item of a Rust library crate a doc comment, and fail checks when one is missing. |
| `code-rust-module-boundaries` | Keep a Rust crate's top-level modules acyclic and its child modules private. |
| `code-rust-module-files` | Declare each Rust module that has child modules in a file named for it beside its folder, never in a mod.rs file under src. |
| `code-rust-numeric-conversions` | Convert Rust numbers with From and TryFrom instead of as, and declare each limit, count, or size in the type its consumers take. |
| `code-rust-source-structure` | Keep Rust entry points thin, alternatives as enums, and errors typed and propagated with context, never unwrapped in production. |
| `code-rust-type-ownership` | Give each Rust type at most one impl block per file, make its fields all private or all public, give each shared counter its own type, and declare no global mutable state. |
| `code-rust-visibility` | Give every Rust item the narrowest visibility its users need, and fail checks on a public item that the crate root does not export. |
| `code-rust-workspace-checks` | Enforce rustfmt and deny-warnings Clippy, share dependencies and lints through the workspace, and commit Cargo.lock. |
| `code-script-entry-points` | Keep the top level of every file the repository executes directly to declarations and one statement that runs its main program. |
| `code-shared-definitions` | Declare each pattern, bound, and derivation that several modules must agree on once, and import it everywhere else. |
| `code-shared-utilities` | Keep domain-free helpers in the application's one shared utilities module, one per file, and use the declared utility library first. |
| `code-spelled-out-names` | Spell out every word of every declared name, with a repository word list and a one-character ban that lint enforces in every language. |
| `code-typescript-class-declarations` | Declare a TypeScript class only where a runtime or library requires one, write every other unit that holds dependencies or state as a factory function, and give each class field a readonly private name. |
| `code-typescript-compiler-strictness` | Type-check every TypeScript package under strict compiler settings that no file relaxes. |
| `code-typescript-const-bindings` | Declare TypeScript variables with `const`, give every `let` its first value where it is declared, and choose a value with a function rather than by assigning in each branch. |
| `code-typescript-effect-errors` | Carry each expected TypeScript failure as a tagged error in an Effect's error type until code handles it by tag, and throw or die only for broken invariants. |
| `code-typescript-effect-schemas` | Decode every value that crosses a TypeScript boundary with an Effect Schema, and derive its type from that schema. |
| `code-typescript-entry-points` | Keep each TypeScript entry point a list of named re-exports from the files that declare them, re-export from no other file, and never add a file named after a sibling folder. |
| `code-typescript-file-names` | Use kebab-case source paths with dotted role suffixes; preserve tool-required names. |
| `code-typescript-function-arguments` | Give every owned TypeScript function that takes input one destructured object argument; keep externally defined signatures. |
| `code-typescript-input-immutability` | Never change a value that a TypeScript function received as a parameter or sort an array in place, and return a new value instead. |
| `code-typescript-module-boundaries` | Share code across source folders only through each folder's explicit named-export entry point, and keep imports between files acyclic, type-only and dynamic imports included. |
| `code-typescript-module-state` | Keep no TypeScript state at module level or in a static class field that changes after the module loads, hold each cache in the object or closure that owns it, and give module constants read-only types. |
| `code-typescript-named-types` | Give every TypeScript object type a name instead of writing an object type literal inline. |
| `code-typescript-node-scripts` | Write repository scripts as `.mts` files that the pinned Node runs directly without a loader or runner dependency, and type-check them for what Node's type stripping accepts. |
| `code-typescript-package-boundaries` | Consume TypeScript packages only through declared dependencies and explicitly exported entry points. |
| `code-typescript-type-assertions` | Narrow TypeScript values with checks the compiler follows, never with type assertions, non-null assertions, return-only type parameters, or the any type. |

#### context

| Contract | Requirement |
| --- | --- |
| `context-agent-instruction-files` | Keep agent instruction files visible, accurate, and consistent, and change them with the code they describe. |
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
| `data-metric-definitions` | Define each metric's cohort, window, and denominator, count each stored fact once, and show coverage gaps beside results. |
| `data-object-upload-lifecycle` | Reserve metadata before bytes, publish only after verified storage, and delete only unreferenced objects. |
| `data-postgres-schema-migrations` | Bound every DDL lock wait, build indexes concurrently, validate NOT VALID constraints, and read dependents from the catalog. |
| `data-record-identifiers` | Give each new record a random UUID, derive an id only where a retry or rebuild must reproduce it, build each derived kind in one named function, and never parse an id. |
| `data-sql-schema-rollouts` | Ship schema changes that the previous release and existing rows survive, in batches an interrupted deploy resumes. |
| `data-sql-store-boundaries` | Write SQL text and database client calls only in the database owner's store module, each statement once and whole, and never expose the client. |
| `data-store-ownership` | Give each owner of persisted data one store module that alone names, parses, reads, and writes it, behind functions named for records and changes. |
| `data-stored-and-shipped-formats` | Migrate every stored instance and keep what released clients read before narrowing a stored or shipped format. |

#### docs

| Contract | Requirement |
| --- | --- |
| `docs-prose-style` | Write documentation in short, direct sentences that lead with what the reader does or needs. |
| `docs-readme-structure` | Open each README with what the project is and how to start, link out for depth, and keep status and history out. |

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
| `llm-code-review-publication` | Publish automated review results against the reviewed head revision, and approve only on complete, current, clean evidence. |
| `llm-confidence-routing` | Keep raw model answers and confidence separate from routing, and never treat confidence as calibrated correctness. |
| `llm-request-lifecycle` | Retry transient model request failures within one owned budget, never to obtain a preferred answer. |
| `llm-response-validation` | Accept only complete, protocol-valid model responses that match exactly what was requested. |

#### release

| Contract | Requirement |
| --- | --- |
| `release-artifact-provenance` | Publish only verified bytes from a successful default-branch check, without rebuilding them. |
| `release-public-source-export` | Export only allowlisted files from a committed private revision, validated in isolation, without private context or history. |

#### security

| Contract | Requirement |
| --- | --- |
| `security-api-key-lifecycle` | Store issued keys as hashes bound to owner, scope, and expiry, revoke them permanently, and fail with distinct unauthenticated errors. |
| `security-approved-external-actions` | Execute external writes only from an approved, exact, immutable request, once, and never replay uncertain outcomes. |
| `security-cli-credential-lifecycle` | Store CLI credentials owner-only and atomically, bound to their origin, and never print them or accept them as arguments. |
| `security-delegated-credential-vending` | Mint a capped, expiring, narrowly scoped child credential per request, return it once, and delete it when it ends. |
| `security-inbound-webhook-verification` | Verify each webhook over its raw body, bind it to the expected source, and store it once before processing. |
| `security-interpreter-injection` | Pass untrusted input to interpreters only as bound data, never as code, commands, query text, templates, or type-constructing serialized objects. |
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
| `test-assertion-integrity` | Change code to satisfy its tests; never weaken a test to match new behavior or special-case test inputs in production code. |
| `test-curation` | Treat development tests as disposable, and commit only checks that guard consequential regressions and declared example tests. |
| `test-example-suite` | Keep a declared, fixed number of one-case example tests for each test runner as templates for temporary tests, and never count one as a regression's protection. |
| `test-scenario-functions` | Give each scenario of an end-to-end check its own function named for the one guarantee it protects, and name every reported check without a sequence marker. |
| `test-support-modules` | Declare each test helper and fixture once, in its family's file of the package's test support folder, and never copy it into another test file. |

#### ui

| Contract | Requirement |
| --- | --- |
| `ui-async-read-states` | Present pending, empty, failed, and refreshing reads truthfully, without false empties, flashing loaders, or displaced content. |
| `ui-component-usage-guidance` | Document each public component's purpose, use, alternatives, and status beside its source, and generate the catalog from it. |
| `ui-control-accessibility` | Use semantic, named, keyboard-operable controls and managed overlays that contain, dismiss, and return focus. |
| `ui-data-tables` | Render application-prepared rows as given, and report sorting and paging through controlled values and callbacks. |
| `ui-design-tokens` | Name shared visual decisions as semantic tokens and expose named variants, not unrestricted style overrides. |
| `ui-deterministic-display-values` | Render identical display values from identical inputs everywhere, with explicit locale, time zone, zero, and missing values. |
| `ui-keyboard-shortcuts` | Register each keyboard command with its action owner, in the narrowest scope, without overriding typing or native keys. |
| `ui-motion-lifecycle` | Keep animation interruptible, reduced-motion aware, pausable, paused when unseen, and released on removal. |
| `ui-presentation-boundaries` | Render supplied data and report intent; leave requests, routing, identity, and domain decisions to applications. |
| `ui-presentation-state` | Hold only ephemeral interaction state and unsaved drafts in presentation; receive application-owned state as inputs. |
| `ui-react-interaction-ownership` | Keep each interaction's state, transitions, subscriptions, and cleanup under one component or hook. |
| `ui-react-typescript-component-apis` | Encode supported component use in public prop types so unsupported combinations fail to compile. |
| `ui-semantic-value-controls` | Give each value domain one control whose name states its value contract, and keep application policy outside it. |
| `ui-storybook-component-checks` | Give every public component synthetic stories of its meaningful states and assert only consequential owned interactions. |
| `ui-time-series-charts` | Render application-prepared series faithfully and give pointer, touch, and keyboard users the same inspected values. |

#### web

| Contract | Requirement |
| --- | --- |
| `web-access-scoping` | Authorize every server entry point; scope private client data to its session and discard it on access change. |
| `web-development-fixtures` | Run presentation work against labeled synthetic responses without changing the production path or reaching production. |
| `web-edge-gateway-routing` | Route exact origins and paths to configured private upstreams, keep credentials away from static and shell upstreams, and hold no authority. |
| `web-public-page-server-rendering` | Render complete public content and real links in server HTML, and let hydration only add interaction. |
| `web-server-state-cache` | Keep server data in one client cache, keyed by every response-changing input and scoped to the viewer. |
| `web-url-search-state` | Validate URL search state in the destination route that owns it, and write only non-default choices. |
| `web-write-lifecycle` | Define each write once, show it saved only on acknowledgment, and retry only when the endpoint makes retries safe. |

## Skills

Start with `tenet` for CLI usage, `tenet-adoption` for adoption and updates, or one of the curation skills. Install one
with Tenet 0.11.0 or later:

```sh
tenet skills add tenet/tenet-adoption
```

Tenet copies the folder to `.agents/skills/tenet-adoption/` and locks each file in `.tenet.lock`. Edit its Markdown
freely; `tenet skills update` merges later releases three ways. Leave its other files as released. Claude Code reads
only `.claude/skills/`, so commit a symlink such as `.claude/skills/tenet-adoption` pointing to
`../../.agents/skills/tenet-adoption`. Each skill folder carries the MIT license as `LICENSE.txt`. Once
`.tenet.lock` records a skill, every `tenet contracts` command and `tenet validate` in that project need Tenet 0.11.0
or later.

## Contributing

Issues and pull requests are welcome. [.contracts](.contracts/index.md) holds the rules for this library's own
contracts and skills: area-first names, one sentence per line, no company or unnamed vendor content, and classified
releases. Run `python3 scripts/lint-contracts.py` before opening a pull request. Accepted changes ship in the next tag
and are credited in the changelog.

## Releases

Releases are `vX.Y.Z` tags. [CHANGELOG.md](CHANGELOG.md) classifies each change. A tightened or removed requirement is a
major release, so review the changelog before updating across one.

See https://tenet-contracts.com/docs/guidance for the full workflow.
