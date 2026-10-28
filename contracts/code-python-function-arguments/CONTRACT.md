---
name: code-python-function-arguments
message: Make every parameter of an owned Python function keyword-only, and keep the signatures that the language, runtime, and dependencies define.
---

## Rules

Make every parameter of an owned function, method, and constructor keyword-only, such as `def clip(*, text: str)` instead of `def clip(text: str)`.
Never give an owned function a positional parameter, whether the function is public or private, nested in another function, or a callback that owned code defines and calls.
Never declare a positional-only parameter before `/` or a variadic `*args` parameter in an owned function.
Leave `self` and `cls` positional, because the language passes them, and make every parameter after them keyword-only, such as `def settle(self, *, invoice: Invoice)`.
Declare each owned dataclass with `kw_only=True`, so the constructor it generates takes every field by name.

Keep the signatures that the language, runtime, and dependencies define, such as a special method's operand, a property setter's value, a signal handler, or a callback a dependency calls.
Never wrap such a function only to turn its positional parameters into keyword-only ones.
Mark a method that overrides a base class's method with `@override`, such as `@override def __format__(self, spec: str) -> str`, which the lint exempts.
Suppress the finding at every other such signature only as `code-lint-suppressions` allows, with a reason that names what defines the signature.
A lambda written directly as a call's argument, such as `sorted(orders, key=lambda order: order.total)`, takes the signature its callee defines.
A test or fixture whose runner passes fixtures by parameter name takes each fixture as a keyword-only parameter, such as `def test_settle(*, tmp_path: Path) -> None`.

Enforce the keyword-only rule with the repository's lint set to allow no positional parameter, as the configuration that `code-lint-strictness` ships does.
Review what that lint does not count: a variadic `*args` parameter and a dataclass declared without `kw_only=True`.

Violation: a private helper declared as `def _clip(text: str) -> str` takes its one input positionally, and `def sum_amounts(*amounts: Decimal) -> Decimal` collects its inputs positionally.
Allowed: `def clip(*, text: str) -> str`, called as `clip(text=line)`, and `def settle(self, *, invoice: Invoice) -> Receipt` on an owned class.
Violation: `@dataclass(frozen=True) class Invoice` generates a constructor that takes its fields by position.
Allowed: `@dataclass(frozen=True, kw_only=True) class Invoice`, and `@override def __format__(self, spec: str) -> str`, whose `spec` the language passes.

## Checks

Run the repository's lint from the repository root, and confirm that it rejects `def clip(text: str)` and `def clip(text: str, /)`.
For each positional parameter a change keeps, which language rule, runtime, or dependency defines its signature?
For each `*args` parameter and dataclass a change adds, does it take every input by name?
Search the change for wrappers that only turn positional parameters into keyword-only ones.
