import { Effect, pipe, Schedule } from "effect";
import { ProviderBusy } from "./errors.ts";
import { Account } from "./schemas.ts";

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
  return Effect.gen(function* buildTimeoutFailureSteps() {
    return yield* new ProviderBusy({ status: BUSY_STATUS });
  });
}

function readStoredAccount({ account }: ReadAccountInput): Effect.Effect<Account, ProviderBusy> {
  return Effect.sync(() => new Account({ id: account }));
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

/** Reads two accounts together. */
export const readAccountPair = Effect.fn("readAccountPair")(function* readAccountPairSteps({
  account,
}: ReadAccountInput) {
  const first = readStoredAccount({ account });
  const second = readStoredAccount({ account });
  const { left, right } = yield* Effect.all({ left: first, right: second });

  return [left, right] as const;
});
