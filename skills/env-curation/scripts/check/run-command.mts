/**
 * Runs one command with a given environment and standard input, and collects what it printed.
 *
 * `check-env-tool.mts` and its modules import it; it is not run directly.
 */
import { spawn } from "node:child_process";
import { once } from "node:events";
import { text } from "node:stream/consumers";
import { Effect, Option } from "effect";
import { StepFailed } from "./errors.mts";
import type { CommandRun } from "./types.mts";

type RunCommandInput = {
  readonly args: readonly string[];
  readonly command: string;
  readonly environment: Readonly<Record<string, string>>;
  readonly input: string;
};

/** Runs the command to its end; starting it or reading its output failing fails the step. */
export function runCommand({
  args,
  command,
  environment,
  input,
}: RunCommandInput): Effect.Effect<CommandRun, StepFailed> {
  const step = `run ${command} ${args.join(" ")}`;

  return Effect.gen(function* () {
    const child = yield* Effect.try(() =>
      spawn(command, args, { env: environment, stdio: "pipe" }),
    ).pipe(Effect.mapError((cause) => new StepFailed({ cause, step })));

    child.stdin.end(input);

    const printing = Effect.tryPromise(async () => await text(child.stdout));
    const warning = Effect.tryPromise(async () => await text(child.stderr));

    const closing = Effect.tryPromise(async (): Promise<void> => {
      await once(child, "close");
    });

    const [stdout, stderr] = yield* Effect.all([printing, warning, closing], {
      concurrency: "unbounded",
    }).pipe(Effect.mapError((cause) => new StepFailed({ cause, step })));

    const status = Option.fromNullishOr(child.exitCode);

    return { status, stderr, stdout };
  });
}
