---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: web.dev Rendering on the Web (updated 2026-01-05), Google Search Central JavaScript SEO basics, react.dev (react 19.3.1), RSC RFC 0188, next 16.4.6 docs (ISR, Streaming), astro 7.4.13 docs, vite 8.3.8, react-router 8.5.2, waku 1.0.0-rc.5, solid-js 2.0.3, svelte 5.59.1, jasonformat.com Islands Architecture (2020-08-11), Remix blog (2024-05-15)
review_by: 2027-05
reviewers:
ledger: reviews/where-code-runs.md
---

# Chapter 1: Where Code Runs: The Execution Boundary

> Every frontend architecture starts with one decision: on whose machine, and at what moment, each page is turned into HTML.

---

## 1. The Decision: Which Machine Renders Each Page

This chapter is for a tech lead or senior developer choosing a rendering model for a new web project, or deciding whether to move an existing one. It covers five models: client-side rendering (CSR), server-side rendering (SSR) with hydration, static generation with optional regeneration (SSG and ISR), islands, and React Server Components (RSC) with streaming.

The choice is about where work happens. In client-side rendering, "all logic, data fetching, templating, and routing are handled on the client instead of on the server"; in server-side rendering, the server generates "the full HTML for a page" in response to each navigation ([web.dev: Rendering on the Web](https://web.dev/articles/rendering-on-the-web), Osmani and Miller, updated 2026-01-05). Each end has a cost. Client-side rendering "can be difficult to make and keep fast for mobile devices" because the JavaScript it needs "tends to grow as an application grows". Server-side rendering's "dynamic nature can have significant compute overhead costs", and generating pages on the server "can increase your page's TTFB" (same source).

The web.dev authors state their own position: "we encourage developers to consider server-side rendering or static rendering over a full rehydration approach." Models can be mixed per route: web.dev notes that "you can always choose to use server-side rendering for some pages and not others". The book's framing is a continuum from origin server to edge to browser:
`Origin Server -> Edge Worker -> Hybrid Island -> Client Browser`.

---

## 2. Choose Where HTML Is Produced: Five Rendering Models

1. **Client-Side Rendering (CSR, single-page application):**
   * *Mechanism:* The server delivers an HTML shell (`<div id="root"></div>`) and a script tag. The browser downloads and runs the bundle, which builds the DOM and fetches data. Vite 8.3 treats a project as a single-page application by default (`appType` defaults to `'spa'`, [Vite: Shared Options](https://vite.dev/config/shared-options)).
   * *Wrong choice when:* public pages must be read by crawlers and link-preview bots. Googlebot queues pages for rendering and runs their JavaScript once its resources allow, but Google's own docs say server-side or pre-rendering "is still a great idea because it makes your website faster for users and crawlers, and not all bots can run JavaScript" ([Google Search Central: JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)). Also wrong for pages with little or no interactivity: for such experiences, web.dev says "server-side rendering can represent a more scalable solution" ([web.dev](https://web.dev/articles/rendering-on-the-web)).
2. **Server-Side Rendering (SSR) with hydration:**
   * *Mechanism:* On each request, a server process (Node.js or an edge runtime) runs the component tree, queries data, renders HTML and sends it. The browser then downloads the JavaScript and React "will 'attach' your components' logic to the initial generated HTML from the server" ([react.dev: hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot), React 19.3). The client render must match the server's: React says to "treat mismatches as bugs and fix them".
   * *Wrong choice when:* the page is the same for every visitor. Static rendering "achieves a consistently fast TTFB, because the HTML for a page doesn't have to be dynamically generated", and web.dev reports that field data from sites using server-side rendering with rehydration "indicate that it's rarely the best option" ([web.dev](https://web.dev/articles/rendering-on-the-web)).
3. **Static Site Generation (SSG) and Incremental Static Regeneration (ISR):**
   * *Mechanism:* Pages are rendered to HTML at build time and can be served from many CDNs. With ISR in Next.js 16.4, after the revalidation window passes "the next request will still return the cached (now stale) page" while "a new version of the page begins generating in the background" ([Next.js: ISR](https://nextjs.org/docs/app/guides/incremental-static-regeneration)). ISR has deployment limits: Next.js says "ISR is only supported when using the Node.js runtime (default)" and "is not supported when creating a Static Export".
   * *Wrong choice when:* pages are personalized ("Pages that need personalization are a concrete example of the type of request that doesn't work well with static rendering"), or the site has too many URLs to predict and build ahead of time ([web.dev](https://web.dev/articles/rendering-on-the-web)). For data that must be live, Next.js advises: "If you need real-time data, consider switching to dynamic rendering" ([Next.js: ISR](https://nextjs.org/docs/app/guides/incremental-static-regeneration)).
4. **Islands Architecture (partial or selective hydration):**
   * *Mechanism:* The page is static HTML, and only marked components ship and run JavaScript. Jason Miller described the pattern as rendering "HTML pages on the server" with placeholders "around highly dynamic regions" that are "hydrated" on the client into "small self-contained widgets" ([Islands Architecture](https://jasonformat.com/islands-architecture/), August 11, 2020). In Astro 7.4, a `client:*` directive opts a component in; `client:idle` loads it "when the browser becomes idle" and `client:visible` "only once it enters the viewport" ([Astro: Islands architecture](https://docs.astro.build/en/concepts/islands/)). Astro pages are "pre-rendered at build time as static pages" by default, with on-demand rendering per route as an option ([Astro: On-demand rendering](https://docs.astro.build/en/guides/on-demand-rendering/)). Astro server islands (`server:defer`) render a personalized component on the server separately from an otherwise static page.
   * *Wrong choice when:* the product is an application rather than a content site. Astro's own docs say other frameworks "excel at building more complex, application-like experiences in the browser: logged-in admin dashboards, inboxes, social networks, todo lists" ([Why Astro?](https://docs.astro.build/en/concepts/why-astro/)). That page is written by the framework's authors, so read it as advocacy.
5. **React Server Components (RSC) and streaming:**
   * *Mechanism:* Server Components run in a separate environment, either "once at build time on your CI server" or "for each request using a web server" ([react.dev: Server Components](https://react.dev/reference/rsc/server-components), React 19.3). They "are not sent to the browser", so their imports stay out of the client bundle; interactive parts are Client Components marked with `"use client"`. By default React returns "a description of the rendered UI, not HTML", which a framework may also server-render to HTML ([RSC RFC](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md)); React's source code calls this wire format "Flight" ([`ReactFlightServer.js`](https://github.com/facebook/react/tree/main/packages/react-server/src)). In the Next.js 16.4 App Router, React's server renderer "produces HTML in chunks aligned with `<Suspense>` boundaries", and streaming "enables selective hydration", hydrating each boundary separately ([Next.js: Streaming](https://nextjs.org/docs/app/guides/streaming)).
   * *Wrong choice when (the book's reasoning):* most of the screen is interactive client state, such as a canvas editor, so most components would need `"use client"` and little code would stay on the server. Also wrong when the team cannot absorb framework churn: React Router 8.5 marks its RSC support "experimental and subject to breaking changes" ([React Router: React Server Components](https://reactrouter.com/how-to/react-server-components)), and react.dev warns that the APIs for building an RSC bundler or framework "do not follow semver and may break between minors in React 19.x".

---

## 3. Comparative Analysis Matrix

Rows cite [web.dev: Rendering on the Web](https://web.dev/articles/rendering-on-the-web) unless another source is linked. Cells marked "(judgment)" are the book's reasoning, not measurements.

| Metric / Constraint | Client-Side SPA | SSR with hydration | Static / ISR | Islands (Astro 7.4) | Server Components (RSC) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Time to First Byte (TTFB)** | Fast: static shell from a CDN (judgment) | Can increase, because pages are generated per request | "Consistently fast" for static files; ISR serves a cached page while regenerating ([Next.js](https://nextjs.org/docs/app/guides/incremental-static-regeneration)) | Same as static for prerendered pages; per request for on-demand routes ([Astro](https://docs.astro.build/en/guides/on-demand-rendering/)) | Static shell sent before slow data resolves ([Next.js: Streaming](https://nextjs.org/docs/app/guides/streaming)) |
| **First Contentful Paint (FCP)** | Later: content waits for JavaScript and data fetches (judgment) | "Generally produces a fast FCP" | Fast FCP | Fast: static HTML, "Zero JS, by default" ([Why Astro?](https://docs.astro.build/en/concepts/why-astro/)) | Fast when server-rendered to HTML and streamed |
| **Initial JS Payload** | Grows with the app | "A complete copy of the UI's implementation" plus serialized data | None to moderate, if client JavaScript is limited | Only components marked `client:*` ([Astro](https://docs.astro.build/en/concepts/islands/)) | Client Components only, plus the component payload embedded in the HTML ([Next.js](https://nextjs.org/docs/app/guides/streaming)) |
| **SEO & Crawlability** | Google queues it for rendering; "not all bots can run JavaScript" ([Google](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)) | Content is in the HTML | Content is in the HTML | Content is in the HTML | Content is in the HTML when server-rendered |
| **Infrastructure Compute Cost** | Near zero: static file hosting (judgment) | "Significant compute overhead costs" | Build-time compute; ISR needs the Node.js runtime and is not supported in a static export ([Next.js](https://nextjs.org/docs/app/guides/incremental-static-regeneration)) | Low for static default; server cost only for on-demand routes and server islands (judgment) | None per request if rendered at build time; server cost if rendered per request ([react.dev](https://react.dev/reference/rsc/server-components)) |
| **Mental Model Friction** | Low (judgment) | Moderate: server and client output must match ([react.dev](https://react.dev/reference/react-dom/client/hydrateRoot)) | Low (judgment) | Low (judgment) | High: two component types and a serialization boundary (judgment) |

---

## 4. Deep Dive on the Mechanisms

### Hydration: HTML That Looks Ready Before It Responds

SSR with hydration has a gap between looking ready and being ready. web.dev describes it: "Server-side rendered pages can appear to be loaded and interactive, but can't actually respond to input until the client-side scripts for components are executed and event handlers have been attached" ([web.dev: Rendering on the Web](https://web.dev/articles/rendering-on-the-web)). React's docs make the same point: "The user will spend some time looking at the server-generated HTML before your JavaScript code loads. Server rendering creates an illusion that the app loads faster by showing the HTML snapshot of its output." ([react.dev: hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot)).

Islands and Server Components narrow this gap by sending less code to hydrate. Astro "will only hydrate exactly what's needed on the page and leave the rest of your site as static HTML" ([Astro: Islands architecture](https://docs.astro.build/en/concepts/islands/)). Server Components are never hydrated because they "are not sent to the browser"; only Client Components are ([react.dev: Server Components](https://react.dev/reference/rsc/server-components)). Streaming with `<Suspense>` splits the remaining hydration into smaller tasks: without boundaries, "React hydrates the entire page in one blocking pass" ([Next.js: Streaming](https://nextjs.org/docs/app/guides/streaming)).

### Data Fetching: Move Sequential Round Trips to the Server

* **In the browser (CSR):** when a parent and child component each fetch in `useEffect`, "the child can't start loading any data until the parent component finishes loading its data" ([RSC RFC: No Client-Server Waterfalls](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md#no-client-server-waterfalls)). Each step is a full round trip over the user's network.
* **On the server (SSR, RSC):** the RFC's answer is "moving sequential round trips to the server. The problem isn't really the round trips, it's that they are from client to server." Server-side rendering likewise "avoids additional round trips for data fetching and templating on the client" ([web.dev](https://web.dev/articles/rendering-on-the-web)). The gain depends on the server sitting close to its data; a server far from its database moves the waterfall rather than removing it (the book's reasoning).

---

## 5. Decision Playbook

The tree below is the book's reasoning, built from the sources above. It is a starting point, not a measured result; the framework versions are those checked on 2026-11-22.

```text
                         [Start: Select Execution Model]
                                       |
                    Is SEO / social sharing vital?
                             |-- No --> [Is team velocity paramount?]
                             |                |-- Yes --> Choose CSR (Vite 8 + SPA)
                             |                `-- No  --> Choose Local-First / Desktop PWA
                             `-- Yes
                                       |
                      Is the content predominantly static?
                             |-- Yes --> Choose Islands (Astro 7) or SSG
                             `-- No
                                       |
                        Do you require low infrastructure cost?
                             |-- Yes --> Choose ISR or cached SSR
                             `-- No  --> Choose streaming RSC (Next.js 16 App Router;
                                         React Router 8 or Waku 1.0 RC, both pre-stable for RSC)
```

### Quick Diagnostic Rules

1. **Choose a client-side SPA (Vite 8.3 with React 19.3, Solid 2.0 or Svelte 5):**
   * For an authenticated internal tool, B2B workspace or local-first utility where SEO is irrelevant and the application shell can be cached by a service worker for repeat visits ([web.dev: application shell caching](https://web.dev/articles/rendering-on-the-web)).
   * Not when the same app also serves public, shareable pages: render those on the server or at build time.
2. **Choose islands (Astro 7.4):**
   * For content sites, documentation, e-commerce product pages and blogs where first-load performance and a small JavaScript payload matter most. Astro names "marketing sites, publishing sites, documentation sites, blogs, portfolios, landing pages, community sites, and e-commerce sites" as its target ([Why Astro?](https://docs.astro.build/en/concepts/why-astro/)).
   * Not for a dashboard or editor where most of the page is interactive; each island would be large and the static share small.
3. **Choose Server Components with streaming SSR (Next.js 16.4 App Router):**
   * For applications with personalized, dynamic data, public pages that need SEO, and a budget for server compute.
   * Not for a team that must deploy as static files with no server, unless every route renders at build time. React Router 8.5 and Waku 1.0.0-rc.5 also support RSC, but React Router labels its support experimental ([React Router](https://reactrouter.com/how-to/react-server-components)) and Waku had not reached a stable 1.0 on npm on 2026-11-22. The Remix team released its planned next version as React Router: "What we planned to release as Remix v3 is now going to be released as React Router v7" ([Remix blog, 2024-05-15](https://remix.run/blog/merging-remix-and-react-router)).

---

## 6. References & Further Reading

* Addy Osmani and Jason Miller: [*Rendering on the Web*](https://web.dev/articles/rendering-on-the-web), web.dev (published 2019-02-06, updated 2026-01-05)
* Jason Miller: [*Islands Architecture*](https://jasonformat.com/islands-architecture/) (2020-08-11)
* Dan Abramov, Lauren Tan, Joseph Savona and Sebastian Markbåge: [*Introducing Zero-Bundle-Size React Server Components*](https://react.dev/blog/2020/12/21/data-fetching-with-react-server-components) (2020-12-21), and the [React Server Components RFC](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md) ([pull request #188](https://github.com/reactjs/rfcs/pull/188), opened by Joseph Savona)
* [react.dev: Server Components](https://react.dev/reference/rsc/server-components) and [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot)
* [Astro: Islands architecture](https://docs.astro.build/en/concepts/islands/)
* [Next.js: Incremental Static Regeneration](https://nextjs.org/docs/app/guides/incremental-static-regeneration) and [Streaming](https://nextjs.org/docs/app/guides/streaming)
* [Google Search Central: JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)
* [Further reading: *High Performance Browser Networking* (Ilya Grigorik)](../library/reading_list.md)
