# Changelog

Each release lists every changed contract or skill under one class. A Tightened or Removed entry makes a major
release, an Added or Loosened entry a minor release, and Clarified entries alone a patch release.

Each major release after v1.0.0 has an `### Upgrading` block. Take one major at a time with the `--ref` it names,
because `tenet contracts update` without `--ref` moves straight to the newest release. Tenet 0.11.0 installs every
release, including the tool files that v9.0.0 and later ship under `assets/`.

## v12.1.0

### Loosened

- `code-lint-strictness`: check runtime assertion values without treating their declared type predicates as redundant in test code.
- `code-typescript-import-statements`: use the repository’s declared test runner, including the runtime’s runner.
  The optional `assets/oxlint/vitest.json` keeps separate-runner import restrictions scoped to repositories that use it.

### Clarified

- `env-curation`: keep the check-only environment codec private to its consumer.
- Rule fixtures cover the shipped structural checks with a violation and an allowed form.

## v12.0.1

### Clarified

- `cargo-dist-release`: explain how version comments stay in generated action references and how standalone planning
  detects workflow drift before publication.
- The contract index identifies shipped tool checks, development evaluations, and unmeasured judgments. These
  coverage labels do not change any requirement.

- `code-lint-strictness`: the cargo-deny asset is tested with 0.19.9, which fixes a build-check deadlock with one or
  two worker threads. The configured checks and lint levels are unchanged.

- `code-lint-strictness`: the Rust lint asset explains how to align C dependencies with Rust's macOS deployment target
  through `MACOSX_DEPLOYMENT_TARGET` while retaining `linker_info = "deny"`.

## v12.0.0

`cli-output-channels` and `contract-maintenance` now ship tool configuration under `assets/`, so installing or updating
them needs Tenet 0.11.0 or later. The other 114 contracts, which ship no `assets/`, still install with Tenet 0.7.0 or
later. The new and changed lint files fail on code that complied before; run each tool's autofix where it has one, then
rewrite or suppress what remains as `code-lint-suppressions` allows.

### Upgrading

Raise Tenet to 0.11.0 first. With `.tenet.lock` and the installed copies committed, run
`tenet contracts update --ref v12.0.0`.

- No rule moved to another contract.
- New assets: 10 files in 4 contracts. `cli-output-channels` ships an ast-grep rule set with
  `numeric-exit-statuses-rust` and an oxlint file. `code-typescript-effect-errors` adds the `floating-effects` rules and
  `code-typescript-input-immutability` the `parameter-mutations` rules, each for TypeScript and Tsx.
  `contract-maintenance` ships `assets/uv/check-guidance.py` with its uv lock and output module; run it with one
  `--require` pattern per kind of guidance document, as its entry says.
- Changed assets: `code-lint-strictness`'s oxlint file rejects a named generator, such as
  `Effect.gen(function* load() { ... })`, so drop the name. Its Clippy file reports `std::io::stdout` and
  `std::io::stderr`; suppress that at each of the output module's calls, as `cli-output-channels` says.
  `telemetry-application-tracing`'s oxlint file rejects `Console` and `Effect.log` calls outside `logger/log.ts`, so
  move them into the logger module. `code-typescript-import-statements` ships an empty namespace library list; a
  repository that imports `@stylexjs/stylex` or `valibot` as a namespace adds it to its own lint file and utility copy.
- New skills: `cargo-dist-release` and `env-curation`. Install either with `tenet skills add tenet/NAME`.
- Roll back with `tenet contracts update --ref v11.1.0`. This release added no contract, so every copy returns to its
  v11.1.0 text. A tool file that v11.1.0 lacks stays in place, leaves the lock, and makes `update` exit 1; delete it
  with `git rm`. Remove an added skill with `tenet skills remove PATH`.

### Tightened

- `cli-output-channels`: the contract now ships its lint. A new `numeric-exit-statuses-rust` ast-grep rule reports an
  integer literal passed to `ExitCode::from` or `std::process::exit`, such as `ExitCode::from(2)`, outside the output
  module and the `ExitStatus` declaration, with one violation and one allowed case under `tests/`. A new oxlint file
  sets `no-console` and exempts `output.ts` from it, from `no-restricted-properties`, and from
  `unicorn/no-process-exit`. The rules say to load these and `code-lint-strictness`'s stream entries, and to suppress a
  rule at each of the output module's calls where the lint cannot scope it to a path. Before, nothing shipped reported a
  stream handle or a numeric exit status.
- `code-blank-lines`: a `yield*` statement now takes a blank line on each side like a call statement, except between
  call statements, and the shipped oxlint file's `padding-line-between-statements` selectors include it. Before,
  `const first = yield* readOrder({ id });` directly followed by `yield* notify({ order: first });` passed.
- `code-lint-strictness`: the shipped oxlint file sets `func-names` `generators` to `never`, so a generator function
  expression is anonymous, such as `Effect.gen(function* () { ... })`, as `code-typescript-effect-errors` now writes it.
  Before, each anonymous generator failed and a named one passed; now a named one fails.
  The shipped Clippy file's new `disallowed-methods` entries report `std::io::stdout` and `std::io::stderr` outside the
  output module that `cli-output-channels` declares; its restriction group already denies the print macros and
  `std::process::exit`. A repository adds each dependency's function that opens a standard stream to that list.
- `code-typescript-effect-errors`: an `Effect` call written as a bare statement, such as
  `Effect.fail(new InvoiceNotFound({ invoice }));`, which builds the Effect and never runs it, now violates the contract.
  The new `floating-effects-typescript` and `floating-effects-tsx` rules report it, except a run function such as
  `Effect.runFork`, with one violation and one allowed case under `tests/`. The bound statements now go in an
  anonymous generator, and `Effect.fn('name')` is the one form for a function whose calls a trace records, never
  `Effect.withSpan` around the function's result.
- `code-typescript-import-statements`: the shipped namespace library list is empty. `import/no-namespace` no longer
  ignores two named vendor packages, and the `misimported-namespace-library` utility matches no library until a
  repository's own copy adds one. A repository that imports a library as a namespace declares it in both lists, as the
  rules already said; before, the shipped list named vendors that the contract's name does not carry.
- `code-typescript-input-immutability`: the new `parameter-mutations-typescript` and `parameter-mutations-tsx` rules
  report `push`, `splice`, `sort`, `reverse`, `set`, `add`, `delete`, or `clear` called on a parameter or on a chain of
  properties and indexes read from one, such as `order.lines.push(line)`, with one violation and one allowed case under
  `tests/`. `clear` joins the rule's list of changing methods, and the lint check again expects a finding on
  `order.lines.push(line)`.
- `contract-maintenance`: each relative link in a guidance document, such as a contract, a skill, or an agent
  instruction file, must resolve to a file in the repository. A repository declares the frontmatter fields each kind of
  guidance document needs, such as a skill's `name` and `description`, and each document of that kind gives every field
  as a nonempty string. The contract now ships the check, `assets/uv/check-guidance.py` with its uv lock and output
  module, and needs Tenet 0.11.0. Run it from the repository root on the paths that hold guidance, with one
  `--require PATTERN=FIELD,...` per kind of document, where the first matching pattern applies and an empty field list
  exempts the documents it matches. It reports each missing link target and missing field on standard output and its
  summary on standard error, and an unreadable frontmatter block or link ends it with the document's path. Before, a
  broken link or a skill without a `description` complied.
- `telemetry-application-tracing`: the shipped oxlint file's `no-restricted-properties` now rejects Effect's `Console`
  module and the `Effect.log`, `logDebug`, `logError`, `logFatal`, `logInfo`, `logTrace`, `logWarning`, and
  `logWithLevel` functions outside `logger/log.ts`, as the rule against a logging library's function outside the
  logger module already required. Before, the lint passed them.

### Loosened

- `cli-output-channels`, `code-lint-strictness`, `code-module-file-roles`, and `telemetry-application-tracing`: each
  shipped oxlint or ast-grep file that exempts a declared file role now also matches the role's `.mts` file, which
  `code-typescript-node-scripts` requires for every script and helper module: `output.mts`, `errors.mts`,
  `schemas.mts`, `settings.mts`, and `logger/log.mts`. Before, a script's output module failed `no-console`, and its
  errors and schemas files took the rules that those roles are exempt from, such as `max-classes-per-file`.
- `code-lint-strictness`: the shipped zizmor file turns the `self-repository` audit off with reason R. The audit asks
  for the `$/` form of a same-repository action or reusable workflow, such as `uses: $/.github/workflows/check.yml`,
  which actionlint 1.7.12 rejects; before, each `uses: ./` call failed one of the two checkers.

### Added

- `scripts/check-library.py` runs zizmor offline and actionlint, with shellcheck and pyflakes, on the library's
  workflows, using `.github/zizmor.yml` and `.github/actionlint.yaml`, its copies of the files that
  `code-lint-strictness` ships. It also runs ruff on the Python scripts that a skill or a contract ships, ty on the
  release script, and every shipped ast-grep rule set on the skills and the guidance check. In the committed copy, it
  installs the env tool's packages, compiles it with `tsc --noEmit`, lints it with every shipped oxlint file, and runs
  its system check with fake values. `ruff.toml` applies the shipped ruff file to those scripts.
- `.github/workflows/check.yml` runs `scripts/check-library.py` on each pull request, with the tools that `mise.toml`
  pins, and installs each contract that ships no `assets/` with Tenet 0.7.0, the oldest Tenet the README names for one.
  `release.yml` runs it before tagging a version commit, in place of its own install with Tenet 0.11.0.
- `env-curation` is a new skill that sets, replaces, or clears one key of a dotenv file, such as the file that mise
  loads through `_.file`, without printing its value. Its `scripts/env-tool.mts` reads the value from a named variable,
  a prompt with echo off, or one line of piped input, refuses a value passed as an argument without printing it, and
  replaces the file through an owner-only temporary file and one rename, refusing a file that changed meanwhile. It is
  written on effect, with 8 tagged error classes, asynchronous `node:fs/promises` calls, and an output module that ends
  with a closed `ExitStatus`. `scripts/check/check-env-tool.mts` runs the real tool on a scratch file with fake values,
  reads them back through `mise env --json`, and checks each refusal. `scripts/package.json` and its lockfile pin
  effect 4.0.4, the probe's version, as the tool's one dependency, and TypeScript 7.0.2 for its type check.
- `cargo-dist-release` is a new skill that regenerates the release workflow cargo-dist writes for a Cargo workspace in a
  subfolder of its repository. Its `scripts/generate-release.py` copies the workspace without `target` to a temporary
  Git repository, runs `dist generate` there, and copies `.github/workflows/release.yml` back. `--workspace` names the
  workspace, `--prefix` the start of the temporary folder's name, and `--dist` the cargo-dist command.

## v11.1.0

### Loosened

- `code-lint-strictness`: the shipped oxlint file turns `typescript/prefer-readonly-parameter-types` off with reason Q.
  Its rule groups enabled the rule in every TypeScript file, where it reported each parameter that holds a tagged error
  class, an `Option`, or an `Effect`, such as `error: ProviderBusy`. `code-typescript-effect-errors` and
  `code-typescript-effect-absent-values` require those types, and their inherited fields and methods are not read-only.
  The override that turns `unicorn/max-nested-calls` off in schema files now also covers files named `errors`, as
  `code-typescript-call-arguments` now allows. The shipped markdownlint file sets MD024 `siblings_only` with reason Q,
  so a heading may repeat one in another section, such as `### Added` under each version of a changelog; before, every
  repeated heading in a document failed.
  The shipped oxlint file turns `no-undef` off in TypeScript files with reason Q, because the compiler's type check
  reports every undeclared name; it reported globals the compiler declares, such as `process` and `URL`, 282 times in
  one adopter. Its vitest override moves to a new `assets/oxlint/vitest.json`, which a repository extends right after
  `oxlintrc.json` only where vitest runs its tests, so vitest's rules no longer run on tests that another runner loads,
  such as tests that import `node:test`. That override now matches only vitest's default test file names, `**/*.test.*`
  and `**/*.spec.*`, not every file in a `test`, `tests`, or `__tests__` folder. The rules now ask a repository to
  extend each shipped file whose opening comment applies to it, and to set in its own configuration each key that a
  checker does not read through an extended file. The oxlint file's new opening comment says that oxlint reads `env`,
  `globals`, and `settings` only from the configuration it runs, so a repository sets `env` there for the runtimes its
  JavaScript files run in.
  A checker may now skip a file that a tool generates, such as a lockfile, through a path scope whose comment names
  that tool; before, every checker had to pass every file it reads. The shipped typos file allows, with reason Q,
  oxlint's `IIFEs` option and, in `CONTRACT.md` files only, the spelling variant that `code-spelled-out-names` names
  and the misspelled field that `code-typescript-effect-schemas` decodes; before, a full install failed typos on
  all 3. Its opening comment says how to exclude a generated file. The shipped tsconfig's comment keeps `skipLibCheck`
  off and gives each runtime's files their own tsconfig where two packages in `types` declare the same global.
  The shipped oxlint file sets `no-duplicate-imports` `includeExports` to `false` with reason Q, because oxlint 1.80.0
  reports each further name of one `export { log, LogEvent } from './log.ts'` statement as a duplicate, and
  `code-typescript-entry-points` writes an entry point's re-exports of one file that way; before, every entry point
  that re-exported two names from one file failed.
- `code-python-exception-propagation`: a handler in a program's entry point may now catch an exception type that the
  program declares for one outcome, report it, and end the process with that outcome's declared exit status, as
  `cli-output-channels` describes. Before, such a handler violated this contract, although `cli-output-channels` has
  only the entry point map each outcome to its exit status. The message, an allowed example, and the check now name it.
- `code-rust-doc-comment-coverage`: the `exported-doc-comments-rust` rule skips a package's binary targets,
  `src/main.rs` and `src/bin/`, and its opening comment and the rules now run it over each library crate's folder,
  never over a binary crate or the repository root. Before, its example scanned the whole repository and reported
  each `pub` item of a binary crate, which the contract leaves out.
- `code-typescript-call-arguments`: a file with the declared errors role may now nest calls, `new` expressions, and
  `await` inside arguments, as a schema file may, because a tagged error class's fields are schemas, such as
  `codes: Schema.Array(Schema.String)`. The shipped ast-grep rules ignore files named `errors` beside files named
  `schemas`.
- `code-typescript-class-declarations`: a schema class that `code-typescript-effect-schemas` allows, such as
  `class Invoice extends Schema.Class<Invoice>('Invoice')({ ... }) {}`, is now a class a library requires; before, the
  list of allowed classes left it out.
- `code-typescript-effect-scheduling`: a retry or deadline that a later invocation resumes from storage, such as a job's
  next attempt time, is a durable job, not an `Effect.retry` or `Effect.timeout`, so a job that stores its next attempt
  and resumes it on a later wake-up now complies. A retry that a library performs on its own requests, such as a model
  client's retry of a rate-limited call, now stays in that library's configuration, as a library's deadline on its own
  resource already did. A new check runs the type check against effect 4.0.0 or later.
- `code-typescript-import-statements`: the shipped oxlint file no longer turns the vitest plugin on in test files, so
  vitest's rules no longer run on tests that another runner loads. Its `no-restricted-imports` entry for tests now
  rejects `node:test`, which `vitest/no-import-node-test` rejected before. `no-restricted-globals` still rejects the
  runner's globals that `vitest/prefer-importing-vitest-globals` also reported, but a runner function imported from a
  module other than `node:test` no longer fails the lint.
- `code-typescript-input-immutability`: a parameter's type may now hold a type that `code-typescript-effect-errors` or
  `code-typescript-effect-absent-values` requires, such as a tagged error class or an `Option`, as declared; before, the
  whole type had to be read-only at every depth. A dependency type with no read-only form, such as `Request`, also stays
  as declared, with no lint allow list. The shipped oxlint file no longer sets
  `typescript/prefer-readonly-parameter-types` or needs type information. The lint check no longer expects a finding on
  a parameter's `order.lines.push(line)` or type `{ invoice: Invoice }`; a review question asks whether each parameter
  property the lint does not reach is `readonly`.
- `test-assertion-integrity`, `test-curation`, and `test-scenario-functions`: each shipped oxlint file now opens with a
  comment to extend it only where vitest runs the repository's tests, after `code-lint-strictness`'s `vitest.json`, and
  matches only vitest's default test file names, `**/*.test.*` and `**/*.spec.*`. Before, every repository that
  extended it ran its vitest rules on every test file and on each helper file in a `test`, `tests`, or `__tests__`
  folder.

### Added

- `scripts/lint-contracts.py` checks that the README lists each contract once, in the table under its area, with its
  message as the requirement, that the area headings follow the naming table in order, and that the stated contract
  count is current. It reads the closed list of areas from that naming table. It also requires each ast-grep rule and
  utility file to declare a top-level `id` that no other file declares. The script runs with
  `uv run --script scripts/lint-contracts.py` and takes no folder argument, because it checks the library that holds it.
  It writes its findings to standard output and its closing summary to standard error through `scripts/output.py`, and
  `ruff.toml` applies the ruff file that `code-lint-strictness` ships to both scripts.
- `tests/<contract>/<tool>/` holds test cases for a contract's shipped tool files outside the contract's folder, so an
  installed contract never carries them. `tests/code-typescript-effect-errors/ast-grep/` starts the tree with one
  allowed and one violating case for `untagged-errors-typescript`; run `ast-grep test` from the library root with the
  `sgconfig.yml` in that folder. `scripts/lint-contracts.py` refuses a `tests/` folder that names no contract, a file
  outside a folder named for one of the contract's `assets/` tools, and an ast-grep case whose file name or id names no
  shipped rule, since `ast-grep test` passes such a case.
- `scripts/check-library.py` is the library's self-check, which a pull request runs before merge. It runs
  `scripts/lint-contracts.py`, then the shipped yamllint, markdownlint, typos, taplo, ruff, and ty files on the library's
  own files, oxfmt on its Markdown, every shipped ast-grep rule set on its scripts and the Effect probe, and
  `ast-grep test` on each test tree. It refuses a newest release whose version does not raise the release below it by
  the part its strongest class sets, a YAML file under `contracts/` or `tests/` that YAML 1.1 and YAML 1.2 read as
  different data, and two shipped oxlint files that set one rule differently. In a committed copy of the library, it
  compiles the probe with `tsc --noEmit`, lints it with every shipped oxlint file in one configuration, checks that the
  pinned effect exports every `Effect`, `Schema`, `Option`, `Schedule`, `Data`, and `Context` member that a contract or
  rule file names, and installs every contract and skill with the pinned Tenet. `mise.toml` pins each tool it runs, and
  it refuses a tool that prints another version; `package.json` pins oxlint and its plugins. Run it with
  `uv run --locked --script scripts/check-library.py`.
- `tests/code-lint-strictness/typescript/` is an Effect probe project written in the TypeScript Allowed forms of
  `code-typescript-effect-absent-values`, `code-typescript-effect-errors`, `code-typescript-effect-scheduling`, and
  `code-typescript-effect-schemas`. Its tsconfig extends the tsconfig files that `code-lint-strictness` and
  `code-typescript-node-scripts` ship, and its `package.json` and lockfile pin effect 4.0.4 and TypeScript 7.0.2.
- Every major release from v2.0.0 to v11.0.0 now has an `### Upgrading` block. It names the rules that moved and the
  contracts that now hold them, the new tool files under `assets/`, the Tenet to install first, and the rollback
  command. `scripts/lint-contracts.py` requires the block in each major release after v1.0.0, with the rollback
  `tenet contracts update --ref` to the release before it.

### Clarified

- `api-typescript-request-paths`, `code-boolean-names`, `code-closed-value-sets`, `code-comment-form`,
  `code-conditional-expressions`, `code-constant-names`, `code-diagnostic-messages`, `code-map-and-set-names`,
  `code-module-file-roles`, `code-module-structure-and-control-flow`, `code-rust-doc-comment-coverage`,
  `code-rust-source-structure`, `code-spelled-out-names`, `code-typescript-call-arguments`,
  `code-typescript-collection-iteration`, `code-typescript-const-bindings`, `code-typescript-effect-absent-values`,
  `code-typescript-effect-errors`, `code-typescript-effect-scheduling`, `code-typescript-effect-schemas`,
  `code-typescript-expression-forms`, `code-typescript-function-arguments`, `code-typescript-import-extensions`,
  `code-typescript-import-statements`, `code-typescript-input-immutability`, `code-typescript-module-state`,
  `code-typescript-object-literal-functions`, `code-typescript-runtime-keyed-maps`, `code-typescript-type-assertions`,
  `telemetry-application-tracing`, `test-assertion-integrity`, `ui-design-tokens`, `ui-react-hook-calls`, and
  `ui-react-typescript-jsx-attributes`: each shipped ast-grep file, 249 in all, now quotes every key and string, sorts
  each map's keys by code point, writes every map in block form, and starts with `---` and ends with `...`. Before,
  these files failed the shipped yamllint file 20,345 times in every repository that installed them. Each file loads
  to the same YAML 1.2 data as before, and the rules report the same matches. The test cases under `tests/` take the
  same form.
- `code-blank-lines`, `code-conditional-expressions`, `code-exhaustive-branches`, `code-function-size`,
  `code-typescript-doc-comment-coverage`, and `code-typescript-function-scoping`: each shipped oxlint file opens with a
  comment that pins the plugin it loads through `jsPlugins` to the version it was checked with:
  `@stylistic/eslint-plugin` 5.10.0, `eslint-plugin-sonarjs` 4.2.2, `eslint-plugin-unicorn` 79.0.0, and
  `eslint-plugin-jsdoc` 65.4.2.
- `code-diagnostic-messages`: the TypeScript and Tsx `diagnostic-case` and `diagnostic-values` rules no longer read
  `Effect.dieMessage`, `Effect.dieSync`, or `orElseFail`, which effect 4 does not export, and their comments give
  `Schema.TaggedError` as an error class example. Their matches on effect 4 code are unchanged. The prefix rule and the
  empty-path violation now state in words the space after `deploy:` and after `read invoice`, since Markdown hides a
  space at the edge of a code span.
- `code-lint-suppressions`: the rules and the allowed example now write the reason separator as two hyphens with a
  space on each side, since Markdown drops a space at both edges of a code span.
- `code-typescript-effect-absent-values`: the type check runs against effect 4.0.0 or later.
- `code-typescript-effect-errors`: the tagged error example and the `untagged-errors` notes declare classes with
  `Schema.TaggedError`. The v11.0.0 entry called `Schema.TaggedErrorClass` the Effect 4 name, but no stable effect 4
  release exports it, so a class copied from the example failed the type check. The `untagged-errors` rules no longer
  report `Effect.dieMessage`, which effect 4 does not export. The type check runs against effect 4.0.0 or later.
- `code-typescript-effect-schemas`: the `excess-properties` rules no longer read `Schema.decodeUnknown` or the `Either`
  decode variants, which effect 4 does not export, and still report every decode call that effect 4 exports. The type
  check runs against effect 4.0.0 or later.
- `code-typescript-module-boundaries`: the rules now state that a configuration that extends the shipped oxlint file
  copies its `settings`, because oxlint does not read them through `extends`, and every file fails
  `boundaries/no-unknown-files` without them. Only a changelog entry said so before. The file's comments pin
  `eslint-plugin-boundaries` 7.3.0 and `eslint-import-resolver-typescript` 4.4.5 and say that `boundaries/elements`
  makes every folder a module.
- `library-contract-format`, `library-contract-generality`, `library-contract-naming`, and `library-skill-portability`:
  each check runs the lint with `uv run --script scripts/lint-contracts.py`, as `code-python-uv-scripts` requires,
  instead of `python3`.
- `tenet-adoption`: the public library's address is written as code instead of a bare URL; its steps are unchanged.
- `tenet-architecture-curation`: the formatter aligns the boundary table in `references/boundaries-and-data.md`; its
  text is unchanged.

## v11.0.0

`code-boolean-names`, `code-comment-form`, `code-constant-names`, `code-declaration-order`, `code-diagnostic-messages`,
`code-lint-strictness`, `code-map-and-set-names`, `code-module-structure-and-control-flow`,
`code-rust-doc-comment-coverage`, `code-rust-source-structure`, `code-spelled-out-names`,
`code-typescript-boolean-conditions`, `code-typescript-collection-iteration`, `code-typescript-compiler-strictness`,
`code-typescript-const-bindings`, `code-typescript-doc-comment-coverage`, `code-typescript-effect-absent-values`,
`code-typescript-effect-scheduling`, `code-typescript-effect-schemas`, `code-typescript-export-return-types`,
`code-typescript-expression-forms`, `code-typescript-function-arguments`, `code-typescript-function-member-signatures`,
`code-typescript-function-scoping`, `code-typescript-import-extensions`, `code-typescript-import-statements`,
`code-typescript-input-immutability`, `code-typescript-module-state`, `code-typescript-named-types`,
`code-typescript-object-literal-functions`, `code-typescript-runtime-keyed-maps`, `code-typescript-type-assertions`,
`telemetry-application-tracing`, `test-assertion-integrity`, `test-curation`, `test-scenario-functions`,
`ui-design-tokens`, `ui-react-hook-calls`, `ui-react-interaction-ownership`, and `ui-react-typescript-jsx-attributes`
now ship tool configuration under `assets/`, so installing or updating them needs Tenet 0.11.0 or later. The shipped
lint files fail on code that complied before; run each tool's autofix where it has one, then rewrite or suppress what
remains as `code-lint-suppressions` allows.

### Upgrading

Raise Tenet to 0.11.0 first. With `.tenet.lock` and the installed copies committed, run
`tenet contracts update --ref v11.0.0`.

- Moved rules: the function-binding rule, its check, and its `func-style` setting move from
  `code-typescript-call-arguments` to `code-typescript-const-bindings`. The relative-import extension rule moves from
  `code-typescript-node-scripts` to `code-typescript-import-extensions`, and its `verbatimModuleSyntax` requirement to
  `code-typescript-compiler-strictness`. The one logger module for a server's log lines moves from `cli-output-channels`
  to `telemetry-application-tracing`. `code-rust-workspace-checks` now denies its lints through the lint tables and
  `clippy.toml` that `code-lint-strictness` ships, and formats with its `rustfmt.toml`. Install each receiving contract
  wherever the old one is installed, or the rule no longer applies there.
- New assets: 266 files in 46 contracts and 19 tool folders, 224 of them for ast-grep. They go to the 40 contracts above
  and to `code-closed-value-sets`, `code-conditional-expressions`, `code-module-file-roles`,
  `code-typescript-call-arguments`, `code-typescript-effect-errors`, and `code-typescript-node-scripts`.
  `code-lint-strictness` alone ships the files for 17 tools. Pin each tool and plugin at the version its entry names
  before running it.
- Roll back with `tenet contracts update --ref v10.0.0`. Copies of the 22 contracts this release added are reported as
  removed upstream and left in place; drop each with `tenet contracts remove PATH`, which also deletes its locked
  assets. A tool file that v10.0.0 lacks stays in place, leaves the lock, and makes `update` exit 1; delete it with
  `git rm`.

### Tightened

- `code-boolean-names`: every owned function and method that returns a boolean must start with a listed predicate
  prefix, never an option prefix such as `include` or `skip`. This covers a function whose boolean arrives through a
  promise, an effect, or a result that may fail. An accessor, which reads as a property or only returns a field, is
  named as a field is. Any function, method, or function-typed constant, field, or member named `on` and a capital
  letter, such as `onSubmit`, is an event handler and keeps that name, as `ui-react-typescript-jsx-attributes` requires.
  A component's prop for an attribute on a declared list of markup boolean attributes, such as `disabled` or `open`, now
  takes that bare name, never `isDisabled`. That holds, with no suppression, when the component forwards the prop to an
  element or a dependency's component. Every other boolean prop takes a listed prefix, such as `isBusy` for `busy`. The
  contract now ships ast-grep rules for TypeScript, Tsx, Python, and Rust that check functions, methods, and
  function-typed constants, fields, and members. Each rule rejects one whose declared return type is such a boolean and
  whose name has no predicate prefix. New TypeScript and Tsx rules, the boolean field rule's first shipped check, reject
  a props type's boolean field that has no predicate or option prefix. A props type is a type whose name ends in `Props`
  or the type written on a component's parameter. A prop itself, rather than a nested field, also passes when its name
  is on the attribute list, and the rules check no other boolean field. The default predicate prefixes, option prefixes,
  and HTML boolean attribute names ship as shared rules that a repository replaces with its own copies. It requires
  Tenet 0.11.0.
- `code-closed-value-sets`: declare each whole closed set, and each subset of two or more members, that code tests
  membership in once, as a module-level read-only set such as `ReadonlySet<SandboxState>`, `frozenset`, or a constant
  array where a module constant cannot hold a set, and test it with its lookup, such as `endedStates.has(state)`, never
  with a collection written at the test, such as `[A, B].includes(state)` or `new Set([A, B]).has(state)`, even for two
  members. Compare a value with one member directly. Test two or more members only with a declared set's lookup, never
  with comparisons or a pattern written at the test: comparisons of one value joined by a logical or, such as `state ===
SandboxState.Stopped || state === SandboxState.Failed`, their negation joined by a logical and, and a pattern such as
  `matches!(state, SandboxState::Stopped | SandboxState::Failed)` no longer comply, and the Allowed line for them is
  removed. A branch that names every member, with members that share a result in one case or arm, stays the form for a
  test that must narrow a type or whose members no constant can hold, as `code-exhaustive-branches` requires, and a new
  Allowed line shows it. A member's literal value is now allowed as a key of a style definition whose library compiles
  only literal keys, when the type checker rejects a key outside the set, so a definition whose type argument is
  `Record<Tone, Style>` that writes `neutral` and `positive` as keys, which violated the contract before, now complies;
  a new Allowed line shows it. The `http-method-literals` rules for TypeScript and Tsx no longer report a key of an
  object passed to `stylex.create`, the one style definition call they declare, and a repository replaces that pattern
  with its own library's call; their counts in the four measured repositories are unchanged. The stored-value and
  migration rules are now one line, with no change to compliance. New ast-grep rules (TypeScript and Tsx) report an
  array literal of fixed values tested with `includes`, an inline `new Set` of them, with or without `as const`, tested
  with `has`, and `includes` on a module-level constant array, including one ending in `as const`; a fixed value is a
  literal, a member of a capitalized name such as `SandboxState.Stopped`, or a SCREAMING_SNAKE_CASE constant, so a list
  of run-time properties such as `[user.id, owner.id]` is not reported. New ast-grep rules
  `member-chains-typescript.yml`, `member-chains-tsx.yml`, `member-chains-python.yml`, and `member-chains-rust.yml`
  report two or more equality comparisons of one value with fixed values joined by a logical or, and inequality
  comparisons joined by a logical and, once per chain, including chains of literals such as `kind === 'draft' || kind
=== 'sent'`; `member-patterns-rust.yml` reports a `matches!`, `if let`, `while let`, or `let ... else` pattern that
  joins two or more members or literals with `|`, ranges excepted. None has an autofix, and a comparison with the value
  on the right or inside another macro's arguments is left to review. A new oxlint file enables `unicorn/prefer-set-has`
  for named arrays used only with `includes`. The lint check now confirms the lint reports `state === A || state === B`,
  a new review check asks whether each style definition a change keys by a closed set's literal values has a type that
  rejects a key outside the set, the suppression rule joins the asset-loading rule, and the path-pattern rule now also
  names the style definition call, so the contract keeps 25 rules.
- `code-comment-content`: a doc comment on any field that may hold no value, such as an `Option` field, must now say
  what the field's absence means, where the rule covered only optional or nullable fields, and the review check asks the
  same of each changed doc comment. A field that can be either omitted or null still says what each means, and the
  example is now `/** Absent when the check sent no model request. */`. The scope rule splits into three lines and says
  that `code-comment-form` governs task markers, commented-out code, step labels, and the form, placement, and layout of
  comments. The stored-format allowance splits into two lines under 30 words, and its example is now a capitalized
  sentence, "Revisions written before format 2 list their files in each assessment." The Allowed comment now sits inside
  the signing function, where `code-comment-form` puts a plain line comment.
- `code-comment-form`: write every comment and doc comment as one or more sentences that start with a capital letter.
  Line comments on consecutive lines form one comment. Put a code identifier that opens a comment in backticks, such as
  ``// `retryAfter` is absent.``. The lint skips a comment that opens with no letter, with a link, with a type
  annotation such as `@type`, or with a listed directive word. The lint, the shipped configuration, or a repository's
  copy lists those directive words. A new `assets/oxlint/oxlintrc.json` sets oxlint's native `capitalized-comments` to
  `always` with `ignoreConsecutiveComments`. Its `ignorePattern` covers `ast-grep-ignore` and a check's `-allow`
  directive, beside the lint and formatter directives the rule skips by default. Its `--fix` capitalizes the first
  letter, so a comment that opens with an identifier is rewritten into backticks by hand. New ast-grep rules
  `comment-capitals-python` and `comment-capitals-rust` report the same comments, and Python docstrings, skip each
  language's directive words, and have no fix. Never number or letter a step in a comment, such as `// 4.` or `// (g)`;
  give each step a function named for what it does. A numbered list inside a doc comment stays allowed. Outside a
  function body, every comment above or beside a declaration, a class, type, interface, or enum member, or a module
  constant is a doc comment directly above it. It takes the line form where a language has both, such as `///`. Inside a
  function body a comment is a plain line comment, never a doc comment. Where the doc comment is a string, it is the
  function's or class's docstring, or a string directly below a module constant's or class field's assignment. A tool's
  directive, such as a lint suppression, and the reason line that `code-lint-suppressions` puts above one keep their
  tool's form. Every file that `code-script-entry-points` covers opens with a summary that says what it does and how to
  run it. New ast-grep rules report step labels in TypeScript, Tsx, JavaScript, Rust, and Python. They report plain
  comments above or beside declarations and members outside function bodies in TypeScript, Tsx, Rust, and Python. They
  report doc comments inside function bodies in TypeScript, Tsx, and Rust. In all five languages, they report an
  executable file under `scripts/` or `bin/` whose first comment after its required opening lines is not a doc comment.
  A repository replaces those path patterns in its own copy. The message now names capitalized sentences, and the
  task-marker, member, and suppression sentences merge into their neighbors without changing what they require. The
  commented-out code example now reads `// Receipts.send({ order });` and the step-label example `// (b) Copy the
rows.`, so each breaks only its own rule. A new example pair and review check cover a comment that opens with an
  identifier. Every doc comment in every language is prose, with no section or tag for parameters, results, yielded
  values, errors, panics, or usage examples. Those include `@param`, `@returns`, `@yields`, `@throws`, `Args:`,
  `Returns:`, `Raises:`, `# Errors`, `# Panics`, `# Examples`, `Examples:`, and `@example`. `# Safety` is the only
  section allowed. New ast-grep rules `prose-doc-comments-<language>` report them in all five languages. They also
  report `@typeParam`, `@template` outside JavaScript, a tag right after a leading asterisk, and a Python section with
  text on its line. No source file carries a copyright or license notice, because the repository's `LICENSE` file states
  the license once. A license notice is no longer a tool directive or an allowed opening line before a file summary. The
  exemption regexes of the declaration-comment and file-summary rules drop it. New ast-grep rules
  `license-notices-<language>` report a comment in any of the five languages that opens with `Copyright`, `©`, `(c)` and
  a year, `Licensed under`, `@license`, or `SPDX-License-Identifier:`. They also report a Python module docstring that
  opens with `Copyright`, `©`, or `SPDX-License-Identifier:`. The message names license notices and prose doc comments,
  and a new example pair covers a tagged doc comment and an SPDX line. The commented-out-code and empty-doc-comment
  sentences and the two asset-loading sentences merge without changing what they require. It requires Tenet 0.11.0.
- `code-conditional-expressions`: choose between branches of markup in a component whose `if` statements, or `switch`
  cases for a closed set, each return one branch, extracted from any larger markup, never in sibling children on a
  condition and its negation such as `{isPaid && <Receipt />}` beside `{!isPaid && <PaymentForm />}`. Show one piece of
  markup or nothing with one `&&` child where it is rendered. Give a component a visibility prop such as `isVisible`
  only when it stays mounted while hidden to keep its elements' state or to animate out, hide it with styles, and never
  return nothing from a component when a boolean prop alone, or its negation, decides it, such as `if (!isVisible) {
return null; }`. The message now names markup chosen with extracted components. New ast-grep rules (Tsx and
  JavaScript, since markup cannot occur in `.ts` files) report a child `{C && A}` or `{C && D && A}` beside a sibling
  `{!C && B}` or `{!C && E && B}`, and a child `{x === v && A}` or `{x === v && D && A}` beside a sibling `{x !== v &&
B}` or `{x !== v && E && B}`. They also report, in a component, an `if` on a bare prop or its negation, whether
  destructured in the parameters or the body or read from the props object, that returns `null`, or that returns markup
  just before `return null`; a component is a function or arrow bound to a capitalized name. The review check on values
  is unchanged, a new check asks that each markup choice be one `&&` child, a branch an extracted component returns, or
  a component kept mounted while hidden, and the lint check now names the forms this contract configures instead of
  listing them. The oxlint `no-ternary` file is unchanged and still reports conditional operators in markup. The
  `pending = refreshToken()` example is removed because it reassigns outside a loop or callback. Example booleans take a
  predicate prefix, as in `isReady ? total : 0`, as `code-boolean-names` requires. The `limit` examples become
  `shippingDays` and `chooseShippingDays({ order })`, which carry a unit as `code-measured-value-names` requires. The
  immediately invoked function Violation returns `RUSH_DAYS` or `STANDARD_DAYS` after a blank line, so it breaks only
  the rule it shows.
- `code-diagnostic-messages`: start every diagnostic with a lowercase word in every language, so that messages chain
  after a colon, as in `tag "v0.3.1": the working tree has changes`. A first word that is a proper noun, an identifier,
  or a code keeps its spelling. A message that starts with an interpolated value starts with that value as it is. Quote
  every value a diagnostic interpolates, whatever its type, with the language's form that prints a string literal with
  escapes, such as `JSON.stringify(value)`, `{value:?}`, or `{value!r}`. Quoting keeps an empty, padded, or multi-line
  value from producing a misleading line. A number is quoted too, and a `bigint` is quoted as its text, such as
  `JSON.stringify(amountText)` after `const amountText = String(amount)`. No other conversion, such as `String(value)`,
  and no hand-written quotes or backticks are allowed. Carry a cause's own message in the error's cause chain when the
  output module prints that chain, and otherwise append it after a colon as text. Write that text as a `message` read,
  `{error:#}`, or `{error!s}`. A log or trace record that the program exports is not a diagnostic;
  `telemetry-application-tracing` governs it. The case rule covers error messages, the message templates that error
  types declare, context added to a cause, and standard error lines; the trailing-period rule is unchanged. The contract
  now ships `assets/ast-grep/` rules for TypeScript, Tsx, Rust, and Python, and it declares `requires-tenet: 0.11.0`.
  The `diagnostic-case-*` rules report a capitalized first word. The `diagnostic-values-*` rules report an unquoted
  value in each message an error carries, whether thrown, failed, declared by its type, or returned beside its code. An
  output module writes the line it receives unquoted after the program's prefix, and the lint leaves those lines to
  review. The default proper nouns live once, in the shared util `assets/ast-grep/utils/proper-nouns.yml` (id
  `proper-noun-text`), which every case rule matches. They are month and weekday names except May, which reads as the
  verb, and Git, Linux, Postgres, Python, and Rust. A repository adds its own names in its own copy of that util with
  the same id, loaded through its own `utilDirs` in place of the shipped one. It edits no shipped file. The Allowed
  examples now quote each value they interpolate, numbers included.
- `code-exhaustive-branches`: `assets/oxlint/oxlintrc.json` no longer turns off 16 type-aware rules that it turned off
  only to keep its own test cases focused, such as `typescript/no-floating-promises` and `typescript/unbound-method`,
  because an off entry in an extended file beats every category and so switched those rules off in every adopting
  repository; they now run at the level the repository's other configuration sets. Never end a branch that names every
  member with a default case or wildcard arm, because a member added later would take it unreviewed;
  `typescript/switch-exhaustiveness-check` now sets `allowDefaultCaseForExhaustiveSwitch` to false, and the lint check
  confirms that a default after every member fails. A test with the lookup of a declared subset of two or more members,
  such as `endedStates.has(state)`, is not a wildcard, so its `else` may serve the remaining members; a test for one
  member whose other branch serves every remaining member stays a wildcard. The final-`else` review check now passes a
  final `else` that follows a declared subset's lookup. The Violation's `else if` chain now tests `OrderStatus.Paid`,
  `OrderStatus.Refunded`, and `OrderStatus.Cancelled` one at a time, so it no longer also joins members with a logical
  or, which `code-closed-value-sets` now rejects.
- `code-function-size`: declare a maximum depth of markup elements nested inside one another, and enforce it with the
  repository's lint on markup written in code, including test code. Move the markup past it into a child component,
  which starts its own count. An element's depth is the number of elements and fragments enclosing it, including through
  a condition, callback, call, local variable, or attribute value. Its `assets/oxlint/oxlintrc.json` now sets oxlint's
  native `react/jsx-max-depth` to 6, which a repository may override like the file's other limits. The rule takes effect
  where the repository's own configuration enables the `react` plugin, and has no autofix. At 6 the rule reports 49
  elements in 12 files of the largest measured repository, whose deepest markup is 8 levels, and none in the other
  three. Declare a maximum number of statements per function too, counting every statement in its body, including those
  inside its blocks, and leaving each nested function to its own count. Declare a maximum complexity in each measure a
  language's lint computes, such as cyclomatic and cognitive complexity. The shipped file now sets `max-statements` to
  10 and `complexity` to 10 in its classic variant, beside the cognitive complexity of 15, and a repository may override
  each. The cyclomatic maximum of 10 matches the `max-complexity` of 10 that `code-lint-strictness` ships for ruff's
  C901, so both languages declare one value. In the four measured repositories, the two rules report 430 / 58 / 25 / 71
  and 204 / 37 / 12 / 33 functions, with no autofix. A language may go without any of these limits only when the
  repository declares the language, the limit, and the reason beside its limits. One such reason is that no lint for the
  language counts statements. This one exemption replaces the separate complexity exemption, so length, nesting, and
  callback limits may now be exempted the same way. The message now names markup depth. The checks now run the
  repository's lint and count depth through the calls, callbacks, and local variables the lint does not follow. For each
  language the repository lints, they ask whether its lint enforces each declared limit or a declaration names the
  language, limit, and reason. The shipped file's keys are now in code point order, as `code-key-order` requires, with
  no change to its settings.
- `code-guard-clauses`: in a language whose blocks take braces, write every `if`, `else`, and loop body in braces, even
  one statement. An `else` followed by `if`, as in `else if`, is the one exception. A new rule configures the lint to
  reject an `if`, `else`, or loop body without braces, wherever the lint supports that rule. The Allowed guard example
  now reads `if (order.lines.length === 0) { return; }`.
- `code-module-file-roles`: export only user interface components, their props types, and declared framework names from
  a source file whose code holds markup, such as a `.tsx` or `.jsx` file. Put the hooks, contexts, and constants that
  components share in source files without markup, so a development server can hot-swap a component file and keep its
  state. Declare the names the repository's frameworks require a file to export, such as `generateMetadata` or `loader`;
  they count toward neither the component-only nor the one-function limit. A page file that exports `generateMetadata`
  beside its component, which violated the one-function limit before, now complies. The names also apply in files
  without markup, so a route handler that exports `GET` and `POST`, which violated the one-function limit before, now
  complies. Declare at most one class and at most one user interface component in each source file, exported or not. A
  file that declares a component and an unexported child component it renders, or two classes, no longer complies. A
  module's error classes, such as tagged error classes, may share one declared errors file, and its schema classes one
  declared schemas file, each holding only those classes. Errors join the example roles. A route, story, or test file,
  which a framework loads by its path, may keep its component unexported and export only what that framework loads, such
  as `Route`. A new `assets/oxlint/oxlintrc.json` turns on oxlint's native `react/only-export-components`,
  `react/no-multi-comp` with `ignoreStateless: false`, and `max-classes-per-file` at 1 with `ignoreExpressions: false`.
  Its default `allowExportNames` list holds route framework names, such as `metadata`, `generateMetadata`,
  `generateStaticParams`, `loader`, `action`, `meta`, `links`, and the HTTP method names. It turns the component-only
  rule off for `.tsx` and `.jsx` files under a `routes` folder and for story and test files by their `.stories.`,
  `.test.`, and `.spec.` suffixes. It does the same for files under `test`, `tests`, `testing`, and `__tests__` folders,
  and turns the class rule off in `errors.ts` and `schemas.ts`. The component rules take effect where the repository's
  own configuration enables the `react` plugin, and none has an autofix. A new
  `assets/ast-grep/utils/framework-exports.yml` (id `framework-export-name`) holds the same default names. The
  `exported-functions` rules for TypeScript, Tsx, and JavaScript now skip an exported function, or a declarator whose
  value is one, under one of them. The same statement's other functions still count. A repository adds its own names in
  its own copy of that util, with the same id, loaded through its own `utilDirs`. It adds them to its own setting of the
  oxlint rule too, and covers its own route and test paths with its own override. The lint rule now enforces the
  one-class and one-component limits beside the declared length and the one-function limit. A language may leave any of
  the three to review only by declaring it and the reason. The lint-loading rule now also says to turn on the lint's
  markup plugin where code holds markup. The function-valued constants rule and the lookup-table rule are now one line,
  and the suppression and generated-file rules are now one line. The contract keeps 25 rules, and neither merge changes
  compliance. The message now names the class and component limits and components in markup files, and no longer names
  the sibling types file, whose rule is unchanged. The lint checks now confirm that the lint reports a second class
  outside errors and schemas files, in every language not left to review. They also confirm it reports a second
  component in a file with markup. A new review check asks what each markup file exports. New examples move a
  `useInvoiceDialog` hook that returns an unexported component's markup out of `use-invoice-dialog.tsx` into
  `use-invoice-dialog.ts`. They also move an unexported `InvoiceRow` out of `invoice-list.tsx` into `invoice-row.tsx`,
  beside an `invoice-import/errors.ts` that declares two tagged error classes. Each off entry in the oxlint file carries
  a comment naming its reason. The comment example in the `exported-functions` rules now reads `export const openOrder =
() => OrderStatus.Open, closeOrder = () => OrderStatus.Closed` instead of writing a bare 2. The oxlint file reports 37
  exports in markup files, 101 second components, and 3 second classes in the largest measured repository, and none in
  the next two. It reports 1 second class in the fourth, and the skipped names remove 4 one-function findings in two
  page files of the fourth.
- `code-module-structure-and-control-flow`: every owned function, method, function-typed member, and function-valued
  constant whose name begins in lowercase must start with a verb from a declared list, matched in every case style and
  rejected by lint. The list also holds the predicate prefixes of `code-boolean-names`, `on` for event handlers, `use`
  for hooks, and per-language constructor and conversion prefixes such as `new` and `into`. Capitalized names,
  language-defined names such as constructors, the `main` function, accessors, including a method that only returns a
  field, test fixtures, and tests titled by their names are exempt, and a name an interface or framework fixes is
  suppressed with a reason. The contract now ships a default verb list and ast-grep rules for TypeScript, Tsx, Rust, and
  Python, and requires Tenet 0.11.0. The default list leaves out `get`, `fetch`, and `load`, which
  `code-spelled-out-names` maps to `read`.
- `code-numeric-literals`: only -1, 0, and 1 may stay bare, in every language, so 2 now takes a named constant like
  every other number, and a repository no longer declares its own list of bare numbers. The shipped
  `assets/oxlint/oxlintrc.json` now sets `no-magic-numbers` to ignore -1, 0, and 1 only, and a repository may override
  its test pattern alone; the test-file off entry carries a comment naming its reason. The rule against listing a
  quantity among the bare numbers is removed, because the list is now fixed. The message, the one-literal rule, and the
  bare-number review check now name -1, 0, and 1. The Allowed example now derives `BYTES_PER_MEBIBYTE =
BYTES_PER_KIBIBYTE * BYTES_PER_KIBIBYTE`, and the Violation names the 2 in `5 * 1024 ** 2`. The reassigned-variable
  and parameter-default examples are now `let maxAttempts = 50` and `listInvoices({ maxPages = 50 }:
ListInvoicesInput)`, whose names end in counted nouns as `code-measured-value-names` requires and whose function takes
  one destructured object argument as `code-typescript-function-arguments` requires. The type example is now `{
retryCount: 3 | 5 }`, matching `type RetryCount = 3 | 5`. Dropping 2 adds 117 / 37 / 22 / 37 findings in the four
  measured repositories, with no autofix.
- `code-rust-doc-comment-coverage`: the contract now ships an ast-grep rule for Rust that reports each exported item
  with no `///` doc comment: a `pub` function, inherent method, struct, enum, union, trait, type alias, constant,
  static, or inline module, each method, associated type, and constant of a `pub` trait, and each `#[macro_export]`
  macro. It requires Tenet 0.11.0. The example function is now `pub fn compute_price`, which starts with a verb, and
  each doc comment takes the prose form that `code-comment-form` requires.
- `code-rust-numeric-conversions`: suffix each numeric literal whose type nothing else fixes, after an underscore, such
  as `let mut retry_count = 0_u32;`, so its type never falls back to `i32` or `f64`. Compute each integer sum,
  difference, product, quotient, remainder, and negation with a `checked_*` method. Clamp with `saturating_*` only a
  quantity that stops at its type's bound by design, and wrap with `wrapping_*` only a value whose magnitude means
  nothing, such as a hash. Every Clippy conversion and arithmetic lint stays denied, as the lint table that
  `code-lint-strictness` ships denies them. The ratio function also suppresses `clippy::float_arithmetic`, which that
  table denies, with a reason that names the ratio it computes. The lint check runs the Clippy check that
  `code-rust-workspace-checks` requires, and a new check reviews each `clippy::float_arithmetic` suppression. A new
  example pair shows `used_bytes.checked_add(reserved_bytes)`, and the integer-arithmetic example is now
  `item_count.div_ceil(ITEMS_PER_PAGE)`.
- `code-rust-source-structure`: every function whose callers branch on its failure returns an error type the crate owns,
  such as `Result<Receipt, SettleError>`, in binary and library crates alike. An opaque error type, such as
  `anyhow::Error`, stays only in a binary crate, for a failure no caller branches on. Each error type derives its
  `Display` and `std::error::Error` implementations with the one derive macro the repository declares, such as
  `thiserror`'s `#[derive(Error)]`. Each error type gives its message in that derive's attribute, on a struct or each
  enum variant, as `code-diagnostic-messages` requires. It carries an underlying error as the derive's source field.
  Code never recovers a type from an opaque error, a cause, or a `dyn Any` value with `downcast_ref`, `downcast_mut`,
  `downcast`, or `is`, in tests too. It matches an `enum`'s variants instead. Only the call that receives a dependency's
  opaque value, such as a panic payload, downcasts it, under a suppression as `code-lint-suppressions` requires. Code
  binds each value a call returns and handles each `#[must_use]` value, such as a `Result` with `?`. It discards any
  other unused value only with a typed wildcard binding, such as `let _: Option<u64> = counts.insert(name, count);`. The
  contract now ships ast-grep rules for Rust that reject each downcast, each hand-written `std::error::Error`
  implementation, and each hand-written `Display` for a type that derives `Error`. It requires Tenet 0.11.0.
- `code-rust-workspace-checks`: format with the `rustfmt.toml` that `code-lint-strictness` ships, using the rustfmt of
  one dated nightly toolchain pinned in the repository's check task, such as `cargo +nightly-2026-10-27 fmt`, while
  `rust-toolchain.toml` pins the stable toolchain with its Clippy component. Clippy runs with `--all-features` and the
  lint tables and `clippy.toml` that `code-lint-strictness` ships, which deny every rustc, Clippy, and rustdoc lint and
  group, including Clippy's nursery and restriction groups, apart from the listed off entries;
  `clippy::allow_attributes`, `clippy::allow_attributes_without_reason`, and `unfulfilled_lint_expectations` stay denied
  through those tables. A crate that needs `unsafe` code copies the workspace lint table into its own `[lints]` table
  with `unsafe_code` at deny instead of inheriting it, and every other member crate inherits it. A new check runs `cargo
doc`, which fails on a rustdoc finding.
- `code-spelled-out-names`: name every type parameter with a word for what it stands for, such as `Row` or `Catalog`.
  The exception for a type parameter of one capital letter, such as `T`, is removed, so the one-character ban now covers
  type parameters, including a mapped type's key, an inferred type, a type variable that an assignment declares, a const
  generic parameter, and a lifetime parameter, so `'a` becomes a word such as `'input`; `_` stays allowed only for a
  value that the code never reads. The repository word list must map `get`, `fetch`, and `load` to `read`, so every
  lookup of one value starts with `read`, whatever its medium, such as `readInvoice` for `getInvoice` or `fetchInvoice`,
  and every language's lint holds these mappings, even a language that defines `get` as a keyword. A search by a
  condition starts with `find` and a lookup of many values with `list`, and an accessor's `get` keyword, as in `get
total()`, is not part of its name. Case each acronym or initialism inside a name as a word, such as `callbackUrl`,
  `parseJson`, and `HttpClient`, never `callbackURL` or `HTTPClient`, so no name that holds a lowercase letter holds two
  capitals in a row, so a one-letter word before another word, such as `XAxis`, is reported too. A name of capitals,
  digits, and underscores alone, such as the constant `MAX_URL_LENGTH`, stays allowed, except as a type's name, such as
  `type URL = string`. A declared name that a framework or dependency fixes, such as a library option `baseURL` or a
  wire field `HTTPStatusCode`, keeps its spelling with a suppression whose reason names that system, and reading another
  system's name, such as an imported `parseURL`, declares nothing. The contract now ships `assets/ast-grep/` rules for
  TypeScript, Tsx, JavaScript, Python, and Rust that reject a one-character type parameter (`type-parameter-names-*`, in
  every language but JavaScript, which declares none), a declared name whose first word is `get`, `fetch`, or `load`
  (`lookup-names-*`), and a declared name that holds a lowercase letter and two capitals in a row or a type, class,
  interface, enum, trait, type parameter, or type variable named in capitals alone (`acronym-names-*`), says to run them
  with the repository's lint, and declares `requires-tenet: 0.11.0`. The lookup and acronym rules check the same
  declarations, including type parameters and a trait's associated types. The message now names acronyms, the lint check
  confirms no acronym is reported, and a new review check asks about an acronym the lint misses, such as `runE2E`, where
  a digit splits the capitals. Never declare a name that the code already binds where the declaration appears, in an
  enclosing scope or earlier in the same block, in every language, such as a callback parameter `invoice` inside
  `computeTotal({ invoice })`; the strictness configuration enforces it with `no-shadow` and Clippy's shadow lints,
  which report 234 / 46 / 13 / 13 TypeScript and 142 / n/a / n/a / 204 Rust findings.
- `code-typescript-call-arguments`: the function-binding rule, its check, and `assets/oxlint/oxlintrc.json` move to
  `code-typescript-const-bindings`, which governs how TypeScript variables are declared. A function bound from an
  argument object is bound as that contract requires. A repository that installs this contract without
  `code-typescript-const-bindings` no longer gets the rule. The message no longer names it. Bind the value of an `await`
  or `yield*` expression to a name before reading a member of it, such as `const invoice = await readInvoice({ id })`,
  then `invoice.status`, never `(await readInvoice({ id })).status`. Calling a method and indexing count as reading a
  member, and the rule holds through parentheses and type or non-null assertions, such as `((await read()) as
Reply).result`. Destructuring in the declaration that binds the value, such as `const { status } = await readInvoice({
id })`, counts as binding it. A new `assets/oxlint/oxlintrc.json`, at the path the function-binding file left, turns
  on oxlint's native `unicorn/no-await-expression-member`; its automatic fix rewrites a declaration that reads a
  same-named member or the first or second element into destructuring, and oxlint 1.80.0 applies it only with
  `--fix-dangerously`. New ast-grep rules `awaited-members-typescript.yml` and `awaited-members-tsx.yml` report what
  that rule misses: a member read from a `yield*` value, and from an awaited value behind an assertion or extra
  parentheses. The message and the lint check now name the rule. The examples now name functions with listed verbs:
  `invoices.listForAccount({ account }).findLatest()`, `computeTotal`, `applyDiscount`, `recordPrice`, `readInvoice`,
  `readOrder`, and `readAmount`, and the rule files' notes write `const invoice = await readInvoice({ id })` and `const
order = yield* readOrder({ id })`. The pipeline examples pass each function as an inline arrow that names its
  arguments, such as `map((price) => applyDiscount({ price }))`. The schema-file example nests `Schema` constructors, as
  in `Schema.Struct({ tags: Schema.Array(Schema.String) })`, and the rule files' comment on schema files nests `Schema`
  constructors too.
- `code-typescript-compiler-strictness`: every package's compiler configuration now extends the compiler configuration
  that `code-lint-strictness` ships, directly or through a base it extends, so every option that file sets applies,
  including `exactOptionalPropertyTypes` and `verbatimModuleSyntax` beside `strict` and `noUncheckedIndexedAccess`, and
  no package, directory, or file relaxes any of them. The contract states why the last two matter. Under the first, an
  argument field declared `dueAt?: Date` may be left out, but a caller can never set it to `undefined`. The second keeps
  each import's runtime effect visible in the source, which type stripping needs, because an unmarked type-only import
  fails when the module loads. The configuration check now reads the compiler's `--showConfig` output against the
  shipped file's options. A new `assets/oxlint/oxlintrc.json` sets `typescript/ban-ts-comment` to reject `@ts-nocheck`,
  `@ts-ignore`, and `@ts-expect-error` without a description, the lint check replaces the search, and the contract
  declares `requires-tenet: 0.11.0`. The Allowed example's package extends a base that extends the shipped configuration
  first, and its test leaves out `dueAt` for an invoice with no due date.
- `code-typescript-const-bindings`: bind a function to a variable only as a function declaration or as a constant
  annotated with a function type, such as `const writeEvent: EventSink = ...`; `any`, `unknown`, `satisfies`, and `as`
  do not count as that annotation. The rule, its check, and `assets/oxlint/oxlintrc.json`, which sets oxlint's native
  `func-style` to `declaration` with `allowTypeAnnotation`, move here from `code-typescript-call-arguments`. A
  repository that installs this contract without `code-typescript-call-arguments` now gets them. The contract declares
  `requires-tenet: 0.11.0`. Add or subtract one with `+= 1` or `-= 1`, never `++` or `--`, even on a property or in a
  `for` loop's update clause. `assets/oxlint/oxlintrc.json` now also sets oxlint's native `no-plusplus` with
  `allowForLoopAfterthoughts` false, beside `func-style`. The rule has no `--fix`; its suggestion rewrites a statement
  such as `index++` safely but turns `++count > limit` into `count += 1 > limit`, so rewrite an increment whose value is
  used by hand. The lint check now confirms the lint rejects `index++` in a `for` loop's update clause, and the
  suppression rule and check cover increments. The message names the rule and is shortened. A `let` may now be
  reassigned inside a callback, meaning a function declared inside the function that declares the `let` and handed to
  other code to call, as well as inside a loop that carries its value. A `let` at a module's top level has no declaring
  function, so only a loop among the module's top-level statements may reassign it. A `let` declared in a loop's body or
  in a `for...of` or `for...in` head starts fresh on each pass, so that loop does not carry it. A value that a loop or
  callback changes is held in its own `let`, never in a field of an object literal, which
  `code-typescript-effect-absent-values` forbids assigning after the literal; such holder objects complied before and
  now violate. The lint must now reject a `let` reassigned outside both a loop and a callback, and the contract ships
  `assets/ast-grep/` rules for TypeScript and Tsx, `let-reassignments-typescript` and `let-reassignments-tsx`, which
  report a plain, augmented, parenthesized, or destructuring assignment with no loop or function between it and the
  `let` it writes, and any write from a function to a module-level `let`, even inside a loop. The rules have no autofix;
  return the chosen value from a function instead. The branch Violation example no longer also omits the initializer, a
  holder-object Violation and a callback Allowed example are added, the increment examples step a `failures` `let` in a
  loop instead of a `summary` field, the lint check confirms the new rule, and the review check now asks only whether a
  loop carries each reassigned `let` or other code calls the nested function that reassigns it. A function may update an
  entry of a closed-set record that it declares, such as `counts[check.state] += 1` in its loop, because
  `code-typescript-runtime-keyed-maps` treats it as a lookup, not a field; this narrows the holder-object rule only for
  that record. A constant whose value a call returns, such as a guard built with `Schema.is`, takes that call's declared
  type and needs no annotation.
- `code-typescript-effect-errors`: where promises remain, such as at entry points, in functions that `Effect.tryPromise`
  calls, and in tests and scripts, code never calls a promise's `then` or `finally` method. It declares every function
  that returns a promise `async`, even one without `await`, writes `return await` for each promise it returns, and
  discards a promise only with `void`. `assets/oxlint/oxlintrc.json` now runs with type information and turns on
  `typescript/promise-function-async` with its full options, `allowAny` false and an empty `allowedPromiseNames`. It
  turns on `typescript/return-await` set to `always` and `preserve-caught-error` with `requireCatchParameter` true. Its
  `typescript/no-floating-promises` runs with its full options, `ignoreVoid` and `checkThenables` true, `ignoreIIFE`
  false, and empty allow lists, so an unhandled thenable also fails. It keeps `require-await` and
  `typescript/require-await` off with their reason comments, turns no other type-aware rule off, and lists its rules in
  code point order. New `assets/ast-grep/rules/promise-chains-typescript.yml` and `promise-chains-tsx.yml` reject each
  `then` or `finally` call. The lint check now runs with type information and confirms that no type configuration error
  makes the lint skip files. Run oxlint's fix twice, since an added `async` exposes a `return` that the second run
  awaits. The examples and the `catch-handlers` notes now name the error builder `buildRequestDropped` and each lookup
  with `read`, such as `const invoice = yield* readInvoice({ id })`. The `catch-handlers` notes and the async Allowed
  example write `Effect.tryPromise({ catch: buildRequestDropped, try: readInvoice })`, with its keys in code point
  order. The `then` Violation passes the inline arrow `(response) => response.json()`. The `promise-chains` comment
  gives `then` and `finally` inline arrows, such as `readInvoice({ id }).then((invoice) => sumTotal({ invoice }))`. The
  `Effect.orDie` Violation calls `Effect.orDie(refunding)` on a bound Effect instead of passing `Effect.orDie` to `pipe`
  by name. The tagged error example and the `untagged-errors` notes declare classes with `Schema.TaggedErrorClass`, the
  Effect 4 name. The `then` Violation and the async Allowed example take `Readonly<AbortSignal>`, as
  `code-typescript-input-immutability` requires. The bare-error Violation now braces its `if` body, as
  `code-guard-clauses` requires, so it breaks only the rule it shows. The async Allowed example declares
  `Promise<unknown>`, so it returns the parsed body as `unknown`, as `code-typescript-type-assertions` requires.
- `code-typescript-effect-schemas`: name each schema constant in PascalCase for the value it decodes, never in camelCase
  or with a `Schema` suffix, and derive its type once, directly below it, in an alias that shares its name, written
  `type Invoice = typeof Invoice.Type`; every other use refers to that alias, never to an inline `typeof Invoice.Type`.
  A schema class needs no alias, a decoder or guard built from a schema keeps a camelCase name, such as `decodeInvoice`
  or `const isInvoice = Schema.is(Invoice)`, and a schema built from a closed set's declaration is written inline where
  it is used. Every decode now passes `{ onExcessProperty: 'error' }` beside the schema, so an owned shape rejects
  unknown fields; a foreign payload, which another system declares and may extend, is marked loose in its own schema
  with an index-signature rest such as `Schema.Record(Schema.String, Schema.Unknown)`, and a framework or common
  validator interface that decodes for the code gets the same option. Making an existing reader of stored or shipped
  data reject unknown fields ships only as `data-stored-and-shipped-formats` allows. The contract ships ast-grep rules
  for TypeScript and Tsx under `assets/ast-grep/` that report non-PascalCase schema constants, derived types outside
  their alias, the helper form `Schema.Schema.Type<typeof Invoice>` anywhere, and decode calls without the option, and
  declares `requires-tenet: 0.11.0`. The message now names unknown fields and the shared PascalCase name.
- `code-typescript-function-arguments`: a default for an optional field of a function's argument object now sits where
  the signature destructures it, such as `function poll({ pollMs = POLL_MS }: PollInput)`, never with `??`, `??=`, or
  `||` where the body reads the field. A default may read an earlier field or make a synchronous call, a default that
  needs `await` becomes a defaulted function, and a nested options field is destructured with its default in the
  signature. A field that takes a signature default is optional, never nullable, and a function that forwards an
  optional field repeats no default. A callback written directly as a call's argument and a parameter whose type a
  dependency declares are outside the default rules. The contract now ships ast-grep rules for TypeScript and Tsx and
  requires Tenet 0.11.0. Name each function's argument type its PascalCase name plus `Input`, such as `retryStep` taking
  `RetryStepInput`, and a component's, whose name starts with a capital letter, its name plus `Props`, such as
  `InvoiceRowProps`. A method's or function member's type is named for the member alone, a constructor's or function
  type's for its class or type, and a function whose only caller passes it every field of its argument takes the
  caller's type. Name each overload's argument type for its function, a word for its case, and `Input`, such as
  `ListInvoicesByCustomerInput` and `ListInvoicesByPageInput` for `listInvoices`, since a lookup of one value starts
  with `read` and a lookup of many with `list`. Shipped ast-grep rules `argument-type-names-typescript` and
  `argument-type-names-tsx` report a destructured argument whose type lacks the suffix, including on overload, `declare
function`, and abstract method signatures; review checks the rest of the name. Write every function that a call takes
  as an argument inline, as an arrow or generator function that names the arguments it reads, such as
  `lines.flatMap((line) => parseLine({ line }))`, never by name, such as `lines.flatMap(parseLine)` or
  `emitter.on('message', recordMessage)`, because the callee decides which arguments it passes; a function in an object
  field or markup attribute, such as `onSave={onSave}`, may still be named. Remove a listener that an inline arrow
  registers by aborting its signal or calling its registration's stop function, such as from the finalizer of the scope
  that registered it, and suppress only a listener that a dependency removes solely by name. The shipped ast-grep rules
  `function-reference-arguments-typescript` and `function-reference-arguments-tsx` report a name that the module or an
  enclosing block declares as a function, and a method or function-valued field of the enclosing class read through
  `this`, never an accessor, passed to any call or `new`, plus every bare reference passed to an array method on any
  receiver except a capitalized namespace. Review checks each call for an imported or parameter-held function passed by
  name, which the rules cannot see. The domain-object and callback sentences merge into neighboring rules without
  changing their meaning, the export and discriminated-union rules and the two external-signature rules join into one
  line each, the options type is now called an argument type, and the positional-parameter rule says a type's function
  member where it said an interface method, since owned object types are declared with `type`. The callback example now
  reads a dependency's `string | undefined`, such as `matches.map((match) => match[1] ?? '')`.
- `code-typescript-input-immutability`: never use the `delete` operator, even on an object the function created. Drop a
  key by rest destructuring, such as `const { secret, ...publicRecord } = record`, and a key known only at run time by a
  computed key. Drop the entries that fail a condition by building the lookup as `code-typescript-runtime-keyed-maps`
  requires. A test file, matched by a declared path pattern, may delete an environment variable it changes. It restores
  each variable one at a time, never by replacing the environment object. The ast-grep assets add `delete-operator` and
  `delete-environment` rules in TypeScript and Tsx variants. The oxlint asset runs `no-unused-vars` at error and ignores
  the keys a rest destructuring drops. Write every array type as `readonly T[]` and every tuple type as `readonly [A,
B]`. This covers parameters, object and class properties, return types, type aliases, type arguments, and module-level
  constants. One exception is a local variable's own annotation inside a function body that builds the array. The other
  is the annotation of a private `#name` class field that only its own class fills. A public field, a getter's return
  type, and every parameter stay read-only, and a type inside either annotation is still written `readonly`. Never write
  `Array<T>` or `ReadonlyArray<T>`, and pass a copy such as `[...rows]` to a dependency whose declared type requires a
  mutable array. The contract now ships ast-grep rules, whose fix prepends `readonly`, and an oxlint configuration for
  `typescript/array-type`, so it requires Tenet 0.11.0. The note on values a function created now names collections
  only, such as an array, `Map`, or `Set`, and points to `code-typescript-effect-absent-values` for an object's fields.
  Give every parameter that declares its type a deeply read-only type, so that each property it reaches is `readonly`.
  Write a dependency's type in its read-only form, such as `Readonly<AbortSignal>`. List each dependency type that has
  none, such as `Request`, in the lint's declared allow list. The oxlint asset now runs with type information and sets
  `typescript/prefer-readonly-parameter-types` with `ignoreInferredTypes` and `checkParameterProperties` true and
  `treatMethodsAsReadonly` false. Its allow list holds the standard library's `ReadonlyMap` and `ReadonlySet`, which
  `code-typescript-module-state` requires. It also holds `AbortController`, `Request`, `Response`, `Uint8Array`, and
  `URL`, which have no read-only form. The three lint-configuration rules merge into one line, which asks the lint to
  reject each forbidden form wherever a tool supports it. The lint check now runs with type information and confirms
  that a parameter type with a property that is not `readonly` fails. The message now also names `delete` and `readonly`
  array and tuple types. Rewrite each reported parameter type by hand; the rule has no autofix.
- `code-typescript-module-boundaries`: declare a maximum number of distinct modules that one file imports, counting
  type-only imports and not re-exports; the shipped `assets/oxlint/oxlintrc.json` sets `import/max-dependencies` to 10
  with type imports counted, which a repository may override. The shipped file no longer turns off `import/default` and
  `import/namespace`, which it turned off only to focus its own test cases, so an extending configuration keeps them at
  the level its categories set. Its keys are now in code point order, as `code-key-order` requires, with no change to
  its settings.
- `code-typescript-module-state`: end each module-level object or array literal with `as const`, exported or not, and
  follow it with `satisfies T` when it must match a declared type. A read-only annotation such as `Readonly<Record<K,
V>>` or `readonly T[]` no longer satisfies the rule. Never annotate the constant that holds such a literal, and never
  wrap it in `Object.freeze`. Write each array type after its `satisfies` read-only, even inside a type argument, as
  `code-typescript-input-immutability` requires. Annotate each module-level `Set` or `Map` as `ReadonlySet<T>` or
  `ReadonlyMap<K, V>`. Primitive constants and values that a call returns need neither form. Where code needs a wider
  type, annotate where the value is read, and pass a dependency that needs a mutable array a copy. The contract now
  ships `assets/ast-grep/` rules in TypeScript and Tsx variants that report each form except an array type after
  `satisfies`, which `code-typescript-input-immutability`'s rules report, and declares `requires-tenet: 0.11.0`. The
  rules also report an anonymous default export whose literal lacks `as const`, such as `export default { fetch:
handleRequest }`, or that `Object.freeze` wraps, and accept `export default { ... } as const satisfies T`. The
  sentence about a dependency that requires a mutable array now names `code-typescript-input-immutability`, which owns
  the copy rule, instead of restating it with its own example.
- `code-typescript-named-types`: declare every object type as a `type` alias, never as an `interface`, including empty
  and generic types and types in tests, scripts, and hand-written declaration files. Write `interface` only to merge
  members into a dependency's declaration inside `declare module` or `declare global`, with a suppression that names the
  dependency. Never merge into a type the repository declares. An interface's `extends` clause becomes an intersection,
  `type Order = Audited & Owned & { id: string }`, whose one object type literal is now allowed. An empty interface that
  extends one type becomes an alias of it. An `extends Record<string, unknown>` that only made an interface assignable
  to a record is dropped. A class implements a `type` alias as it would an interface. Generated files and copied
  third-party source may be exempted by a path pattern declared in the lint configuration. The contract ships
  `assets/oxlint/oxlintrc.json`, which sets oxlint's native `typescript/consistent-type-definitions` to `type`, and
  declares `requires-tenet: 0.11.0`. Suppress each augmenting interface before running the autofix, which otherwise
  rewrites an augmentation inside `declare module` into an alias that no longer merges. The inline-type examples now
  name `buildCommand`, and the Violation types its argument `BuildCommandInput`, as `code-typescript-function-arguments`
  requires, and writes only its return type inline, so it breaks only this rule.
- `code-typescript-node-scripts`: the relative-import extension rule, its Violation, and its check move to
  `code-typescript-import-extensions`, which this contract now extends. A repository that installs this contract without
  `code-typescript-import-extensions` no longer gets the rule. The script type-check rule and its `--showConfig` check
  no longer list `verbatimModuleSyntax`, which `code-typescript-compiler-strictness` now requires of every package
  configuration, scripts included. The rule now names that contract's settings, its reason has its own line, and
  `assets/typescript/tsconfig.json` still sets the flag, now with its options in code point order. The Allowed script
  now opens with `#!/usr/bin/env node` and a summary of what it does and how to run it, as `code-comment-form` requires
  of every executed script. Scripts call each Node function in its asynchronous form, such as `readFile` from
  `node:fs/promises`, never `readFileSync` or `execFileSync`. The contract now ships `assets/oxlint/oxlintrc.json`,
  which turns on oxlint's native `node/no-sync` for `.mts` files, and says to load it from the repository's lint. The
  lint check now confirms that the lint rejects `readFileSync` in a script.
- `code-typescript-type-assertions`: annotate a constant or field that must match a declared type where it is declared,
  such as `const reminders: ReminderSchedule = { ... }`, write `satisfies` instead only where later code reads the
  narrower inferred type, and bind any other value that needs a declared type to an annotated constant; the contract no
  longer accepts either form at will. Such reads include a story's `typeof meta`, a table's literal keys, an anonymous
  default export a runtime loads, and a module-level literal's `as const` type, which `code-typescript-module-state`
  requires. The lint must also list each `satisfies` expression for review without failing, through the shipped ast-grep
  rules `satisfies-expressions-typescript` and `satisfies-expressions-tsx` at severity info, and a new check asks, for
  each listed `satisfies` in changed code, whether later code reads the inferred type. Never write a type predicate,
  such as `invoice is PaidInvoice`, or an assertion signature, such as `asserts value is Invoice`, in any file; tests
  and scripts lose their exception for assertion signatures, and may still call a dependency's assertion function such
  as `assert.ok(row)`. Test an `unknown` value against a schema with the guard that the schema library builds from it,
  named as `code-typescript-effect-schemas` requires, and narrow every other value inline; TypeScript 5.5 and later
  infer a predicate from an inline callback's check, such as `orders.filter((order) => order.status ===
OrderStatus.Paid)`. The lint must also reject type predicates and assertion signatures, including a predicate in a
  function type such as `(value: unknown) => value is Invoice`, and the contract ships ast-grep rules
  `type-predicates-typescript` and `type-predicates-tsx` under `assets/ast-grep/`, says to load them from the
  repository's lint configuration, and declares `requires-tenet: 0.11.0`. The examples now follow round 5. The non-null
  examples are `rows[0]!`, `invoices.get(id)!.total`, and the Violation `const invoice =
this.#invoices.get(this.#invoiceId)!;`, and the Allowed accessor is `this.#readInvoice()`, which starts with a listed
  verb. The default example is `paymentTimes.get(invoice.id) ?? 0` for a paid invoice. The return-only type parameter
  examples are `parseJson<Value>({ text }: ParseJsonInput): Value`, `parseLines<Line>({ text }: ParseLinesInput):
readonly Line[]`, and `request<Body>({ path }: RequestInput): Promise<Body>`. A Violation and Allowed pair contrasts
  `orders.filter((order): order is PaidOrder => ...)` with the inferred form, and another contrasts `const reminders = {
... } satisfies ReminderSchedule` with its annotation; three more Allowed lines show `StoryObj<typeof meta>` after
  `const meta = { component: InvoiceCard } as const satisfies Meta<typeof InvoiceCard>`, `layouts.compact` after a keyed
  table's `as const satisfies Record<string, ColumnLayout>`, and `export default { fetch: handleRequest } as const
satisfies ExportedHandler<Bindings>`. The default rule, the lint configuration rule, and the lint check each split
  into two lines under 30 words, and the rule on reading a record whose absence breaks an invariant is shortened to one
  line under 30 words. The message now names type predicates and says to annotate declared types unless code reads
  inferred ones.
- `contract-maintenance`: each rule names one allowed form for each case it covers, never a choice between equivalent
  forms, and states the observable condition that tells its cases apart. Each violation example breaks only the rule it
  illustrates, and each allowed example breaks no contract the repository adopts. Each rule's form is chosen because it
  is clean, readable, consistent with other adopted rules, easily enforced by a lint or an agent reading code, and needs
  the fewest exceptions, never because most scoped code already follows it; counting the code a form would change only
  plans its rollout. A rule's verification path is a tool's command with its working directory wherever a tool can check
  the rule; otherwise a focused behavior check or a review question that reviewers answer the same way every time. The
  ban on requiring new checkers for subjective style now names checker scripts, so shipped tool configuration may check
  a style choice. Defining shared obligations once and nested contracts' inheritance now share one sentence, with no
  change in meaning. A new check asks whether each added or tightened rule allows one form per case, chosen without
  prevalence as a reason, and whether a tool checks it wherever one can.
- `library-contract-format`: each rule names one allowed form for each case it covers, never a choice between equivalent
  forms, and two forms are allowed only for disjoint cases with the observable condition that tells them apart. A
  requirement is written in a form a tool can check whenever such a form expresses the same decision; where a tool can
  check a rule, the contract ships that tool's configuration under `assets/<tool>/` and a check that runs it, and a
  shipped file turns a rule off only for a reason `code-lint-strictness` lists, never to scope that file's own test
  cases. A rule is left to review alone only when two reviewers would decide each case the same way. Each violation
  example breaks only the rule it illustrates, and each allowed example breaks no library contract that would govern it.
  Two checks cover these rules.
- `library-contract-generality`: a team-chosen number becomes a requirement to declare its maximum or minimum, instead
  of a bounded value. When a shipped `assets/` file enforces the number, that file sets the default and the text may
  state it as a value a repository may override, and the file may set a different value for one kind of code when the
  text names the kind and its reason. Each rule's form is chosen because it is clean, readable, consistent with other
  library rules, easily enforced by a lint or an agent reading code, and needs the fewest exceptions, never because most
  code in the source projects already follows it; counting the code a form would change only plans its rollout. A new
  check asks whether the pull request for any added or tightened rule gives how much code already follows a form as a
  reason for choosing it.
- `library-skill-portability`: each code example in a skill obeys every library contract that governs that code, except
  a labeled bad example, which breaks only the rule it illustrates.
- `telemetry-application-tracing`: every server, and every other process a host runs until it is stopped, writes each
  log line as one JSON object. It passes the logger module's function one object literal whose `event` field names a
  member of the closed set that module declares. That set follows `code-closed-value-sets`, and the field names a
  member, such as `LogEvent.InvoiceSettled`, never the member's literal value. Each value of that set is two snake case
  parts joined by a dot, such as `invoice.settle_failed`. The logger input's `event` field is typed as the set, so an
  undeclared event fails the type check. Every other value is its own field, never interpolated into a string. A failure
  is an `error` field that lists its cause chain outermost first, never the exception object. Each cause appears as its
  error type, or as a generic error's safe error code. Code outside the logger module calls no console method, print
  function or macro, or logging library function, and opens no standard stream. A command-line program's lines for its
  user follow `cli-output-channels` instead, and browser code is not covered. The contract now ships
  `assets/oxlint/oxlintrc.json`, which reports console calls and `process.stdout`, `process.stderr`, and
  `globalThis.console` outside the `logger/log` file. It also ships ast-grep rules for TypeScript and Tsx. They report a
  call of the logger function, `log` by default, whose first argument is not an object literal with an `event` field.
  They also report an `event` value written with a string or template literal, and a value of the `LogEvent` declaration
  in another form. Outside the `logger/log` file, they report an import or re-export of `stdout` or `stderr` from
  `node:process` or `process`. A repository may rename the file, the function, and the set. It adds its command-line
  output module and its browser code to the console allowance. It now needs Tenet 0.11.0. The error-recording and
  boundary-sanitizing rules, the exporter-credential and local-destination rules, and the two sampling rules each merge
  into one sentence without changing what they require. The message now names log lines.
- `test-assertion-integrity`: write no branch in a test case's body, such as an `if`, a `switch`, a conditional
  expression, or `&&`, `||`, or `??`. Where the test runner counts assertions, open each test by declaring how many it
  must run, such as `expect.assertions(1)`, never `expect.hasAssertions()`. Assert with the runner's plain assertion and
  error expectation, such as `assert total == 42`, never a test-case class's methods, such as `self.assertEqual` or
  `self.assertRaises`. The contract now ships `assets/oxlint/oxlintrc.json`, which sets `vitest/no-conditional-in-test`
  and `vitest/prefer-expect-assertions` in test files. It also ships ast-grep rules for TypeScript and Tsx that reject
  `expect.hasAssertions()`, which `vitest/prefer-expect-assertions` accepts. Two new Violation examples, a new Allowed
  example, and two lint checks that run the shipped files cover these rules, and it requires Tenet 0.11.0. The Allowed
  example now rewords `order not found` to `no order with ID "42"`, so its diagnostics start lowercase and quote the id
  as `code-diagnostic-messages` requires.
- `test-curation`: where the test runner takes a per-test timeout, give every test an explicit one, written as a number
  literal. It is still used only to bound a hung test and never to define expected ordering. A new
  `assets/oxlint/oxlintrc.json` sets `vitest/require-test-timeout` in test files, a new check runs the lint and that
  configuration for a test with no timeout, and it requires Tenet 0.11.0.
- `test-scenario-functions`: in every test file whose runner declares suites by a call, every case and every setup or
  teardown hook sits in one top-level suite, such as `describe('order export', ...)`. A new
  `assets/oxlint/oxlintrc.json` sets `vitest/require-top-level-describe` with `maxNumberOfTopLevelDescribes` 1 in test
  files. A new check confirms that the lint run reports a case or hook outside a top-level suite and a second top-level
  suite. The contract requires Tenet 0.11.0.
- `ui-design-tokens`: where styles are defined as an object keyed by name, select a variant's style by indexing one
  definition keyed by the variant's members, such as `toneStyles[tone]`. Never pick that style by comparing the variant
  with a member, such as `tone === Tone.Positive && styles.positive`. Give every member a key, with an empty style for a
  member that adds nothing. Give that definition a type argument keyed by the variant's set, such as `Record<Tone,
Style>`, so the type checker rejects a missing member and a key outside the set. `code-closed-value-sets` requires
  that type argument of a style definition that writes members' literal values as keys. The contract now ships
  `assets/ast-grep/` rules for TypeScript and Tsx, `variant-style-comparisons-typescript` and
  `variant-style-comparisons-tsx`, which target StyleX. They report a comparison with `===`, `==`, `!==`, or `!=`
  against a fixed value when it is an operand of `&&` inside the arguments of `stylex.props`. Such a comparison inside
  an array argument reports too. A fixed value is a string literal or a member of a capitalized name, such as
  `Tone.Positive`. A comparison of two run-time values, such as `row.id === selectedId`, and a `typeof` test stay
  allowed, and the rules have no autofix. The contract says to load that configuration from the repository's lint and to
  suppress a finding only as `code-lint-suppressions` allows. It adds a Violation and an Allowed example, whose
  definition's type argument is `Record<Tone, Style>`, and a lint check, and declares `requires-tenet: 0.11.0`. The
  rules report 17 comparisons in 5 files of the largest measured repository and none in the other three.
- `ui-react-interaction-ownership`: an effect may no longer call a state setter synchronously in its body, directly or
  through a function the body calls, even under a condition; it sets state only in code that runs after its body
  returns, such as a subscription's listener or code after an `await`. State that resets when its data changes identity
  now resets through a `key` from that data on the component that holds it, and every list item is keyed by a value of
  the item, never its array index. The contract now ships `assets/oxlint/oxlintrc.json`, which turns on
  `react/no-array-index-key` and `react/set-state-in-effect` and sets no plugins, so a repository loads it and turns on
  its lint's React plugin; without that plugin the lint ignores every rule in the file. The shipped file also turns on
  `react/rules-of-hooks`, and the lint check now confirms it rejects a conditional hook, an index key, and a setter in
  an effect's body; a new check reviews every added key, including in lists built by `Array.from`, which the shipped
  lint does not follow, and another asks whether a function an effect's body calls sets state synchronously, which the
  shipped lint also misses. It requires Tenet 0.11.0.
- `ui-react-typescript-component-apis`: an empty prop value now takes the type `code-typescript-effect-absent-values`
  requires, so `value: number | null` no longer complies.

### Loosened

- `cli-output-channels`: lines that `telemetry-application-tracing` covers, such as a server's log lines, follow that
  contract instead of these rules. This contract no longer requires a server to write its log lines through one logger
  module, because `telemetry-application-tracing` now owns that requirement. A repository that installs this contract
  without `telemetry-application-tracing` no longer gets that rule. The Allowed example's progress function is now
  `reportProgress({ line })`, which starts with a verb.
- `code-lint-suppressions`: a rule turned off with one of the reasons `code-lint-strictness` lists, named in the comment
  above its entry, is no longer a violation, and the configuration check asks about rules turned off without such a
  reason.

### Added

- 22 contracts:
  - code: `code-constant-names`, `code-declaration-order`, `code-key-order`, `code-lint-strictness`,
    `code-map-and-set-names`, `code-python-doc-comment-coverage`, `code-python-function-arguments`,
    `code-typescript-boolean-conditions`, `code-typescript-collection-iteration`,
    `code-typescript-doc-comment-coverage`, `code-typescript-effect-absent-values`, `code-typescript-effect-scheduling`,
    `code-typescript-export-return-types`, `code-typescript-expression-forms`,
    `code-typescript-function-member-signatures`, `code-typescript-function-scoping`,
    `code-typescript-import-extensions`, `code-typescript-import-statements`,
    `code-typescript-object-literal-functions`, `code-typescript-runtime-keyed-maps`.
  - ui: `ui-react-hook-calls`, `ui-react-typescript-jsx-attributes`.

### Clarified

- `api-typescript-request-paths`: the path functions in the examples now start with a verb. `packs/pack-paths.ts`
  exports `formatPack` and `formatChunk`, callers request `PackPaths.formatChunk({ index, key })`, and the shipped lint
  rules' message names that call. The generic request example now passes one object argument with an `HttpMethod` member
  and still writes a path template at the call site. It reads `request({ account, method: HttpMethod.Get, path:
'/accounts/{account}/invoices' })`. Both calls list their keys in code point order, as `code-key-order` requires.
- `code-blank-lines`: the one-line example now reads `if (orders.length === 0) { return []; }`, a braced body of one
  statement, because `code-guard-clauses` requires braces on every block. The spacing rules are unchanged. The shipped
  `assets/oxlint/oxlintrc.json` now lists its keys in code point order, as `code-key-order` requires, with no change to
  its settings.
- `code-comment-attribution`: the Python attribution example now puts the contract name that opens it in backticks, ``#
`orders-retention-lifecycle`: purge closed orders``, as `code-comment-form` requires of a comment that opens with an
  identifier.
- `code-duplicated-blocks`: the Allowed example now calls `startWorker({ log, port })`, with its keys in code point
  order as `code-key-order` requires. No code's compliance changes.
- `code-export-consumers`: the Violation's `export function formatUsd` now declares its `string` return type, so it
  breaks only the rule it shows.
- `code-python-none-guards`: the `connect` and `handle` examples now take keyword-only parameters, as
  `code-python-function-arguments` requires, and write each `None` check as a block rather than a one-line `if`
  statement. The allowed-check line splits into two lines under 30 words, without the `Optional[X]` form that the
  shipped ruff configuration reports. The `connect` example's parameter is now `timeout_seconds`, defaulted from
  `DEFAULT_TIMEOUT_SECONDS`, as `code-measured-value-names` requires. No code's compliance changes.
- `code-rust-type-ownership`: the impl examples name their type parameter `State`, as in `impl<State> Order<State>` and
  `impl<State: Clone> Order<State>`. The one-impl-block rule splits into two lines under 30 words: the rule itself, and
  a line saying which impl blocks share a self type. What code must do is unchanged.
- `code-shared-utilities`: the misplaced utility in the Violation is now `clip({ text })`, which takes one object
  argument as `code-typescript-function-arguments` requires. No code's compliance changes.
- `code-typescript-class-declarations`: the client example's lookup of many invoices is now `listInvoices`, as
  `code-spelled-out-names` requires. Both the plain-record example's `listInvoices({ account })` and the Allowed factory
  that returns `{ listInvoices }` use it. The plain-record call no longer passes a `path`, which
  `api-typescript-request-paths` builds with a path function. The plain-record example's fields are now `readonly`, as
  `code-typescript-input-immutability` requires of a parameter's type. The plain-record rule splits into two lines under
  30 words: the rule and its example. No code's compliance changes.
- `code-typescript-entry-points`: the exported-object examples now end in `as const`, such as `export const uuidModule =
{ generate, validate } as const`, as `code-typescript-module-state` requires of a module-level literal, so each breaks
  only the rule it shows. The first Violation now says that `invoice-export/index.ts` imports three exporters and
  declares the `exporters` record from them, instead of quoting the literal. The rule against exporting such an object
  splits into two lines under 30 words. What code must do is unchanged.
- `data-record-identifiers`: the derived id function example is now `deriveRefundEffectId({ invoice })`, which starts
  with a verb as `code-module-structure-and-control-flow` requires. No code's compliance changes.
- `data-sql-store-boundaries`: the example functions now start with a verb. The forbidden function that runs
  caller-supplied SQL is `readFirstRow({ query, values })`, and the transaction function is `runInTransaction`. The
  transaction rule splits into two lines under 30 words.
- `data-store-ownership`: the example store functions now start with a verb, as `code-module-structure-and-control-flow`
  requires. The read functions are `readFinishedResults({ run })` and `listPendingInvoices()`, and the transaction
  function is `runInTransaction`. The storage-operation examples are now `read`, `write`, `put`, and `execute`, names on
  the default verb list that a function only the store module calls may take. The storage-operation exception splits
  into two lines under 30 words.
- `security-interpreter-injection`: the query-text Violation now interpolates the order identifier with a template
  literal instead of `+`, as `code-typescript-expression-forms` requires, so it breaks only the rule it shows.
- `tenet-code-curation`: the Rust reference's module entry-point example re-exports `stream::parse_events` instead of
  `stream::interpret`, so its function name starts with a verb on the default list that
  `code-module-structure-and-control-flow` ships. The TypeScript reference's stage function is now `chooseNextStage`,
  which also starts with a verb. The new state comes from `advanceJob`, which declares its `JobProgress` return type and
  lists `lastEventAtMs` before `stage`, in code point order.
- `tenet-contract-curation`: a new "What makes a good contract" section names what `contract-maintenance` requires (one
  form per case, chosen on its merits, examples that obey other contracts, and a tool check where one can decide) and
  how to meet it: look for a formatter, lint, or structural-search rule before writing prose and ship its configuration
  under `assets/<tool>/` (Tenet 0.11.0 or later) with the command under `Checks`; leave to review only what two
  reviewers decide alike; allow one of two equivalent forms, or write the condition that picks between them; write the
  rule's examples in each candidate form and pick the one that is clean, readable, consistent with the project's other
  rules, easily enforced by a lint or an agent reading code, and needs the fewest exceptions, counting the code each
  form would change only to plan the rollout; keep chosen numbers in tool configuration as a declared maximum, with a
  separate maximum and reason for a kind of code such as components; and check every example against every other adopted
  contract. A mechanical requirement is enforced with a tool the project already runs, and a project script only when no
  tool can check it.
- `tenet-test-curation`: the TypeScript examples assert with `expect(output).toBe(...)`, `toMatch(/.../v)`, and
  `not.toContain("\u001B")` instead of `node:assert`.
- `test-example-suite`: the Allowed example's case now calls `computeOrderTotal({ prices: [300, 200] })`, which starts
  with a verb, and its sentence is shorter. What code must do is unchanged.

## v10.0.0

`api-typescript-request-paths`, `code-closed-value-sets`, `code-conditional-expressions`, `code-exhaustive-branches`,
`code-module-file-roles`, `code-numeric-literals`, `code-typescript-call-arguments`, `code-typescript-effect-errors`,
and `code-typescript-module-boundaries` now ship tool configuration under `assets/`, beside `code-blank-lines`,
`code-function-size`, and `code-typescript-node-scripts`, so installing or updating them needs Tenet 0.11.0 or later.
Every other contract still installs with Tenet 0.7.0 or later. The shipped lint files fail on code that complied before;
run each tool's autofix where it has one, then rewrite or suppress what remains as `code-lint-suppressions` allows.

### Upgrading

Raise Tenet to 0.11.0 first. With `.tenet.lock` and the installed copies committed, run
`tenet contracts update --ref v10.0.0`.

- Moved rules: the tag-literal allowance of `code-typescript-effect-errors` is now stated only in
  `code-closed-value-sets`. For code that `code-typescript-call-arguments` governs, its rule to bind every nested call
  replaces the intermediate-value rule of `code-module-structure-and-control-flow`. An entry point's re-exports of its
  nested folders follow `code-typescript-entry-points` instead of `code-typescript-module-boundaries`. Install each
  receiving contract wherever the old one is installed, or the rule no longer applies there.
- New assets: 32 files in the 9 contracts above, 26 for ast-grep and 6 for oxlint. Install the oxlint plugins each entry
  names, at the versions it was checked with, and `oxlint-tsgolint` for `code-exhaustive-branches`.
- Roll back with `tenet contracts update --ref v9.0.0`. Copies of `api-typescript-request-paths`,
  `code-numeric-literals`, and `code-typescript-call-arguments`, which this release added, are reported as removed
  upstream and left in place; drop each with `tenet contracts remove PATH`, which also deletes its locked assets. A tool
  file that v9.0.0 lacks stays in place, leaves the lock, and makes `update` exit 1; delete it with `git rm`.

### Tightened

- `code-blank-lines`: besides control flow, each `return`, `throw`, or `raise` statement, each call or `await`
  statement, each multi-line declaration, exported or not, and each multi-line assignment or expression statement now
  takes one blank line before it unless it opens its block and after it unless it closes its block. Call statements
  include `new`, `void`, and optional-call statements. Consecutive call statements need no blank line between them, even
  when one spans several lines. `break` and `continue` statements, one-line assignments, imports, re-exports, and lists
  of exported names need a blank line only where a neighboring statement requires one. A function's overload signatures
  need none before their implementation. Where the repository's formatter requires more blank lines, such as two around
  a top-level function, its count stands. The rule that exempted jump statements is removed. The shipped
  `assets/oxlint/oxlintrc.json` extends `@stylistic/eslint-plugin`'s `padding-line-between-statements` to match. Its
  `lineMode` selector options need the plugin at 5.10.0 or later. It was checked with oxlint 1.80.0 and
  `@stylistic/eslint-plugin` 5.10.0. One `oxlint --fix` clears every finding, and oxfmt 0.65.0 keeps the inserted lines.
  Review still covers logical phases, comment placement, and Python and Rust code.
- `code-closed-value-sets`: HTTP methods and status codes leave the exemption for protocol values. Code names each one
  through a declared closed set whose members hold the protocol's values, such as `HttpMethod.Post` and
  `HttpStatus.MethodNotAllowed`, wherever it writes, passes, or compares one. Code such as `{ method: 'POST' }`, `{
status: 404 }`, `request.method === 'GET'`, and a type `'GET' | 'POST'` complied before and now violates. Each set's
  declaration sits in a module that holds only that declaration, unless the standard library or a dependency already
  exports the set with named members. A status code is also a numeric literal under `code-numeric-literals`, and its
  named constant is the status set's member, never a second constant such as `NOT_FOUND = 404`. Test files, matched by a
  declared path pattern, may still write methods and status codes as literals. The contract now ships `assets/ast-grep/`
  with TypeScript and Tsx rules and declares `requires-tenet: 0.11.0`. The rules report an uppercase method literal
  anywhere. They report `HEAD` or a lowercase method only where a method belongs: a `method`, `formMethod`,
  `httpMethod`, or `requestMethod` property, a comparison or `switch` on one, or a list of methods. They report a status
  code from 100 to 599 only where the `code-numeric-literals` lint skips it: as a `status` or `statusCode` property's
  value in an object, a member assignment, a readonly class field, or a markup attribute, and in a type named for
  statuses, such as `type ErrorStatus = 404 | 410`. So the two lints report no literal twice. The rules exempt files
  named `http-method` and `http-status` and common test folders and suffixes, and a repository may override those
  patterns. Load the rules from the repository's own configuration, such as by adding the installed
  `assets/ast-grep/rules` folder to its `ruleDirs`. They were checked with ast-grep 0.51.0; pin it to an exact version,
  as `ci-reproducible-checks` requires. The message now names HTTP methods and status codes.
- `code-conditional-expressions`: never compute a value with an immediately invoked function, such as `const limit = (()
=> { ... })()` or `pending = (async () => { ... })()`. A value that needs statements comes from a named function
  called by name, and a function that chooses a value only chooses and returns it. That function is an independent
  operation under `code-module-structure-and-control-flow`, even when it has one caller. A callback passed to an array
  method, a memoizing hook, or any other call is still allowed, even when that call runs it at once. Declare a maximum
  number of logical operators in one expression, counting `&&`, `||`, and `??` together, or the words `and` and `or` in
  a language that spells them as words. Every logical operator nested inside a chain counts with that chain, including
  through parentheses, negation, array elements, template placeholders, `new` arguments, arrow function bodies, and
  markup fragments. A call's callee and arguments, an object literal's values, a `function` expression's body, and a
  named markup element's attributes and children start their own count. Never shorten a long expression with a call that
  only restarts the count, such as `Boolean(isOpen && isShipped) && isPaid && isReady`. A null-coalescing default is
  still allowed and counts toward the maximum. Both new rules hold in every language, and review covers a language
  without a shipped asset. The contract ships `assets/oxlint/oxlintrc.json`. That file enables oxlint's native
  `no-ternary` and loads `eslint-plugin-sonarjs` through oxlint's `jsPlugins` to set `expression-complexity` to a
  maximum of 2. At that maximum, `a && b && c` and `x ?? y ?? z` pass, while `a && b && c && d` and `(a && b) || (c &&
d)` fail. A repository's lint configuration may extend that file and override its maximum. sonarjs also counts the `?`
  of a conditional operator, so a conditional operator that remains counts toward the maximum and also fails
  `no-ternary`. The contract also ships `assets/ast-grep/sgconfig.yml`, whose `rules/` folder holds JavaScript,
  TypeScript, and Tsx rules that reject a function expression invoked where it is written. They see through parentheses,
  a comma sequence, `call`, `apply`, `bind`, and `new`, and in TypeScript through a type assertion, `satisfies`, and a
  non-null assertion. They skip an invocation whose result is discarded, such as a statement of its own or one started
  with `void`, because it computes no value; a chained result, as in `void (async () => { ... })().catch(...)`, is still
  rejected. Load that `rules/` folder from the repository's own `sgconfig.yml` `ruleDirs`, or run `ast-grep scan -c`
  with the shipped file. It was checked with oxlint 1.80.0, `eslint-plugin-sonarjs` 4.2.2, and ast-grep 0.51.0. Pin
  oxlint, the plugin, and ast-grep to exact versions, as `ci-reproducible-checks` requires, because oxlint documents JS
  plugins as alpha and not subject to semver. Install the plugin in the package that holds the `.contracts` folder or in
  one above it, because oxlint resolves it from the installed file's folder. The contract declares `requires-tenet:
0.11.0`.
- `code-exhaustive-branches`: an `else if` that tests the same value for equality as the test before it now becomes a
  `switch` statement, for an open set as well as a closed one, so that the exhaustiveness lint can check every member;
  before, both forms complied. The requirement applies only where a `switch` accepts any expression as a case and
  compares it by strict equality, so a pattern `match` is never required. Comparisons of the value joined by a logical
  or form one equality test, and a test joined by a logical and stays outside the rule. Lint rules that require a
  default case or final `else` on a branch over a closed set, or an `if` instead of a short `switch`, must be off, and
  the lint must run with type information. A default case beside cases that already name every member stays allowed. The
  contract ships `assets/oxlint/oxlintrc.json` and declares `requires-tenet: 0.11.0`. The file loads
  `eslint-plugin-unicorn` through oxlint's `jsPlugins` under the alias `unicorn-js`, because oxlint reserves `unicorn`
  for its native plugin, and sets `prefer-switch` to its minimum of 2 cases with `emptyDefaultCase: "no-default-case"`.
  It sets `options.typeAware` and configures `typescript/switch-exhaustiveness-check` to reject a missing member beside
  a default and a switch on a non-union type without a default, and to allow a default on an exhaustive switch. It was
  checked with oxlint 1.80.0, `eslint-plugin-unicorn` 79.0.0, and `oxlint-tsgolint` 7.0.2005. Pin oxlint, the plugin,
  and `oxlint-tsgolint` to exact versions, as `ci-reproducible-checks` requires, because oxlint documents JS plugins as
  alpha and not subject to semver. Install the plugin in the package that holds the `.contracts` folder or in one above
  it, because oxlint resolves it from the installed file's folder. Install `oxlint-tsgolint` where the lint runs, such
  as a dev dependency at the repository root, because oxlint looks for it from its working directory. Type-aware mode
  would also turn on oxlint's 16 default type-aware rules, such as `unbound-method` and `no-floating-promises`, so the
  file turns each of them off and enforces only this contract; a repository's own configuration may turn any of them
  back on. On conductor this removes 6 warnings and keeps the 5 contract errors. A tsconfig error makes the
  exhaustiveness rule skip that project's files with only a warning. A repository that lints only JavaScript can set
  `options.typeAware` to false in its own configuration. `oxlint --fix-suggestions` rewrites every chain, with a second
  run for a chain nested in another; run the formatter afterwards.
- `code-function-size`: its `assets/oxlint/oxlintrc.json` now also sets the length, nesting, and callback limits beside
  cognitive complexity 15. `max-lines-per-function` allows 50 lines, counted without blank lines and comments, and also
  checks immediately invoked functions. An override allows 60 lines for functions in `.tsx` and `.jsx` files, such as
  React components, as an example of a limit declared for one kind of function. The text now lets a repository declare
  such a limit, with its reason beside the limits. In the largest measured repository, the override lowers the asset's
  findings from 573 to 555. `max-depth` allows 3 nested blocks, and `max-nested-callbacks` allows 3 nested callbacks.
  Code that passed a lint configuration extending the file can now fail, such as a 101-line method or a fourth nested
  block. None of the three rules has an autofix, so each finding needs a rewrite or a suppression that
  `code-lint-suppressions` allows. A repository may still override any limit the file sets, and the text now says "any
  limit". The three rules are native to oxlint and need no plugin beyond `eslint-plugin-sonarjs`. It was checked with
  oxlint 1.80.0 and 1.89.0 and `eslint-plugin-sonarjs` 4.2.2.
- `code-module-file-roles`: declare at most one exported function in each source file. A function counts when the file
  declares it or binds it as a value to a name for another file to import; a re-export does not count. A file may keep
  the exported function's private helpers, such as the function for one case of its branch, unexported beside it. A
  namespace file, which an entry point re-exports under one namespace named for the file, may still export several
  functions on that namespace's concept. The repository exempts namespace files from the limit by a declared path
  pattern that matches no other file. A language may leave the limit to review only when the repository declares that
  language and the reason beside its declared file length. Before, every independent operation of a behavior module
  needed its own file. A private independent operation, or one that an exported class or another exported value that is
  not a function holds, which violated that rule, now complies. The contract ships `assets/ast-grep/` rules for
  JavaScript, TypeScript, and Tsx that report each exported function after a file's first, including one inside
  parentheses or a type assertion, and declares `requires-tenet: 0.11.0`. They were checked with ast-grep 0.51.0; pin
  ast-grep to an exact version, as `ci-reproducible-checks` requires. Keep the installed rules folder out of the
  repository's root ast-grep configuration, because `--globs` applies to every rule in a scan. Run the rules alone with
  the installed `sgconfig.yml` and the declared namespace and generated path patterns, such as `ast-grep scan -c
.contracts/001-code-module-file-roles/assets/ast-grep/sgconfig.yml --globs '!src/uuid/uuid.ts'`. Review covers a
  function that an export list or a default export names or a call returns, and a new check confirms that each path the
  namespace pattern matches is a namespace file. The message now names the one-function limit.
- `code-script-entry-points`: the main program can no longer run as one call that ends the process with a main call as
  its only argument, such as `process.exit(await main())`, because `code-typescript-call-arguments` forbids nesting that
  call.
- `code-typescript-effect-errors`: a failure is expected when any caller or user could act differently because of it,
  such as a requested record that does not exist or a dropped request. Every other failure is a defect, such as a record
  that the same object wrote now missing or corrupt, which means the code's own invariant broke. A lookup that finds no
  record for a caller's identifier stays an expected failure. Each defect now carries a tagged error class with fields
  that locate it, such as `new InvoiceMissing({ invoice })`, and only a defect uses `Effect.die`, `Effect.orDie`, or
  `throw`. Code never builds or extends a bare runtime error, such as `new Error(message)` or `class InvoiceError
extends Error`, and never fails, dies, or throws with a string or plain object. A test fake may throw what the
  dependency it stands in for throws. Each foreign call that can throw or reject, such as `fetch`, JSON parsing, or a
  storage or library call, is wrapped once where it is called with `Effect.tryPromise` or `Effect.try`. Its `catch`
  option maps the failure to a tagged error class that keeps the caught value as its `cause`. A `catch` clause or a
  promise's `catch` method is now a violation; a `try` with only a `finally` clause stays allowed. Each entry point has
  one defect handler that records the defect and ends its unit of work, such as a server's 500 response or a command's
  error exit status. A user interface wraps each route in an error boundary and passes it the defects of that route's
  event handlers and asynchronous reads. Only that handler catches a defect, and no code logs a failure or defect and
  then continues. `pipe` stays allowed as `code-typescript-call-arguments` allows, and the bound statements that
  contract requires go inside `Effect.gen` with `yield*`. The tag-literal allowance is now stated only in
  `code-closed-value-sets`. The contract ships `assets/oxlint/oxlintrc.json`, which enables oxlint's native
  `no-throw-literal` and `preserve-caught-error` and keeps `unicorn/throw-new-error` off, because that rule reports and
  rewrites the base of a tagged error class. It also ships `assets/ast-grep/` with TypeScript and Tsx variants of an
  `untagged-errors` rule and a `catch-handlers` rule; run them from the repository root with `ast-grep scan -c` and the
  installed `assets/ast-grep/sgconfig.yml`. They were checked with oxlint 1.80.0 and ast-grep 0.51.0; pin both to exact
  versions, as `ci-reproducible-checks` requires. The contract declares `requires-tenet: 0.11.0`.
- `test-support-modules`: each fixture server, fixture builder, and harness helper in the test support folder goes in
  its own file, named for its behavior, such as `start-process`, as `code-module-file-roles` requires. Before, one file
  per helper family, such as `processes`, could hold several helpers. Where a contract such as
  `code-typescript-module-boundaries` gives each folder an entry point, tests import every helper through the test
  support folder's entry point, not its files.

### Loosened

- `code-module-structure-and-control-flow`: the rule "Name intermediate values when nested calls hide the sequence" no
  longer applies to code that `code-typescript-call-arguments` governs, which binds every nested call instead. In other
  code it is unchanged.
- `code-typescript-module-boundaries`: A file may now import files directly in a folder that contains it, such as
  `orders/lines/sum.ts` importing `orders/format.ts`, except the package's own entry point. An entry point's re-exports
  of its nested folders' symbols now follow `code-typescript-entry-points`, which lets an entry point re-export from a
  nested folder's declaring file. Before this change, the entry-point import rule forbade both. Every other folder is
  still imported only through its entry point. The entry point of the test support folder that `test-support-modules`
  declares may export what only test files use, so tests import helpers through it. The contract now ships
  `assets/oxlint/oxlintrc.json` and declares `requires-tenet: 0.11.0`. The file loads `eslint-plugin-boundaries` through
  oxlint `jsPlugins`, uses `eslint-import-resolver-typescript`, and treats every folder as a module. It fails on any
  import of a code file that goes past a folder's index file. That covers type-only imports, re-exports, dynamic
  imports, `import()` types, import-equals, `require()`, extensionless and `.js` specifiers, and tsconfig and package
  `imports` aliases. It also fails on a relative import it cannot resolve. It fails on cycles through `import/no-cycle`
  with `ignoreTypes: false`, but that rule does not see cycles through dynamic imports, `import()` types, import-equals
  declarations, or `require()`, so those cycles need another check. It skips dot-named files, such as a package's
  `.prettierrc.cjs`, so an import of a dot-named file in another folder is left to review. It turns off `import/default`
  and `import/namespace`, which enabling oxlint's `import` plugin would otherwise run. Package-name imports and imports
  of data files are left to review. The file was checked with oxlint 1.80.0, `eslint-plugin-boundaries` 7.3.0, and
  `eslint-import-resolver-typescript` 4.4.5. Use `eslint-plugin-boundaries` 7.3.0 or later, because 7.2.1 and earlier
  misplace a folder whose name appears earlier in its own path, such as `workspaces/api/src/work`. oxlint does not pass
  `settings` through `extends`, so either run the file as its own configuration from the repository root or extend it
  and copy its `settings`. Without those settings, `boundaries/no-unknown-files` fails on every file. Pin exact versions
  as `ci-reproducible-checks` requires. Install the plugin and the resolver in the package that holds `.contracts` or in
  one above it. The resolver reads the `tsconfig.json` in the folder the lint runs from, plus its references, so list
  every other tsconfig that declares path aliases under `project`, as the contract now requires.

### Added

- Contract `api-typescript-request-paths`: build each request path and URL with one typed path function per operation,
  declared once in the module that owns the routes or stored layout it addresses. This covers fixed paths, test code,
  and other systems' APIs, whose path functions belong to the module that owns that API's client. Each path function
  takes one named, typed field per variable part, percent-encodes each text part, builds its query with a query encoder,
  and returns the whole path; callers never append to it, and a full URL resolves it against a configured origin. A path
  function holds no state, so a chained builder does not count as one. Hand-written path functions sit in the module's
  one paths file, whose stem names the module and ends in `paths`, such as `packs/pack-paths.ts`, which its entry point
  re-exports as one namespace such as `PackPaths`, so calls read `PackPaths.chunk({ key, index })`. A served route's
  pattern and its path function derive from one declaration. A typed call that a client or router derives from one route
  declaration counts as a path function; a call-site template such as `request('GET /accounts/{account}/invoices', {
account })` is a hand-written path. The contract ships `assets/ast-grep/` rules for TypeScript and Tsx. They report
  each template literal, and each `+` concatenation, that starts with `/` outside files whose stem ends in `-paths`; a
  repository that declares another pattern may override it. The rules were checked with ast-grep 0.51.0. The contract
  declares `requires-tenet: 0.11.0`.
- Contract `code-numeric-literals`: give every number a named constant, meaning a constant binding or read-only field
  whose whole value is one number, and refer to the number by that name. A reassignable variable and a parameter's
  default are not named constants. A declared few numbers may stay bare anywhere, such as -1, 0, 1, and 2, and that list
  never holds a quantity such as a limit, size, duration, conversion factor, or status code. An enumeration member's
  value, an array or type index, a type alias's whole value or union member, such as `type RetryCount = 3 | 5`, and an
  object property's whole value, including property assignments and markup attributes, may also stay bare. Elsewhere in
  a type, such as `{ size: 3 | 5 }`, code refers to such an alias. Each constant holds one literal at most besides the
  bare numbers. A derived constant composes other constants' names, such as
  `UPLOAD_CHUNK_BYTES = UPLOAD_CHUNK_MEBIBYTES * BYTES_PER_MEBIBYTE`, never literal arithmetic such as `5 * 1024 ** 2`
  or its computed value such as `5242880`. A constant is named for what its number means, not its digits, and a status
  code takes its closed set's member as its name under `code-closed-value-sets`. Test files, generated files, and copied
  third-party source are exempt by declared path patterns. The contract ships `assets/oxlint/oxlintrc.json`, which
  configures oxlint's native `no-magic-numbers` rule, so it needs no JS plugin. The file also turns the rule off for
  `*.test.*`, `*.spec.*`, `test/`, `tests/`, `testing/`, and `__tests__/`, the same test patterns
  `code-closed-value-sets` ships. A repository's own lint configuration may override the bare numbers and add or
  re-enable test patterns. Review covers the numbers the lint misses, such as a markup child, a parse call's radix, or
  an object key. It was checked with oxlint 1.80.0. The contract declares `requires-tenet: 0.11.0`.
- Contract `code-typescript-call-arguments`: never write a call, `new` expression, or `await` inside the arguments of
  another call or `new` expression; bind the result to a name and pass the name. The ban reaches through object fields,
  array elements, templates, operators, spreads, and type assertions. It counts a call chain once and starts afresh
  inside a function, class, or embedded markup element written in the arguments. A tagged template is a template, not a
  call. Files with the schema role a repository declares under `code-module-file-roles` may nest calls, `new`
  expressions, and `await` inside arguments. Each direct argument of `pipe(...)` or `.pipe(...)` may itself be one call,
  but not a `new` or an `await`, and that call's own arguments follow the rule. When a step needs an earlier step's
  result other than its input, or chooses between paths, each step's result is bound in a statement, such as `const
amount = yield* fetchAmount`. The formatter decides pipeline layout. A function written as a field, method, or element
  of an object or array in a call's arguments is bound to a name first, while a function passed directly as an argument,
  such as an array-method callback, stays inline. A function bound to a variable is a function declaration or a constant
  annotated with a function type; `any`, `unknown`, `satisfies`, and `as` do not count as that annotation. Such a
  binding is an independent operation even with one use. The contract ships ast-grep rules for TypeScript and Tsx in
  `assets/ast-grep/rules/`: `call-arguments-*` for nesting, which exempt files named `schemas`, and
  `argument-object-functions-*` for functions in argument objects and arrays. A repository that declares another schema
  file name copies the nesting rules with that name. It also ships an `assets/ast-grep/sgconfig.yml` that runs them on
  their own, and a repository can instead list the installed `assets/ast-grep/rules` folder under `ruleDirs` in its own
  `sgconfig.yml`. It also ships `assets/oxlint/oxlintrc.json`, which sets the native `func-style` rule to `declaration`
  with `allowTypeAnnotation` and needs no plugin. They were checked with ast-grep 0.51.0 and oxlint 1.80.0; pin both to
  exact versions, as `ci-reproducible-checks` requires. None of the three rules has an autofix. The contract declares
  `requires-tenet: 0.11.0`.

### Clarified

- `code-guard-clauses`: an `if` that is the only statement of an `else` block may become a `switch` or `match` where
  `code-exhaustive-branches` requires one, instead of an `else if`.
- `code-measured-value-names`: the unit-conversion example multiplies by the named constant `MILLISECONDS_PER_SECOND`
  instead of a bare `1000`, and the violation example builds `UPLOAD_LIMIT` from named constants, as
  `code-numeric-literals` requires.
- `code-typescript-class-declarations`: the `override` field example sets `defaultPort` from a named constant, as
  `code-numeric-literals` requires.
- `code-typescript-type-assertions`: the annotation example declares an invoice, replacing a status-text map keyed by a
  bare `404`, which `code-closed-value-sets` and `code-numeric-literals` reject.
- `tenet-architecture-curation`: the recovery guidance no longer names one repository's durable infrastructure.
- `tenet-code-curation`: the TypeScript decision example puts a blank line after each `if` statement, as
  `code-blank-lines` requires.

## v9.0.0

`code-blank-lines`, `code-function-size`, and `code-typescript-node-scripts` ship tool configuration under `assets/`,
so installing or updating them needs Tenet 0.11.0 or later. Every other contract still installs with Tenet 0.7.0 or
later. The Release workflow now validates every contract with Tenet 0.11.0.

### Upgrading

Raise Tenet to 0.11.0 first. With `.tenet.lock` and the installed copies committed, run
`tenet contracts update --ref v9.0.0`.

- No rule moved to another contract.
- New assets: `code-blank-lines` and `code-function-size` ship `assets/oxlint/oxlintrc.json`, and the new
  `code-typescript-node-scripts` ships `assets/typescript/tsconfig.json`. Install `@stylistic/eslint-plugin` 5.10.0 and
  `eslint-plugin-sonarjs` 4.2.2 where oxlint resolves them, as their entries say.
- Roll back with `tenet contracts update --ref v8.0.0`. Copies of the 4 contracts this release added are reported as
  removed upstream and left in place; drop each with `tenet contracts remove PATH`, which also deletes its locked
  assets. The oxlint files of `code-blank-lines` and `code-function-size` stay in place, leave the lock, and make
  `update` exit 1; delete them with `git rm`.

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

### Upgrading

Raise Tenet to 0.11.0 first; `tenet skills` and the `tenet-adoption` skill need it. With `.tenet.lock` and the installed
copies committed, run `tenet contracts update --ref v8.0.0`.

- No rule moved to another contract, and no contract ships assets.
- Rename an installed curation skill's `resources/` folder to `references/`, as described above, before recording it
  with `tenet skills add`.
- Roll back with `tenet contracts update --ref v7.0.0`. This release added no contract, so every copy returns to its
  v7.0.0 text.

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

### Upgrading

Raise Tenet to 0.11.0 first. With `.tenet.lock` and the installed copies committed, run
`tenet contracts update --ref v7.0.0`.

- No rule moved to another contract, and no contract ships assets.
- Roll back with `tenet contracts update --ref v6.0.0`. This release added no contract, so every copy returns to its
  v6.0.0 text.

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

### Upgrading

Raise Tenet to 0.11.0 first. With `.tenet.lock` and the installed copies committed, run
`tenet contracts update --ref v6.0.0`.

- Moved rules: the unit clause of `code-module-structure-and-control-flow` moves to `code-measured-value-names`, the
  suppression rules of `code-function-size` to `code-lint-suppressions`, boolean naming in
  `code-typescript-function-arguments` to `code-boolean-names`, the choice of what an entry point exports in
  `code-typescript-package-boundaries` to `code-export-consumers`, and the assertion rule of
  `code-typescript-effect-schemas` to `code-typescript-type-assertions`. Each receiving contract is new in this release;
  install it wherever the old one is installed, or the rule no longer applies there.
- No contract ships assets.
- Roll back with `tenet contracts update --ref v5.0.0`. Copies of the 34 contracts this release added are reported as
  removed upstream and left in place; drop each with `tenet contracts remove PATH`.

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

### Upgrading

Raise Tenet to 0.11.0 first. With `.tenet.lock` and the installed copies committed, run
`tenet contracts update --ref v5.0.0`.

- Moved rules: type placement moves from `code-module-structure-and-control-flow` to `code-module-file-roles`, and blank
  lines between phases to `code-blank-lines`; a shared utilities module now follows `code-shared-utilities`. Each
  receiving contract is new in this release; install it wherever `code-module-structure-and-control-flow` is installed,
  or the rule no longer applies there. The rule to follow the area's established conventions is removed with no
  replacement.
- No contract ships assets.
- Roll back with `tenet contracts update --ref v4.1.0`. Copies of the 12 contracts this release added are reported as
  removed upstream and left in place; drop each with `tenet contracts remove PATH`.

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

### Upgrading

Raise Tenet to 0.11.0 first. With `.tenet.lock` and the installed copies committed, run
`tenet contracts update --ref v4.0.0`.

- No rule moved to another contract, and no contract ships assets.
- Roll back with `tenet contracts update --ref v3.0.0`. Copies of the 5 contracts this release added are reported as
  removed upstream and left in place; drop each with `tenet contracts remove PATH`.

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

### Upgrading

Raise Tenet to 0.11.0 first. With `.tenet.lock` and the installed copies committed, run
`tenet contracts update --ref v3.0.0`.

- No contract changed, so `update` moves each lock entry to v3.0.0 and leaves every copy as it is. No rule moved, and no
  contract ships assets.
- Roll back with `tenet contracts update --ref v2.1.0`.

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

### Upgrading

Raise Tenet to 0.11.0 first. With `.tenet.lock` and the installed copies committed, run
`tenet contracts update --ref v2.0.0`.

- Renamed contracts: `update` exits 1 and reports `execution-lifecycle` and `ownership-and-boundaries` as removed
  upstream. To move an installed copy, move its `## Local adaptations` aside, run `tenet contracts remove PATH`, add the
  new name with `tenet contracts add`, such as `tenet contracts add tenet/code-execution-lifecycle@v2.0.0 --scope DIR`,
  then restore the adaptations.
- Moved rules: where proposals live moves from `contract-maintenance` to `context-note-curation`. Its model-assessment
  and retry-until-approved rules, and the model-assessment clause in the checks of `data-and-apis`, move to
  `llm-code-review-evidence`. Install each receiving contract wherever the old one is installed, or the rule no longer
  applies there. The fixture-contract rule of `contract-maintenance` is dropped.
- No contract ships assets.
- Roll back with `tenet contracts update --ref v1.0.0`. Copies of the 71 contracts this release added, the renamed ones
  included, are reported as removed upstream and left in place; drop each with `tenet contracts remove PATH`. Then add
  `execution-lifecycle` or `ownership-and-boundaries` back with `tenet contracts add tenet/NAME@v1.0.0 --scope DIR`.

### Removed

- `execution-lifecycle`, renamed `code-execution-lifecycle`. The new contract also gives each request exactly one retry
  owner, records a required external effect's intent and operation identity before starting it, rejects identity reuse
  with different inputs, never replays an uncertain effect unless the external system deduplicates it, and keeps
  cleanup running when its caller fails.
- `ownership-and-boundaries`, renamed `code-ownership-and-boundaries`. The new contract also limits imports to declared
  dependencies and public entry points, consumes other repositories only through versioned artifacts or configured
  endpoints, and keeps test fixtures out of production builds.

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
