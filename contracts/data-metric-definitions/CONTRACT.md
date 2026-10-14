---
name: data-metric-definitions
message: Define each metric's cohort, window, and denominator, count each stored fact once, and show coverage gaps beside results.
---

## Rules

Define each metric's cohort, time window, time zone, eligibility, numerator, and denominator in one definition that computation and display both use.
Name the stored fact that marks each counted occurrence, and count different kinds of occurrence, such as orders placed and orders shipped, as separate metrics.
Count an occurrence only when stored evidence establishes it, and report occurrences with unresolved evidence separately instead of counting or dropping them.
Count a condition as met at an occurrence only when its evidence existed before that occurrence, such as an approval recorded before an order shipped.
Never infer a fact from a proxy record, such as inferring who reviewed an order from who closed it.

Count each source event once by its source identity, so replays and redeliveries never change a metric.
Never let an older observation replace a newer fact; order updates by the source's own time or revision, not by arrival.
Commit event receipts and the projections derived from them in one transaction.
Run historical imports apart from live collection, so an import cannot delay live facts.
Record the eligibility and configuration that applied to each occurrence when it happened.
Keep history without such a record unknown, and never infer past eligibility from current configuration.

Show incomplete imports, collection failures, and coverage gaps beside the results they affect; see `data-and-apis`.
Report each rate with its numerator and denominator, and show a rate with an empty denominator as unavailable rather than zero.
Keep the meaning and source of each displayed time, such as occurrence time versus collection time, when a metric combines sources.
Keep each environment's facts and aggregates separate.

Serve dashboards and summaries from stored projections, and never call a provider while answering a read.
Compute each total on the server over the full requested window, never from one page of results.
Bound aggregate queries by time window, result size, and deadline, and keep the window, filters, and access scope fixed across pages.
Keep source code, comment text, prompts, and credentials out of metric events and projections.
Require organization-level authorization for organization-wide aggregates, and never let a narrow client credential or an event-producer credential acquire it.

## Checks

Recompute one displayed metric from stored facts, and compare its cohort, window, numerator, and denominator with the definition.
Replay a batch of source events and deliver an older observation after a newer one, and confirm metrics and facts are unchanged.
Inject a collection failure and an incomplete import, and confirm the affected results show the gap.
Request an organization-wide aggregate with a narrow client credential and with an event-producer credential, and confirm refusal.
Page through a summary with different page sizes, and confirm the totals and window do not change.
Review dashboard read paths for provider calls.
