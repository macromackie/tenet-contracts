---
name: ui-react-interaction-ownership
message: Keep each interaction's state, transitions, subscriptions, and cleanup under one component or hook.
---

## Rules

Keep each state value and the handlers that maintain its invariants in the same component or hook.
Extract an interaction into a named hook only when the hook owns its complete lifecycle, and do not split its state, events, and effects across separate hooks or files.
Compute values derivable from props and state during render instead of mirroring them into state through an effect.
Preserve controlled and uncontrolled ownership when extracting code.
Let child parts render their item and report actions without duplicating the owning component's state.

Set up and tear down each subscription in the same effect, disconnecting observers, removing listeners, and cancelling timers.
Ignore asynchronous results that complete after their owner unmounts or after the input they were started for changes.
Coordinate a surface's close request, exit animation, and unmount in one owner, so a callback from an earlier cycle cannot close a reopened surface.
Reset or close interaction state when the data it refers to changes identity, so it never stays attached to replaced data.

Call hooks unconditionally at the top level of components and hooks.
Keep state above a conditionally rendered child when it must survive that child's unmounting.
Preserve mount, reset, focus, and announcement behavior when moving a component.
Keep child components independent of the parent that composes them, and move values they share with it into a module beside both instead of importing them from the parent.

## Checks

For each mutable value, identify the owning component or hook, the events that change it, and what ends its lifetime.
Exercise focus, dismissal, and controlled updates through the public component rather than asserting private hook state.
Reopen a surface during its exit and replace data during an interaction, and confirm stale callbacks neither close the surface nor leave state on replaced data.
Review each moved component against its previous owner for changes in state lifetime, effect cleanup, focus, or callback timing.
Run the React hooks lint rules, knowing that lint does not establish lifecycle correctness.
