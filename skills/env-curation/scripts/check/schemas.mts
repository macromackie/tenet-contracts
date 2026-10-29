/**
 * The schema of the environment that mise prints as JSON.
 *
 * `check-env-tool.mts` and its modules import it; it is not run directly.
 */
import { Schema } from "effect";

/** The variables `mise env --json` prints, each name with its value. */
export const MiseEnvironment = Schema.Record(Schema.String, Schema.String);

/** Decodes the JSON text that `mise env --json` prints. */
export const decodeMiseEnvironment = Schema.decodeUnknownEffect(
  Schema.fromJsonString(MiseEnvironment),
  {
    onExcessProperty: "error",
  },
);
