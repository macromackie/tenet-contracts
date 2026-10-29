import { Effect } from "effect";
import { RefundRefused } from "./errors.ts";

type RefundInvoiceInput = { readonly invoice: string; readonly status: number };

type RespondToRefusalInput = { readonly error: RefundRefused };

const ACCEPTED = 200;

const CONFLICT = 409;

function refundInvoice({
  invoice,
  status,
}: RefundInvoiceInput): Effect.Effect<Response, RefundRefused> {
  return Effect.gen(function* refundInvoiceSteps() {
    if (status !== ACCEPTED) {
      return yield* new RefundRefused({ invoice, status });
    }

    return new Response(invoice);
  });
}

function respondToRefusal({ error }: RespondToRefusalInput): Response {
  return new Response(error.invoice, { status: CONFLICT });
}

/** Answers one refund request, handling the provider's refusal by its tag. */
export async function handleRefund(request: Request): Promise<Response> {
  const url = new URL(request.url);
  const invoice = url.searchParams.get("invoice") ?? "";

  const refunding = refundInvoice({ invoice, status: ACCEPTED }).pipe(
    Effect.catchTag("RefundRefused", (error) => Effect.sync(() => respondToRefusal({ error }))),
  );

  return await Effect.runPromise(refunding);
}
