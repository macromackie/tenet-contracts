import { Effect } from "effect";
import type { ProviderBusy } from "./errors.ts";
import { Account } from "./schemas.ts";

type ReadStoredAccountInput = { readonly account: string };

/** Reads an account from its stored identity. */
export function readStoredAccount({
  account,
}: ReadStoredAccountInput): Effect.Effect<Account, ProviderBusy> {
  return Effect.sync(() => new Account({ id: account }));
}
