import { type Cause, Context, Effect, Option } from "effect";
import { INVOICE_URL, READ_DEADLINE } from "./constants.ts";
import { InvoiceNotFound, ProviderReplyInvalid, RequestDropped } from "./errors.ts";
import { decodeInvoice, type Invoice } from "./schemas.ts";

type InvoiceStoreShape = {
  readonly findInvoice: (input: FindInvoiceInput) => Effect.Effect<Option.Option<Invoice>>;
  readonly sendReminder: (input: SendReminderInput) => Effect.Effect<void, RequestDropped>;
};

type FindInvoiceInput = { readonly invoice: string };

type SendReminderInput = { readonly invoice: Invoice };

type ReadInvoiceInput = { readonly invoice: string };

type ReadProviderInvoiceInput = {
  readonly invoice: string;
  readonly signal: Readonly<AbortSignal>;
};

/** The store that holds this service's invoices. */
export class InvoiceStore extends Context.Service<InvoiceStore, InvoiceStoreShape>()(
  "InvoiceStore",
) {}

async function readProviderInvoice({
  invoice,
  signal,
}: ReadProviderInvoiceInput): Promise<unknown> {
  const response = await fetch(`${INVOICE_URL}/${invoice}`, { signal });

  return await response.json();
}

function buildRequestDropped(cause: unknown): RequestDropped {
  return new RequestDropped({ cause });
}

/** Reads one invoice from the provider by the number a caller supplied. */
export function readInvoice({
  invoice,
}: ReadInvoiceInput): Effect.Effect<
  Invoice,
  Cause.TimeoutError | InvoiceNotFound | ProviderReplyInvalid | RequestDropped,
  InvoiceStore
> {
  return Effect.gen(function* () {
    const store = yield* InvoiceStore;
    const found = yield* store.findInvoice({ invoice });

    if (Option.isNone(found)) {
      return yield* new InvoiceNotFound({ invoice });
    }

    async function readBody(signal: Readonly<AbortSignal>): Promise<unknown> {
      return await readProviderInvoice({ invoice, signal });
    }

    const body = yield* Effect.tryPromise({ catch: buildRequestDropped, try: readBody }).pipe(
      Effect.timeout(READ_DEADLINE),
      Effect.withSpan("invoice.read"),
    );

    return yield* decodeInvoice(body).pipe(
      Effect.mapError((cause) => new ProviderReplyInvalid({ cause })),
    );
  });
}
