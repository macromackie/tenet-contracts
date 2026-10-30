import { Effect, pipe, Schedule } from "effect";
import { ProviderBusy } from "./errors.ts";
import { readStoredAccount } from "./read-stored-account.ts";
import type { Account } from "./schemas.ts";

type ReadAccountInput = { readonly account: string };

const RETRY_ATTEMPTS = 3;

const BUSY_STATUS = 503;

const RETRY_DELAY = "200 millis";

const READ_DEADLINE = "5 seconds";

const retrySchedule = Schedule.spaced(RETRY_DELAY);

function isTransient(error: ProviderBusy): boolean {
  return error.status === BUSY_STATUS;
}

function buildTimeoutFailure(): Effect.Effect<never, ProviderBusy> {
  return Effect.gen(function* () {
    return yield* new ProviderBusy({ status: BUSY_STATUS });
  });
}

/** Reads one account, retrying a busy provider a few times within a deadline. */
export function readAccount({ account }: ReadAccountInput): Effect.Effect<Account, ProviderBusy> {
  const reading = readStoredAccount({ account });

  return pipe(
    reading,
    Effect.retry({ schedule: retrySchedule, times: RETRY_ATTEMPTS, while: isTransient }),
    Effect.timeoutOrElse({ duration: READ_DEADLINE, orElse: buildTimeoutFailure }),
    Effect.withSpan("account.read"),
  );
}
