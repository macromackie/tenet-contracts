/**
 * Runs the env tool on a scratch env file with fake values and checks each edit.
 *
 * `check-env-tool.mts` imports it; it is not run directly.
 */
import { mkdtemp, readFile, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { Effect, Option, type Scope } from "effect";
import {
  ACCIDENTAL_VALUE,
  MISE_CONFIG,
  ORIGINAL_ENV,
  OWNER_ONLY_MODE,
  PERMISSION_BITS,
  PROBE_KEY,
  REPLACEMENT_VALUE,
  SOURCE_KEY,
  SUCCESS,
  TRICKY_VALUE,
} from "./constants.mts";
import { type CheckFailed, StepFailed } from "./errors.mts";
import { expectChecks } from "./expect-checks.mts";
import { runCommand } from "./run-command.mts";
import { decodeMiseEnvironment } from "./schemas.mts";
import type { CheckSettings, CommandRun, Fixture } from "./types.mts";

type RunScenariosInput = { readonly settings: CheckSettings };

type ScenarioInput = {
  readonly fixture: Fixture;
  readonly settings: CheckSettings;
};

type RunToolInput = {
  readonly args: readonly string[];
  readonly input: string;
  readonly settings: CheckSettings;
  readonly variables: Readonly<Record<string, string>>;
};

type ReadEnvInput = { readonly file: string };

type HasSucceededInput = { readonly run: CommandRun };

type ScenarioError = CheckFailed | StepFailed;

/** The scratch folder's name before the random part that the system adds. */
const SCRATCH_PREFIX = "env-tool-check-";

function hasSucceeded({ run }: HasSucceededInput): boolean {
  const status = Option.getOrUndefined(run.status);

  return status === SUCCESS;
}

function runTool({
  args,
  input,
  settings,
  variables,
}: RunToolInput): Effect.Effect<CommandRun, StepFailed> {
  const environment = { ...settings.environment, ...variables };
  const toolArgs = [settings.tool, ...args];

  return runCommand({ args: toolArgs, command: process.execPath, environment, input });
}

function readEnv({ file }: ReadEnvInput): Effect.Effect<string, StepFailed> {
  return Effect.tryPromise(async () => await readFile(file, "utf-8")).pipe(
    Effect.mapError((cause) => new StepFailed({ cause, step: "read the env file" })),
  );
}

function checkReadBack({ fixture, settings }: ScenarioInput): Effect.Effect<void, ScenarioError> {
  return Effect.gen(function* () {
    const environment = { ...settings.environment, MISE_TRUSTED_CONFIG_PATHS: fixture.folder };
    const args = ["-C", fixture.folder, "env", "--json"];
    const printed = yield* runCommand({ args, command: "mise", environment, input: "" });

    const decoded = yield* decodeMiseEnvironment(printed.stdout).pipe(
      Effect.mapError((cause) => new StepFailed({ cause, step: "decode mise env --json" })),
    );

    yield* expectChecks({
      checks: [
        { check: "mise reads back the value set", holds: decoded[PROBE_KEY] === TRICKY_VALUE },
      ],
    });
  });
}

function checkSet({ fixture, settings }: ScenarioInput): Effect.Effect<void, ScenarioError> {
  return Effect.gen(function* () {
    const args = ["set", fixture.file, PROBE_KEY, "--from-env", SOURCE_KEY];
    const variables = { [SOURCE_KEY]: TRICKY_VALUE };
    const run = yield* runTool({ args, input: "", settings, variables });

    const stats = yield* Effect.tryPromise(async () => await stat(fixture.file)).pipe(
      Effect.mapError((cause) => new StepFailed({ cause, step: "stat the env file" })),
    );

    const written = yield* readEnv({ file: fixture.file });
    const succeeded = hasSucceeded({ run });
    const printed = run.stdout + run.stderr;
    const hidden = !printed.includes(TRICKY_VALUE);
    const kept = written.startsWith(ORIGINAL_ENV);

    yield* expectChecks({
      checks: [
        { check: "set from a variable succeeds", holds: succeeded },
        { check: "set prints no value", holds: hidden },
        {
          check: "set keeps the file owner-only",
          holds: stats.mode % PERMISSION_BITS === OWNER_ONLY_MODE,
        },
        { check: "set keeps the other lines", holds: kept },
      ],
    });
  });
}

function checkReplace({ fixture, settings }: ScenarioInput): Effect.Effect<void, ScenarioError> {
  return Effect.gen(function* () {
    const args = ["set", fixture.file, PROBE_KEY];
    const run = yield* runTool({ args, input: `${REPLACEMENT_VALUE}\n`, settings, variables: {} });
    const written = yield* readEnv({ file: fixture.file });
    const assignments = written.split("\n").filter((line) => line.startsWith(`${PROBE_KEY}=`));
    const succeeded = hasSucceeded({ run });
    const printed = run.stdout + run.stderr;
    const hidden = !printed.includes(REPLACEMENT_VALUE);

    yield* expectChecks({
      checks: [
        { check: "set from piped input succeeds", holds: succeeded },
        { check: "replace prints no value", holds: hidden },
        { check: "replace keeps one assignment", holds: assignments.length === 1 },
      ],
    });
  });
}

function checkClear({ fixture, settings }: ScenarioInput): Effect.Effect<void, ScenarioError> {
  return Effect.gen(function* () {
    const args = ["clear", fixture.file, PROBE_KEY];
    const run = yield* runTool({ args, input: "", settings, variables: {} });
    const written = yield* readEnv({ file: fixture.file });
    const succeeded = hasSucceeded({ run });

    yield* expectChecks({
      checks: [
        { check: "clear succeeds", holds: succeeded },
        { check: "clear removes the key", holds: written === ORIGINAL_ENV },
      ],
    });
  });
}

function checkRefusals({ fixture, settings }: ScenarioInput): Effect.Effect<void, ScenarioError> {
  return Effect.gen(function* () {
    const accidentalArgs = ["set", fixture.file, "NEW", ACCIDENTAL_VALUE];
    const accidental = yield* runTool({ args: accidentalArgs, input: "", settings, variables: {} });
    const emptyArgs = ["set", fixture.file, "NEW"];
    const empty = yield* runTool({ args: emptyArgs, input: "\n", settings, variables: {} });
    const written = yield* readEnv({ file: fixture.file });
    const accidentalSucceeded = hasSucceeded({ run: accidental });
    const emptySucceeded = hasSucceeded({ run: empty });
    const printed = accidental.stdout + accidental.stderr;
    const hidden = !printed.includes(ACCIDENTAL_VALUE);

    yield* expectChecks({
      checks: [
        { check: "a value argument is refused", holds: !accidentalSucceeded },
        {
          check: "a refused value argument is not printed",
          holds: hidden,
        },
        { check: "an empty value is refused", holds: !emptySucceeded },
        { check: "refusals leave the file unchanged", holds: written === ORIGINAL_ENV },
      ],
    });
  });
}

function prepareFixture(): Effect.Effect<Fixture, StepFailed, Scope.Scope> {
  const scratch = tmpdir();
  const prefix = join(scratch, SCRATCH_PREFIX);

  const creating = Effect.tryPromise(async () => await mkdtemp(prefix)).pipe(
    Effect.mapError((cause) => new StepFailed({ cause, step: "create the scratch folder" })),
  );

  return Effect.gen(function* () {
    const folder = yield* Effect.acquireRelease(creating, (created) =>
      Effect.promise(async () => {
        await rm(created, { force: true, recursive: true });
      }),
    );

    const file = join(folder, ".env");
    const config = join(folder, "mise.toml");

    yield* Effect.tryPromise(async () => {
      await writeFile(file, ORIGINAL_ENV, { mode: OWNER_ONLY_MODE });
      await writeFile(config, MISE_CONFIG);
    }).pipe(Effect.mapError((cause) => new StepFailed({ cause, step: "write the scratch files" })));

    return { file, folder };
  });
}

/** Sets, reads back, replaces, and clears a key, then checks that bad input changes nothing. */
export function runScenarios({ settings }: RunScenariosInput): Effect.Effect<void, ScenarioError> {
  return Effect.gen(function* () {
    const fixture = yield* prepareFixture();

    yield* checkSet({ fixture, settings });
    yield* checkReadBack({ fixture, settings });
    yield* checkReplace({ fixture, settings });
    yield* checkClear({ fixture, settings });
    yield* checkRefusals({ fixture, settings });
  }).pipe(Effect.scoped);
}
