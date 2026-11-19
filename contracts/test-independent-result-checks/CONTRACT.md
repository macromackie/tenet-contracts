---
name: test-independent-result-checks
message: Check computed results against expectations derived independently of the operation under test.
requires-tenet: 0.11.0
---

## Rules

For each computed result under test, establish the expected value or defining relation from the public specification and the original inputs.
When the specification allows approximation, derive the acceptance bound from its stated precision and input scale.
Keep the operation under test and its implementation helpers out of the calculation of the expected result.

## Checks

For a linear solver, multiply the reported solution by the original matrix and compare the product with the original right-hand side.
Use the small exact system in `assets/tenet/linear-solve.json` as a reference example when adapting the check to a solver.
Check that substituting the solution in reversed component order fails the same calculation and that swapping both input rows with their right-hand sides still passes.
For a paired encoder and decoder, compare the encoder's output with an independently specified wire example so a shared encoding error fails even if the round trip succeeds.
