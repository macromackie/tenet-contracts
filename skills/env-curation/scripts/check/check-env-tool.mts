#!/usr/bin/env node
/**
 * Checks the env tool end to end on a scratch env file with fake values.
 *
 * Run `node check/check-env-tool.mts` from the env tool's folder, or by its path from any folder, with mise on the path.
 * It sets a key from a variable and reads it back through mise, replaces it from piped input, clears it,
 * and confirms that a value passed as an argument and an empty value change nothing.
 */
import { Effect } from "effect";
import { completeAction } from "../complete-action.mts";
import { ExitStatus, OutputChannel, report } from "../output.mts";
import type { CheckFailed, StepFailed } from "./errors.mts";
import { runScenarios } from "./run-scenarios.mts";
import { readCheckSettings } from "./settings.mts";

type DescribeCheckFailureInput = { readonly error: CheckFailed | StepFailed };

/** The line for a defect, which never repeats what the defect holds. */
const DEFECT_LINE = "the check stopped on a defect";

/** The line for a run in which every check held. */
const PASS_LINE = "set, read back, replace, clear, and refusals pass";

function describeCheckFailure({ error }: DescribeCheckFailureInput): string {
  switch (error._tag) {
    case "CheckFailed": {
      return `check failed: ${error.check}`;
    }
    case "StepFailed": {
      return `step failed: ${error.step}`;
    }
  }
}

async function main(): Promise<void> {
  const settings = readCheckSettings();

  const checking = runScenarios({ settings }).pipe(
    Effect.map(() => {
      report({ channel: OutputChannel.Diagnostic, text: PASS_LINE });

      return ExitStatus.Done;
    }),
  );

  const completing = completeAction({
    action: checking,
    defectLine: DEFECT_LINE,
    describeFailure: describeCheckFailure,
  });

  process.exitCode = await Effect.runPromise(completing);
}

await main();
