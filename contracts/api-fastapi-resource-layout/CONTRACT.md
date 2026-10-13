---
name: api-fastapi-resource-layout
message: Give each resource one folder of router, schema, query and service modules, and keep URLs fixed when code moves.
---

## Rules

Keep each FastAPI resource in one folder with up to four modules: `router.py`, `schemas.py`, `queries.py`, and `service.py`.
Limit `router.py` to paths, dependencies, parameter parsing, and delegation; it takes no database session and holds no database statements or transaction boundaries.
Keep wire models and their conversions in `schemas.py`.
Put database reads and writes in `queries.py` functions that receive the caller's session and never create, commit, or close one.
Put application operations, including single reads, in `service.py`, which owns session lifetime and transaction boundaries and passes the session to queries.
Create a role module only when the resource has behavior for that role; do not add empty role modules.

Create one folder per resource, not per endpoint, and do not require an index module or package initializer.
Nest a sub-resource folder only when its endpoints share a path segment under the parent's identifier and it has its own storage or wire shape.
Keep endpoints that only rename or set defaults on the parent record in the parent folder.

Name each version folder after the URL prefix it serves, and place each resource in the folder whose prefix its paths carry.
Declare new public resources under the current version prefix.
Never change a URL by moving code; a URL change is a wire change made in its own change.
Comment each router that keeps an inherited path outside its folder's prefix, naming the callers that depend on that path.
Register a static path segment before a parameterized route that would match it, because FastAPI matches routes in registration order.

Mount sub-resource routers from the parent `router.py` with `include_router`, and declare tags only on the parent router.
Compose each version folder's resources in one router that carries the version prefix, and mount each composition root once in the application.

Import only up the tree: a sub-resource may import its ancestors' modules, and an ancestor imports a descendant only to include its router.
Never import between sibling resources, including sub-resources under different parents.
Never import shared types or constants from a router module.
Put an operation that several resources share in a module named for the question it answers, outside every resource folder, and pass it the caller's session.
Place shared code beside the routes when only routes call it, and in the owning domain package when anything outside the routes calls it.

Mirror the resource tree in the test tree, and drive a resource's route tests through the real router.

## Checks

Review each changed resource folder against the four roles: does a router hold database statements or transactions, or a query open or commit a session?
Compare the application's registered paths and methods before and after a code move; any difference is a URL change.
Review imports in changed resource folders for sibling or downward imports, or run the project's import-boundary linter.
Review each new sub-resource folder against the nesting test.
Request a static path that shares a prefix with a parameterized route and confirm its own handler answers.
