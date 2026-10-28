---
name: ui-react-typescript-jsx-attributes
message: Write inline JSX handlers as one expression, name declared ones `on` and their event, spread only declared style calls or story args, and name visible text and literal props.
requires-tenet: 0.11.0
---

## Rules

Write each function passed inline to an event attribute, one named `on` and a capital letter such as `onClick`, as an arrow whose body is one expression.
A body is one expression when it is neither a block nor a comma sequence, such as `onClick={() => saveDraft({ draft })}` or `onChange={(event) => setTitle(event.target.value)}`.
Move a handler that needs a block into a named function, and pass that function by name, such as `onSave={onSave}`.
Name that function `on` and what it handles, the same form as the prop it serves, such as `onSave` or `onArchiveOrder`, never `handleSave` or `save`.
Place and bind that function as `code-typescript-function-scoping` and `code-typescript-const-bindings` require.
A function that the component receives or imports, such as a prop or a state setter, keeps its own name, such as `onChange={setTitle}` or `onBack={onBack}`.
Never name a function that an inline event handler calls `handle` and what it handles, such as `handleSave`; name it for what it does, such as `saveDraft`.

Spread nothing into an element's attributes except the result of a declared style call and, in a story file, the story's `args`.
Declare the style calls whose result an element may spread, each a function of the repository's style library that returns an element's class name and inline style.
This contract's `assets/` folder declares one style library's call, and a repository replaces that list with its own in its copy.
Write the style call inside the spread, never a variable that holds its result.
A story file holds a component's stories, such as `orders.stories.tsx`, and the shipped files recognize one by its `.stories.tsx` ending.
Pass every other attribute by name, on native elements and components alike, including the props a component forwards to the element it wraps.

Take every string that markup shows a person, as a child or an attribute such as `placeholder` or `aria-label`, from a named constant or a message module.
A message module holds the visible strings of a feature in one source file without markup, such as a catalog that a translation library reads.
Pass no object or array literal as an attribute's value, directly or through a variable the component declares; hoist it to a module-level named constant.
Build an object or array that reads the component's props or state with `useMemo`, so each render passes the same value while its inputs stay the same.

Configure the repository's lint to report an inline event handler that is a block, a comma sequence, or a `function` expression.
Configure it also to report a declared handler passed to an event attribute under a name without `on`, and a `handle` function that an inline event handler calls.
Configure it also to report each spread into an element other than a declared style call or, in a story file, the story's `args`.
Configure it also to report a string written directly as a child in markup, and an object or array literal that a component passes to an attribute.
Where the repository's lint can load the configuration in this contract's `assets/` folder, load it from the repository's own lint configuration.
Suppress a finding only as `code-lint-suppressions` allows.

Violation: `<button onClick={() => { saveDraft({ draft }); closeEditor({ editor }); }}>` puts a block of two statements in an inline handler.
Violation: `function handleSave() { ... }` passed as `<Editor onSave={handleSave} />` names a declared handler with `handle`.
Violation: `<button onClick={() => handleSave({ draft })}>` calls a function named with `handle` from an inline handler.
Allowed: `function onSave() { saveDraft({ draft }); closeEditor({ editor }); }` in the component, passed as `<Editor onSave={onSave} />`.
Violation: `<OrderList {...state} />` spreads a hook's result into a component.
Allowed: `<OrderList orders={state.orders} onRefresh={state.onRefresh} />` passes each attribute by name.
Violation: `<h2>Orders</h2>` writes visible text in the markup, and `<OrderList filters={{ isArchived: false }} />` builds a new object on every render.
Allowed: `<h2>{orderMessages.heading}</h2>` reads the feature's message module, and `<OrderList filters={OPEN_ORDER_FILTERS} />` passes a module-level constant.

## Checks

Run the repository's lint from the repository root, and confirm it rejects a block arrow in `onClick`, a declared `handleSave` handler, and a spread hook result.
Run it also on a component, and confirm it rejects `<h2>Orders</h2>` and `filters={{ isArchived: false }}`.
For each event handler a change adds, is an inline one a single expression, and does a declared one's name start with `on`?
For each string a change shows in markup, as a child or a visible attribute, does it come from a named constant or a message module?
For each spread a change adds into an element, is it a declared style call written in the spread, or a story's `args` in a story file?
Does a change add to the declared style calls a function that returns anything other than an element's class name and inline style?
Does a change turn a rule off, or narrow the files, attributes, or spreads it checks?
