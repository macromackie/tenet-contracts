import type { Option } from "effect";
import type { Invoice } from "./schemas.ts";

type ReplaceInvoiceInput = {
  readonly id: string;
  readonly note: Option.Option<string>;
  readonly previous: Option.Option<string>;
};

/** Builds the invoice that replaces a previous one, with nothing due yet. */
export function replaceInvoice({ id, note, previous }: ReplaceInvoiceInput): Invoice {
  return { id, note, replaces: previous, total: 0 };
}
