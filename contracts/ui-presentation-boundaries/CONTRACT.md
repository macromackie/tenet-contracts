---
name: ui-presentation-boundaries
message: Render supplied data and report intent; leave requests, routing, identity, and domain decisions to applications.
---

## Rules

Render presentation components from explicit input values and report user intent through callbacks.
Keep requests, caches, routing, authentication, authorization, persistence, validation policy, analytics, and domain decisions in the application.
Do not import application source, network or API clients, routers, data-fetching or cache libraries, credential stores, or generated transport types into presentation code, including through type-only or relative imports.
Accept presentation-shaped records; the application converts API responses, query results, and stored models before passing them in.
Let the application map domain concepts onto presentation choices, such as an order status onto a badge tone.
Receive internal navigation through an application-supplied link renderer or destination value, not through a router import.
Render the permission state the application supplies instead of deriving access decisions in presentation.
Pass independently loaded regions into a component as ready content through named slots, never as pending requests for the component to resolve.

Limit a shared component library to product-neutral visual and interaction primitives, such as controls, layout, typography, and tokens.
Keep product entities, status mappings, and business rules out of the shared component library.
Keep the shared component library independent of every application and feature presentation package that consumes it.

Keep a feature view's components, presentation types, display formatting, styles, and examples together in one folder or package.
Do not split one view between a presentation package and application-local components.

Give each third-party UI library one stated responsibility, and import it only inside the components that wrap it.
Declare dependencies used only by examples or the component catalog as development dependencies.

Keep every presentation component renderable in isolation from synthetic inputs, without application context, live services, network access, or credentials.

## Checks

Inspect changed presentation manifests and imports, including type-only and relative imports, for application, transport, routing, or data-access dependencies.
Render each changed component in isolation from synthetic inputs with no application context or services.
Trace one user action from its presentation callback to the application handler: does the application own the request and the domain decision?
Review new shared-library exports: does any export name a product concept, status mapping, or business rule?
Review changed presentation event handlers and lifecycle code for requests, persistence, or cache work, which an import check cannot see when it arrives through an injected function.
