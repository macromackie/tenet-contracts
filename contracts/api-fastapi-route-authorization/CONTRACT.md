---
name: api-fastapi-route-authorization
message: Declare route admission as named shared dependencies and apply ownership in the statement, never after loading.
---

## Rules

Declare every route's admission, meaning which principals and credential types may call it, as a FastAPI dependency.
Define each admission dependency once, as a named constant in a shared admission-policy module, and import it into routers.
Never build an admission dependency inline in a route signature or define a private copy in a resource's router.
Add a missing policy to the shared module beside the policies it extends.
Keep the admission-policy module a leaf: it loads no resource, opens no session, and imports no route module.
Declare a deliberately public route with a named public-admission constant, so every public route is explicit and enumerable.

Treat admission as entry only, and apply the owner or visibility scope that `security-resource-access-control` requires inside each query, update, and delete statement before it executes.
Never load an unscoped row and compare its owner afterwards in Python.
Pass the principal's scope from the admission dependency to the service and query explicitly.
Use an owner-bound scope for every route that writes principal-owned rows unless its admission policy names a wider write grant.

Override admission in tests through FastAPI dependency overrides keyed by the shared dependency, not by patching modules.
Keep an enumerated record of each route's admission, and update it in the same change that changes admission.

## Checks

Review each changed router: does every admission dependency come from the shared policy module or the public constant?
Review each changed statement for a scope applied before execution, on list, detail, update, and delete paths.
Review each POST, PUT, PATCH, and DELETE route for an owner-bound scope or a named wider write grant.
Regenerate the route admission record after changing dependencies, and confirm every difference is intended.
Exercise one resource as two different owners and confirm that own actions succeed and foreign actions are denied.
