/**
 * The types the env tool's check modules share.
 *
 * `check-env-tool.mts` and its modules import it; it is not run directly.
 */
import type { Option } from "effect";

/** What one finished command printed and the status it ended with. */
export type CommandRun = {
  readonly status: Option.Option<number>;
  readonly stderr: string;
  readonly stdout: string;
};

/** The decoded settings of one check run. */
export type CheckSettings = {
  readonly environment: Readonly<Record<string, string>>;
  readonly tool: string;
};

/** The scratch folder of one check run and the env file inside it. */
export type Fixture = {
  readonly folder: string;
  readonly file: string;
};

/** One behavior the check expects, and whether it held. */
export type Expectation = {
  readonly check: string;
  readonly holds: boolean;
};
