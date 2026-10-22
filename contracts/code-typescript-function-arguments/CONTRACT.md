---
name: code-typescript-function-arguments
message: Give every owned TypeScript function that takes input one destructured object argument; keep externally defined signatures.
---

## Rules

Give every owned function, method, and constructor that takes input a single object argument with named fields, even when it takes one input, such as `parse({ line })` instead of `parse(line)`.
Pass a domain object as a named field too, such as `total({ invoice })`.
Never give an owned function a positional parameter, whether it is exported or private, a declaration or an arrow function, a helper or an interface method.
Destructure the object argument in the signature.

Export an options type beyond its module's folder only when another module needs to name it.
Use a discriminated union when combinations of options would otherwise allow invalid states.
Keep required fields required; do not add defaults that hide missing caller input.
Give a callback that owned code defines and calls a single object argument as well.

Preserve signatures defined by the language, the runtime, frameworks, and other dependencies, including their callbacks and entry points.
Do not wrap an external function or callback only to convert its positional arguments into an object.
A function that a higher-order helper returns to forward a wrapped function's arguments unchanged keeps that function's signature.

Violation: a private helper declared as `function clip(text: string): string` takes its one input positionally.
Allowed: `function clipText({ text, maxChars }: ClipTextInput)`, and `orders.map((order) => order.id)`, whose callback signature belongs to `map`.

## Checks

Read changed declarations and their call sites together, and confirm each call names its inputs.
For each positional parameter, identify the external API that fixes the signature.
Run the type check for the owning package and for affected consumers after a signature change.
Search the change for wrappers whose only job is converting positional arguments into an object.
