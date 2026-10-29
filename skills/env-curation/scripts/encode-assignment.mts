/**
 * Writes one dotenv assignment with a double-quoted value.
 *
 * The env tool's modules import it; it is not run directly.
 */
type EncodeAssignmentInput = {
  readonly name: string;
  readonly value: string;
};

/** Writes `NAME="value"`, escaping the backslashes, quotes, and dollar signs a dotenv reader expands. */
export function encodeAssignment({ name, value }: EncodeAssignmentInput): string {
  const escaped = value.replaceAll(/[\\"$]/gv, String.raw`\$&`);

  return `${name}="${escaped}"`;
}
