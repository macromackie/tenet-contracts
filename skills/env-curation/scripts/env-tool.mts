#!/usr/bin/env node
/**
 * Adds, replaces, or removes one key of a dotenv file without printing its value.
 *
 * Run `node env-tool.mts set FILE NAME [--from-env SOURCE_NAME]` or `node env-tool.mts clear FILE NAME`.
 * `set` reads the value from the named variable, a hidden terminal prompt, or one line of piped input.
 */
import { Effect } from "effect";
import { describeFailure } from "./describe-failure.mts";
import { editEnv } from "./edit-env.mts";
import { ExitStatus, OutputChannel, report } from "./output.mts";
import { readSettings } from "./settings.mts";

/** The line for a defect, which never repeats what the defect holds, since it may hold the value. */
const DEFECT_LINE = "could not edit the env file";

async function main(): Promise<void> {
  const editing = readSettings().pipe(
    Effect.flatMap((settings) => editEnv({ settings })),
    Effect.map((text) => {
      report({ channel: OutputChannel.Result, text });

      return ExitStatus.Done;
    }),
    Effect.catch((error) =>
      Effect.sync(() => {
        const text = describeFailure({ error });

        report({ channel: OutputChannel.Diagnostic, text });

        return ExitStatus.Failed;
      }),
    ),
    Effect.catchDefect(() =>
      Effect.sync(() => {
        report({ channel: OutputChannel.Diagnostic, text: DEFECT_LINE });

        return ExitStatus.Failed;
      }),
    ),
  );

  process.exitCode = await Effect.runPromise(editing);
}

await main();
