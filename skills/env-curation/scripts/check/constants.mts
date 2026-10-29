/**
 * The fake values and file contents that the env tool's check writes.
 *
 * `check-env-tool.mts` and its modules import it; it is not run directly.
 */

/** A fake value with every character a dotenv reader could expand or end a value at. */
export const TRICKY_VALUE = String.raw`a'\"$b # &-1234`;

/** A fake value that replaces the first through piped input. */
export const REPLACEMENT_VALUE = "replacement-fake-5678";

/** A fake value passed by mistake as an argument, which the tool must refuse without printing. */
export const ACCIDENTAL_VALUE = "unexpected-fake-7890";

/** The env file the check starts from, whose lines every edit keeps. */
export const ORIGINAL_ENV = '# keep this comment\nEXISTING="untouched-token-4567"\n';

/** The mise configuration that loads the env file, so that mise reads back what the tool wrote. */
export const MISE_CONFIG = '[env]\n_.file = ".env"\n';

/** The key the check adds, replaces, and removes. */
export const PROBE_KEY = "PROBE";

/** The variable that holds the tricky value for `--from-env`. */
export const SOURCE_KEY = "SOURCE_PROBE";

/** The permissions of a file that only its owner reads and writes. */
export const OWNER_ONLY_MODE = 0o600;

/** The divisor that keeps a file mode's permission bits. */
export const PERMISSION_BITS = 0o1000;

/** The status of a command that succeeded. */
export const SUCCESS = 0;
