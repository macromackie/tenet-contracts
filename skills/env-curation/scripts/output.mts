/**
 * The env tool's output module, the one file that writes the standard streams.
 *
 * `env-tool.mts` and `check-env-tool.mts` import it; it is not run directly.
 */

/** The statuses the env tool and its check end with. */
export const ExitStatus = {
  Done: 0,
  Failed: 1,
} as const;

/** One status the env tool and its check end with. */
export type ExitStatus = (typeof ExitStatus)[keyof typeof ExitStatus];

/** What a line written to the standard streams is. */
export const OutputChannel = {
  Diagnostic: "diagnostic",
  Prompt: "prompt",
  Result: "result",
} as const;

/** One kind of line written to the standard streams. */
export type OutputChannel = (typeof OutputChannel)[keyof typeof OutputChannel];

type ReportInput = {
  readonly channel: OutputChannel;
  readonly text: string;
};

/**
 * Writes the result, the key and what changed, to standard output, and every other line to standard error.
 *
 * A prompt is written as given, so its answer follows on the same line; every other text ends its own line.
 */
export function report({ channel, text }: ReportInput): void {
  switch (channel) {
    case OutputChannel.Result: {
      process.stdout.write(`${text}\n`);

      return;
    }
    case OutputChannel.Prompt: {
      process.stderr.write(text);

      return;
    }
    case OutputChannel.Diagnostic: {
      process.stderr.write(`env tool: ${text}\n`);
    }
  }
}
