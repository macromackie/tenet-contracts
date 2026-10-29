/**
 * The env tool's settings module, which decodes its arguments and the `--from-env` variable.
 *
 * `env-tool.mts` imports it; it is not run directly.
 */
import { Effect, Option } from "effect";
import { ArgumentsProblem, KEY_PATTERN } from "./constants.mts";
import { ArgumentsRefused } from "./errors.mts";
import type { Settings } from "./types.mts";

type ReadSourceInput = { readonly options: readonly string[] };

type ReadSourceValueInput = { readonly source: string };

type CheckKeyNameInput = { readonly name: string };

type ReadCommandInput = {
  readonly file: string;
  readonly name: string;
  readonly options: readonly string[];
};

/** The option that names the variable holding the new value. */
const FROM_ENV = "--from-env";

/** The arguments before the command's own: the interpreter and this script. */
const LEADING_ARGUMENTS = 2;

function checkKeyName({ name }: CheckKeyNameInput): Effect.Effect<void, ArgumentsRefused> {
  return Effect.gen(function* () {
    if (!KEY_PATTERN.test(name)) {
      return yield* new ArgumentsRefused({ problem: ArgumentsProblem.KeyName });
    }
  });
}

function readSourceValue({
  source,
}: ReadSourceValueInput): Effect.Effect<string, ArgumentsRefused> {
  return Effect.gen(function* () {
    const value = Option.fromNullishOr(process.env[source]);

    if (Option.isNone(value)) {
      return yield* new ArgumentsRefused({ problem: ArgumentsProblem.SourceUnset });
    }

    return value.value;
  });
}

function readSource({
  options,
}: ReadSourceInput): Effect.Effect<Option.Option<string>, ArgumentsRefused> {
  return Effect.gen(function* () {
    const [option, source = "", ...extra] = options;

    if (option === undefined) {
      return Option.none();
    }

    if (option !== FROM_ENV || extra.length > 0) {
      return yield* new ArgumentsRefused({ problem: ArgumentsProblem.SetShape });
    }

    if (!KEY_PATTERN.test(source)) {
      return yield* new ArgumentsRefused({ problem: ArgumentsProblem.SourceName });
    }

    const value = yield* readSourceValue({ source });

    return Option.some(value);
  });
}

function readSetSettings({
  file,
  name,
  options,
}: ReadCommandInput): Effect.Effect<Settings, ArgumentsRefused> {
  return Effect.gen(function* () {
    if (file === "" || name === "") {
      return yield* new ArgumentsRefused({ problem: ArgumentsProblem.SetShape });
    }

    yield* checkKeyName({ name });

    const source = yield* readSource({ options });

    return { command: "set", file, name, source };
  });
}

function readClearSettings({
  file,
  name,
  options,
}: ReadCommandInput): Effect.Effect<Settings, ArgumentsRefused> {
  return Effect.gen(function* () {
    if (file === "" || name === "" || options.length > 0) {
      return yield* new ArgumentsRefused({ problem: ArgumentsProblem.ClearShape });
    }

    yield* checkKeyName({ name });

    return { command: "clear", file, name };
  });
}

/** Decodes the command, the env file, the key name, and the `--from-env` value of this run. */
export function readSettings(): Effect.Effect<Settings, ArgumentsRefused> {
  return Effect.gen(function* () {
    const [command = "", file = "", name = "", ...options] = process.argv.slice(LEADING_ARGUMENTS);

    switch (command) {
      case "set": {
        return yield* readSetSettings({ file, name, options });
      }
      case "clear": {
        return yield* readClearSettings({ file, name, options });
      }
      default: {
        return yield* new ArgumentsRefused({ problem: ArgumentsProblem.CommandUnknown });
      }
    }
  });
}
