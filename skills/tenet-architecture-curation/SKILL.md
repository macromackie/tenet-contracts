---
name: tenet-architecture-curation
description: Design or review ownership, package boundaries, data flow, recovery, and observability when changing how parts of the system work together.
---

# Architecture curation

Choose the simplest structure that makes ownership, effects, and failure behavior predictable. Apply this workflow
to the affected system; an ordinary implementation task does not require a repository-wide redesign.

## Choose the target before the migration

Given today's requirements, what is the simplest complete system we would choose? Start with observable behavior,
authoritative data, ownership, and interfaces. Read applicable contracts and separate real constraints—stored data,
access guarantees, and supported consumers—from incidental folders, wrappers, flags, and historical boundaries.
Challenge the model that makes a requirement hard before adding another special case. Scale this reasoning to the task;
a small fix may need only a sentence, not a design document or a repository-wide rewrite.

Then trace an existing operation from entry point to result, including effects and recovery. Use the implementation
as evidence and migration input. Compare concrete alternatives by the decisions callers must make, independently
maintained state, and operational cost. More packages or a larger rewrite are not evidence of a better target.

Prefer focused modules and nested folders. Introduce a package when a current dependency, runtime, ownership, or reuse
boundary warrants it. Keep cohesive state transitions together. A small file is useful only if its responsibility is
understandable. See [boundaries and data](resources/boundaries-and-data.md).

## Design the flow

Give each boundary explicit inputs, results, and failure semantics. Pass the data an operation needs rather than a
whole application context. Keep domain decisions separate from provider transport, storage, and terminal rendering.
Use one authoritative state and derive reports from it. Validate untrusted inputs at entry points; avoid repeated
conversions and checks for invariants already established by types or their owner.

Review the data model from its actual callers. Distinguish authoritative fields from derived values; look for
contradictory flags, optional fields that hide distinct outcomes, repeated conversions, and unused parameters.
Simplify the representation where it removes decisions from callers. See [boundaries and data](resources/boundaries-and-data.md).

Design interruption and recovery alongside the happy path. Prefer operations that can safely repeat and state that
can explain what remains unfinished. Bound retries, concurrency, and deadlines. Durable infrastructure such as celld
is useful where work must survive disconnection; it is not required for every operation. See [recovery](resources/recovery.md).

Make important transitions and failures inspectable without scattering logging through every helper. Keep correlation,
redaction, and diagnostic conventions consistent. See [observability](resources/observability.md).

## Make the change complete

Choose the migration after the target is clear. Break compatibility when the task permits it; preserve actual data
and update supported consumers explicitly. Do not keep an old path merely to avoid changing callers, or add extension
points for imagined requirements. If a staged cutover is necessary, give the temporary path an owner and removal condition.

Update affected callers, configuration, commands, exports, documentation, and checks together. Retire superseded paths,
representations, dependencies, fixtures, and guidance in the same scope. Explain any retained alternative's current need.
Reuse established patterns, or replace an inadequate convention across its affected callers. Keep useful language and
runtime differences rather than forcing identical implementations.

When convention changes are authorized, record concrete ownership and dependency requirements in the nearest contracts.
Inherit shared rules instead of copying them. Keep design rationale in the repository's context notes; neither research
nor a skill silently establishes new repository requirements.

Use the optional tenet-code-curation skill for local readability and the optional tenet-test-curation skill for
verification. Exercise the affected flow, including the relevant failure or restart path. Report what was verified;
architecture diagrams and passing type checks alone do not prove recovery works.
