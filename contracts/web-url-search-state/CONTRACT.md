---
name: web-url-search-state
message: Validate URL search state in the destination route that owns it, and write only non-default choices.
---

## Rules

Let each destination route declare its accepted search parameters, their validation, and their defaults.
Declare ordinary page state at the route that renders it, not on a shared layout or shell.
Keep each feature's allowed values in its own route's schema; shared controls or navigation do not justify accepting another page's parameters.
Do not add a separate URL-state store, and do not copy control state into the address bar from component lifecycle callbacks.
Keep shareable view state, such as search text, filters, sort order, the selected item, and the pagination cursor, in the URL.
Keep the resource's identity in the path; a search parameter must not replace or override it.

Omit default values from URLs, and never serialize a missing value.
Resolve a missing parameter to the view's default, and keep a meaningful non-default false value.
Replace an invalid value with its default, and discard unknown parameters.
Normalize an incoming URL by replacing the current history entry, preserving its path and fragment, without redirect loops.
Treat URLs that differ only in parameter order as equivalent, and do not redirect only to reorder them.

Reset the pagination cursor when a filter or sort changes, and keep the filter while paging.
Let same-page updates keep that page's other parameters.
Start cross-page navigation from the destination's defaults or explicitly chosen destination state, never from the current page's parameters, even when both pages use the same parameter name.
Read controls from the validated route state, so direct links, reloads, and back and forward navigation show the same view.

Let sign-in and integration callbacks declare their protocol parameters and consume them before any ordinary cleanup runs.
Do not let generic cleanup strip a callback's protocol state or change a validated sign-in return destination.

## Checks

In a browser, open a clean default URL, choose a non-default value, reset it, load a URL with invalid and unknown parameters, reload, and go back and forward, recording each observed URL.
Navigate from a filtered page to an unrelated page, and confirm no parameter carries over.
Confirm that normalizing a URL adds no history entry and does not loop.
Review changed route schemas together with every navigation caller that targets them.
Exercise sign-in and integration callbacks separately, and confirm their protocol parameters survive until consumed.
