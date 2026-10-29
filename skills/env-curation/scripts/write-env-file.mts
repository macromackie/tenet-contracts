/**
 * Replaces an env file through a synced temporary file beside it and one rename.
 *
 * `edit-env.mts` imports it; it is not run directly.
 */
import { randomBytes } from "node:crypto";
import { open, readFile, rename, rm } from "node:fs/promises";
import { basename, dirname, join } from "node:path";
import { Effect } from "effect";
import { EnvFileProblem, FileOperation, OWNER_ONLY_MODE } from "./constants.mts";
import { EnvFileFailed, EnvFileRefused } from "./errors.mts";
import type { EnvContents } from "./types.mts";

type WriteEnvFileInput = {
  readonly contents: EnvContents;
  readonly file: string;
  readonly lines: readonly string[];
};

type ConfirmUnchangedInput = {
  readonly contents: EnvContents;
  readonly file: string;
};

type WriteTemporaryInput = {
  readonly file: string;
  readonly lines: readonly string[];
  readonly temporary: string;
};

/** The random bytes that make a temporary file's name unique beside the env file. */
const TEMPORARY_NAME_BYTES = 8;

function confirmUnchanged({
  contents,
  file,
}: ConfirmUnchangedInput): Effect.Effect<void, EnvFileFailed | EnvFileRefused> {
  return Effect.gen(function* () {
    const current = yield* Effect.tryPromise(async () => await readFile(file)).pipe(
      Effect.mapError((cause) => new EnvFileFailed({ cause, file, operation: FileOperation.Read })),
    );

    if (!current.equals(contents.original)) {
      return yield* new EnvFileRefused({ file, problem: EnvFileProblem.Changed });
    }
  });
}

function writeTemporary({
  file,
  lines,
  temporary,
}: WriteTemporaryInput): Effect.Effect<void, EnvFileFailed> {
  // The `wx` flag refuses a path that already exists, so the file is new and only the owner reads it.
  const opening = Effect.tryPromise(async () => await open(temporary, "wx", OWNER_ONLY_MODE)).pipe(
    Effect.mapError((cause) => new EnvFileFailed({ cause, file, operation: FileOperation.Write })),
  );

  const text = lines.join("");

  return Effect.gen(function* () {
    const handle = yield* Effect.acquireRelease(opening, (opened) =>
      Effect.promise(async () => {
        await opened.close();
      }),
    );

    yield* Effect.tryPromise(async () => {
      await handle.writeFile(text, { encoding: "utf-8" });
      await handle.sync();
    }).pipe(
      Effect.mapError(
        (cause) => new EnvFileFailed({ cause, file, operation: FileOperation.Write }),
      ),
    );
  }).pipe(Effect.scoped);
}

/** Replaces the env file with the given lines, refusing when another writer changed it meanwhile. */
export function writeEnvFile({
  contents,
  file,
  lines,
}: WriteEnvFileInput): Effect.Effect<void, EnvFileFailed | EnvFileRefused> {
  const suffix = randomBytes(TEMPORARY_NAME_BYTES).toString("hex");
  const folder = dirname(file);
  const name = basename(file);
  const pid = String(process.pid);
  const temporary = join(folder, `${name}.${pid}.${suffix}`);

  // Removing the temporary file after the rename finds nothing, so `force` keeps the release from failing.
  const reserving = Effect.acquireRelease(Effect.void, () =>
    Effect.promise(async () => {
      await rm(temporary, { force: true });
    }),
  );

  return Effect.gen(function* () {
    yield* confirmUnchanged({ contents, file });
    yield* reserving;
    yield* writeTemporary({ file, lines, temporary });
    yield* confirmUnchanged({ contents, file });
    yield* Effect.tryPromise(async () => {
      await rename(temporary, file);
    }).pipe(
      Effect.mapError(
        (cause) => new EnvFileFailed({ cause, file, operation: FileOperation.Write }),
      ),
    );
  }).pipe(Effect.scoped);
}
