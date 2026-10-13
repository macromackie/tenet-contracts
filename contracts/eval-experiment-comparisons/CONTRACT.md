---
name: eval-experiment-comparisons
message: Compare only frozen, equivalent experiments with a declared intervention, tuning on development cases and validating on holdout cases.
---

## Rules

Declare the intervention and the claim it tests before running a comparison.
Hold every compared condition to the same frozen cases, instructions, budgets, and configuration except the declared intervention.
Compare scores only between completed runs with identical frozen cases, rubric, grader version, and grader settings.
Report a comparison only over cases graded in every compared condition.
Treat a changed rubric, grader, or input selection as a new measurement linked to the original, and keep both versions and their results.
When only grading changes, regrade the saved outputs instead of rerunning the assessed system.
Distinguish a comparison of complete policies from a test that changes only how fixed inputs are represented, and credit newly acquired inputs to acquisition, not to representation.

Report per-case changes and failures beside the averages, because a favorable average does not erase a regression.
State the numbers on both sides when a change improves one metric and worsens another.
When selecting a variant, run every case and repeat in that variant and require complete grades there.
Disclose excluded conditions and their failures, and exclude their usage from the selected condition's cost.
Never choose a favorable subset of cases or discard failed runs of a selected condition.
Evaluate a routing or abstention policy by its supported outcomes and total work, not by a lower uncertain rate alone, and audit its decisive favorable answers as well as its uncertain ones.

Assign each case to a development or holdout split before tuning, and keep cases derived from the same underlying item, such as one defect, in the same split.
Tune only on development cases, and never change the assessed system for a single holdout case.
Select development cases by default, and run holdout cases only on explicit request.
State which cases informed a change when reporting its results.
Before merging a change that can alter evaluated behavior, compare it with the current baseline on the same frozen cases, including the holdout cases.
Do not claim generalization from variants of one source project or dataset, or production reliability from either split.

Compare performance only on frozen workloads with equivalent requested work, and record the executed build, environment, concurrency, cache state, warmup, and sample count.
Keep raw samples, errors, and timeouts, keep offline, simulated, and live measurements apart, and never count faster incomplete work as an equivalent speedup.
Pair each performance claim with quality results on the same cases, and name any downstream work an end-to-end claim excludes.

## Checks

Compare a saved report with itself and confirm that every delta is zero.
Attempt a comparison whose frozen cases or grader settings differ, and confirm that it is rejected.
Read per-case changes before the summary, and confirm that regressions and failures appear.
Run with the default selection and confirm that no holdout case is selected.
For a performance claim, inspect raw samples and completed work before the summary.
