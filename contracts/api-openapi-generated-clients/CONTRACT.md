---
name: api-openapi-generated-clients
message: Generate the OpenAPI description from the live route registry, and publish pinned, framework-free clients from it.
---

## Rules

Generate the OpenAPI description from the application's registered routes and schemas, never from a hand-maintained file.
Declare public request and response schemas beside the routes that serve them, and keep persistence schemas out of the description.
Give every operation a stable operation ID, and document its error responses, pagination, and authentication requirements.
Keep protocol endpoints that a library owns, such as login callbacks, out of the product operations and the generated product client.
Fail the build when the committed description or generated client differs from what current source generates.

Generate client types from the checked description, and never hand-edit generated files.
Export supported types and client construction only through the client package's entry point.
Keep UI frameworks, database models, credentials, query caches, and browser navigation out of the client package.
Accept transport configuration, such as the base URL and request function, from the caller.
Leave credential storage and session lifecycle to the consuming application.

Publish each client as an immutable versioned build to a package registry, and have consumers pin a released version.
Do not publish a source-only client that needs another repository checkout to build.
Treat as breaking any change a released client cannot handle, such as a removed operation or response field, a new required request field, or a new response enumeration value; see `data-stored-and-shipped-formats`.

Do not treat generated types as validation: they check callers at compile time and never inspect a response body.
Validate response bodies at runtime against the declared response schemas, on the server before sending or at the client's entry point.
Review a public schema diff for changed meaning, defaults, and error behavior that type generation cannot detect.

## Checks

Regenerate the description and the client from current source and confirm there is no diff.
Build the client package and confirm it imports no UI framework, database model, or credential store.
Compile and exercise a consuming application against the packed or published client, not against its source.
Validate real responses from an integration flow against the published response schemas.
Review each public schema diff for changes that generated types would accept but callers would misread.
