/**
 * The check's settings module, which picks the variables its commands inherit.
 *
 * `check-env-tool.mts` imports it; it is not run directly.
 */
import { fileURLToPath } from "node:url";
import type { CheckSettings } from "./types.mts";

/** The env tool that the check runs, beside this folder. */
const TOOL_URL = new URL("../env-tool.mts", import.meta.url);

/** The env tool's path. */
const TOOL = fileURLToPath(TOOL_URL);

/** Reads the parent variables each command inherits: `PATH` finds mise, and mise reads its state under `HOME`. */
export function readCheckSettings(): CheckSettings {
  const environment = { HOME: process.env["HOME"] ?? "", PATH: process.env["PATH"] ?? "" };

  return { environment, tool: TOOL };
}
