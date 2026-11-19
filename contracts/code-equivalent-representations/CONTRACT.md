---
name: code-equivalent-representations
message: Give inputs that a public operation declares equivalent the same documented result or error.
---

## Rules

For representations the interface declares equivalent, preserve their shared meaning on every public entry point that accepts both.
Return the same documented result for an accepted pair and the same documented kind of error for an invalid pair.
Preserve distinctions the interface exposes, including the sign of zero or the unit of a quantity when they affect its meaning.

## Checks

Choose a pair whose equivalence follows from the public specification and compare the outcome of the same call under each representation.
For an exact-length conversion that accepts both a whole number and its decimal text, compare the outcomes for zero in both forms and for a negative length in both forms.
Change the text path so it treats zero as absent and confirm the test detects the difference.
Compare a pair that the interface explicitly distinguishes and confirm the check accepts the documented difference.
