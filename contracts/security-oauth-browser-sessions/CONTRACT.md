---
name: security-oauth-browser-sessions
message: Keep OAuth tokens server-side behind host-only HttpOnly cookies with exact-origin checks.
---

## Rules

Keep OAuth access, ID, and refresh tokens out of browser JavaScript, browser storage, HTML, JSON responses, and forwarded cookies.
Let one server-side component per application own code exchange, PKCE, state and nonce validation, and refresh.
Give each application its own confidential client secret from the server's secret store, and expose only public configuration to the browser.
Keep the session in an application-specific, host-only, HttpOnly cookie with `SameSite=Strict`, `Path=/`, and a declared maximum age, and encrypt any session state the cookie carries.
Require `Secure` and the `__Host-` prefix outside loopback development.
Bind encrypted cookies to their application origin and purpose, and keep them within browser cookie size limits.
Carry the authorization callback with a short-lived, encrypted, HttpOnly `SameSite=Lax` transaction cookie, and validate state and issuer before establishing a session.

Restrict callback and return URLs to the application's own origin, and require HTTPS outside loopback.
Accept session, login, and logout requests only as `POST` with an exact same-origin `Origin` header and a custom request header, and answer them with `Cache-Control: no-store`.
Treat sibling origins under a shared parent domain as foreign.
Never let a browser request choose where the server sends a token, or supply a token for the server to use.
On authenticated API calls, reject a request whose expected account differs from the session's, attach the server-held access token, and strip browser cookies before calling the owning API.
Strip session cookies from requests forwarded to anything other than the application's session and API handlers, such as static-asset servers, and never set cookies on static-asset responses.

Reuse unexpired access tokens across reloads, and refresh only near expiry.
Cache issuer metadata and signing keys with bounded lifetimes, refetch the keys when a token names an unknown key ID, and never cache user credentials in state shared across users.
Restore a fresh page load from the session cookie, and try one non-interactive authorization only when that session is missing or invalid.
Never restart automatic authorization from a completed callback, an access denial, or a failed API request, and preserve the requested destination.
Keep signed out, access denied, and provider unavailable distinct, and never erase a valid session cookie because the provider is unreachable.

Serialize session exchanges and logout across same-origin tabs.
On sign-out, cancel queued session restoration and wait for in-flight session exchanges before clearing the cookie, so a late exchange cannot set it again.
Expire the application cookie on logout even when the revocation endpoint is unavailable, and end the central session through the discovered logout endpoint.

## Checks

After login and refresh, inspect browser storage, page HTML, JSON responses, and script-readable cookies for tokens.
Inspect the `Set-Cookie` attributes of the session and transaction cookies.
Call the session and logout endpoints from a sibling origin, without the custom header, and with `GET`, and confirm refusal.
Try callback and return URLs outside the application origin and confirm rejection.
Exercise reload, concurrent tabs, account switching, logout during refresh, and an unreachable provider in a real browser.
