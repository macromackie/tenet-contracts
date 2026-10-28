---
name: code-typescript-function-arguments
message: Give each owned TypeScript function that takes input one destructured object argument whose type carries its name, default there, pass callbacks as inline arrows, and keep external signatures.
requires-tenet: 0.11.0
---

## Rules

Give every owned function, method, and constructor that takes input a single object argument with named fields, even when it takes one input, such as `parse({ line })` instead of `parse(line)`.
Never give an owned function a positional parameter, exported or private, a declaration or arrow, a helper, a type's function member, or a callback owned code defines and calls.
Destructure the object argument in the signature, and pass a domain object as a named field of it, such as `computeTotal({ invoice })`.

Name each function's argument type its PascalCase name plus `Input`, such as `retryStep` taking `RetryStepInput`, and a component's, whose name starts with a capital letter, its name plus `Props`.
Name a method's or function member's argument type for the member alone, such as `PostInput` for `post`, and a constructor's or function type's for its class or type.
Name each overload's argument type for its function, a word for its case, and `Input`, such as `ListInvoicesByCustomerInput` and `ListInvoicesByPageInput` for `listInvoices`.
A function whose only caller passes it every field of that caller's argument, such as a case that `advance` calls, takes the caller's type, `AdvanceInput`.
Export an argument type beyond its module's folder only when another module needs to name it, and use a discriminated union when combinations of options would allow invalid states.

When an optional field of the argument object takes a default, give it where the signature destructures it, such as `function poll({ pollMs = POLL_MS }: PollInput)`.
Never default such a field where the body reads it, such as `input.label ?? 'untitled'`, `label ?? 'untitled'`, `label ??= 'untitled'`, or `label || 'untitled'`.
A default may read an earlier field or make a synchronous call, such as `{ start, end = start + DAY_MS }` or `{ client = createClient() }`.
When a default needs `await`, which a signature cannot hold, default the function that produces it, such as `{ readToken = readStoredToken }`, and await it in the body.
Default a field of a nested options object by destructuring that object in the signature, such as `{ retry: { attempts = MAX_ATTEMPTS } = {} }`.
A field of a domain value that the argument carries, such as `invoice.coupon`, is that value's data, and `code-typescript-boolean-conditions` decides how it is defaulted.
Declare a field that takes a signature default as optional, never as one that accepts `null`, because a signature default replaces only an omitted or `undefined` field.
Keep required fields required, add no default that hides missing caller input, and repeat no default for an optional field a function only forwards.

Write each function that a call takes as an argument inline, as an arrow or generator function naming the arguments it reads, such as `lines.flatMap((line) => parseLine({ line }))`.
Never pass a function by name, such as `emitter.on('message', recordMessage)`, because the callee decides its arguments; an object field or markup attribute, such as `onSave={onSave}`, may name one.
Remove a listener that an inline arrow registers by aborting its signal or calling its registration's stop function, such as from the finalizer of the scope that registered it.

Preserve signatures that the language, runtime, and dependencies define, including callbacks and entry points, and never wrap such a function only to turn its positional arguments into an object.
A function that a higher-order helper returns to forward a wrapped function's arguments unchanged keeps that function's signature.
A callback written directly as a call's argument, such as `matches.map((match) => match[1] ?? '')`, and a parameter whose type a dependency declares are outside the default and argument type rules above.

Configure the repository's lint to reject a body default for a parameter's field, an argument type without its suffix, and a function passed by name as a call argument.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Suppress a finding only as `code-lint-suppressions` allows, such as where a dependency declares a parameter's type or removes a listener only by name, naming that dependency.

Violation: a private helper declared as `function clip(text: string): string` takes its one input positionally, and `function formatTitle(input: FormatTitleInput)` returns `input.label ?? 'untitled'`.
Allowed: `function clipText({ text, maxChars }: ClipTextInput)`, `function formatTitle({ label = 'untitled' }: FormatTitleInput)`, and `orders.map((order) => order.id)`, whose callback signature belongs to `map`.
Violation: `function retryStep({ job }: RetryOptions)` names its argument type with another suffix, and `lines.flatMap(parseLine)` hands `parseLine` each line's index and the array.
Allowed: `function retryStep({ job }: RetryStepInput)`, `function InvoiceRow({ invoice }: InvoiceRowProps)`, `lines.flatMap((line) => parseLine({ line }))`, and `target.addEventListener('message', (event) => recordMessage({ event }), { signal })`.

## Checks

Run the repository's lint from the repository root, and confirm it rejects `input.label ?? 'untitled'`, a destructured `label ?? 'untitled'`, an argument type `RetryOptions`, `lines.flatMap(parseLine)`, and `emitter.on('message', recordMessage)`.
Read changed declarations and their call sites together, and confirm each call names its inputs and passes no imported or parameter-held function by name.
For each positional parameter, identify the external API that fixes the signature, and search the change for wrappers that only convert positional arguments into an object.
For each argument type a change names, is it the PascalCase name of its function, member, class, function type, or only forwarding caller, plus any case word and suffix?
Run the type check for the owning package and for affected consumers after a signature change.
For each default a change writes on a field of a field, such as `options.retry.mode ?? 'linear'`, is that field a domain value's data rather than a nested option?
For each defaulted field a change adds, does no caller pass `null` for it, and does each caller that forwards it pass it on without repeating its default?
