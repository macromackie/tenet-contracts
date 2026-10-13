---
name: ui-time-series-charts
message: Render application-prepared series faithfully and give pointer, touch, and keyboard users the same inspected values.
---

## Rules

Accept finite, strictly increasing timestamps in a declared unit and exactly one value per series per timestamp.
Reject malformed series input instead of repairing it.
Represent a missing observation as an explicit missing value and draw it as a gap, never as an invented or interpolated value.
Require stacked series to supply observed, nonnegative values, and let the application decide when an absent count means zero.
Keep fetching, bucketing, ranking, weighted metrics, and remainder groups in the application; stacking supplied additive values is rendering geometry.
Align every annotation marker with an observation timestamp, and make each point marker reference an existing series and supply its value.

Space observations by elapsed time, not by index.
Start stacked areas at zero, and fit line charts to the observed values, including context series.
Use linear interpolation, and add smoothing, animation, or other scale options only for a stated consumer requirement.
Format timestamps and values with caller-supplied formatters.
Keep supplied partial-period markers visible, including during inspection.
Render a single observation visibly, and show an explicit empty state when no observations exist.

Assign automatic series colors from shared tokens in supplied series order, and let explicit colors consume no automatic slot.
Let the application pin a series color when its identity must persist across filters, ranks, or charts, and render remainder groups in a neutral color.

Give pointer, touch, and keyboard users the same inspected values, including marker descriptions.
Make the plot focusable, with arrow-key and Home and End inspection, a visible focus indicator, and an accessible current value.
Drive the inspection line, values, and annotations from one inspected timestamp.
Show inspection details in one chart-owned surface that consumers do not rebuild.
Expose inspected values as text, not only as graphic marks.
Support touch inspection without blocking scrolling of the surrounding content.
Dismiss inspection details on Escape or an outside press, and keep keyboard focus on the plot after Escape.
Keep inspection open when equivalent observations arrive in new arrays, and close it when values, series identity, or markers change.
Keep inspection details inside the viewport and in the active theme, and keep series legends visible while idle.

## Checks

Render examples with a gap, irregular intervals, a single observation, a partial period, and no observations.
Inspect one timestamp by pointer, touch, and keyboard, and confirm the displayed values equal the supplied values.
Replace the data with equivalent arrays and then with changed values, and confirm inspection persists and then closes.
Review consumer projections for units, aggregation, timestamp order, and color identity.
Inspect light and dark themes and a narrow layout with inspection details open.
