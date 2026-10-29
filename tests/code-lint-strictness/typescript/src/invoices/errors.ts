import { Schema } from "effect";

/** A caller asked for an invoice number that no stored invoice carries. */
export class InvoiceNotFound extends Schema.TaggedError<InvoiceNotFound>()("InvoiceNotFound", {
  invoice: Schema.String,
}) {}

/** The provider's request failed before it returned a response. */
export class RequestDropped extends Schema.TaggedError<RequestDropped>()("RequestDropped", {
  cause: Schema.Unknown,
}) {}

/** A row that the same store wrote is missing, so the store's invariant broke. */
export class InvoiceMissing extends Schema.TaggedError<InvoiceMissing>()("InvoiceMissing", {
  invoice: Schema.String,
}) {}

/** The provider returned a body that the invoice schema rejects. */
export class ProviderReplyInvalid extends Schema.TaggedError<ProviderReplyInvalid>()(
  "ProviderReplyInvalid",
  {
    cause: Schema.Unknown,
  },
) {}
