import { Effect } from "effect";
import { REMINDER_CONCURRENCY } from "./constants.ts";
import { InvoiceStore } from "./invoices.ts";
import type { Invoice } from "./schemas.ts";

type SendInvoiceRemindersInput = { readonly invoices: readonly Invoice[] };

/** Sends one reminder for each overdue invoice, a few at a time. */
export const sendInvoiceReminders = Effect.fn("invoice.send_reminders")(function* ({
  invoices,
}: SendInvoiceRemindersInput) {
  const store = yield* InvoiceStore;

  yield* Effect.forEach(invoices, (invoice) => store.sendReminder({ invoice }), {
    concurrency: REMINDER_CONCURRENCY,
  });

  yield* Effect.annotateCurrentSpan({ reminders: invoices.length });
});
