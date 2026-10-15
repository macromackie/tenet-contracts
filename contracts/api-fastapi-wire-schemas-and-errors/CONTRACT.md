---
name: api-fastapi-wire-schemas-and-errors
message: Declare explicit wire models, keep secrets on mint responses only, and map each failure to one status and detail.
---

## Rules

Define each resource's request and response models in its schema module, with a type on every field.
Forbid unexpected fields on a request model whose shape is closed.
Declare a response model for every route, through its return annotation or `response_model`.
Never return a storage or ORM object, or an untyped dictionary, as an implicit response.
Build each response from the fields the wire exposes; never dump a storage model wholesale into a response.
Keep each conversion function, which builds a response model from storage objects, pure: it selects fields from already loaded objects and never queries, commits, calls clients, or generates secrets.
A service operation may still call clients before or after it calls a conversion, such as calling another service after its commit.
Reuse a shared response model when its owner already defines the wire shape, instead of copying it.
Preserve existing field names and wire types when refactoring schemas.

Return a minted secret only through a response model that its minting route alone uses, and keep secrets and their hashes out of every other response model; see `security-api-key-lifecycle`.

Map each domain failure to one HTTP status and one detail shape, and use that mapping in every route that can produce the failure.
Keep the failure mapping in one place a reviewer can read, with any resource-specific exception stated beside it.
Translate domain failures into HTTP responses in exactly one layer, such as the service or an exception handler, and keep that translation out of every other layer.
Give malformed input, a conflict with current state, and a consumed, revoked, or expired capability distinct statuses.
Follow `security-resource-access-control` for the status a request for an inaccessible resource receives.

Name each database constraint the code reacts to once, beside the model that declares it, and compare the violated constraint against that name rather than a string literal.
Catch an integrity error only around the write or commit that can raise it, map only the named constraint, and re-raise any other cause.
Chain the original exception when raising a mapped error.
Catch only the specific exception type a library raises for bad input; never catch a broad exception to produce a client error.
Leave unmapped failures unhandled, so the client receives only a generic server error.

## Checks

Review every changed route for a declared response model.
Review changed conversions for I/O, client calls, or secret generation.
Confirm that list, detail, update, and delete responses cannot carry hashes, plaintext secrets, or unrelated storage fields.
Review each raised HTTP error against the mapping, and confirm it comes from the chosen layer only.
Review each `except` clause in changed code for a specific exception type, a single write or commit, a named constraint, and a chained re-raise.
