---
name: web-server-state-cache
message: Keep server data in one client cache, keyed by every response-changing input and scoped to the viewer.
---

## Rules

Keep interactive server data in the application's one client cache.
Do not add a second cache, store, or router-level freshness layer for the same responses.
Do not start interactive reads from component lifecycle callbacks; subscribe to them through the cache.
Pass data loaded on the server for the first render directly to the page, or seed it into the cache entry the client will refresh, but never keep both as independent copies.

Define each read once, beside the route or feature that owns it, with its request, key, and freshness together.
Reuse that definition wherever another screen or a navigation preload reads the same resource.
Include in the key every resource identifier, filter, sort, cursor, and request option that changes the response.
Include the viewer and privilege context in the key, or give each viewer a separate cache instance.
Nest related keys under shared prefixes, such as viewer and then resource, so invalidation, cancellation, and removal can address them together.
Cache response data, and format it only when building presentation values.

Send each read through the existing typed transport for its endpoint owner; do not add a parallel request client.
Pass the cache's cancellation signal through the transport to the network request, and keep the transport's deadline as well.
A late response for a previous key must not replace the data shown for the current key.
Request the next page with the cursor the server returned.

Let navigation wait only for reads that have no cached entry, and refresh cached entries after the destination shows them; see `ui-async-read-states` for presenting retained data and refresh failures.

## Checks

Trace one changed read from its definition through the transport, and confirm its key contains every input the request sends.
Settle an older request after a newer one with controllable responses, and confirm the older request was cancelled and the visible data belongs to the current key.
Navigate to a view whose reads are cached, and confirm it renders without waiting for their refresh.
Switch viewer or privilege context, and confirm no entry from the previous context is served.
Search the change for new cache libraries, parallel request clients, and reads started from component lifecycle callbacks.
