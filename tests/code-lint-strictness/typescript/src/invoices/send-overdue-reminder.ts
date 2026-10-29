import { Option } from "effect";
import type { Invoice } from "./schemas.ts";

type FindOverdueInvoiceInput = { readonly invoices: readonly Invoice[] };

type IsOverdueInput = { readonly invoice: Invoice };

type NotifyInput = { readonly invoice: string; readonly text: string; readonly channel?: string };

type NotifyAccountInput = {
  readonly channel: Option.Option<string>;
  readonly invoice: string;
  readonly note: Option.Option<string>;
  readonly notify: (request: NotifyInput) => void;
};

type RecordQuietRunInput = { readonly account: string };

type SendOverdueReminderInput = {
  readonly account: string;
  readonly channel: Option.Option<string>;
  readonly invoices: readonly Invoice[];
  readonly notify: (request: NotifyInput) => void;
  readonly recordQuietRun: (input: RecordQuietRunInput) => void;
};

function isOverdue({ invoice }: IsOverdueInput): boolean {
  return invoice.total > 0;
}

function findOverdueInvoice({ invoices }: FindOverdueInvoiceInput): Option.Option<Invoice> {
  const found = invoices.find((invoice) => isOverdue({ invoice }));

  return Option.fromNullishOr(found);
}

function notifyAccount({ channel, invoice, note, notify }: NotifyAccountInput): void {
  const text = Option.getOrElse(note, () => "");

  const request: NotifyInput = {
    invoice,
    text,
    ...(Option.isSome(channel) && { channel: channel.value }),
  };

  notify(request);
}

/** Sends a reminder for an account's first overdue invoice, or records a quiet run when it has none. */
export function sendOverdueReminder({
  account,
  channel,
  invoices,
  notify,
  recordQuietRun,
}: SendOverdueReminderInput): void {
  const found = findOverdueInvoice({ invoices });

  if (Option.isNone(found)) {
    recordQuietRun({ account });

    return;
  }

  notifyAccount({ channel, invoice: found.value.id, note: found.value.note, notify });
}
