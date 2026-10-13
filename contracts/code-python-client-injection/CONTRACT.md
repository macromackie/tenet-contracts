---
name: code-python-client-injection
message: Construct stateful Python clients at composition roots and inject them into consumers as abstract types.
---

## Rules

Treat a client that holds connections, credentials, buffers, or background workers as a stateful service object.
Construct production clients at the composition root, such as application startup or a worker entry point, never inside the routes, services, or jobs that use them.
Do not create clients when a module is imported, or keep them in module-level globals that consumers read directly.
Define a consumer-facing abstract type for each client as an `abc.ABC` subclass or a `typing.Protocol`, and annotate consumers with that type rather than the production class.
Pass clients to consumers explicitly, through parameters or the framework's dependency injection.
Never branch on which implementation a consumer received, such as with `isinstance` checks against concrete client classes.

Separate callers that only use a client from the owner of its lifecycle, and give those callers a type without start or shutdown methods.
Start each client once per process in its lifecycle owner, and drain or close it at shutdown after its producers have stopped.
Match lifecycle methods to the runtime: a synchronous close method for synchronous workers and an awaited coroutine for `asyncio` applications.

Put shared request construction on the abstraction when every implementation must produce the same typed value.
Keep external configuration, transport, batching, and retries in the production implementation or the library it wraps, never in consumers.
Provide a disabled implementation for environments without the external service, and select it at the composition root rather than with conditionals in consumers.

When a retained check needs to observe what consumers send through a client, inject a recording fake that implements the abstract type, performs no external I/O, and records typed calls.
Substitute clients in tests by injecting an implementation of the abstract type, never by patching the production client's methods or module paths, such as with `unittest.mock.patch`.
Write clients and fakes as ordinary classes, not as validated data models, because their fields are mutable runtime state.

## Checks

Run the project's Python type checker and confirm every consumer accepts the abstract client type.
Review each production construction site and confirm it sits at a composition root.
Search consumers for direct construction, module-level client instances, and checks against concrete client classes.
Exercise process startup and shutdown and confirm each client starts once and drains after its producers stop.
In each retained check that replaces a client, confirm that it injects an implementation of the abstract type and performs no external I/O.
