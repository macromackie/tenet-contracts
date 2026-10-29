/**
 * The tagged errors of the env tool's check.
 *
 * `check-env-tool.mts` and its modules import it; it is not run directly.
 */
import { Schema } from "effect";

/** One behavior the check expects did not hold. */
export class CheckFailed extends Schema.TaggedError<CheckFailed>()("CheckFailed", {
  check: Schema.String,
}) {}

/** A step that sets up or observes a check failed, such as starting a command or reading a file. */
export class StepFailed extends Schema.TaggedError<StepFailed>()("StepFailed", {
  cause: Schema.Unknown,
  step: Schema.String,
}) {}
