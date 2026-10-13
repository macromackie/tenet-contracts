---
name: ui-design-tokens
message: Name shared visual decisions as semantic tokens and expose named variants, not unrestricted style overrides.
---

## Rules

Define shared color, typography, spacing, radius, elevation, layer, control-size, breakpoint, and motion-timing decisions as semantic tokens in one token source.
Name tokens for their role, such as surface, danger, or control height, not for their raw value.
Keep literal palette values in the token source, and do not define feature-local themes.
Give each foreground color token at least the declared contrast ratio against every surface token it is used on, in every supported theme.
Reference tokens for shadows, stacking order, transition and animation timing, and interactive target sizes.
Use named breakpoint and user-preference conditions instead of repeating raw screen-size or preference checks.
Add a token when more than one component shares a new visual decision.
Do not extend a feature-specific accent to unrelated controls.
Keep structural literals local when they describe content geometry or rendering mechanics, such as grid tracks, percentages, border widths, focus offsets, and glyph or chart geometry.

Expose supported visual choices as named variants, such as size, tone, density, and padding.
Do not accept unrestricted style overrides, such as arbitrary style classes or style values, on public components.
Accept placement of a component's root only through a constrained layout input.
Style application composition through the application's own wrappers rather than by overriding shared components.
Do not restyle a shared component's internal parts or its focus, dialog, or disabled states from application styles.
Keep one styling system per component, and never define the same element's properties in two systems.

Keep global styles in application shells, and do not make components depend on a shell's global styles for their appearance.

## Checks

Review each new literal in changed styles: is it structural geometry, or a reusable color, spacing, typography, elevation, layer, or motion decision?
Search changed public component inputs for unrestricted class, style, or style-object parameters.
Render changed components in an isolated catalog without application styles, and compare them with the visual reference.
Check the contrast of changed color tokens against the surfaces that use them in every supported theme.
Run the repository's existing style lint for literals and repeated conditions where it exists, and review the rest by hand.
