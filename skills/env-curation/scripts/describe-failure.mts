/**
 * States why the env tool refused, without any value it read.
 *
 * The env tool's modules import it; it is not run directly.
 */
import {
  ARGUMENTS_MESSAGES,
  ENV_FILE_MESSAGES,
  FILE_OPERATION_MESSAGES,
  INPUT_MESSAGES,
  VALUE_MESSAGES,
} from "./constants.mts";
import type {
  ArgumentsRefused,
  EnvFileFailed,
  EnvFileRefused,
  EnvKeyDuplicate,
  EnvLineMalformed,
  InputFailed,
  InputRefused,
  ValueRefused,
} from "./errors.mts";

type DescribeFailureInput = {
  readonly error:
    | ArgumentsRefused
    | EnvFileFailed
    | EnvFileRefused
    | EnvKeyDuplicate
    | EnvLineMalformed
    | InputFailed
    | InputRefused
    | ValueRefused;
};

/** States why the tool refused, without any value it read. */
export function describeFailure({ error }: DescribeFailureInput): string {
  switch (error._tag) {
    case "ArgumentsRefused": {
      return ARGUMENTS_MESSAGES[error.problem];
    }
    case "EnvFileFailed": {
      return `${error.file}: ${FILE_OPERATION_MESSAGES[error.operation]}`;
    }
    case "EnvFileRefused": {
      return `${error.file}: ${ENV_FILE_MESSAGES[error.problem]}`;
    }
    case "EnvKeyDuplicate": {
      return `${error.file}: assigns ${error.name} twice`;
    }
    case "EnvLineMalformed": {
      return `${error.file}: line ${String(error.line)} is not an assignment`;
    }
    case "InputFailed": {
      return `input ${FILE_OPERATION_MESSAGES[error.operation]}`;
    }
    case "InputRefused": {
      return INPUT_MESSAGES[error.problem];
    }
    case "ValueRefused": {
      return VALUE_MESSAGES[error.problem];
    }
  }
}
