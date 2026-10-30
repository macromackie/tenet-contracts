import { Effect } from "effect";
import { readStoredAccount } from "./read-stored-account.ts";

type ReadAccountPairInput = { readonly account: string };

/** Reads two accounts together. */
export const readAccountPair = Effect.fn("account.read_pair")(function* ({
  account,
}: ReadAccountPairInput) {
  const first = readStoredAccount({ account });
  const second = readStoredAccount({ account });
  const { left, right } = yield* Effect.all({ left: first, right: second });

  return [left, right] as const;
});
