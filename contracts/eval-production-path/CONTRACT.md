---
name: eval-production-path
message: Evaluate the shipped system through its public interface at pinned revisions without external effects.
---

## Rules

Evaluate the assessed system through the same public interface and build that production uses.
Do not maintain a second implementation of the assessed system in the evaluation, or import its private modules.
Consume the assessed system's published request and result schemas instead of redefining them.
Keep case selection, grading, saved results, and reporting outside the shipped system, and do not add an evaluation engine to it.
Keep one evaluation runner, one case format, and one editable case catalog for each assessed system.

Mark every evaluation request as evaluation, with a stable trial identity, so that the assessed system keeps it apart from production state.
Give every repeat a new trial identity and fresh assessed-system state, and keep one trial identity across the rounds of a multi-round case.
Supply history to a round only from earlier rounds of the same trial.
Disable persistent learned state, such as memory, in baseline runs, and require each result to record that it was disabled.
Supply learned state to an experiment only as an immutable, content-addressed snapshot saved before submission, send the same snapshot every round, and verify its digest in each result.
Keep supplied learned state independent of case answers and grading material, and check its provenance for information from after the case's revision.

Pin every case's material to full, immutable revision identifiers, never to branch names or other movable references.
Never read or modify the caller's working tree or version-control index while preparing a case.
Reproduce a case that depends on an external service from its frozen original metadata, and validate the reproduction exactly before submission.
Reject a completed result unless it reports the exact revisions and inputs that were submitted.

Disable external effects, such as publication, on evaluation requests, and reject results that report a performed effect.
Exercise a required external effect only against a local fake of that service, and read the effect back from the fake.
Record the effect state observed in the fake for each round, and require it to name that round's revision.

Send the run's variant with every request, and reject results that do not record it.
Record in each result the resolved version of every component that can change it, such as models, prompts, instructions, tools, policy, and learned state, and reject a result that leaves any version pending.

## Checks

Inspect the evaluation's imports and confirm that it reaches the assessed system only through its public interface and published schemas.
Run one case and confirm that the saved result reports the submitted revisions, inputs, variant, and resolved component versions.
Repeat a case and confirm that it gets a new trial identity and fresh state, while the rounds of one case share a trial.
Confirm that an evaluation request produced no external effect, and that a required effect reached only the local fake.
