---
name: ui-keyboard-shortcuts
message: Register each keyboard command with its action owner, in the narrowest scope, without overriding typing or native keys.
---

## Rules

Register each application keyboard command beside the application code that owns its action, not inside a presentation component.
Let the shared component library provide the key-binding mechanism, and let the application declare each command, its binding, and its eligibility.
Register a command that many views share once, at the owner those views share, and do not add per-view listeners for the same binding.
Unregister each binding when its owner is removed or its command is turned off, so no binding outlives its action.

Attach each binding to the smallest focus region that contains its action, such as an editor, a list, or a panel.
Bind a command to the whole document only when it declares the routes where it is active and whether it runs while a modal overlay is open.
Never let a command run an action of the view behind an open modal overlay.

Ignore key events that originate in text fields, editable content, and other text-entry controls by default.
Opt a command into text-entry contexts only when it is the editor's own command, such as submitting the message being composed.
Leave native text editing, selection, and in-page find keys working in forms, dialogs, and document content.

Invoke the same action, with the same eligibility checks, as the visible control that performs the command, so a binding never does what the control would refuse.
Ignore auto-repeated key events for commands that write, submit, or delete.
Let each key event run at most one command.
Consume a key event only when a command runs, and leave unmatched keys to their native behavior.
For a multi-key sequence, keep each earlier key's native behavior, consume only the key that completes the sequence, and reset the sequence after a declared time window.

Leave activation, menu and list navigation, overlay dismissal, and focus movement to native elements and the shared component library, and do not bind commands that replace them; see `ui-control-accessibility`.
Do not bind keys that the operating system, browser, or assistive technology reserves, such as those that close or switch tabs, focus the address bar, open a link in a new tab, or drive a screen reader.
Give a binding that uses a single character key without a modifier a setting to turn it off or remap it, or activate it only while its focus region has focus.

Define each binding once, and derive every displayed shortcut label, tooltip, and help entry from that definition.
Write bindings with a platform-neutral primary modifier, and display the key names of the current platform.

## Checks

Type ordinary text containing each new binding's keys into every text field in the affected view, and confirm only an opted-in editor command runs.
Open a modal overlay over a view with an active command, press the binding, and confirm the background action does not run.
Hold down a write command's binding, and confirm the action runs once.
Make the visible control ineligible and press the binding, then remove the owning view and press it again, and confirm nothing runs either time.
Compare displayed shortcut labels with the binding definitions on each supported platform.
Review new bindings for scope, activation conditions, repeat handling, conflicts with other bindings, and reserved keys.
