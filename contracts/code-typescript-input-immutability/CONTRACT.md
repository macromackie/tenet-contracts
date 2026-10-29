---
name: code-typescript-input-immutability
message: Never change a TypeScript function's input, sort in place, or use `delete`, and type arrays and tuples `readonly` except a local or private field its owner fills.
requires-tenet: 0.11.0
---

## Rules

Never assign to a parameter, or to a property at any depth of an object that a parameter holds, such as `order.status = status` or `order.totals.net = net`.
Never call a method that changes a collection a parameter holds at any depth, such as `push`, `splice`, `sort`, `reverse`, `set`, `add`, `delete`, or `clear`, and never pass a parameter's value as the target of `Object.assign`.
Changing a field of `this` in the class's own method, such as `this.#cache.set(key, value)`, is not changing a parameter.
A collection that the function itself created, such as an array, `Map`, or `Set`, may change before the function returns it, except through `sort`, `reverse`, or the `delete` operator.
`code-typescript-effect-absent-values` decides whether code may assign a field of an object that the function created.
Sort or reverse an array with `toSorted` or `toReversed`, never with `sort` or `reverse`.

Never use the `delete` operator, which leaves the key in the object's type; drop a key by rest destructuring, such as `const { secret, ...publicRecord } = record`.
Drop a run-time key with a computed key, such as `const { [name]: dropped, ...kept } = headers`, and filter a lookup's entries as `code-typescript-runtime-keyed-maps` requires.
A test file, matched by a declared path pattern, may delete an environment variable it changes, such as `delete process.env.ORDER_API_URL`, because assigning `undefined` stores the string `'undefined'`.
Such a test restores each variable it changes, never by replacing the whole environment object, which code that read it earlier still holds.

Write every array type as `readonly T[]` and every tuple type as `readonly [A, B]`.
This holds in a parameter, an object or class property, a return type, a type alias, a type argument, and a module-level constant.
The compiler then rejects `push`, `sort`, `splice`, and index writes on the value wherever it travels, not only where a parameter first receives it.
Schemas that `code-typescript-effect-schemas` requires already decode arrays to read-only types, so a mutable parameter type would refuse decoded data.
One exception is a local variable's own annotation inside a function body when the function builds the array, such as `const rows: Row[] = []` before `rows.push(row)`.
The other is the annotation of a private `#name` field that only its own class fills, such as `readonly #entries: Entry[] = []`, since no caller can reach it.
A public field, a getter's return type, and every parameter stay `readonly T[]`, even when they hold or return that private array.
A type inside either annotation, such as the `Row[]` in `Map<string, Row[]>`, is still written `readonly`.
Never write an array type as `Array<T>` or `ReadonlyArray<T>`, including in a local variable's or a private field's annotation.
When a dependency's declared type requires a mutable array, pass it a copy, such as `[...rows]`, and keep the value's own type read-only.

Give each parameter that declares its type a deeply read-only type, such as `type AddLineInput = { readonly line: Line; readonly order: Order }`.
Write a dependency's type in its read-only form, such as `Readonly<AbortSignal>`, and write as declared each type that has none, such as `Request`, and each type that `code-typescript-effect-errors` or `code-typescript-effect-absent-values` requires, such as a tagged error class or an `Option`.

Configure the lint to reject each forbidden form wherever a tool supports it, except a test file's `delete` of an environment variable, and to ignore keys rest destructuring drops.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `function addLine({ order, line }: AddLineInput) { order.lines.push(line); }` changes a collection the caller passed in.
Violation: `type Order = { lines: Line[] }` lets any code that receives an order push to its lines.
Violation: `function settle({ invoice }: SettleInput)` with `type SettleInput = { invoice: Invoice }` takes a parameter whose `invoice` property is not `readonly`.
Violation: `delete copy.secret` changes `copy` and leaves `secret` in its type.
Allowed: `function addLine({ order, line }: AddLineInput) { return { ...order, lines: [...order.lines, line] }; }` returns a new order.
Allowed: `type Order = { readonly lines: readonly Line[] }`, and `const ids: string[] = []` inside the function that fills and returns `ids`.
Allowed: `const { secret, ...publicRecord } = record`, and `delete process.env.ORDER_API_URL` in a test that restores a variable absent before it.

## Checks

Run the lint and `assets/` rules from the repository root, and confirm they reject `lines: Line[]`, a local `Array<Line>`, `delete copy.secret`, and `order.lines.push(line)`.
From the package directory, run the package's type check.
For each value a change modifies in place, did the same function create it?
For each mutable array type a change writes in a local's or a private field's annotation, does only that function or class fill the array?
For each array type and parameter property that the lint does not reach, such as an array's element that is itself an array or the `invoice` in `{ invoice: Invoice }`, is it written `readonly`?
For each copy a change passes to a dependency, does the dependency's declared type require a mutable array?
For each environment variable a test changes or deletes, does the test restore its earlier value or absence one variable at a time, never by replacing the environment object?
