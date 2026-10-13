---
name: web-public-page-server-rendering
message: Render complete public content and real links in server HTML, and let hydration only add interaction.
---

## Rules

Render each public page's core copy, headings, meaningful images, and navigation in the server HTML.
Keep public content readable and navigable with scripts disabled.
Render navigation as anchors with real destination URLs; script handlers may enhance a link but not replace it.
Link pages of the same site by same-site URLs, and link externally hosted content by its canonical absolute URL.
Do not link to destinations that are not yet published.

Render public routes outside any layout or wrapper that requires a session.
Render public pages' server HTML without session requests or authenticated data.
Do not cover public content with an application startup overlay, a sign-in prompt, or a loading screen while a session restores.
Do not read browser-only globals during server rendering.

Do not make the first paint of public content wait for hydration, client startup, or animation setup.
Let hydration attach interaction to the server markup without replacing, hiding, or reflowing its content.
Render meaningful illustrations deterministically in the server HTML, with unique element identifiers and accessible descriptions.
Reserve the dimensions of media before it loads.
Keep a useful poster or still image and its destination link usable when media fails to load or autoplay is blocked, without drawing loading indicators over it.

## Checks

Fetch each changed public page with scripts disabled, and confirm its core content, headings, and links are present in the response HTML.
Review public routes for session requests, authenticated data, and browser-only globals read during server rendering.
Block client scripts and media in a browser, and confirm the page stays readable with usable links and reserved media space.
Check the browser console for hydration mismatch warnings on changed public pages.
Confirm that every navigation element is an anchor with a real URL.
