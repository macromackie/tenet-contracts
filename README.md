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

| Area        | Covers                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------ |
| `agent`     | Systems that give autonomous agents tools, credentials, memory, and attributed activity.   |
| `api`       | HTTP and RPC interfaces: routes, wire schemas, and generated clients.                      |
| `ci`        | Automated checks: reproducible inputs and what a result may be trusted for.                |
| `cli`       | Command-line programs: command definitions, published references, output, and exit status. |
| `code`      | Source structure, boundaries, and comments in any language.                                |
| `context`   | Durable repository notes for people and agents.                                            |
| `contract`  | Writing and maintaining adopted contracts.                                                 |
| `data`      | Stored data, schemas, migrations, and object storage.                                      |
| `docs`      | Documentation that people read: READMEs, guides, and reference pages.                      |
| `eval`      | Evaluating a system against curated cases.                                                 |
| `infra`     | Provisioned infrastructure and its state.                                                  |
| `llm`       | Systems that send requests to language models and act on the answers.                      |
| `release`   | Building, publishing, and activating artifacts.                                            |
| `security`  | Authentication, authorization, credentials, and untrusted content.                         |
| `service`   | Server-side writes, jobs, events, and their effects.                                       |
| `telemetry` | Traces, logs, and metrics.                                                                 |
| `test`      | Test suites and what they keep.                                                            |
| `ui`        | Presentation components and design systems.                                                |
| `web`       | Browser applications: routing, URLs, server rendering, and server data.                    |

### By area

The library has 170 contracts.

Coverage describes the available checks: `tool-checked` means the contract ships tool configuration;
`judged with eval` means development cases exercise model judgments; `judged and unmeasured` means neither is
recorded here. Tool configuration checks its named patterns, and development cases cover only their stated scope.
These labels do not establish whole-contract compliance or general model accuracy.

#### agent

| Contract                     | Requirement                                                                                           | Coverage              |
| ---------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------- |
| `agent-activity-attribution` | Attribute activity to individual agents without letting attribution grant access or change outcomes.  | judged and unmeasured |
| `agent-shared-memory`        | Let one writer edit agent memory, and give readers verified immutable snapshots identified by digest. | judged and unmeasured |
| `agent-tool-authorization`   | Let agents discover and call only reviewed, explicitly selected tools through one assigned backend.   | judged and unmeasured |

#### api

| Contract                              | Requirement                                                                                                                                                   | Coverage              |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `api-fastapi-resource-layout`         | Give each resource one folder of router, schema, query and service modules, and keep URLs fixed when code moves.                                              | judged with eval      |
| `api-fastapi-route-authorization`     | Declare route admission as named shared dependencies and apply ownership in the statement, never after loading.                                               | judged with eval      |
| `api-fastapi-wire-schemas-and-errors` | Declare explicit wire models, keep secrets on mint responses only, and map each failure to one status and detail.                                             | judged with eval      |
| `api-openapi-generated-clients`       | Generate the OpenAPI description from the live route registry, and publish pinned, framework-free clients from it.                                            | judged and unmeasured |
| `api-typescript-request-paths`        | Build each request path and URL with one typed path function per operation, declared once in the module that owns its routes, and encode each part inside it. | tool-checked          |

#### ci

| Contract                 | Requirement                                                                                      | Coverage              |
| ------------------------ | ------------------------------------------------------------------------------------------------ | --------------------- |
| `ci-check-trust`         | Run complete required checks with explicit trust and no inherited cache or credential authority. | judged and unmeasured |
| `ci-reproducible-checks` | Run the same declared checks locally and in CI with pinned tools and complete inputs.            | judged and unmeasured |

#### cli

| Contract                           | Requirement                                                                                                                                                                                           | Coverage              |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `cli-command-reference-generation` | Declare each command once in a model that drives both the CLI parser and its published reference.                                                                                                     | judged and unmeasured |
| `cli-output-channels`              | Write a command-line program's result to standard output and every other line to standard error through one output module, and end the process only from its entry point with a declared exit status. | tool-checked          |

#### code

| Contract                                     | Requirement                                                                                                                                                                                                                                       | Coverage              |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `code-blank-lines`                           | Separate a block's logical phases, control flow, returns, throws, calls, and multi-line declarations and expressions from neighboring code with one blank line.                                                                                   | tool-checked          |
| `code-boolean-names`                         | Start every owned boolean's name with a declared predicate or option prefix and every boolean function's with a predicate prefix, and decode each external boolean name at the boundary.                                                          | tool-checked          |
| `code-closed-value-sets`                     | Declare each closed set of values once, HTTP methods and status codes included, name its members instead of their literal values, and test membership with a module-level set.                                                                    | tool-checked          |
| `code-comment-attribution`                   | Explain source behavior without attributing it to repository contracts or review tools.                                                                                                                                                           | judged with eval      |
| `code-comment-content`                       | Write comments that state what the code cannot show, never what it already says, what it used to do, or a shape that a declaration could carry.                                                                                                   | judged with eval      |
| `code-comment-form`                          | Write comments as capitalized sentences without task markers, commented-out code, step labels, license notices, or empty doc comments, and declaration comments and file summaries as lint-enforced prose doc comments.                           | tool-checked          |
| `code-conditional-expressions`               | Choose values with statements, lookups, pattern matching, or named functions, and markup with extracted components, not conditional operators, complementary pairs, or immediately invoked functions, within a declared logical-operator maximum. | tool-checked          |
| `code-constant-names`                        | Name each module-level constant whose value is a number or string written in source in SCREAMING_SNAKE_CASE, such as `STOP_TICK_MS`.                                                                                                              | tool-checked          |
| `code-cross-repository-copies`               | Keep each file that several repositories use in one source repository, and consume it from a release or as a locked copy whose hash checks verify.                                                                                                | judged with eval      |
| `code-declaration-order`                     | Declare each function and class above the code that uses it, so each file reads from its helpers down to its exported function.                                                                                                                   | tool-checked          |
| `code-dependency-boundaries`                 | Declare which packages each package may depend on once, in configuration that checks enforce, and keep that declaration acyclic and exact.                                                                                                        | tool-checked          |
| `code-diagnostic-messages`                   | Write each diagnostic as one clause that starts with a lowercase word, names the failed operation and its input, quotes every value it interpolates, and ends without a period.                                                                   | tool-checked          |
| `code-domain-vocabulary`                     | Name each domain concept with its one glossary word in code, output, documentation, and interface text, and never with a word it replaced.                                                                                                        | judged and unmeasured |
| `code-duplicated-blocks`                     | Fail checks on every copied block that the repository's copy detector reports, and remove the copy by calling one declaration.                                                                                                                    | tool-checked          |
| `code-environment-settings`                  | Read a program's environment only in its settings module, decode it once there, and pass decoded settings to the code that needs them.                                                                                                            | judged with eval      |
| `code-execution-lifecycle`                   | Bound work and preserve authoritative results through failure and interruption.                                                                                                                                                                   | judged and unmeasured |
| `code-exhaustive-branches`                   | Write an `else if` chain of equality tests on one value as a `switch`, and name every member of a declared closed set instead of a default or wildcard.                                                                                           | tool-checked          |
| `code-export-consumers`                      | Give every export, source file, and dependency a production consumer, and let the repository's dead-code check prove it.                                                                                                                          | judged with eval      |
| `code-folder-size`                           | Keep every source folder within lint-enforced limits on its file count and depth, and name and justify each exempt folder in the lint configuration.                                                                                              | tool-checked          |
| `code-function-size`                         | Keep every function within lint-enforced length, nesting, callback, markup depth, and complexity limits, and give each case of a branch on a closed set its own function.                                                                         | tool-checked          |
| `code-guard-clauses`                         | Leave a block early with a guard instead of nesting its remaining work, and never write an `else` after a branch that leaves.                                                                                                                     | judged with eval      |
| `code-key-order`                             | Write the keys of every object, struct, and configuration map in code point order, and keep another order only where order is behavior.                                                                                                           | judged and unmeasured |
| `code-lint-strictness`                       | Run every lint, type checker, compiler, and formatter at its strictest setting, and turn a rule off only for a listed reason named beside its entry.                                                                                              | tool-checked          |
| `code-lint-suppressions`                     | Suppress a lint or check finding only at the one site it reports, with the rule's name and a reason, and fail checks on every suppression that suppresses nothing.                                                                                | judged with eval      |
| `code-map-and-set-names`                     | End every map's and set's name with a plural noun of what it holds, such as `orders` or `endedStates`, never a participle or adjective.                                                                                                           | tool-checked          |
| `code-measured-value-names`                  | End the name of every numeric limit, duration, and bound with a declared unit, counted noun, or unitless measure that the repository's lint enforces.                                                                                             | judged with eval      |
| `code-mise-script-tasks`                     | Make every repository script a mise file task in the `mise-tasks/` folder of the root or package that owns it, and run repository work in CI only through `mise run`.                                                                             | judged and unmeasured |
| `code-module-file-roles`                     | Give each source file one declared role and at most one class, component, and exported function, export only components from markup files, and split multi-role modules into folders.                                                             | tool-checked          |
| `code-module-structure-and-control-flow`     | Keep modules focused and named for their behavior, start every lowercase function name with a declared verb, and keep inputs, results, and control flow explicit.                                                                                 | tool-checked          |
| `code-numeric-literals`                      | Give every number except -1, 0, and 1 a named constant that holds one literal, and build each derived constant from other constants' names.                                                                                                       | tool-checked          |
| `code-ownership-and-boundaries`              | Give decisions and state one owner, with explicit dependency direction.                                                                                                                                                                           | judged and unmeasured |
| `code-python-client-injection`               | Construct stateful Python clients at composition roots and inject them into consumers as abstract types.                                                                                                                                          | judged with eval      |
| `code-python-doc-comment-coverage`           | Give every public Python module, class, function, method, and `__init__` a docstring, and fail checks when one is missing.                                                                                                                        | judged and unmeasured |
| `code-python-exception-propagation`          | Let Python exceptions propagate; catch one only to re-raise it, translate it with its cause, retry it, record a failed unit of work, or map it to an exit status in the entry point.                                                              | judged and unmeasured |
| `code-python-function-arguments`             | Make every parameter of an owned Python function keyword-only, and keep the signatures that the language, runtime, and dependencies define.                                                                                                       | judged and unmeasured |
| `code-python-none-guards`                    | Trust non-optional Python annotations, and check for None only where the checked value's type includes None.                                                                                                                                      | judged and unmeasured |
| `code-python-uv-scripts`                     | Run each Python repository script with `uv run --script`, and declare its dependencies in its own PEP 723 inline metadata block.                                                                                                                  | judged and unmeasured |
| `code-rust-doc-comment-coverage`             | Give every public item of a Rust library crate a doc comment, and fail checks when one is missing.                                                                                                                                                | tool-checked          |
| `code-rust-module-boundaries`                | Keep a Rust crate's top-level modules acyclic and its child modules private.                                                                                                                                                                      | tool-checked          |
| `code-rust-module-files`                     | Declare each Rust module that has child modules in a file named for it beside its folder, never in a mod.rs file under src.                                                                                                                       | judged with eval      |
| `code-rust-numeric-conversions`              | Convert Rust numbers with From and TryFrom instead of as, and declare each limit, count, or size in the type its consumers take.                                                                                                                  | judged with eval      |
| `code-rust-source-structure`                 | Keep Rust entry points thin, alternatives as enums, and errors as derived types that callers match by variant, propagated with context and never unwrapped in production.                                                                         | tool-checked          |
| `code-rust-type-ownership`                   | Give each Rust type at most one impl block per file, make its fields all private or all public, give each shared counter its own type, and declare no global mutable state.                                                                       | judged with eval      |
| `code-rust-visibility`                       | Give every Rust item the narrowest visibility its users need, and fail checks on a public item that the crate root does not export.                                                                                                               | judged with eval      |
| `code-rust-workspace-checks`                 | Enforce the rustfmt and Clippy settings that code-lint-strictness ships, share dependencies and lints through the workspace, and commit Cargo.lock.                                                                                               | judged and unmeasured |
| `code-script-entry-points`                   | Keep the top level of every file the repository executes directly to declarations and one statement that runs its main program.                                                                                                                   | judged with eval      |
| `code-shared-definitions`                    | Declare each pattern, bound, and derivation that several modules must agree on once, and import it everywhere else.                                                                                                                               | judged with eval      |
| `code-shared-utilities`                      | Keep domain-free helpers in the application's one shared utilities module, one per file, and use the declared utility library first.                                                                                                              | judged with eval      |
| `code-spelled-out-names`                     | Spell out every word of every declared name, case acronyms as words, map `get`, `fetch`, and `load` to `read`, and ban one-character names in every language's lint.                                                                              | tool-checked          |
| `code-typescript-boolean-conditions`         | Give every TypeScript condition a boolean or a nullable object, compare strings, numbers, and lengths explicitly, and supply defaults with `??`, never `\|\|`.                                                                                    | tool-checked          |
| `code-typescript-call-arguments`             | Bind to a name each nested call, `new`, `await`, and function written in an argument object or array, and each awaited or `yield*` value before reading a member.                                                                                 | tool-checked          |
| `code-typescript-class-declarations`         | Declare a TypeScript class only where a runtime or library requires one, write every other unit that holds dependencies or state as a factory function, and give each class field a readonly private name.                                        | judged with eval      |
| `code-typescript-collection-iteration`       | Iterate over TypeScript collections with `for...of`, keep a running total in a `let` that the loop advances, and never call `forEach` or `reduce` or write `for...in`.                                                                            | tool-checked          |
| `code-typescript-compiler-strictness`        | Type-check every TypeScript package under strict compiler settings that no file relaxes.                                                                                                                                                          | tool-checked          |
| `code-typescript-const-bindings`             | Declare TypeScript variables with `const`, initialize each `let` and reassign it only in a loop or callback, step with `+= 1`, and bind functions as declarations or typed constants.                                                             | tool-checked          |
| `code-typescript-doc-comment-coverage`       | Give every exported TypeScript function and class a doc comment, and fail checks when one is missing.                                                                                                                                             | tool-checked          |
| `code-typescript-effect-absent-values`       | Type each TypeScript result and record field that may hold no value as an Effect `Option`, writing `null` and `undefined` only where a foreign format or signature requires them.                                                                 | tool-checked          |
| `code-typescript-effect-errors`              | Carry each TypeScript failure that a caller can act on as a tagged error in an Effect's error type, and every other failure as a tagged defect.                                                                                                   | tool-checked          |
| `code-typescript-effect-scheduling`          | Sleep, bound, retry, poll, race, and fan out TypeScript work only with Effect's operators, never with hand-built promises, promise combinators, or timers.                                                                                        | tool-checked          |
| `code-typescript-effect-schemas`             | Decode every value that crosses a TypeScript boundary with an Effect Schema, reject unknown fields on owned shapes, and give each schema and its type one PascalCase name.                                                                        | tool-checked          |
| `code-typescript-entry-points`               | Keep each TypeScript entry point a list of named re-exports from the files that declare them, re-export from no other file, and never add a file named after a sibling folder.                                                                    | judged with eval      |
| `code-typescript-export-return-types`        | Declare the return type of every exported TypeScript function and method, and let local functions and callbacks infer theirs.                                                                                                                     | tool-checked          |
| `code-typescript-expression-forms`           | Destructure same-name TypeScript reads, use shorthand properties, expression-bodied arrows, template strings, `replaceAll`, `===`, and `for (;;)`, and convert or parse values with comparisons, `Boolean`, `Number`, or `String`.                | tool-checked          |
| `code-typescript-file-names`                 | Use kebab-case source paths with dotted role suffixes; preserve tool-required names.                                                                                                                                                              | judged with eval      |
| `code-typescript-function-arguments`         | Give each owned TypeScript function that takes input one destructured object argument whose type carries its name, default there, pass callbacks as inline arrows, and keep external signatures.                                                  | tool-checked          |
| `code-typescript-function-member-signatures` | Declare each function member of a TypeScript type as a property with a function type, never as a method signature, so the compiler checks its parameters strictly.                                                                                | tool-checked          |
| `code-typescript-function-scoping`           | Declare a named TypeScript function inside another function only when it captures that function's scope, and move every other one to the top level of its file.                                                                                   | tool-checked          |
| `code-typescript-import-extensions`          | Name the imported file in each relative TypeScript import by its own name and extension, such as `./harness.ts`, never a bare path, a folder, or the emitted `.js` name.                                                                          | tool-checked          |
| `code-typescript-import-statements`          | Import modules at the top in sorted blocks without blank lines, once each and by name, test functions from the runner, listed libraries as namespaces, type-only names as `type`.                                                                 | tool-checked          |
| `code-typescript-input-immutability`         | Never change a TypeScript function's input, sort in place, or use `delete`, and type arrays and tuples `readonly` except a local or private field its owner fills.                                                                                | tool-checked          |
| `code-typescript-module-boundaries`          | Share code across source folders only through each folder's explicit named-export entry point, and keep imports between files acyclic, type-only and dynamic imports included.                                                                    | tool-checked          |
| `code-typescript-module-state`               | Keep no TypeScript module state that changes after loading, hold each cache in its owner, end module-level literals with `as const`, and type module-level sets and maps read-only.                                                               | tool-checked          |
| `code-typescript-named-types`                | Name every TypeScript object type with a `type` alias instead of writing it inline, and write `interface` only to augment a dependency's declaration.                                                                                             | tool-checked          |
| `code-typescript-node-scripts`               | Write repository scripts as `.mts` files that the pinned Node runs directly without a loader or runner dependency, and type-check them for what Node's type stripping accepts.                                                                    | tool-checked          |
| `code-typescript-object-literal-functions`   | Declare each function a TypeScript object literal holds by name and list the name, such as `return { settleInvoice }`, instead of writing a method or function-valued property.                                                                   | tool-checked          |
| `code-typescript-package-boundaries`         | Consume TypeScript packages only through declared dependencies and explicitly exported entry points.                                                                                                                                              | judged and unmeasured |
| `code-typescript-runtime-keyed-maps`         | Hold each TypeScript lookup that code fills at run time or builds from a collection in a `Map`, and create each record whole.                                                                                                                     | tool-checked          |
| `code-typescript-type-assertions`            | Narrow values with checks the compiler follows, annotate declared types unless code reads inferred ones, and never write type or non-null assertions, type predicates, return-only type parameters, or `any`.                                     | tool-checked          |

#### context

| Contract                          | Requirement                                                                                                       | Coverage              |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------- |
| `context-agent-instruction-files` | Keep agent instruction files visible, accurate, and consistent, and change them with the code they describe.      | judged and unmeasured |
| `context-note-curation`           | Keep context notes useful beyond a task, with dated, sourced evidence and execution tracking in the task tracker. | judged and unmeasured |

#### contract

| Contract               | Requirement                                                                          | Coverage     |
| ---------------------- | ------------------------------------------------------------------------------------ | ------------ |
| `contract-maintenance` | Keep adopted contracts scoped, reviewable, and consistent with their implementation. | tool-checked |

#### data

| Contract                          | Requirement                                                                                                                                                             | Coverage              |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `data-alembic-revision-history`   | Keep one Alembic head, never delete or re-identify a merged revision, and undo applied work with a new revision.                                                        | judged with eval      |
| `data-and-apis`                   | Keep authoritative facts and explicit outcomes behind small, usable APIs.                                                                                               | judged and unmeasured |
| `data-metric-definitions`         | Define each metric's cohort, window, and denominator, count each stored fact once, and show coverage gaps beside results.                                               | judged and unmeasured |
| `data-object-upload-lifecycle`    | Reserve metadata before bytes, publish only after verified storage, and delete only unreferenced objects.                                                               | judged and unmeasured |
| `data-postgres-schema-migrations` | Bound every DDL lock wait, build indexes concurrently, validate NOT VALID constraints, and read dependents from the catalog.                                            | judged and unmeasured |
| `data-record-identifiers`         | Give each new record a random UUID, derive an id only where a retry or rebuild must reproduce it, build each derived kind in one named function, and never parse an id. | judged with eval      |
| `data-sql-schema-rollouts`        | Ship schema changes that the previous release and existing rows survive, in batches an interrupted deploy resumes.                                                      | judged and unmeasured |
| `data-sql-store-boundaries`       | Write SQL text and database client calls only in the database owner's store module, each statement once and whole, and never expose the client.                         | judged with eval      |
| `data-store-ownership`            | Give each owner of persisted data one store module that alone names, parses, reads, and writes it, behind functions named for records and changes.                      | judged with eval      |
| `data-stored-and-shipped-formats` | Migrate every stored instance and keep what released clients read before narrowing a stored or shipped format.                                                          | judged and unmeasured |

#### docs

| Contract                | Requirement                                                                                                      | Coverage         |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------- | ---------------- |
| `docs-prose-style`      | Write documentation in short, direct sentences that lead with what the reader does or needs.                     | judged with eval |
| `docs-readme-structure` | Open each README with what the project is and how to start, link out for depth, and keep status and history out. | judged with eval |

#### eval

| Contract                      | Requirement                                                                                                                            | Coverage              |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `eval-case-curation`          | Add only distinct, justified cases with clean controls and stated premises, and never edit cases to fit results.                       | judged and unmeasured |
| `eval-experiment-comparisons` | Compare only frozen, equivalent experiments with a declared intervention, tuning on development cases and validating on holdout cases. | judged and unmeasured |
| `eval-grading-isolation`      | Keep expected outcomes from the assessed system, and condition, identity, and prior grades from the grader.                            | judged and unmeasured |
| `eval-production-path`        | Evaluate the shipped system through its public interface at pinned revisions without external effects.                                 | judged and unmeasured |
| `eval-run-lifecycle`          | Freeze inputs before paid work, checkpoint results atomically, and resume only the same experiment.                                    | judged and unmeasured |
| `eval-score-accounting`       | Report every score with its denominator, and never turn failures, unknowns, or missing cost into values.                               | judged and unmeasured |

#### infra

| Contract                          | Requirement                                                                                                | Coverage              |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------- |
| `infra-terraform-apply-authority` | Apply infrastructure only from the exact reviewed source and saved plan, with narrowly scoped credentials. | judged and unmeasured |
| `infra-terraform-state-ownership` | Keep one state owner per resource and preserve data and physical identities through ownership transfers.   | judged and unmeasured |

#### llm

| Contract                      | Requirement                                                                                                                 | Coverage              |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `llm-assessment-inputs`       | Capture bounded inputs once, reject rather than truncate, and keep selected, supporting, and omitted source distinct.       | judged and unmeasured |
| `llm-assessment-outcomes`     | Keep pass, fail, uncertain, error, and incomplete outcomes distinct, and never let failed execution pass.                   | judged and unmeasured |
| `llm-code-review-evidence`    | Ground automated review conclusions in cited requirements, confirmed source, and observed execution receipts.               | judged and unmeasured |
| `llm-code-review-publication` | Publish automated review results against the reviewed head revision, and approve only on complete, current, clean evidence. | judged and unmeasured |
| `llm-confidence-routing`      | Keep raw model answers and confidence separate from routing, and never treat confidence as calibrated correctness.          | judged and unmeasured |
| `llm-request-lifecycle`       | Retry transient model request failures within one owned budget, never to obtain a preferred answer.                         | judged and unmeasured |
| `llm-response-validation`     | Accept only complete, protocol-valid model responses that match exactly what was requested.                                 | judged and unmeasured |

#### release

| Contract                       | Requirement                                                                                                                  | Coverage              |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `release-artifact-provenance`  | Publish only verified bytes from a successful default-branch check, without rebuilding them.                                 | judged and unmeasured |
| `release-public-source-export` | Export only allowlisted files from a committed private revision, validated in isolation, without private context or history. | judged and unmeasured |

#### security

| Contract                                | Requirement                                                                                                                                       | Coverage              |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `security-api-key-lifecycle`            | Store issued keys as hashes bound to owner, scope, and expiry, revoke them permanently, and fail with distinct unauthenticated errors.            | judged and unmeasured |
| `security-approved-external-actions`    | Execute external writes only from an approved, exact, immutable request, once, and never replay uncertain outcomes.                               | judged and unmeasured |
| `security-cli-credential-lifecycle`     | Store CLI credentials owner-only and atomically, bound to their origin, and never print them or accept them as arguments.                         | judged and unmeasured |
| `security-delegated-credential-vending` | Mint a capped, expiring, narrowly scoped child credential per request, return it once, and delete it when it ends.                                | judged and unmeasured |
| `security-inbound-webhook-verification` | Verify each webhook over its raw body, bind it to the expected source, and store it once before processing.                                       | judged and unmeasured |
| `security-interpreter-injection`        | Pass untrusted input to interpreters only as bound data, never as code, commands, query text, templates, or type-constructing serialized objects. | judged and unmeasured |
| `security-oauth-authorization-server`   | Issue audience-bound tokens through PKCE, and never let a login confer authorization.                                                             | judged and unmeasured |
| `security-oauth-browser-sessions`       | Keep OAuth tokens server-side behind host-only HttpOnly cookies with exact-origin checks.                                                         | judged and unmeasured |
| `security-resource-access-control`      | Authorize every request on the server from current grants; logins, plain links, and caller-supplied facts grant nothing.                          | judged with eval      |
| `security-server-secret-storage`        | Encrypt held secrets bound to their record, keep keys outside the database, and never log secret values.                                          | judged and unmeasured |
| `security-user-content-serving`         | Treat user content as untrusted; never execute markup, inline only verified passive formats, and serve the rest as downloads.                     | judged and unmeasured |

#### service

| Contract                             | Requirement                                                                                                                 | Coverage              |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `service-background-job-state`       | Read job state only from its status, allow only declared transitions, and complete on the current attempt's verdict.        | judged and unmeasured |
| `service-event-records`              | Keep events immutable, source-bound, and typed, with producer-owned retry and consumers that deduplicate by event identity. | judged and unmeasured |
| `service-mutation-idempotency-keys`  | Commit a caller-generated key's receipt with the mutation, return it on exact retries, and reject conflicting reuse.        | judged and unmeasured |
| `service-optimistic-revision-writes` | Write against the expected revision, reject a stale edit whole, and preserve the rejected draft.                            | judged and unmeasured |
| `service-transaction-side-effects`   | Emit best-effort effects after commit, and commit durable delivery intent with the state change.                            | judged with eval      |

#### telemetry

| Contract                              | Requirement                                                                                                                                        | Coverage     |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| `telemetry-application-tracing`       | Trace operations and write each log line as one JSON object with a declared event, without exposing secrets or letting diagnostics change results. | tool-checked |
| `telemetry-rust-tracing`              | Centralize Rust tracing, keep entered spans out of suspended futures, and install exporters only in application binaries.                          | tool-checked |
| `telemetry-typescript-effect-tracing` | Name traced TypeScript Effects with literal operation names and compose telemetry once at the application entry point.                             | tool-checked |

#### test

| Contract                   | Requirement                                                                                                                                                      | Coverage              |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `test-assertion-integrity` | Change code to satisfy its tests; never weaken a test to match new behavior or special-case test inputs in production code.                                      | tool-checked          |
| `test-curation`            | Treat development tests as disposable, and commit only checks that guard consequential regressions and declared example tests.                                   | tool-checked          |
| `test-example-suite`       | Keep a declared, fixed number of one-case example tests for each test runner as templates for temporary tests, and never count one as a regression's protection. | judged and unmeasured |
| `test-scenario-functions`  | Give each scenario of an end-to-end check its own function named for the one guarantee it protects, and name every reported check without a sequence marker.     | tool-checked          |
| `test-support-modules`     | Declare each test helper and fixture once, in its own file of the package's test support folder, and never copy it into another test file.                       | judged with eval      |

#### ui

| Contract                             | Requirement                                                                                                                                                                    | Coverage              |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- |
| `ui-async-read-states`               | Present pending, empty, failed, and refreshing reads truthfully, without false empties, flashing loaders, or displaced content.                                                | judged and unmeasured |
| `ui-component-usage-guidance`        | Document each public component's purpose, use, alternatives, and status beside its source, and generate the catalog from it.                                                   | judged and unmeasured |
| `ui-control-accessibility`           | Use semantic, named, keyboard-operable controls and managed overlays that contain, dismiss, and return focus.                                                                  | judged and unmeasured |
| `ui-data-tables`                     | Render application-prepared rows as given, and report sorting and paging through controlled values and callbacks.                                                              | judged and unmeasured |
| `ui-design-tokens`                   | Name shared visual decisions as semantic tokens and expose named variants, not unrestricted style overrides.                                                                   | tool-checked          |
| `ui-deterministic-display-values`    | Render identical display values from identical inputs everywhere, with explicit locale, time zone, zero, and missing values.                                                   | judged and unmeasured |
| `ui-keyboard-shortcuts`              | Register each keyboard command with its action owner, in the narrowest scope, without overriding typing or native keys.                                                        | judged and unmeasured |
| `ui-motion-lifecycle`                | Keep animation interruptible, reduced-motion aware, pausable, paused when unseen, and released on removal.                                                                     | judged and unmeasured |
| `ui-presentation-boundaries`         | Render supplied data and report intent; leave requests, routing, identity, and domain decisions to applications.                                                               | judged and unmeasured |
| `ui-presentation-state`              | Hold only ephemeral interaction state and unsaved drafts in presentation; receive application-owned state as inputs.                                                           | judged and unmeasured |
| `ui-react-hook-calls`                | Name each state pair `[thing, setThing]`, and call state, ref, and context hooks before every other hook and effect hooks after them.                                          | tool-checked          |
| `ui-react-interaction-ownership`     | Keep each interaction's state, transitions, subscriptions, and cleanup under one component or hook.                                                                            | tool-checked          |
| `ui-react-typescript-component-apis` | Encode supported component use in public prop types so unsupported combinations fail to compile.                                                                               | judged and unmeasured |
| `ui-react-typescript-jsx-attributes` | Write inline JSX handlers as one expression, name declared ones `on` and their event, spread only declared style calls or story args, and name visible text and literal props. | tool-checked          |
| `ui-semantic-value-controls`         | Give each value domain one control whose name states its value contract, and keep application policy outside it.                                                               | judged and unmeasured |
| `ui-storybook-component-checks`      | Give every public component synthetic stories of its meaningful states and assert only consequential owned interactions.                                                       | judged and unmeasured |
| `ui-time-series-charts`              | Render application-prepared series faithfully and give pointer, touch, and keyboard users the same inspected values.                                                           | judged and unmeasured |

#### web

| Contract                           | Requirement                                                                                                                                  | Coverage              |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `web-access-scoping`               | Authorize every server entry point; scope private client data to its session and discard it on access change.                                | judged and unmeasured |
| `web-development-fixtures`         | Run presentation work against labeled synthetic responses without changing the production path or reaching production.                       | judged and unmeasured |
| `web-edge-gateway-routing`         | Route exact origins and paths to configured private upstreams, keep credentials away from static and shell upstreams, and hold no authority. | judged and unmeasured |
| `web-public-page-server-rendering` | Render complete public content and real links in server HTML, and let hydration only add interaction.                                        | judged and unmeasured |
| `web-server-state-cache`           | Keep server data in one client cache, keyed by every response-changing input and scoped to the viewer.                                       | judged and unmeasured |
| `web-url-search-state`             | Validate URL search state in the destination route that owns it, and write only non-default choices.                                         | judged and unmeasured |
| `web-write-lifecycle`              | Define each write once, show it saved only on acknowledgment, and retry only when the endpoint makes retries safe.                           | judged and unmeasured |

## Skills

Start with `tenet` for CLI usage, `tenet-adoption` for adoption and updates, or one of the curation skills.
`env-curation` sets or clears one key of a dotenv file without printing its value, and `cargo-dist-release` regenerates
cargo-dist's release workflow for a Cargo workspace in a subfolder of its repository. Install one with Tenet 0.11.0 or
later:

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
releases. Run `uv run --locked --script scripts/check-library.py` before opening a pull request, with the tools that
`mise.toml` pins installed, such as through `mise install`. It runs `scripts/lint-contracts.py`, which also checks that
the tables above list each contract once, under its area, with its message. It then runs the shipped checkers on the
library, compiles and lints the Effect probe and the env tool, runs the env tool's check with fake values, checks the
release version, and installs every contract and skill. The Check workflow runs it on each pull request and before each
release, and installs each contract without assets with Tenet 0.7.0. Test cases for a contract's tool files live in
`tests/<contract>/<tool>/`, outside the folder that projects install. Accepted changes ship in the next tag and are
credited in the changelog.

## Releases

Releases are `vX.Y.Z` tags. [CHANGELOG.md](CHANGELOG.md) classifies each change. A tightened or removed requirement is a
major release, so review the changelog before updating across one.

See <https://tenet-contracts.com/docs/guidance> for the full workflow.
