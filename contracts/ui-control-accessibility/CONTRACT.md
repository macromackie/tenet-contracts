---
name: ui-control-accessibility
message: Use semantic, named, keyboard-operable controls and managed overlays that contain, dismiss, and return focus.
---

## Rules

Use native elements for links, buttons, tables, and form controls whose built-in behavior is sufficient.
Use the adopted control library for custom selection, toggles, menus, dialogs, and tooltips instead of hand-built equivalents.
Use links for navigation and buttons for actions; never make one imitate the other.
Give exclusive choices radio behavior, independent pressed state a toggle, submitted choices a checkbox, and immediately applied settings a switch.
Preserve native naming, form submission, disabled, read-only, required, and invalid semantics.
Keep native table semantics, and expose the sort state of each sortable column header.

Give every control an accessible name, and give an icon-only control an explicit text label.
Convey state with text or shape in addition to color.
Expose a disclosure through a labeled button that reports its expanded state.
Make scrollable content regions keyboard-focusable and give them accessible names.

Support the keyboard actions that the platform's interaction pattern defines for each control, such as Enter, Space, arrow keys, Home, End, and Escape.
Show a visible focus indicator during keyboard navigation.
Keep interactive targets at or above the declared minimum size on coarse pointers.
Change a selection only on activation by click, tap, or key press; hover or focus alone must not change a selection, start requests, or change destinations.

Delegate focus containment, Escape and outside-press dismissal, background scroll locking, and layering of overlays to the adopted control library.
Open at most one modal overlay at a time.
Name the affected record in a destructive confirmation.
Return focus to the invoking control when an overlay or disclosure closes, or to a surviving related control when the invoker was removed.

## Checks

Operate each changed control with a pointer and with Tab, Shift+Tab, arrow keys, Enter, Space, and Escape as applicable.
Inspect each changed control's role, accessible name, and state in the accessibility tree.
Open and close each changed overlay by keyboard, and confirm initial focus, focus containment, Escape, outside press, and focus return.
Search changed code for hand-built focus traps, global Escape handlers, and background scroll changes; a global key listener alone is not a violation.
Review changed state indicators with color removed.
Run the repository's automated accessibility checks where they exist; they do not replace keyboard review.
