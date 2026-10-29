/**
 * The env tool's patterns, limits, closed sets, and messages.
 *
 * The env tool's modules import it; it is not run directly.
 */
/** A key name: ASCII letters, digits, and underscores, never starting with a digit. */
export const KEY_PATTERN = /^[A-Za-z_][A-Za-z0-9_]*$/v;

/** An assignment line, whose `name` group is the key name. */
export const ASSIGNMENT_PATTERN = /^(?<name>[A-Za-z_][A-Za-z0-9_]*)=.*$/v;

/** Each line of a file, with its line ending, and a last line without one. */
export const LINE_PATTERN = /[^\n]*\n|[^\n]+$/gv;

/** The line break that ends a line, if it has one. */
export const LINE_ENDING = /\r?\n$/v;

/** The line break that a file written on Windows uses. */
export const CRLF = "\r\n";

/** The line break of every other file. */
export const LF = "\n";

/** The longest value the tool writes: 64 KiB of UTF-8. */
export const MAX_VALUE_BYTES = 65_536;

/** The permissions of a file that only its owner reads and writes. */
export const OWNER_ONLY_MODE = 0o600;

/** The shortest value whose last four characters the tool shows. */
export const SUFFIX_MIN_LENGTH = 12;

/** How many of a value's last characters the tool shows. */
export const SUFFIX_LENGTH = 4;

/** The ways a run's arguments or `--from-env` variable can be refused. */
export const ArgumentsProblem = {
  ClearShape: "clear-shape",
  CommandUnknown: "command-unknown",
  KeyName: "key-name",
  SetShape: "set-shape",
  SourceName: "source-name",
  SourceUnset: "source-unset",
} as const;

/** One way a run's arguments can be refused. */
export type ArgumentsProblem = (typeof ArgumentsProblem)[keyof typeof ArgumentsProblem];

/** The ways an env file that was read can be refused. */
export const EnvFileProblem = {
  Changed: "changed",
  Irregular: "irregular",
  KeyAbsent: "key-absent",
} as const;

/** One way an env file can be refused. */
export type EnvFileProblem = (typeof EnvFileProblem)[keyof typeof EnvFileProblem];

/** The file operations whose failure the tool reports. */
export const FileOperation = {
  Decode: "decode",
  Read: "read",
  Write: "write",
} as const;

/** One file operation whose failure the tool reports. */
export type FileOperation = (typeof FileOperation)[keyof typeof FileOperation];

/** The ways standard input can end without a value. */
export const InputProblem = {
  Cancelled: "cancelled",
  Ended: "ended",
  TerminalMissing: "terminal-missing",
} as const;

/** One way standard input can end without a value. */
export type InputProblem = (typeof InputProblem)[keyof typeof InputProblem];

/** The ways a value can be refused. */
export const ValueProblem = {
  ControlCharacters: "control-characters",
  Empty: "empty",
  TooLarge: "too-large",
} as const;

/** One way a value can be refused. */
export type ValueProblem = (typeof ValueProblem)[keyof typeof ValueProblem];

/** What the tool says for each refused argument. */
export const ARGUMENTS_MESSAGES: Readonly<Record<ArgumentsProblem, string>> = {
  "clear-shape": "invalid arguments; use clear FILE NAME",
  "command-unknown": "invalid command; use set or clear",
  "key-name":
    "key name must contain ASCII letters, digits, and underscores and cannot start with a digit",
  "set-shape": "invalid arguments; use set FILE NAME [--from-env SOURCE_NAME]",
  "source-name": "source environment variable name is invalid",
  "source-unset": "source environment variable is not set",
};

/** What the tool says after the file's path for each refused env file. */
export const ENV_FILE_MESSAGES: Readonly<Record<EnvFileProblem, string>> = {
  changed: "changed during the edit; retry",
  irregular: "must be a regular file",
  "key-absent": "does not hold the key",
};

/** What the tool says after the file's path for each failed file operation. */
export const FILE_OPERATION_MESSAGES: Readonly<Record<FileOperation, string>> = {
  decode: "must be UTF-8",
  read: "could not be read",
  write: "could not be written",
};

/** What the tool says for each way input ended without a value. */
export const INPUT_MESSAGES: Readonly<Record<InputProblem, string>> = {
  cancelled: "input cancelled",
  ended: "input ended before a value was entered",
  "terminal-missing": "interactive input requires a terminal",
};

/** What the tool says for each refused value. */
export const VALUE_MESSAGES: Readonly<Record<ValueProblem, string>> = {
  "control-characters": "value must be one line without control characters",
  empty: "empty value; use clear to remove a key",
  "too-large": "value exceeds 64 KiB",
};
