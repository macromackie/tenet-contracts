---
name: llm-assessment-outcomes
message: Keep pass, fail, uncertain, error, and incomplete outcomes distinct, and never let failed execution pass.
---

## Rules

Give every model assessment exactly one outcome from a declared set that distinguishes pass, fail, not applicable, uncertain, error, and incomplete.
Keep semantic uncertainty, where the model answered without a confident choice, distinct from execution failure, where no valid answer was obtained.
Never convert a failed request, an unreadable input, missing evidence, or an exhausted budget into pass, fail, or not applicable.
Treat an uncertain outcome as unresolved: it is neither a pass nor evidence of a defect in the subject or the model.
Report a cancelled run as cancelled, distinct from errors and from completed outcomes.

Keep applicability distinct from violation: an applicable subject can still satisfy the requirement.
A supported failure for a subject remains a failure even when a separate applicability answer says not applicable.
When a combined answer contradicts a supported failure for one of its subjects, report the combined result as unresolved and name the conflicting subjects.
A favorable outcome for selected subjects supports a claim about those subjects only, not about the whole scope that contains them.
Report a scope as verified only with complete evidence for that scope, and never report an unaffected scope as newly verified.

Count skipped and excluded inputs separately from assessed inputs, and report them.
Include every completed assessment, including negative ones, in machine-readable output.
Finish every completed run with a summary that counts each outcome.

Declare one precedence for combining outcomes into an overall status, and apply it to every exit status, summary, and report.
Give cancellation precedence over execution errors, and execution errors precedence over uncertain, incomplete, and failed outcomes.
Report an overall pass only when every requested subject completed with a pass or not-applicable outcome.
Derive the overall status from final outcomes, never from intermediate or superseded answers.
Keep confirmed failures visible at every overall status, including when an error or cancellation decides it.

## Checks

Force a failed request, an unreadable input, and an exhausted budget, and confirm each yields error or incomplete rather than pass, fail, or not applicable.
Run inputs that mix passes, failures, uncertainty, errors, and cancellation, and compare the overall status with the declared precedence.
Can any code path fill a missing or failed answer with a default outcome?
Confirm that skipped inputs are counted and that confirmed failures remain in the output when an error decides the overall status.
Review user-facing documentation of outcomes and exit statuses alongside any change to them.
