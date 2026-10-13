---
name: eval-score-accounting
message: Report every score with its denominator, and never turn failures, unknowns, or missing cost into values.
---

## Rules

Keep assessed-system failures, grader failures, cancellations, and low-quality grades distinct in saved results and summaries.
Let only complete grades contribute to scores, means, and observed ranges.
Record a missing grade or missing dimension as a grading failure, never as zero, success, or a skipped case.
Count an expected item that the assessed system did not address as a miss, never as an exclusion from the denominator.
Record an explicit unknown when the grader cannot decide, and never average an unknown as a score.
Treat material the grader needed but could not obtain as an unknown grade, not as evidence against the assessed output.
Never count an exhausted, cancelled, or incomplete case as a success, even when its partial output matched every expected outcome.
Score abstention on an answerable case separately from justified abstention, and wrong decisive answers separately from decisive answers the inputs do not support.

Report the number graded beside the total selected, and give every score its denominator.
Report a score with an empty denominator as unavailable, not as zero or full marks.
Report answer coverage beside accuracy on answered cases, since a system that rarely answers can show high accuracy on very few cases.
Give component-level and final results separate scopes and denominators.
Report case groups with different expectations, such as defect cases and clean controls, separately, and never merge them into one mean.
Label a run with unfinished cases as partial, keep its completed scores visible, and count it apart from finalized runs.

Report the assessed system's usage and cost separately from grading usage and cost.
Record unavailable usage or cost as unknown, and never show it as zero or show partial cost as total cost.
Identify attempts without usage records, and state which interrupted attempts the totals exclude.
Record observed side outcomes, such as executed commands or published states, separately from quality grades, and treat a missing observation as unknown, never favorable.

Derive every summary, comparison, and displayed score from saved per-case records, never from progress events or terminal output.
Store regrades, audits, and human labels beside the original grade, and never overwrite the original grade or the summaries derived from it.
Never rerun or regrade a case because its result was unfavorable.
Describe scores from a judgment-based grader, such as a model or a human rater, as grader scores rather than measured accuracy, and score ranges as observed variation rather than statistical confidence.

## Checks

Recompute one summary from saved per-case records and confirm each score's numerator and denominator.
Inject an assessed-system failure, a grader failure, and a cancellation into a small run, and confirm that each stays distinct and none becomes a score.
Confirm that missing cost appears as unknown and that grading cost is reported apart from assessed-system cost.
Regrade a saved run and confirm that the original grades and summaries are unchanged.
Does any average include an unknown, a failure, or an empty denominator?
