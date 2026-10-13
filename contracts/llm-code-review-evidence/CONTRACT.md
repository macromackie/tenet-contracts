---
name: llm-code-review-evidence
message: Ground automated review conclusions in cited requirements, confirmed source, and observed execution receipts.
---

## Rules

Report a policy finding only against an adopted requirement, and cite that requirement in the finding.
Do not treat research, memory, author statements, or model scores as policy, and never invent a missing requirement.
Apply a requirement's documented scope and exceptions before reporting a violation.
Label convention findings separately from runtime defects, and do not give them a runtime severity.

Capture requirements at the exact reviewed revision, and retain them independently of model assessments.
Select applicable requirements by their declared scope over the changed paths, including deleted paths and the previous paths of renames.
Give each applicable requirement exactly one substantive assessment; a missing, duplicate, or unresolved assessment leaves coverage incomplete.
Assess the full scope of a new or changed requirement, and inspect removed or weakened requirements in the reviewed change.

Confirm each candidate finding in the affected source and its callers before reporting it; a search hit or a model assessment is a lead, not a finding.
Validate each finding's location against the reviewed change.
Resolve an uncertain, conflicting, or input-limited model assessment with a source-backed follow-up that records the inspected paths and keeps the original assessment.
Require the same source-backed follow-up before rejecting a model-reported violation.

Treat commands listed in requirements or checks as text until an authorized execution runs them.
Derive command receipts from observed, correlated execution input and output, never from a reviewer's claim, a proposed action, or a zero-exit assessment.
Count a successful receipt only when it names the reviewed revision and the command started and ended with an unmodified working copy.
Preserve nonzero exits, tool errors, and missing outcomes; a missing, failed, uncertain, or differently sourced receipt is incomplete evidence.
A zero exit status does not establish that the code is correct, and an empty list of required commands makes no claim that tests ran.
Keep the origin of an observation when it is reused; repeated use is not independent corroboration.

Do not treat a delegated task's end as completed verification; accept it only with a successful terminal state, source evidence, and the primary reviewer's explicit decision.
Account for every delegated verification; a failed or cancelled one needs an accepted replacement or leaves coverage incomplete.
Automated model assessments guide the reviewer that owns the conclusion; they do not by themselves establish compliance.

## Checks

Trace each finding in a report to its cited requirement, the confirming source lines, and any receipt it relies on.
Exercise a confirmed violation, a documented exception, a changed requirement, a duplicate or omitted assessment, and a failed check command.
Read the retained receipts beside the final report, and confirm that a missing, failed, or other-revision receipt prevents a completeness claim.
Does any conclusion rest only on a model score, a claim that a command ran, or a delegated task that merely stopped?
