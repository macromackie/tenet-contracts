---
name: ui-semantic-value-controls
message: Give each value domain one control whose name states its value contract, and keep application policy outside it.
---

## Rules

Provide exactly one shared control for each value domain, and name it for the value it accepts and reports rather than for its appearance.
Express appearance differences within one value domain as named variants of its control, not as a second control; see `ui-design-tokens`.
Give every appearance of a control the same value contract, keyboard behavior, and selection behavior.

Edit a single-line string with the text control, and limit its modes to string formats such as email, password, or native search.
Edit a number with the number control, never with a text control in a numeric mode.
Edit search text that needs a clear action with the search control, and make clearing empty the value and report the change.
Choose one value from a fixed list no longer than a declared length with a select control, and from a longer or application-supplied list with a searchable option control.
Choose exactly one view or filter from a few always-visible options with a single-selection group, such as a segmented control.
Choose between a checkbox and a switch for a boolean value as `ui-control-accessibility` requires.

Pass the change callback the domain value, such as a string, number, boolean, or option value, in either mode, never a raw input event or display text.
Identify each option by a stable value separate from its label, and report the selected value rather than its label or position.
Report a cleared number or selection as an explicit empty value, never as zero, an empty string, or the first option.

Accept either a controlled value with a required change callback or an initial value, never both, and reject a controlled value without a change callback.
Return an uncontrolled control to its initial value when its form resets.

Keep domain parsing, debouncing, query and URL state, and validation policy in the application, outside value controls; see `ui-presentation-boundaries`.
Report search text on every change, and let the application debounce the request it derives.
Receive options, constraints, and invalid state with its message as inputs from the application, and never fetch options or decide domain validity inside the control.

## Checks

For each new or changed control, name its value domain and confirm no other shared control already covers it.
Render each changed control controlled and uncontrolled, then with both a value and an initial value, then with a value but no change callback, and confirm the last two are rejected.
Submit and reset a form holding each changed control, and confirm the submitted and reset values.
Clear each changed number, selection, and search control, and confirm the callback receives an explicit empty value.
Inspect change callback payloads for domain values rather than events, labels, or positions.
Review changed controls for parsing, debouncing, requests, URL access, or validation decisions.
