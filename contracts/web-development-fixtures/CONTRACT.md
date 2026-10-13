---
name: web-development-fixtures
message: Run presentation work against labeled synthetic responses without changing the production path or reaching production.
---

## Rules

Choose between fixture and connected transport only in development composition.
Keep routes, reads, writes, and presentation code identical in fixture and connected modes.
Give synthetic records a recognizable marker, and fail the production build when that marker appears in its output; see `code-ownership-and-boundaries` for keeping fixtures out of production code.
Label fixture mode in developer output.

Point connected development at an explicit local or non-production endpoint, and never fall back to production silently.
Keep fixture requests isolated from production services and production data.
Build fixtures from synthetic records only; never copy production records or credentials into them.

Provide fixture responses for loading, empty, failure, long-content, paginated, and signed-out states.
Provide development-only controls to hold and release responses and to switch synthetic accounts, so that account-change and late-response races can be reproduced.

## Checks

Build for production, and search the emitted assets for the fixture marker and synthetic records.
Run the application in fixture and connected modes, and confirm both use the same routes, reads, and presentation code.
Confirm fixture mode is labeled and connected mode targets an explicit non-production endpoint.
Hold a response, switch the synthetic account, and release the response, and confirm the race is visible for review.
