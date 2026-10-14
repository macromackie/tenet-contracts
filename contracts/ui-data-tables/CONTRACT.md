---
name: ui-data-tables
message: Render application-prepared rows as given, and report sorting and paging through controlled values and callbacks.
---

## Rules

Pass a data table rows that the application has already filtered, ordered, projected onto the table's columns, and windowed to the current page.
Give a data table no inputs that process rows, such as a page size, comparator, filter predicate, search text, or data loader; see `ui-presentation-state`.
Use an internal table engine, when there is one, only for its row and column model, and enable none of its sorting, filtering, grouping, or pagination processing.
Define rows, columns, sort values, and pagination values with the table's own presentation types, never with data-access types or the internal table engine's types.

Require a caller-supplied identifier for every row and a unique identifier for every column that stays the same when its header text, position, or visibility changes.
Model sorting as a controlled value naming a column identifier and direction, and show each header's sort state from that value rather than from the last click.
Activate sorting through a button in each sortable header cell, and expose the sort state on that header as `ui-control-accessibility` requires.
Mark a column sortable only when the application's query can order every matching record by it, not just the rows on the current page.
End the application's order for every sortable column with a unique row key, so paging neither repeats nor skips rows whose sort values tie.

Model pagination as controlled values from the application, such as a position label and whether previous and next pages exist, with callbacks that request a move.
Take the availability of previous and next pages from the application's query result, never from the number of supplied rows.
Hold sort and pagination values in the application, and in the URL when they are shareable view state; see `web-url-search-state`.

Give every data table a caption that names its records, either visible or exposed to assistive technology.
Require a caller-supplied empty-state message, so the application can say whether no records exist or none match the current filters.
Show the empty-state message in place of rows when the supplied rows are empty, and leave pending and failed reads to `ui-async-read-states`.

Use a data table to compare several records across shared columns, not to lay out one record's labels and values or to arrange a page.
Build custom table structures, such as grouped headers, spanning cells, or expandable rows, from the lower-level table primitive instead of adding options for them to the data table.

## Checks

Review the data table's public interface for row-processing inputs, data-access types, and internal table-engine types.
Supply rows in an order that no column defines, and confirm the table renders that order.
Activate a sortable header and a page control with callbacks that do not apply the change, and confirm the rows, header sort state, and page position stay as supplied.
Page through a sorted query whose sort column has tied values, and confirm no row repeats or goes missing.
Render an empty result and inspect the caption, empty-state message, and header sort states in the accessibility tree.
Review changed custom table layouts: are they built from the lower-level primitive rather than as data-table options?
