/**
 * The types the env tool's modules share.
 *
 * The env tool's modules import it; it is not run directly.
 */
import type { Option } from "effect";

/** Where one key's assignment sits in an env file. */
export type EnvEntry = {
  readonly ending: string;
  readonly index: number;
};

/** An env file as read, with the entry of each key. */
export type EnvContents = {
  readonly entries: ReadonlyMap<string, EnvEntry>;
  readonly lines: readonly string[];
  readonly newline: string;
  readonly original: Buffer;
};

/** A request to add or replace one key, with the value of `--from-env` when it was given. */
type SetSettings = {
  readonly command: "set";
  readonly file: string;
  readonly name: string;
  readonly source: Option.Option<string>;
};

/** A request to remove one key. */
type ClearSettings = {
  readonly command: "clear";
  readonly file: string;
  readonly name: string;
};

/** The decoded arguments and environment of one run. */
export type Settings = SetSettings | ClearSettings;
