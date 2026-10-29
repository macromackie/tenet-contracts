import { type Cause, Effect, Layer, Logger, Option } from "effect";
import {
  type Invoice,
  type InvoiceNotFound,
  InvoiceStore,
  type ProviderReplyInvalid,
  readInvoice,
  type RequestDropped,
} from "./invoices/index.ts";
import { log, LogEvent } from "./logger/index.ts";

type RespondToFailureInput = {
  readonly error: Cause.TimeoutError | InvoiceNotFound | ProviderReplyInvalid | RequestDropped;
};

type RespondToDefectInput = { readonly defect: unknown };

const DEFECT_BODY = "internal error";

type FindStoredInvoiceInput = { readonly invoice: string };

type SendStoredReminderInput = { readonly invoice: Invoice };

const NOT_FOUND = 404;

const BAD_GATEWAY = 502;

const SERVICE_UNAVAILABLE = 503;

const INTERNAL_ERROR = 500;

const storedInvoices: ReadonlyMap<string, Invoice> = new Map<string, Invoice>();

function respondToFailure({ error }: RespondToFailureInput): Response {
  switch (error._tag) {
    case "InvoiceNotFound": {
      return new Response(error.invoice, { status: NOT_FOUND });
    }
    case "ProviderReplyInvalid": {
      return new Response("provider reply invalid", { status: BAD_GATEWAY });
    }
    case "TimeoutError": {
      return new Response("timed out", { status: SERVICE_UNAVAILABLE });
    }
    case "RequestDropped": {
      return new Response("retry", { status: SERVICE_UNAVAILABLE });
    }
  }
}

type RespondWithInvoiceInput = { readonly found: Invoice };

function respondWithInvoice({ found }: RespondWithInvoiceInput): Response {
  return Response.json(found);
}

function respondToDefect({ defect }: RespondToDefectInput): Response {
  void defect;

  return new Response(DEFECT_BODY, { status: INTERNAL_ERROR });
}

function findStoredInvoice({
  invoice,
}: FindStoredInvoiceInput): Effect.Effect<Option.Option<Invoice>> {
  return Effect.sync(() => {
    const found = storedInvoices.get(invoice);

    return Option.fromNullishOr(found);
  });
}

function sendStoredReminder({ invoice }: SendStoredReminderInput): Effect.Effect<void> {
  return log({ event: LogEvent.InvoiceRead, invoice: invoice.id });
}

const storeLayer = Layer.succeed(InvoiceStore, {
  findInvoice: findStoredInvoice,
  sendReminder: sendStoredReminder,
});

const loggerLayer = Logger.layer([Logger.consoleJson]);

const appLayer = Layer.mergeAll(storeLayer, loggerLayer);

/** Answers one invoice request; the runtime calls it for each request. */
export async function handleRequest(request: Request): Promise<Response> {
  const url = new URL(request.url);
  const invoice = url.searchParams.get("invoice") ?? "";

  const reading = readInvoice({ invoice }).pipe(
    Effect.map((found) => respondWithInvoice({ found })),
    Effect.catch((error) => Effect.sync(() => respondToFailure({ error }))),
    Effect.catchDefect((defect) => Effect.sync(() => respondToDefect({ defect }))),
    Effect.provide(appLayer),
  );

  return await Effect.runPromise(reading);
}
