---
name: code-python-exception-propagation
message: Let Python exceptions propagate; catch one only to re-raise it, translate it with its cause, retry it, record a failed unit of work, or map it to an exit status in the entry point.
---

## Rules

Apply this contract to Python source, including tests.
An `except` handler may end with a bare `raise`.
A handler may translate the exception with `raise OtherError(...) from exc` into one its caller handles.
A handler in a retry loop may catch a declared transient exception type and try again within a bounded number of attempts, re-raising the last exception when the attempts run out.
A handler in the outermost loop of a worker, job runner, or server may record the current unit of work as failed with the exception and continue with the next unit.
A handler in a program's entry point may catch an exception type that the program declares for one outcome, such as `ManifestRejected`, report it, and end the process with that outcome's declared exit status, as `cli-output-channels` describes.
Every other handler violates this contract, including `pass`, logging and then carrying on, returning `None`, an empty collection, or a default value, and setting a failure flag.
`contextlib.suppress(...)` hides exceptions the same way and violates this contract.

`try`/`finally` blocks and context managers that release resources are allowed.
Asserting in a test that code raises an exception is allowed.

Allowed, because the handler raises: `except ValidationError as exc: raise ManifestRejected(path) from exc`.
Allowed, because the entry point maps a declared outcome to its exit status: `except ManifestRejected as exc: return finish(status=ExitStatus.REFUSED, error=exc)`.
Violation, because execution continues after the handler: `except OSError: logger.info("scratch cleanup failed")`.

## Checks

Search changed Python files for `except` and `suppress(`, and confirm that each handler raises, retries a declared transient exception within a bound, records a failed unit of work at the outermost loop, or maps a declared outcome to its exit status in the entry point.
