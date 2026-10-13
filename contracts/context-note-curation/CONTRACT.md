---
name: context-note-curation
message: Keep context notes useful beyond a task, with dated, sourced evidence and execution tracking in the task tracker.
---

## Rules

Place each new context note with the nearest owner whose decisions it informs, and keep repository-wide reasoning and navigation at the repository root.
Link each owner-local context index from the nearest ancestor's context index, falling back to the root index.
Keep one maintained home for shared reasoning and link to it from other owners.

Put research, evidence, tradeoffs, lessons, decision rationale, and proposals in context notes rather than in contracts.
Distinguish observations, external claims, hypotheses, proposals, and adopted decisions.
Give each idea, goal, and proposal its provenance and a decision status, such as proposed, accepted, rejected, or superseded.
Keep repository requirements and agent workflows out of notes, and link to the contract or skill that holds them; a note establishes neither.
Keep task progress, assignments, execution plans, next steps, rollout checklists, phase checkpoints, and pending change lists in the task tracker.
Keep operating procedures and implementation specifications with the owning component's documentation, not in context notes.
Renaming a plan as a proposal, goal, or research note does not change its purpose; a comparison of startup behavior is a note, while a checklist to deploy a particular fleet is a task.

Give each new or materially revised factual claim an observed or as-of date and cited sources.
Identify the repository and immutable source revision for implementation observations, such as with a revision-pinned link.
Scope each date to the evidence it describes; one note may hold observations from different dates.
Record the workload and limitations of measurements, and label vendor claims and access or evaluation gaps.
Link to maintained sources instead of copying API fields, inventories, procedures, articles, transcripts, or raw tool output, and never copy a secret into a note.

Treat a date as evidence of a snapshot, not a promise that the claim is current.
A note's generation timestamp is neither an observation date nor a verification event.
Record a verification only when a check happened, stating what was checked and when.
Revalidate volatile facts such as ownership, routes, defaults, credential handling, provider capabilities, prices, and performance before relying on them for a new decision, after a relevant change, or when evidence conflicts.
Add a dated correction or newer snapshot when findings change instead of rewriting an older observation as though it described the present.
When a historical claim lacks a date or revision, recover it from evidence or label it unknown; never infer it from the note's generation time.

When curating a mixed note, keep its reusable evidence, move execution tracking to the task tracker, and move specification content to its owner.
Do not archive a removed plan in another context note.
Delete an empty or redundant note and repair its inbound links.

## Checks

Read each changed note and ask whether its content stays useful after the current task completes.
Confirm that the nearest owner's index reaches the note and that each idea, goal, and proposal has provenance and a decision status.
For each factual claim, check its observation date, its source revision where applicable, its limitations, and any reason to revalidate it.
Confirm that generation, observation, and verification dates stay distinguishable and that historical evidence is not presented as current.
Follow links to confirm that requirements, procedures, and execution records live with their actual owners.
Run the repository's context-note validation, where one exists, for metadata, citations, and links; it does not establish the truth or currency of claims.
