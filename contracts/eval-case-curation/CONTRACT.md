---
name: eval-case-curation
message: Add only distinct, justified cases with clean controls and stated premises, and never edit cases to fit results.
---

## Rules

Add a case only to cover a consequential failure mode the existing cases miss, or to reach the sample size a stated measurement needs, never as a near-duplicate.
Record beside each case or case group the behavior it targets, the failure mode it belongs to, and why a miss would matter.
Write a synthetic case's inputs, such as its task description, as its real author would.
Never remove or weaken a case because the assessed system fails it, and remove a case only as a stated duplicate or when its premise no longer holds.
Do not edit a case, its expected outcomes, or the original material it was built from to make a run, fixture, or score succeed.

Add clean controls that expect no defect wherever false positives are plausible, without requiring a paired control for every case.
Grade clean controls on avoiding unsupported outputs, and give full credit to a correctly empty output.
Audit a control when a grader confirms a supported defect in it.

Write each case's expected outcomes in readable form beside the case.
Express expected outcomes as distinct behaviors confirmed in the case material, not as required wording or action sequences.
When expected outcomes do not enumerate every correct output, accept additional outputs that the case material supports.
Record a possible new issue found during grading for adjudication instead of silently expanding the expected outcomes.
When a case expects behavior that no adopted requirement states, label it as desired behavior and never present it as an existing rule.

State the premises, such as source revision, callers, runtime, and dependencies, behind an expected outcome derived from an executed probe.
Limit an expected outcome to the effect its evidence demonstrates, because a probe under controlled conditions shows a scoped counterexample, not reachability in the original deployment.

## Checks

Pick a case and confirm that its targeted behavior, failure mode, premises, and expected outcomes are recorded beside it.
Inspect a clean control's grades for unsupported outputs, and confirm that a correctly empty output earns full credit.
Review each removed or edited case for a stated duplicate or invalid premise rather than an unfavorable result.
Does any expected outcome require exact wording or a particular sequence of actions?
For an expected outcome backed by a probe, confirm that its premises hold for the claimed implementation and that its assertions establish the claimed effect.
