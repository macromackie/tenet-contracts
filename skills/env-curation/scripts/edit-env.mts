/**
 * Adds, replaces, or removes one key of an env file.
 *
 * The env tool's modules import it; it is not run directly.
 */
import { Effect, Option } from "effect";
import { EnvFileProblem, LF } from "./constants.mts";
import { describeValue } from "./describe-value.mts";
import { encodeAssignment } from "./encode-assignment.mts";
import {
  type EnvFileFailed,
  EnvFileRefused,
  type EnvKeyDuplicate,
  type EnvLineMalformed,
  type InputFailed,
  type InputRefused,
  type ValueRefused,
} from "./errors.mts";
import { readEnvFile } from "./read-env-file.mts";
import { readNewValue } from "./read-new-value.mts";
import type { EnvContents, Settings } from "./types.mts";
import { writeEnvFile } from "./write-env-file.mts";

type EditEnvInput = { readonly settings: Settings };

type PlaceAssignmentInput = {
  readonly assignment: string;
  readonly contents: EnvContents;
  readonly name: string;
};

type CloseLastLineInput = {
  readonly lines: readonly string[];
  readonly newline: string;
};

type ClearKeyInput = {
  readonly contents: EnvContents;
  readonly file: string;
  readonly name: string;
};

type EditEnvError =
  | EnvFileFailed
  | EnvFileRefused
  | EnvKeyDuplicate
  | EnvLineMalformed
  | InputFailed
  | InputRefused
  | ValueRefused;

function closeLastLine({ lines, newline }: CloseLastLineInput): readonly string[] {
  const lastIndex = lines.length - 1;
  const last = lines.at(lastIndex);

  if (last === undefined || last.endsWith(LF)) {
    return lines;
  }

  return lines.with(lastIndex, last + newline);
}

function placeAssignment({ assignment, contents, name }: PlaceAssignmentInput): readonly string[] {
  const { entries, lines, newline } = contents;
  const found = entries.get(name);
  const entry = Option.fromNullishOr(found);

  if (Option.isSome(entry)) {
    return lines.with(entry.value.index, assignment + entry.value.ending);
  }

  const closed = closeLastLine({ lines, newline });

  return [...closed, assignment + newline];
}

function clearKey({ contents, file, name }: ClearKeyInput): Effect.Effect<string, EditEnvError> {
  return Effect.gen(function* () {
    const found = contents.entries.get(name);
    const entry = Option.fromNullishOr(found);

    if (Option.isNone(entry)) {
      return yield* new EnvFileRefused({ file, problem: EnvFileProblem.KeyAbsent });
    }

    const lines = contents.lines.toSpliced(entry.value.index, 1);

    yield* writeEnvFile({ contents, file, lines });

    return `${name} removed from ${file}`;
  });
}

/** Adds, replaces, or removes one key in the env file, and returns the line that reports it. */
export function editEnv({ settings }: EditEnvInput): Effect.Effect<string, EditEnvError> {
  return Effect.gen(function* () {
    const { file, name } = settings;
    const contents = yield* readEnvFile({ file });

    if (settings.command === "clear") {
      return yield* clearKey({ contents, file, name });
    }

    const value = yield* readNewValue({ name, source: settings.source });
    const assignment = encodeAssignment({ name, value });
    const lines = placeAssignment({ assignment, contents, name });
    const status = describeValue({ value });

    yield* writeEnvFile({ contents, file, lines });

    return `${name} ${status}`;
  });
}
