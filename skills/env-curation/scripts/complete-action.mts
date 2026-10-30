/** Maps a command's declared failures and defects to value-free diagnostics and exit status. */
import { Effect } from "effect";
import { ExitStatus, OutputChannel, report } from "./output.mts";

type DescribeActionFailureInput<Failure> = { readonly error: Failure };

type CompleteActionInput<Failure> = {
  readonly action: Effect.Effect<ExitStatus, Failure>;
  readonly defectLine: string;
  readonly describeFailure: (input: DescribeActionFailureInput<Failure>) => string;
};

/** Completes an action without exposing a failure's raw value. */
export function completeAction<Failure>({
  action,
  defectLine,
  describeFailure,
}: CompleteActionInput<Failure>): Effect.Effect<ExitStatus> {
  return action.pipe(
    Effect.catch((error) =>
      Effect.sync(() => {
        const text = describeFailure({ error });

        report({ channel: OutputChannel.Diagnostic, text });

        return ExitStatus.Failed;
      }),
    ),
    Effect.catchDefect(() =>
      Effect.sync(() => {
        report({ channel: OutputChannel.Diagnostic, text: defectLine });

        return ExitStatus.Failed;
      }),
    ),
  );
}
