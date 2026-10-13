---
name: ci-reproducible-checks
message: Run the same declared checks locally and in CI with pinned tools and complete inputs.
---

## Rules

Pin every tool and runtime version that checks use in tracked configuration.
Keep any duplicated version declaration consistent with its single pinned source.
Pin dependencies with committed lockfiles, and use frozen or locked installs both locally and in CI.
Pin images and downloaded tools to fixed versions, and verify them against recorded digests or hashes.

Expose one root command that runs the complete check graph, and run that same command locally and in CI.
Register every check the repository runs, such as type checking, tests, linting, formatting, documentation validation, workflow validation, and production builds, in that graph.
Give equivalent check commands the same name in every package.
Check repository-owned automation scripts with the same type checking and linting as product code; running a script does not establish its correctness.

Declare each build and test action's actual source, tool, and runtime inputs.
Give each action only the inputs it consumes, and keep production build inputs separate from test-only inputs.
Keep the declared file inventory complete, so that added and moved files invalidate the checks that read them.
Run effectful steps, such as dependency installs, database migrations, registry reconciliation, image builds, runtime qualification, and publication, as explicit uncached steps, never inside cached actions.

Keep credentials, local settings files, and build outputs out of version control, and keep personal cache paths and machine-specific paths out of tracked configuration.
Keep the root check graph runnable from a clean checkout without private setup, live services, or their credentials.

## Checks

From a clean checkout, run the frozen install and the root check command.
Compare the CI workflow's check command with the documented local command.
Review version files and lockfiles for drift from their pinned source.
When moving or changing build inputs, inspect representative forward and reverse dependency edges; passing checks alone do not prove isolation.
A cache hit does not prove the input closure, so confirm that a changed input invalidates the actions that read it.
