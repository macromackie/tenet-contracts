import { Effect, Option } from "effect";
import { InvoiceMissing } from "./errors.ts";
import { InvoiceStore } from "./invoices.ts";
import type { Invoice } from "./schemas.ts";

type ReadSavedInvoiceInput = { readonly invoice: string };

/** Reads back an invoice that this store wrote, so a missing row is a defect. */
export function readSavedInvoice({
  invoice,
}: ReadSavedInvoiceInput): Effect.Effect<Invoice, never, InvoiceStore> {
  return Effect.gen(function* () {
    const store = yield* InvoiceStore;
    const found = yield* store.findInvoice({ invoice });

    if (Option.isNone(found)) {
      throw new InvoiceMissing({ invoice });
    }

    return found.value;
  });
}
