import { type Cause, Effect, Schedule } from "effect";
import { POLL_INTERVAL, SETTLEMENT_DEADLINE } from "./constants.ts";
import type { InvoiceNotFound, ProviderReplyInvalid, RequestDropped } from "./errors.ts";
import { type InvoiceStore, readInvoice } from "./invoices.ts";
import type { Invoice } from "./schemas.ts";

type AwaitSettlementInput = { readonly invoice: string };

const pollSchedule = Schedule.spaced(POLL_INTERVAL);

function isSettled(invoice: Invoice): boolean {
  return invoice.total === 0;
}

/** Polls one invoice until the provider settles it, within a deadline. */
export function awaitSettlement({
  invoice,
}: AwaitSettlementInput): Effect.Effect<
  Invoice,
  Cause.TimeoutError | InvoiceNotFound | ProviderReplyInvalid | RequestDropped,
  InvoiceStore
> {
  const reading = readInvoice({ invoice });

  return reading.pipe(
    Effect.repeat({ schedule: pollSchedule, until: isSettled }),
    Effect.timeout(SETTLEMENT_DEADLINE),
  );
}
