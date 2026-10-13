---
name: ui-presentation-state
message: Hold only ephemeral interaction state and unsaved drafts in presentation; receive application-owned state as inputs.
---

## Rules

Hold only ephemeral interaction state in presentation components: disclosure, unsaved drafts, focus, hover, and in-progress gestures.
Receive server data, persisted preferences, shareable view state, and any selection the application acts on as input values with change callbacks.
Derive displayed values from current input values, and keep a separate local value only for a distinct interaction state, such as a held selection, never as a copy of a supplied record.
Give each value one owner at a time; a component that can either hold a value or receive it as an input must not keep a second copy of a received value.

Render supplied collections in the supplied order.
Do not filter, sort, paginate, fetch, or mutate supplied records inside a component.
Report sorting, filtering, pagination, and search changes through callbacks, and let the application compute the resulting records.

Keep unsaved edits in a draft separate from the saved data, and show the saved data when no draft exists.
Keep an unedited form showing refreshed saved data, and never overwrite an edited draft when saved data refreshes.
Submit a draft only from an explicit save action or a declared autosave trigger; selection, focus, and hover never submit one.
Keep the draft when a save fails or is rejected, and clear it only after the save succeeds.
While a save is pending, disable conflicting edits or clear only the submitted part of the draft, so later edits survive.
Reset the draft when the record it edits changes, and never let a late save result clear or fill the draft of another record.

## Checks

Review each piece of local state in changed components: is it disclosure, draft, focus, or other ephemeral interaction state that the application never needs?
Change a supplied value from outside the component and confirm it shows the new value without a stale local copy.
Trigger sorting, filtering, and pagination, and confirm the callbacks change the application's query rather than reorder records inside the component.
Refresh saved data during an edit, fail a save, and switch records while a save is pending, and confirm the draft survives the first two and never appears on the other record.
