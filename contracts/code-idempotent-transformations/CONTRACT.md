---
name: code-idempotent-transformations
message: Keep canonical source and document transformations idempotent while preserving comments, line endings, and opt-out regions.
---

## Rules

Apply this rule to each public formatter, sorter, normalizer, or canonical serializer that promises stable output across repeated runs.
Running the transformation a second time on its own output must produce the exact same bytes or string as the first run (`transform(transform(x)) == transform(x)`), including when comments, trailing directives, or added entries are present.
Preserve the input's line-ending convention (`\n` vs `\r\n`), leading or trailing comments, and regions explicitly marked as skipped or disabled, without duplicating comments or inserting spurious blank lines on whitespace-only inputs.
Exclude intentionally lossy conversions or one-way encoders whose interface documents non-idempotent output.

## Checks

Apply the public transformation twice to inputs containing mixed comments, CRLF line endings, inline opt-out directives, and whitespace-only content, and compare the first and second outputs byte-for-byte.
Confirm that comments stay attached without duplication, that CRLF inputs retain CRLF line endings, and that code inside a disabled or skip region remains byte-for-byte identical.
Verify that a defect duplicating an inline comment or normalizing CRLF to LF fails the check while an idempotent, preservation-safe implementation passes.
