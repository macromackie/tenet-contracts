/**
 * Applies the erase keys in text typed at a raw-mode terminal.
 *
 * `read-hidden-value.mts` imports it; it is not run directly.
 */

type ApplyErasuresInput = { readonly typed: string };

/** The characters a terminal in raw mode sends for the two erase keys. */
const ERASE_KEYS: ReadonlySet<string> = new Set(["\b", "\u007F"]);

/** The last character of a string, as one code point. */
const LAST_CHARACTER = /.$/v;

/** Removes each erase key and the character before it, as a terminal in cooked mode would. */
export function applyErasures({ typed }: ApplyErasuresInput): string {
  let value = "";

  for (const character of typed) {
    if (ERASE_KEYS.has(character)) {
      value = value.replace(LAST_CHARACTER, "");
      continue;
    }

    value += character;
  }

  return value;
}
