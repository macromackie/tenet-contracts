/**
 * Reads an env file and finds the line of each key it assigns.
 *
 * `edit-env.mts` imports it; it is not run directly.
 */
import { lstat, readFile } from "node:fs/promises";
import { TextDecoder } from "node:util";
import { Effect, Option } from "effect";
import {
  ASSIGNMENT_PATTERN,
  CRLF,
  EnvFileProblem,
  FileOperation,
  LF,
  LINE_ENDING,
  LINE_PATTERN,
} from "./constants.mts";
import { EnvFileFailed, EnvFileRefused, EnvKeyDuplicate, EnvLineMalformed } from "./errors.mts";
import type { EnvContents, EnvEntry } from "./types.mts";

type ReadEnvFileInput = { readonly file: string };

type IndexEntriesInput = {
  readonly file: string;
  readonly lines: readonly string[];
};

type ReadEntryInput = {
  readonly file: string;
  readonly index: number;
  readonly line: string;
};

type NamedEntry = {
  readonly entry: EnvEntry;
  readonly name: string;
};

type ChooseNewlineInput = { readonly original: Buffer };

type ReadEnvFileError = EnvFileFailed | EnvFileRefused | EnvKeyDuplicate | EnvLineMalformed;

function chooseNewline({ original }: ChooseNewlineInput): string {
  if (original.includes(CRLF)) {
    return CRLF;
  }

  return LF;
}

function readEntry({
  file,
  index,
  line,
}: ReadEntryInput): Effect.Effect<Option.Option<NamedEntry>, EnvLineMalformed> {
  return Effect.gen(function* () {
    const ending = LINE_ENDING.exec(line)?.[0] ?? "";
    const body = line.slice(0, line.length - ending.length);

    if (body.trim() === "" || body.trimStart().startsWith("#")) {
      return Option.none();
    }

    const match = ASSIGNMENT_PATTERN.exec(body);
    const name = Option.fromNullishOr(match?.groups?.["name"]);

    if (Option.isNone(name)) {
      return yield* new EnvLineMalformed({ file, line: index + 1 });
    }

    return Option.some({ entry: { ending, index }, name: name.value });
  });
}

function indexEntries({
  file,
  lines,
}: IndexEntriesInput): Effect.Effect<
  ReadonlyMap<string, EnvEntry>,
  EnvKeyDuplicate | EnvLineMalformed
> {
  return Effect.gen(function* () {
    const entries = new Map<string, EnvEntry>();

    for (const [index, line] of lines.entries()) {
      const read = yield* readEntry({ file, index, line });

      if (Option.isNone(read)) {
        continue;
      }

      if (entries.has(read.value.name)) {
        return yield* new EnvKeyDuplicate({ file, name: read.value.name });
      }

      entries.set(read.value.name, read.value.entry);
    }

    return entries;
  });
}

/** Reads a regular UTF-8 env file and finds the line of each key it assigns. */
export function readEnvFile({
  file,
}: ReadEnvFileInput): Effect.Effect<EnvContents, ReadEnvFileError> {
  return Effect.gen(function* () {
    const stats = yield* Effect.tryPromise(async () => await lstat(file)).pipe(
      Effect.mapError((cause) => new EnvFileFailed({ cause, file, operation: FileOperation.Read })),
    );

    if (!stats.isFile()) {
      return yield* new EnvFileRefused({ file, problem: EnvFileProblem.Irregular });
    }

    const original = yield* Effect.tryPromise(async () => await readFile(file)).pipe(
      Effect.mapError((cause) => new EnvFileFailed({ cause, file, operation: FileOperation.Read })),
    );

    const text = yield* Effect.try(() =>
      new TextDecoder("utf-8", { fatal: true }).decode(original),
    ).pipe(
      Effect.mapError(
        (cause) => new EnvFileFailed({ cause, file, operation: FileOperation.Decode }),
      ),
    );

    const lines = text.match(LINE_PATTERN) ?? [];
    const entries = yield* indexEntries({ file, lines });
    const newline = chooseNewline({ original });

    return { entries, lines, newline, original };
  });
}
