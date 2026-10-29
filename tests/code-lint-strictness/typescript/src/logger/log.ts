import { Effect } from "effect";

/** The closed set of events this service logs. */
export const LogEvent = {
  InvoiceRead: "invoice.read",
  InvoiceReadFailed: "invoice.read_failed",
} as const;

/** One event this service logs. */
export type LogEvent = (typeof LogEvent)[keyof typeof LogEvent];

type LogInput = {
  readonly event: LogEvent;
  readonly error?: readonly string[];
  readonly invoice?: string;
};

/** Writes one log line as one JSON object through Effect's logger. */
export function log({ event, ...fields }: LogInput): Effect.Effect<void> {
  return Effect.logInfo(event).pipe(Effect.annotateLogs(fields));
}
