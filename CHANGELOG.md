# Changelog

Each release lists every changed contract or skill under one class. A Tightened or Removed entry makes a major
release, an Added or Loosened entry a minor release, and Clarified entries alone a patch release.

## v9.0.0

`code-blank-lines`, `code-function-size`, and `code-typescript-node-scripts` ship tool configuration under `assets/`,
so installing or updating them needs Tenet 0.11.0 or later. Every other contract still installs with Tenet 0.7.0 or
later. The Release workflow now validates every contract with Tenet 0.11.0.

### Tightened

- `code-blank-lines`: the contract ships `assets/oxlint/oxlintrc.json` and declares `requires-tenet: 0.11.0`. Where the
  repository's lint can load that file, extend it from the repository's own lint configuration. The file loads
  `@stylistic/eslint-plugin` through oxlint's `jsPlugins` and configures `padding-line-between-statements`. It requires
  a blank line before each `if`, `for`, `while`, `do`, `switch`, and `try` statement that is not first in its block and
  after each one that is not last, and forbids a blank line between switch cases. It was checked with oxlint 1.80.0 and
  1.89.0 and `@stylistic/eslint-plugin` 5.10.0. Pin oxlint and the plugin to exact versions, as `ci-reproducible-checks`
  requires, because oxlint documents JS plugins as alpha and not subject to semver. Install the plugin in the package
  that holds the `.contracts` folder or in one above it, because oxlint resolves it from the installed file's folder,
  then run `oxlint --fix` once. Review still covers logical phases, comment placement, and Python and Rust code.
- `code-function-size`: declare a maximum complexity per function, in a measure the repository's lint computes, for each
  language the repository lints, and enforce it on the same functions as the length, nesting, and callback limits. A
  language may go without a complexity limit only when the repository declares that language and the reason beside its
  limits. The contract ships `assets/oxlint/oxlintrc.json`, which loads `eslint-plugin-sonarjs` through oxlint's
  `jsPlugins` and sets cognitive complexity to 15; a repository's lint configuration may extend that file and override
  its limit. It was checked with oxlint 1.80.0 and 1.89.0 and `eslint-plugin-sonarjs` 4.2.2. Pin oxlint and the plugin
  to exact versions, as `ci-reproducible-checks` requires, because oxlint documents JS plugins as alpha and not subject
  to semver. Install the plugin in the package that holds the `.contracts` folder or in one above it, because oxlint
  resolves it from the installed file's folder. The contract declares `requires-tenet: 0.11.0`.
- `code-module-structure-and-control-flow`: a generic stored or wire name or value that another system fixes, or that a
  released format keeps as `data-stored-and-shipped-formats` requires, appears only in the mapping that reads or writes
  it, such as a serializer rename that decodes an order's `item` field into `lineItem`, or an enumeration member
  `LineItem` whose value is `'item'`. Owned code that reads such a name directly, such as a provider's `item` field
  outside its decoder, complied before and now goes through that mapping. A released generic name that the repository
  chose, which violated the naming rule before, may now stay in its mapping. Owned fields, types, and members still take
  a name for their concept. A new check asks whether each such name appears only in that mapping.
- `test-curation`: temporary tests, probes, fixtures, and test-only dependencies stay out of every commit, including
  intermediate commits and commits pushed only to run CI, unless a retained check uses them; before, they only had to
  be gone before merging. Its check now inspects each commit, not only the complete diff. Its message and rules now
  also allow committing the declared example tests of `test-example-suite`, which need no guarded regression to be
  retained and no reason or remaining protection to be deleted; its rule against hiding a regression still covers them.
  A declared example limit is exempt from its ban on test-count targets and gates.
- `ui-storybook-component-checks`: an explicit tag or list selects the stories that run as tests, so adding a story
  adds no test until it is selected. Storybook's default gives every story the `test` tag, which the test run
  includes, so that setup no longer complies. Set `tags: ['!test']` in the preview, then add `test` or another
  selecting tag to each chosen story.

### Loosened

- `code-closed-value-sets`: an error's tag, which its error class declares once, may be written as a literal in a tag
  comparison or as a tag handler's argument when the type checker rejects a tag outside the error type.

### Added

- Contract `code-mise-script-tasks`: make every repository script, such as a check, a code generator, a smoke run, or a
  release step, a mise file task in the `mise-tasks/` folder of the root or package that owns it. Helper modules that
  only tasks use go in `mise-tasks/lib/` without the executable bit. Only the bootstrap that installs mise and one-line
  shims may live elsewhere. A TOML task may only run one command of one tool, group tasks through `depends`, or define
  or extend a template. Every CI step that runs repository work calls `mise run`.
- Contract `code-python-uv-scripts`: run Python repository scripts with `uv run --script`, starting from
  `#!/usr/bin/env -S uv run --script`. Give each one a PEP 723 block that lists its dependencies, even an empty list,
  so it never runs in the surrounding project's environment.
- Contract `code-typescript-node-scripts`: write repository scripts as `.mts` files that a pinned Node with default type
  stripping runs from `#!/usr/bin/env node`, with no loader, TypeScript runner, or process helper dependency. Imports
  name the real file. The compiler checks every script folder under `nodenext`, `erasableSyntaxOnly`,
  `verbatimModuleSyntax`, `allowImportingTsExtensions`, and `noEmit`. The contract ships those options as
  `assets/typescript/tsconfig.json`, so it needs Tenet 0.11.0 or later.
- Contract `test-example-suite`: keep, for the whole repository, at most a declared, fixed number of example tests of
  each kind for each test runner command that CI invokes, counting a command that CI invokes once per package as one, at
  a declared path marker, and never let that number grow with packages, modules, or features. Each example is a new
  file, never cut from an existing test, with one case and one assertion of a literal value or stable error code, and no
  loop, table, parameterized rows, generator, asserting helper, or second instantiation from build configuration. It
  calls a stable public entry point, imports helpers only from the test support folder, and opens with a header that
  states its kind, when to copy it, and the command that runs a copy. An isolated example starts no child process, opens
  no socket, and touches no disk outside a temporary folder; a local-dependency example starts one local dependency
  through a support fixture; a test that runs the product's own entry point is end-to-end and never an example. An
  example never guards a regression or counts as the protection that remains, and is replaced only while it passes, in a
  change that touches no other file. Each temporary test for a runner and kind that has an example starts as a renamed
  copy of that example in a declared scratch folder that version control ignores and the runner collects. Its Allowed
  example declares one isolated and one local-dependency example per runner command.
- `scripts/lint-contracts.py` allows `mise`, `Node`, and `uv` only in a contract whose name carries `mise`, `node`, or
  `uv`; before, it refused `mise` and `Node.js` in every contract and did not check `Node` or `uv`. It skips a
  backticked library contract name, such as `code-mise-script-tasks`, so any contract may name another.

### Clarified

- `code-typescript-effect-errors`: a `_tag` comparison or a tag handler's argument, such as
  `Effect.catchTag('RefundRefused', ...)`, may write the tag as a literal, as `code-closed-value-sets` allows, because
  the compiler rejects a tag outside the Effect's error type.
- `data-stored-and-shipped-formats`: renaming an owned field or member while its mapping keeps the stored or shipped
  name is not a narrowing; `code-module-structure-and-control-flow` requires that mapping for a generic name.
- `tenet-adoption`: a contract that ships files under `assets/` needs Tenet 0.11.0 or later to install.
- `tenet-test-curation`: a declared example test needs no named consequential failure before committing, as
  `test-example-suite` allows.

## v8.0.0

Tenet 0.11.0 adds `tenet skills`, which installs a skill folder into `.agents/skills/` and locks every file in
`.tenet.lock`. The `tenet-adoption` skill uses it and needs Tenet 0.11.0 or later. Installing contracts still needs
Tenet 0.7.0 or later, because no contract ships assets yet. Once `.tenet.lock` records a skill or contract assets,
every `tenet contracts` command and `tenet validate` in that project need Tenet 0.11.0 or later.

The curation skills' `resources/` folders are now `references/`, the Agent Skills folder name. Before recording an
installed copy with `tenet skills add tenet/NAME --path PATH`, run `git mv PATH/resources PATH/references` and update
its links, so its local edits still merge.

### Tightened

- `library-contract-format`: a contract folder holds nothing but `CONTRACT.md` and tool configuration and data files
  under `assets/<tool>/`, where any other file was allowed before. A contract that ships assets declares
  `requires-tenet` with the minimum Tenet that installs them, 0.11.0 or later, and the frontmatter now allows that key.
- `library-skill-portability`: a library skill's frontmatter holds only the Agent Skills fields `name`, `description`,
  `license`, `compatibility`, `metadata`, and `allowed-tools`. Its `name` uses lowercase letters, digits, and single
  hyphens, at most 64 characters, its `description` is one line of at most 1024 characters, and any `compatibility`
  is one line of at most 500 characters. Each skill folder carries the library license as `LICENSE.txt`, which may
  name its copyright holder, and keeps documents in `references/`, code in `scripts/`, and data files in `assets/`.
- `tenet-adoption`: install, update, and remove skills with `tenet skills`, and commit a `.claude/skills/NAME` symlink
  to each one for Claude Code. Edit only an installed skill's Markdown and leave installed contract assets as released.
  The adoption record keeps only decisions, because `.tenet.lock` holds sources, revisions, and hashes.

### Loosened

- `code-cross-repository-copies`: an installed skill's documents, like an installed contract's, follow the installer's
  lock and may carry local edits. Any other file that a contract or skill installer locks, such as a lint configuration
  shipped with a contract, is a permitted locked copy, which the repository's own configuration extends.
- `library-contract-generality`: a contract whose name carries no tool may ship `assets/<tool>/` files that configure
  any tool to enforce its stated rules, while its text still names no tool.

### Added

- `scripts/lint-contracts.py` checks skill frontmatter fields, names, descriptions, and compatibility notes. It also
  refuses any file in a contract folder other than `CONTRACT.md` and `assets/<tool>/` files, and requires
  `requires-tenet: 0.11.0` or later in a contract that ships assets.

### Clarified

- `tenet`, `tenet-architecture-curation`, `tenet-code-curation`, `tenet-contract-curation`, and `tenet-test-curation`:
  each skill folder carries the library's MIT license as `LICENSE.txt` and declares `license: MIT`. The three curation
  skills keep their examples in `references/` instead of `resources/`.

## v7.0.0

### Tightened

- `code-export-consumers`: in a language that marks which names another file may import, a name never starts with an
  underscore to mark it private, except a binding, parameter, or field that the code never reads.
- `code-typescript-entry-points`: an entry point may re-export a file under the PascalCase form of its stem, such as
  `export * as Uuid from './uuid.ts'`, whose names leave out the namespace's word; an exported object that code uses
  only to call its functions by fixed names is banned, while one that code indexes with a computed key, passes as an
  implementation of an interface type, or receives from a factory whose functions close over dependencies stays
  allowed.

### Loosened

- `code-module-file-roles`: a file that an entry point re-exports under one namespace may hold several operations on
  the concept that the namespace names.
- `code-typescript-file-names`: a file that an entry point re-exports under a namespace matches its stem to that
  namespace instead of to a primary export.
- `code-typescript-module-boundaries`: a namespace re-export is allowed in an entry point, as
  `code-typescript-entry-points` allows.

### Clarified

- `code-cross-repository-copies`: re-locking an edited copy under the same revision is a violation example.
- `code-rust-visibility`: a doc-comment link is not a use, so it never justifies a wider visibility.
- `code-script-entry-points`: parsing arguments into a top-level constant is a violation example.

## v6.0.0

### Tightened

- `code-module-file-roles`: a behavior file holds only functions and classes; a cache lives in the object or closure
  that owns it, as `code-typescript-module-state` requires.
- `code-module-structure-and-control-flow`: only state that one object or closure owns is exempt from the ambient-state
  rule. The unit clause moves to `code-measured-value-names`, and a test support folder that `test-support-modules`
  defines is not a catch-all module.
- `code-ownership-and-boundaries`: allowed dependencies come from the declaration that `code-dependency-boundaries`
  requires.
- `code-rust-workspace-checks`: suppress a lint only with an outer `#[expect(lint, reason = "...")]`, and deny
  `clippy::allow_attributes`, `clippy::allow_attributes_without_reason`, and `unfulfilled_lint_expectations`.
- `code-typescript-module-boundaries`: imports between files stay acyclic, type-only and dynamic imports included; a
  nested folder's outside API goes through its parent's entry point; a dependency check that resolves imports to files
  enforces both.

### Loosened

- `code-function-size`: its suppression rules move to `code-lint-suppressions`.
- `code-shared-utilities`: a domain-free helper that only tests call lives in the test support folder.
- `code-typescript-function-arguments`: boolean naming moves to `code-boolean-names`.
- `code-typescript-package-boundaries`: which symbols an entry point exports moves to `code-export-consumers`, and a new
  entry point needs a consumer that `code-export-consumers` accepts, such as the tests of a test support package.

### Added

- 34 contracts:
  - cli: `cli-output-channels`.
  - code: `code-boolean-names`, `code-comment-content`, `code-comment-form`, `code-cross-repository-copies`,
    `code-dependency-boundaries`, `code-diagnostic-messages`, `code-duplicated-blocks`, `code-environment-settings`,
    `code-exhaustive-branches`, `code-export-consumers`, `code-folder-size`, `code-guard-clauses`,
    `code-lint-suppressions`, `code-measured-value-names`, `code-rust-doc-comment-coverage`,
    `code-rust-module-boundaries`, `code-rust-module-files`, `code-rust-numeric-conversions`,
    `code-rust-type-ownership`, `code-rust-visibility`, `code-script-entry-points`, `code-shared-definitions`,
    `code-spelled-out-names`, `code-typescript-class-declarations`, `code-typescript-const-bindings`,
    `code-typescript-entry-points`, `code-typescript-input-immutability`, `code-typescript-module-state`,
    `code-typescript-type-assertions`.
  - data: `data-sql-store-boundaries`, `data-store-ownership`.
  - test: `test-scenario-functions`, `test-support-modules`.

### Clarified

- `code-conditional-expressions`: an `if` statement chooses a value without the rule saying it assigns one.
- `code-typescript-effect-schemas`: the assertion rule moves to `code-typescript-type-assertions`; decoding every
  boundary value still forbids reading an asserted one.
- `tenet-code-curation`: the TypeScript example chooses a stage in a function that returns it and leaves the job
  unchanged, as `code-typescript-const-bindings` and `code-typescript-input-immutability` require.

## v5.0.0

This release adds the `docs` area: documentation that people read, such as READMEs, guides, and reference pages.

### Tightened

- `code-typescript-function-arguments`: every owned function, method, constructor, and owned callback that takes input
  takes one destructured object argument, including a single input or a domain object, such as `parse({ line })` and
  `total({ invoice })`. Signatures that a language, runtime, framework, or dependency defines stay exempt, and so
  does a function that forwards a wrapped function's arguments unchanged.
- `code-module-structure-and-control-flow` names every function, type, and file, exported or not, and every stored
  or wire value for what it stands for, never with a generic word alone such as `data`, `item`, `handler`, or
  `script`. It also gives each concern to the contract that owns it:
  - A shared utilities module that `code-shared-utilities` defines is not a catch-all module, so `utils` leaves the
    banned names, and only helpers that depend on their module's domain stay private to it.
  - A file named for a declared role, such as `types`, may take the role as its name.
  - State that one module owns and changes only through its own functions, such as a cache, is not ambient state.
  - Type placement moves to `code-module-file-roles`, and blank lines between phases move to `code-blank-lines`.
  - The rule to follow the area's established conventions is removed: it matched every other convention contract's
    violations, and one file does not show which convention an area follows. The rule on established libraries
    forbids only hand-written parsing, validation, and provider integration that a maintained library provides.

- `code-rust-source-structure`: a library crate carries each expected failure as a variant of a typed error `enum`
  until code handles it, and only a binary crate uses an opaque error type, such as `anyhow::Error`.

### Loosened

- `code-typescript-file-names`: a declared role file, such as `types.ts`, `constants.ts`, or `schemas.ts` inside a
  module's folder, takes the role as its whole stem and may hold many exports of that role.

### Added

- 12 contracts:
  - code: `code-blank-lines`, `code-closed-value-sets`, `code-conditional-expressions`, `code-function-size`,
    `code-module-file-roles`, `code-shared-utilities`, `code-typescript-effect-errors`,
    `code-typescript-effect-schemas`, `code-typescript-named-types`.
  - data: `data-record-identifiers`.
  - docs: `docs-prose-style`, `docs-readme-structure`.

### Clarified

- `tenet-contract-curation` no longer advises against a file size limit, since `code-module-file-roles` asks for a
  declared maximum file length enforced by lint. It warns against catch-all rules and allowed forms that resemble
  forbidden ones, and adds two checks before the first model run: a small model labels the patches from the contract
  text alone, and another writes changes that obey a rule's letter but break its intent.
- `tenet-code-curation` defers to installed contracts for file and function length, file roles, argument shapes,
  conditionals, and closed value sets. Its TypeScript example uses ordinary branches over declared members and passes
  dependencies as named fields, and a package exports only what another package imports.

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
