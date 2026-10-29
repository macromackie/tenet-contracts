/**
 * Reads the value that `set` writes, from `--from-env`, a hidden prompt, or piped input.
 *
 * `edit-env.mts` imports it; it is not run directly.
 */
import { buffer } from "node:stream/consumers";
import { TextDecoder } from "node:util";
import { Effect, Option } from "effect";
import { FileOperation, LINE_ENDING, MAX_VALUE_BYTES, ValueProblem } from "./constants.mts";
import { InputFailed, type InputRefused, ValueRefused } from "./errors.mts";
import { readHiddenValue } from "./read-hidden-value.mts";

type ReadNewValueInput = {
  readonly name: string;
  readonly source: Option.Option<string>;
};

type CheckValueInput = { readonly value: string };

type ReadNewValueError = InputFailed | InputRefused | ValueRefused;

/** A control character, such as a line break, which a one-line value never holds. */
const CONTROL_CHARACTER = /\p{Cc}/v;

function readPipedValue(): Effect.Effect<string, InputFailed> {
  return Effect.gen(function* () {
    const raw = yield* Effect.tryPromise(async () => await buffer(process.stdin)).pipe(
      Effect.mapError((cause) => new InputFailed({ cause, operation: FileOperation.Read })),
    );

    const decoded = yield* Effect.try(() =>
      new TextDecoder("utf-8", { fatal: true }).decode(raw),
    ).pipe(Effect.mapError((cause) => new InputFailed({ cause, operation: FileOperation.Decode })));

    return decoded.replace(LINE_ENDING, "");
  });
}

function checkValue({ value }: CheckValueInput): Effect.Effect<string, ValueRefused> {
  return Effect.gen(function* () {
    if (value === "") {
      return yield* new ValueRefused({ problem: ValueProblem.Empty });
    }

    if (Buffer.byteLength(value, "utf-8") > MAX_VALUE_BYTES) {
      return yield* new ValueRefused({ problem: ValueProblem.TooLarge });
    }

    if (CONTROL_CHARACTER.test(value)) {
      return yield* new ValueRefused({ problem: ValueProblem.ControlCharacters });
    }

    return value;
  });
}

/** Reads the new value from `--from-env`, a hidden terminal prompt, or piped standard input. */
export function readNewValue({
  name,
  source,
}: ReadNewValueInput): Effect.Effect<string, ReadNewValueError> {
  return Effect.gen(function* () {
    if (Option.isSome(source)) {
      return yield* checkValue({ value: source.value });
    }

    if (process.stdin.isTTY) {
      const typed = yield* readHiddenValue({ name });

      return yield* checkValue({ value: typed });
    }

    const piped = yield* readPipedValue();

    return yield* checkValue({ value: piped });
  });
}
