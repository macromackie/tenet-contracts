---
name: ui-react-hook-calls
message: Name each state pair `[thing, setThing]`, and call state, ref, and context hooks before every other hook and effect hooks after them.
requires-tenet: 0.11.0
---

## Rules

Destructure every `useState` call into its value and setter, and name the setter `set` followed by the value's name with a capital first letter, such as `[draft, setDraft]`.
Bind the value alone only when it never changes and its initializer is an inline arrow function, such as `const [revision] = useState(() => order.revision)`.
Never bind a `useState` call's result to one name, skip its value, or return it without destructuring it, such as `return useState(false)`.

Inside each component and hook, call the state, ref, and context hooks, `useState`, `useReducer`, `useRef`, and `useContext`, before every other hook.
Call the effect hooks, `useEffect`, `useLayoutEffect`, and `useInsertionEffect`, after every other hook, so a body reads as state, then derived values, then synchronization.
A hook is a function whose name is `use` followed by a capital letter or digit, and a statement that calls no hook may stand anywhere in the body.

Configure the repository's lint to report a `useState` call that is not destructured into a `set` pair or a lazily initialized lone value.
Configure it also to report a state, ref, or context hook called after another hook, and any other hook called after an effect hook.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
The shipped rules check that a setter starts with `set` and a capital letter, and review checks that the rest repeats the value's name.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `const [notes, updateNotes] = useState('')` names the setter without `set`.
Violation: `const [revision] = useState(order.revision)` binds the value alone without an inline initializer.
Allowed: `const [revision] = useState(() => order.revision)` keeps the revision the component mounted with.
Violation: `const order = useOrder({ orderId })` followed by `const [isOpen, setIsOpen] = useState(false)` calls a state hook after another hook.
Violation: `const label = useMemo(() => formatOrder({ order }), [order])` follows a `useEffect` call in the same component.
Allowed: a component calls `useState`, then `useOrder({ orderId })` and `useMemo`, then `useEffect`.

## Checks

Run the repository's lint from the repository root, and confirm it rejects `const [notes, updateNotes] = useState('')` and a `useState` call after a `useEffect` call.
For each state pair a change adds, does the setter's name repeat the value's name after `set`, such as `setDraft` for `draft`?
For each lone state value a change adds, does the component never need to change it?
Does a change turn a rule off, or narrow the files or hooks it checks?
