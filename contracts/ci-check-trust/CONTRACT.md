---
name: ci-check-trust
message: Run complete required checks with explicit trust and no inherited cache or credential authority.
---

## Rules

Run every job on an explicitly declared runner, and do not fall back to a runner with different trust or environment.
Pin third-party CI steps to immutable identifiers, such as full commit hashes or content digests, not tags or branches.
Grant each job only the repository permissions it needs.
Run native checks on their declared operating systems and architectures.

Run the complete check graph for pull requests, default-branch pushes, and manual runs.
Require every required job to succeed; a skipped, canceled, or missing required job is not success.
Make each required aggregate status depend on every required job, so that any failure fails the aggregate.
Propagate step failures instead of masking them with ignored exit codes or continue-on-failure settings.
Do not shorten a required check by omitting targets or reusing earlier results without complete dependency evidence and a full-check fallback.
Do not change shared quotas, runner profiles, or branch protection to make a check pass.
Preserve diagnostics and failure artifacts from failed checks.

Never let concurrency cancel a newer default-branch check, and keep retries and manual runs separate from ordinary supersession.
Give parallel jobs explicit joins, separate outputs, cancellation propagation, and cleanup ownership.
Do not share a mutable build output directory between concurrent jobs.
Clean up only the resources a job created.

Keep production and deployment credentials out of check jobs.
Start publishable checks with fresh execution state, and do not accept or upload remote cache results for them.
Never restore caches or executable results written by another repository or by pull-request jobs into a default-branch check.
Bind any trusted cache or remote execution to this repository's immutable identity and trust subject, verified by the infrastructure owner before it is enabled.
Fail closed when trusted-cache authorization is missing, and never fall back to a weaker cache.
Do not inherit another repository's identity-token subject or permissions.

## Checks

Inspect every workflow's triggers, runners, permissions, pinned step references, and required jobs.
Confirm that a failing, skipped, or canceled required job fails the required aggregate status.
Confirm that pull-request and manual runs cannot write caches or executable results that default-branch runs consume.
Confirm that check jobs receive no production credentials and no cache authority the infrastructure owner has not verified.
