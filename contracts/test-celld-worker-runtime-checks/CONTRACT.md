---
name: test-celld-worker-runtime-checks
message: Exercise the built Worker on pinned Celld with local dependencies and verify that each run releases its resources.
---

## Rules

Start the checked Worker entry point and its built modules with the pinned Celld executable in the repository's required checks.
Keep environment differences in runtime bindings and settings so qualification exercises the same application artifact that ships.
Bind dependencies to test-owned local services and supply synthetic credentials where a binding needs authentication.
Fail setup when a required binding is missing instead of falling back to a hosted service.

Bound startup and wait for the Worker to answer a readiness request before exercising it.
Send a request through the Worker and verify an observable result that depends on its local dependency whenever the Worker has one.
For a Worker that promises durable state, write through the Worker, restart it against the same isolated state, and read back the value through the Worker.

Track each process, listener, and temporary state directory that the run owns from the moment it is acquired.
On success, failure, or interruption, stop those processes within a declared deadline, release the listeners, and remove the run's disposable state.
Preserve the original failure when teardown succeeds and report any teardown failure.

## Checks

Run the repository's Worker qualification from its root and confirm that Celld loaded the release build output with only local bindings.
For a dependency-backed route, confirm that the response reflects data supplied by the local dependency.
For a persistence guarantee, compare the value read after the Worker restart with the one written before it.
Force a failure after the first resource starts and confirm that the check exits unsuccessfully, its processes exit, and its ports can be rebound.
After a successful run, confirm that the same resources have been released.
