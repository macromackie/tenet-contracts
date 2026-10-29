/**
 * The tagged errors the env tool reports.
 *
 * The env tool's modules import it; it is not run directly.
 */
import { Schema } from "effect";
import {
  ArgumentsProblem,
  EnvFileProblem,
  FileOperation,
  InputProblem,
  ValueProblem,
} from "./constants.mts";

/** The arguments or the `--from-env` variable cannot run, such as a value passed as an argument. */
export class ArgumentsRefused extends Schema.TaggedError<ArgumentsRefused>()("ArgumentsRefused", {
  problem: Schema.Literals(Object.values(ArgumentsProblem)),
}) {}

/** The env file is not one the tool edits, or it changed while the tool edited it. */
export class EnvFileRefused extends Schema.TaggedError<EnvFileRefused>()("EnvFileRefused", {
  file: Schema.String,
  problem: Schema.Literals(Object.values(EnvFileProblem)),
}) {}

/** Reading, decoding, or replacing the env file failed. */
export class EnvFileFailed extends Schema.TaggedError<EnvFileFailed>()("EnvFileFailed", {
  cause: Schema.Unknown,
  file: Schema.String,
  operation: Schema.Literals(Object.values(FileOperation)),
}) {}

/** A line of the env file is neither blank, a comment, nor an assignment. */
export class EnvLineMalformed extends Schema.TaggedError<EnvLineMalformed>()("EnvLineMalformed", {
  file: Schema.String,
  line: Schema.Number,
}) {}

/** The env file assigns one key twice. */
export class EnvKeyDuplicate extends Schema.TaggedError<EnvKeyDuplicate>()("EnvKeyDuplicate", {
  file: Schema.String,
  name: Schema.String,
}) {}

/** Standard input ended without a value, such as at Ctrl-C. */
export class InputRefused extends Schema.TaggedError<InputRefused>()("InputRefused", {
  problem: Schema.Literals(Object.values(InputProblem)),
}) {}

/** Reading or decoding piped standard input failed. */
export class InputFailed extends Schema.TaggedError<InputFailed>()("InputFailed", {
  cause: Schema.Unknown,
  operation: Schema.Literals([FileOperation.Decode, FileOperation.Read]),
}) {}

/** The value is empty, too long, or more than one line. */
export class ValueRefused extends Schema.TaggedError<ValueRefused>()("ValueRefused", {
  problem: Schema.Literals(Object.values(ValueProblem)),
}) {}
