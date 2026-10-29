import { Schema } from "effect";

/** The provider refused an account read for now, with the status it returned. */
export class ProviderBusy extends Schema.TaggedError<ProviderBusy>()("ProviderBusy", {
  status: Schema.Number,
}) {}
