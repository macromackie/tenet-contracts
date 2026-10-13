---
name: security-user-content-serving
message: Treat user content as untrusted; never execute markup, inline only verified passive formats, and serve the rest as downloads.
---

## Rules

Treat user-supplied filenames, extensions, declared content types, text, markup, and bytes as untrusted.
Set the served content type from the stored bytes or as a generic binary type, never from a user-supplied extension or declared type.
Allow inline display only for an explicit allowlist of passive formats, such as raster images, and only when the stored bytes decode as the allowed format.
Serve every other format, including HTML, SVG, and text, as a download; over HTTP, use an attachment disposition with `X-Content-Type-Options: nosniff`.
Sanitize user filenames before using them in a response header, and never use one as a storage key or a filesystem path.

Render user text and Markdown without executing it: no raw HTML, scripts, event handlers, or `javascript:` links from the content.
Do not automatically load remote resources that user content references, such as remote images.
Declare a maximum size for content accepted and rendered, and reject larger content.

Decode user images within bounded dimensions, re-encode them, and strip identifying metadata before publishing.
Import content from external URLs through the same validation path as uploads, and do not hot-link it at render time.
When fetching a user-supplied URL, connect only to public addresses, checking the resolved address and every redirect, so the fetch never reaches private, loopback, link-local, or metadata endpoints.

Serve private user content only through paths that authorize the viewer on each request, and mark it uncacheable by shared caches, such as with HTTP `Cache-Control: private, no-store`.
Never expose a storage credential or a public storage URL for private content.

## Checks

Upload a file whose extension and declared type disagree with its bytes, and inspect the served content type and disposition.
Store text and Markdown containing script tags, raw HTML, event handlers, `javascript:` links, and remote image references, and confirm nothing executes or loads.
Inspect response headers for `nosniff` and attachment disposition on every format outside the inline allowlist, and for private, no-store caching on private content.
Inspect a published image for removed metadata and bounded dimensions.
Import from a URL that resolves or redirects to a loopback or private address, and confirm the fetch is refused.
Does any response expose a storage credential, a public storage URL, or an unsanitized filename?
