/**
 * Reads one value at a terminal prompt with echo off.
 *
 * `read-new-value.mts` imports it; it is not run directly.
 */
import { Effect, Option } from "effect";
import { applyErasures } from "./apply-erasures.mts";
import { InputProblem, MAX_VALUE_BYTES, ValueProblem } from "./constants.mts";
import { InputRefused, ValueRefused } from "./errors.mts";
import { OutputChannel, report } from "./output.mts";

type ReadHiddenValueInput = { readonly name: string };

type ReadHiddenValueError = InputRefused | ValueRefused;

type FinishTypedInput = { readonly typed: string };

type CheckLineInput = { readonly line: string };

type StopReadingInput = { readonly wasRaw: boolean };

type OnDataInput = { readonly chunk: Readonly<Buffer> };

/** The character a terminal in raw mode sends for Ctrl-C. */
const INTERRUPT = "\u0003";

/** Enter, as either line break. */
const LINE_BREAK = /[\r\n]/v;

function checkLine({ line }: CheckLineInput): Effect.Effect<string, ReadHiddenValueError> {
  return Effect.gen(function* () {
    if (line.includes(INTERRUPT)) {
      return yield* new InputRefused({ problem: InputProblem.Cancelled });
    }

    const value = applyErasures({ typed: line });

    if (Buffer.byteLength(value, "utf-8") > MAX_VALUE_BYTES) {
      return yield* new ValueRefused({ problem: ValueProblem.TooLarge });
    }

    return value;
  });
}

function finishTyped({
  typed,
}: FinishTypedInput): Option.Option<Effect.Effect<string, ReadHiddenValueError>> {
  const [line = ""] = typed.split(LINE_BREAK, 1);
  const pending = line === typed && !line.includes(INTERRUPT);

  if (pending && Buffer.byteLength(line, "utf-8") <= MAX_VALUE_BYTES) {
    return Option.none();
  }

  const checking = checkLine({ line });

  return Option.some(checking);
}

function stopReading({ wasRaw }: StopReadingInput): void {
  // The tool alone reads standard input, so these listeners are its own.
  process.stdin.removeAllListeners("data");
  process.stdin.removeAllListeners("end");
  process.stdin.setRawMode(wasRaw);
  process.stdin.pause();
  report({ channel: OutputChannel.Prompt, text: "\n" });
}

/** Prompts on the terminal with echo off and reads one line, so the value never appears on screen. */
export function readHiddenValue({
  name,
}: ReadHiddenValueInput): Effect.Effect<string, ReadHiddenValueError> {
  return Effect.callback<string, ReadHiddenValueError>((resume) => {
    const wasRaw = process.stdin.isRaw;
    let typed = "";

    function onData({ chunk }: OnDataInput): void {
      typed += chunk.toString("utf-8");
      const finished = finishTyped({ typed });

      if (Option.isNone(finished)) {
        return;
      }

      stopReading({ wasRaw });
      resume(finished.value);
    }

    function onEnd(): void {
      const ended = new InputRefused({ problem: InputProblem.Ended });

      stopReading({ wasRaw });
      resume(ended);
    }

    // Input can arrive as soon as the prompt appears, so turn echo off first.
    process.stdin.setRawMode(true);
    process.stdin.on("data", (chunk: Readonly<Buffer>) => {
      onData({ chunk });
    });
    process.stdin.on("end", () => {
      onEnd();
    });
    process.stdin.resume();
    report({ channel: OutputChannel.Prompt, text: `Value for ${name}: ` });

    return Effect.sync(() => {
      stopReading({ wasRaw });
    });
  });
}
