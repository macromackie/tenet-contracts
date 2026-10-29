/**
 * States that a value is set, with a masked suffix.
 *
 * The env tool's modules import it; it is not run directly.
 */
import { SUFFIX_LENGTH, SUFFIX_MIN_LENGTH } from "./constants.mts";

type DescribeValueInput = { readonly value: string };

/** Says a value is set and, for a long value, shows its last characters with symbols masked. */
export function describeValue({ value }: DescribeValueInput): string {
  if (value.length < SUFFIX_MIN_LENGTH) {
    return "set";
  }

  const suffix = value.slice(-SUFFIX_LENGTH).replaceAll(/[^A-Za-z0-9]/gv, "*");

  return `set (...${suffix})`;
}
