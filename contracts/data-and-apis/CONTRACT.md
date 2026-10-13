---
name: data-and-apis
message: Keep authoritative facts and explicit outcomes behind small, usable APIs.
---

## Rules

Store authoritative facts and derive dependent values.
Materialized summaries and caches are useful when their owner defines how they stay consistent; they must not become competing sources of truth.
Keep units and identities consistent across the affected flow.

Represent distinct outcomes explicitly when independent optional fields or booleans permit contradictory states.
For example, a graded result contains a grade; a failed result contains an error.
Raw provider evidence may accompany either result for diagnosis without deciding success.
Missing evidence is not a zero value or a successful empty result.

Validate untrusted inputs at their entry point, then use the established domain representation internally.
Revalidate when crossing a new trust boundary.
Keep provider and persistence formats in their adapters unless the format is itself the intended API.
Pass only the data an operation needs; avoid unrestricted context objects.

Review API changes from actual callers.
Remove unused parameters, redundant conversions, and obsolete options made unnecessary by the new model.
Do not add a flag or wrapper to compensate for a representation that should change.

## Checks

Follow one representative input through execution and output.
Can two fields disagree about the same fact?
Can the type express an impossible outcome?
Does a caller repeat validation, reinterpret an error, or repair a result?
Check serialization and all affected callers when changing a representation.
Use types for structural guarantees and focused tests for conversions and behavior; model assessments guide this review rather than establish compliance.
