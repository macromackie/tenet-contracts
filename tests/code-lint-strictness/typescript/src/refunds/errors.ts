import { Schema } from "effect";

/** The provider refused a refund, with the status it returned. */
export class RefundRefused extends Schema.TaggedError<RefundRefused>()("RefundRefused", {
  invoice: Schema.String,
  status: Schema.Number,
}) {}
