---
name: web-client-navigation
message: Keep ordinary links to recognized application routes in the mounted client and preserve native link behavior.
---

## Rules

Render each navigation destination as a link with a real destination URL.
Use the mounted application's router for ordinary activation of a link to a recognized client route.
Keep the document and the nearest shared layout mounted when moving between its child routes.
Give recognition of client routes to the application, including links composed by feature components.
Let the browser handle external destinations, downloads, protocol endpoints, native resources and same-document fragments.
Preserve modified and auxiliary clicks, non-self targets and events already handled by the component.
Keep directly opening a destination, reloading it and traversing browser history consistent with following its link.
Apply `web-url-search-state` when the destination owns search parameters.

## Checks

Follow an ordinary link between two routes under a shared layout and verify the destination and its content change while the same document and layout remain mounted.
Copy that link, open the destination in a new tab, reload it and traverse Back and Forward between the original routes.
Activate the link with the keyboard, then open it with a modified click and verify the browser opens the destination separately.
Exercise an external link, download, protocol endpoint and same-document fragment and verify each retains its native behavior.
Inspect programmatic navigation and generated destinations for any path the application mistakes for a client route.
