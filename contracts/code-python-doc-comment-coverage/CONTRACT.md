---
name: code-python-doc-comment-coverage
message: Give every public Python module, class, function, method, and `__init__` a docstring, and fail checks when one is missing.
---

## Rules

Apply these rules to maintained Python source, tests, and scripts, and not to generated or copied third-party source.
Treat a module, class, function, or method as public when neither its name nor the name of a module or class that contains it starts with an underscore.
A name that starts and ends with two underscores, such as `__init__`, does not make its declaration private.
A function or class declared inside a function is not public.
Where a module declares `__all__`, treat only the names that list holds, and the methods and classes declared inside them, as its public classes and functions.
Give a docstring to every public module, including a package's `__init__.py`, and to every public class, including a class nested in another.
Give a docstring to every public function and method, including a special method such as `__format__`, and to every public class's `__init__` method.
A method marked `@override` needs no docstring of its own, because the base class's docstring documents it.
A property's setter and deleter and each `@overload` signature need no docstring, because the property's getter and the overloaded function's implementation document them.

A docstring that `code-comment-content` forbids, such as `"""Reads the invoice."""` in `read_invoice`, does not satisfy these rules.
Write each docstring in the prose form and layout that `code-comment-form` requires.
Renaming a declaration with a leading underscore so that the check passes while other modules still import it is a violation.

Enforce these rules with the repository's lint over every package, as the configuration that `code-lint-strictness` ships does, and fail checks on each missing docstring.
Write each docstring by hand, because the only text a tool can insert is the empty docstring that `code-comment-form` forbids.
Exempt a declaration only with the suppression that `code-lint-suppressions` describes.

Violation: a public module's `def settle_invoice(*, invoice: Invoice) -> Receipt` carries no docstring, or carries `"""Settles the invoice."""`, which restates its name.
Allowed: `"""Marks the invoice paid, and raises InvoiceRefunded when a refund already closed it."""` opens its body, and an `@override` method `__format__` carries none.

## Checks

Run the repository's lint from the repository root, and confirm that it fails on an undocumented public module, class, function, method, and `__init__`.
For each name a change adds to `__all__` or re-exports, does the declaration it names carry a docstring?
For each docstring that a change adds to satisfy these rules, what does it tell callers that the name and signature do not?
For each change to the lint configuration, does it keep every declaration kind above required, with no decorator or name pattern exempted?
