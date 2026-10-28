---
name: code-python-none-guards
message: Trust non-optional Python annotations, and check for None only where the checked value's type includes None.
---

## Rules

Apply this contract to Python source that a static type checker verifies.
A value annotated with a type that excludes `None`, such as `str`, `int`, `Order`, or a model field without `| None`, is never `None`.
The result of a call whose return annotation excludes `None` is never `None` either.
Do not guard such a value with `is None`, `is not None`, `== None`, `assert value is not None`, or `getattr(obj, "field", None)` for a declared attribute.
A fallback that changes nothing except a `None` value, such as `count or 0` on an `int` or `items or []` on a `list`, is a guard too.
When a value can be `None`, annotate it `X | None` and handle `None` as a meaningful case, or fix the caller so it never passes `None`.

A `None` check is allowed when the checked value's declared type includes `None`, such as a parameter annotated `X | None`, or a value typed `Any` or `object`.
A `None` check is also allowed on the result of an API that returns `None` for absence, such as `re.match`, `next(iterator, None)`, or `dict.get`.
A function that callers outside the type-checked code reach, such as a published library's entry point, may reject `None` by raising an error.

Allowed, because `timeout_seconds` is annotated `float | None`: `def connect(*, host: str, timeout_seconds: float | None = None)` with an `if timeout_seconds is None:` block setting `timeout_seconds = DEFAULT_TIMEOUT_SECONDS`.
Violation, because `request` is annotated `Request`: `def handle(*, request: Request)` with an `if request is None:` block returning `Response.empty()`.

## Checks

Run the project's Python type checker over the changed files; it reports a value that may be `None` where an annotation excludes it.
For each changed `None` check or fallback, find the declared type of the checked value and confirm that it includes `None`.
