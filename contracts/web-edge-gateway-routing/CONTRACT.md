---
name: web-edge-gateway-routing
message: Route exact origins and paths to configured private upstreams, keep credentials away from static and shell upstreams, and hold no authority.
---

## Rules

Match each request's host against the configured public origins exactly, and reject any other host.
Route API paths, such as `/api` and everything beneath it, before application paths, so no application route can shadow an API route.
Match path prefixes on whole segments, so `/api` never matches `/apiary`.
Serve each route only on the origins configured for it, such as browser sign-in only on the application origin.
Reject paths with encoded separators, such as `%2F` or `%5C`, encoded dot segments, and other ambiguous or invalid encodings before forwarding.
Select each upstream only from configuration, never from a host, header, path, or query value in the request.
Keep upstream services private, reachable only through the gateway.

Remove client-supplied forwarding headers, such as `Forwarded` and `X-Forwarded-For`, and set them from what the gateway observed.
Replace any client-supplied request identifier with one the gateway generates.
Forward the public URL the client requested, so upstreams build redirects and callbacks for the public origin.

On API routes, forward authorization headers, cookies, and the `Origin` header unchanged.
On API routes, return response cookies, redirects, and status codes unchanged, without following redirects.
Stream request and response bodies on API routes without buffering them whole.
Strip cookies and authorization headers from requests to static-asset and application-shell upstreams.
Remove cookies set by static-asset and application-shell responses.

Keep accounts, database access, authorization decisions, and request and response schemas out of the gateway.
Leave HTML generation and content-security-policy nonces to the application that renders the page.
Deploy the gateway independently of the applications behind it, with its own release credentials.

## Checks

Send requests with an unconfigured sibling host, the path `/apiary`, and paths containing encoded slashes, backslashes, and dot segments, and confirm none reaches an unintended upstream.
Send client-supplied forwarding headers and request identifiers, and inspect what the upstream receives.
Request a static asset with cookies and an authorization header, and confirm the upstream receives neither and the response sets no cookie.
Exercise sign-in redirects, cookie-setting responses, and streamed responses through the deployed gateway; local fixtures do not prove hosted behavior.
Try to reach each upstream directly from the public internet, and confirm it is unreachable.
Review gateway code for account, database, authorization, or schema logic.
