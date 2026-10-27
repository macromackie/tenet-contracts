# Changelog

Each release lists every changed contract or skill under one class. A Tightened or Removed entry makes a major
release, an Added or Loosened entry a minor release, and Clarified entries alone a patch release.

## v10.0.0

`api-typescript-request-paths`, `code-closed-value-sets`, `code-conditional-expressions`, `code-exhaustive-branches`,
`code-module-file-roles`, `code-numeric-literals`, `code-typescript-call-arguments`, `code-typescript-effect-errors`,
and `code-typescript-module-boundaries` now ship tool configuration under `assets/`, beside `code-blank-lines`,
`code-function-size`, and `code-typescript-node-scripts`, so installing or updating them needs Tenet 0.11.0 or later.
Every other contract still installs with Tenet 0.7.0 or later. The shipped lint files fail on code that complied before;
run each tool's autofix where it has one, then rewrite or suppress what remains as `code-lint-suppressions` allows.

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
  bare numbers. A derived constant composes other constants' names, such as `UPLOAD_CHUNK_BYTES = UPLOAD_CHUNK_MEBIBYTES
  * BYTES_PER_MEBIBYTE`, never literal arithmetic such as `5 * 1024 ** 2` or its computed value such as `5242880`. A
  constant is named for what its number means, not its digits, and a status code takes its closed set's member as its
  name under `code-closed-value-sets`. Test files, generated files, and copied third-party source are exempt by declared
  path patterns. The contract ships `assets/oxlint/oxlintrc.json`, which configures oxlint's native `no-magic-numbers`
  rule, so it needs no JS plugin. The file also turns the rule off for `*.test.*`, `*.spec.*`, `test/`, `tests/`,
  `testing/`, and `__tests__/`, the same test patterns `code-closed-value-sets` ships. A repository's own lint
  configuration may override the bare numbers and add or re-enable test patterns. Review covers the numbers the lint
  misses, such as a markup child, a parse call's radix, or an object key. It was checked with oxlint 1.80.0. The
  contract declares `requires-tenet: 0.11.0`.
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
