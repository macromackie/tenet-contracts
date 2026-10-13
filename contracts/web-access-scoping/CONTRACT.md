---
name: web-access-scoping
message: Authorize every server entry point; scope private client data to its session and discard it on access change.
---

## Rules

Authorize inside each directly callable server entry point, such as a data loader, form or mutation handler, server function, or API route, before it reads restricted data; see `security-resource-access-control`.
A check in a layout, page, or navigation guard does not protect the loaders and mutations that page uses.
Authorize a restricted region before mounting the component that reads it, so a viewer without access never sends its requests.
Load public data separately from restricted data, so a public page does not depend on a restricted read.
Remove the fields a viewer may not see on the server, before the response reaches the browser.
Make elevated privilege an explicit request option, and do not let a visit to an elevated area elevate requests from ordinary pages.

On sign-out, account change, privilege change, or access loss, cancel private requests and discard private cached data, drafts, and remembered selection immediately.
Remove private views as soon as access ends, without keeping them visible through a transition.
Discard a late response for a previous session or privilege context so it cannot repopulate disposed state.
Preload private data only after a successful session check; an identity cached from an earlier session does not authorize preloading.
Show private navigation and account details only after the session check succeeds.
Offer a retry when the session check fails, rather than presenting the viewer as signed out.
Send an anonymous viewer of a protected page through sign-in, and return them to the requested destination.

Keep each viewer's private records out of server state shared between requests.

## Checks

Call each changed server entry point directly as an anonymous viewer and as a signed-in viewer without access, and confirm both are rejected before any restricted data returns.
Use the browser's network log to confirm a viewer without access never requests a restricted region's data.
Sign out, change account, and revoke access while a held response is in flight, and confirm private data disappears and the late response does not restore it.
Return from an elevated area to an ordinary page, and confirm its requests and cached data carry no elevated context.
Inspect a private page's server-rendered HTML for fields the viewer may not see and for other viewers' records.
