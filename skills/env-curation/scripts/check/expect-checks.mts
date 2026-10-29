/**
 * Fails the check at the first expected behavior that does not hold.
 *
 * `check-env-tool.mts` and its modules import it; it is not run directly.
 */
import { Effect } from "effect";
import { CheckFailed } from "./errors.mts";
import type { Expectation } from "./types.mts";

type ExpectChecksInput = { readonly checks: readonly Expectation[] };

/** Succeeds when every named behavior holds, and fails with the first one that does not. */
export function expectChecks({ checks }: ExpectChecksInput): Effect.Effect<void, CheckFailed> {
  return Effect.gen(function* () {
    const failed = checks.find((expectation) => !expectation.holds);

    if (failed !== undefined) {
      return yield* new CheckFailed({ check: failed.check });
    }
  });
}
