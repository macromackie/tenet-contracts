import { Schema } from "effect";

/** One stored invoice. */
export const Invoice = Schema.Struct({
  id: Schema.String,
  note: Schema.OptionFromNullOr(Schema.String),
  replaces: Schema.OptionFromOptionalKey(Schema.String),
  total: Schema.Number,
});

/** One stored invoice. */
export type Invoice = typeof Invoice.Type;

/** A provider webhook that this repository reads in part. */
export const ProviderEvent = Schema.StructWithRest(Schema.Struct({ type: Schema.String }), [
  Schema.Record(Schema.String, Schema.Unknown),
]);

/** A provider webhook that this repository reads in part. */
export type ProviderEvent = typeof ProviderEvent.Type;

/** Decodes a stored invoice and rejects unknown fields. */
export const decodeInvoice = Schema.decodeUnknownEffect(Invoice, { onExcessProperty: "error" });

/** Decodes a provider webhook and rejects fields outside its declared rest. */
export const decodeProviderEvent = Schema.decodeUnknownEffect(ProviderEvent, {
  onExcessProperty: "error",
});
