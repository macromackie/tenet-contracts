---
name: code-explicit-input-precedence
message: Use a caller's explicit value and read its fallback only when the input is absent.
---

## Rules

For each input with a fallback, use the public interface's definition of absence.
Preserve each accepted explicit value, including zero, false and empty values when the interface accepts them.
If the caller supplies an invalid value, report the documented outcome for invalid input.
Read the fallback only in the absent case and at most once per resolution.

## Checks

Call the public entry point with an accepted value that would otherwise trigger a fallback, and observe both the returned value and the number of fallback reads.
For a timeout that accepts zero and reads a default of thirty when omitted, expect zero and no reads for an explicit zero, then thirty and one read when omitted.
Check that the same test catches a change that eagerly reads the fallback and still returns the right explicit value.
Move resolution into a helper without changing either observation and confirm the test still passes.
