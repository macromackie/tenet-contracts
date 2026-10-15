---
name: code-python-exception-propagation
message: Let Python exceptions propagate; catch one only to re-raise it, translate it with its cause, retry it, or record a failed unit of work.
---

## Rules

Apply this contract to Python source, including tests.
An `except` handler may end with a bare `raise`.
A handler may translate the exception with `raise OtherError(...) from exc` into one its caller handles.
A handler in a retry loop may catch a declared transient exception type and try again within a bounded number of attempts, re-raising the last exception when the attempts run out.
A handler in the outermost loop of a worker, job runner, or server may record the current unit of work as failed with the exception and continue with the next unit.
Every other handler violates this contract, including `pass`, logging and then carrying on, returning `None`, an empty collection, or a default value, and setting a failure flag.
`contextlib.suppress(...)` hides exceptions the same way and violates this contract.

`try`/`finally` blocks and context managers that release resources are allowed.
Asserting in a test that code raises an exception is allowed.

Allowed, because the handler raises: `except ValidationError as exc: raise ManifestRejected(path) from exc`.
Violation, because execution continues after the handler: `except OSError: logger.info("scratch cleanup failed")`.

## Checks

Search changed Python files for `except` and `suppress(`, and confirm that each handler raises, retries a declared transient exception within a bound, or records a failed unit of work at the outermost loop.
