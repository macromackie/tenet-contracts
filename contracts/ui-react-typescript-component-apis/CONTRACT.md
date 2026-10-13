---
name: ui-react-typescript-component-apis
message: Encode supported component use in public prop types so unsupported combinations fail to compile.
---

## Rules

Treat each exported prop type as the component's supported surface, and make a combination that should not ship fail to compile.
Model mutually exclusive modes, such as controlled and uncontrolled state, as a discriminated union of prop types.
Type the props that belong to another mode as optional `never` in each union member.
Require the change callback in controlled mode.
Type visual choices such as `size`, `tone`, and `density` as string-literal unions, not open `string`.
Type catalogued choices such as icon names as a finite union of stable names, and keep the underlying library's component names private.
Make a prop required when the component cannot render correctly without it, such as the accessible label of an icon-only button or an empty-state message.
Allow `null` in a value type only where the component renders a gap or missing state for it.
Type content that the component renders verbatim, such as code or a label, as `string` rather than `ReactNode` or a pre-rendered element tree.
Make collection components generic over the record type, so their callbacks receive the caller's record type.

Export the package's own prop and value types, and keep third-party component, chart, positioning, and animation library types out of exported props.
Keep data-layer types, such as query builders, database collections, and transport state, out of exported props.

Guard a consequential rejected combination with a compile-time assertion such as `@ts-expect-error` rather than prose alone.

## Checks

Run the TypeScript compiler over the component package and its consumers.
Write the rejected combinations for a changed union, such as mixed controlled and uncontrolled props or a missing change callback, and confirm each fails to compile.
Review exported prop types for third-party library types, data-layer types, and open `string` where a finite set applies.
