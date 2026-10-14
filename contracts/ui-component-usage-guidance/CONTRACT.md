---
name: ui-component-usage-guidance
message: Document each public component's purpose, use, alternatives, and status beside its source, and generate the catalog from it.
---

## Rules

Document every public component beside its source with its purpose, when to use it, and a nearby alternative or common misuse.
State in each component's guidance what the application must supply and decide, such as data, formatting, and permissions.
Document each non-obvious input where it is declared and each non-obvious example where it is defined.
Write guidance for what the interface cannot express, such as selection, composition, and misuse, rather than restating input types.
Mark each public component's support status in its source documentation, and define in the catalog what each status promises consumers.

Keep foundations, token use, component selection, and composition guidance in the component catalog beside the examples, not in application documentation.
Keep component guidance in source documentation, examples, or catalog pages, so the generated catalog exposes all of it.
Document the intended meaning and search terms of each name in a finite catalog of choices, such as icon names, beside that catalog's examples.

Generate the catalog and all agent-facing component metadata from component source, examples, and guidance pages, and never maintain a parallel registry.
List every public export in the generated catalog with its guidance and status.
Verify the inputs the catalog extracts for each component against its public interface.
Give coding agents the catalog through its supported query interface, and never read its generated metadata files from product code.

Keep a component private until its public behavior, types, examples, and guidance are complete.
Change a component's guidance and examples in the same change as its behavior or interface, so the catalog never describes another version.

## Checks

Build the catalog and confirm every public export appears with its purpose, usage, alternative, and status.
Compare the catalog's extracted inputs for each changed component with its public interface.
Query the catalog through its agent interface for a changed component, and confirm it returns that component's guidance and the guidance pages.
Search for hand-maintained component registries or metadata files, and for product code that reads generated catalog files.
Review changed public components: does the guidance say when to choose each over its nearby alternative, and what its types cannot express?
