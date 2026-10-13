---
name: ui-storybook-component-checks
message: Give every public component synthetic stories of its meaningful states and assert only consequential owned interactions.
---

## Rules

Give every exported component at least one story, alone or in a representative composition.
Show each supported variant and meaningful state as a story, including populated, empty, loading, initial failure, refresh failure with retained data, disabled, and denied states where the component owns them.
Do not repeat a story per theme or viewport; add a narrow-viewport story only when the layout changes behavior at that size.
Document a primary component and its public subcomponents in one story file's metadata, so the generated documentation covers both.
Cover private parts through their public component, and do not add stories or exports for internal extractions.

Render stories from fixed synthetic data, without application providers, live services, production records, or credentials.
Build Storybook with the same compiler and styling configuration as the application.

Add a `play` function only for a primary owned interaction or a distinct consequential failure that existing coverage would miss.
Assert outcomes through accessible roles, visible state, and callback payloads.
Do not assert style classes, incidental markup, or each intermediate step of an interaction.
Let composition-only wrappers rely on their children's coverage.
Reproduce timing-dependent states with story inputs or gated responses, and never assert exact timing.
Do not treat a passing story as proof of application wiring, authorization, or real requests.

## Checks

Compare exported components with story files and confirm each has a story.
Build the Storybook catalog without application services.
Run the interaction tests for changed `play` functions locally, and confirm the selected stories actually execute.
Review each new `play` function against `test-curation`: does it guard a consequential, owned interaction?
Inspect changed stories in every supported theme, at a narrow viewport, and with the keyboard.
