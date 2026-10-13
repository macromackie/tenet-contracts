---
name: ui-async-read-states
message: Present pending, empty, failed, and refreshing reads truthfully, without false empties, flashing loaders, or displaced content.
---

## Rules

Present each read as exactly one of pending, failed, or ready, with refresh status attached to ready data.
Treat a result that has not arrived as pending, never as empty or zero.
Show an empty or not-found view only after a successful read establishes that result.
Treat an open connection or subscription as pending until its first snapshot arrives.
Show a failed initial read as an actionable failure with a retry, never as an empty result.

Keep usable results visible while the same resource refreshes or reconnects for the same viewer.
Show refresh progress, and a refresh failure with its retry, beside the retained results.
Preserve focus and scroll position through pending, failed, and successful refreshes.
Show a newly selected resource as pending until its own result arrives, rather than keeping the previous resource's results on screen.

Delay placeholder visibility by one shared declared delay, so a fast read completes without a visible loader.
Do not impose a minimum loading duration or replay the loader on each refresh.
Render a result that is ready at mount, including a cached empty result, immediately and fully visible.
Reveal a view's heading, permission-dependent actions, and primary content together.

Reserve the space of pending content immediately, so its arrival does not move surrounding content.
Build placeholders from the same layout definitions as the loaded view for known headings, toolbars, columns, and control sizes.
Do not invent records, counts, or permissions to make a placeholder look complete.
Never mount a hidden form or editor only to measure it.
Show one loading indicator per region; nested regions must not stack fades or replace each other's loaders.

Hide decorative loading visuals from assistive technology and make them noninteractive.
Mark the pending region busy, and announce loading once, after the shared delay.
Do not let loading transitions move keyboard focus or delay failure or denial feedback.

## Checks

Hold a read pending beyond the shared delay, then release it, and confirm the placeholder appears only after the delay and the content does not shift surrounding layout.
Complete a read faster than the delay and confirm no loader appears.
Exercise a successful empty read, a failed initial read, a failed refresh after success, and a resource switch, and confirm each shows its own state.
Reopen a cached populated view and a cached empty view, and confirm both appear immediately at full visibility.
Compare held-pending and loaded views at the same viewport for heading, row, and control positions.
Inspect the pending region in the accessibility tree for its busy state and a single announcement.
