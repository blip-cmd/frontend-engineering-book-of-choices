---
page: book/01_where_code_runs.md
verified: 2026-11-22
---

# Claim Ledger: Chapter 1, Where Code Runs: The Execution Boundary

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead or senior frontend developer choosing a rendering model for a new web project, or deciding whether to move an existing one. The page helps them decide where each page's HTML is produced: in the browser (CSR), per request on a server (SSR with hydration), at build time with optional background regeneration (SSG and ISR), as static HTML with isolated interactive islands, or with React Server Components and streaming. Thesis (unchanged from the draft): neither client-only nor server-only rendering fits every page; pick per route by SEO needs, how static the content is, and the compute budget, and prefer approaches that ship less JavaScript to hydrate.

**History.** The AI-generated draft was rewritten by the author pass on 2026-11-22. Main corrections: the draft said Server Components "execute exclusively on the server" and need a Node or edge runtime (react.dev says they can run once at build time with no web server); it placed ISR on static CDN infrastructure at "periodic build-time compute" cost and suggested "ISR at Edge" (Next.js supports ISR only on the Node.js runtime and not in a static export); it rated CSR SEO as "poor without pre-rendering bots" (Google renders JavaScript and calls dynamic rendering a workaround it does not recommend; the real limit is that not all bots run JavaScript); it said SSR HTML "arrives in first packet"; it listed Remix as an RSC framework (Remix continues as React Router, whose RSC support is experimental); it gave unsourced numbers ("multi-megabyte" bundles, "200ms penalties per request", "sub-millisecond queries"); it misattributed the RSC RFC to "Dan Abramov & Laurent Tan" and gave Jason Miller's post an invented title. No recommendation was changed.

---

## 1. Author pass (2026-11-22)

Sources were fetched in the same session with `curl` and searched as text; package versions were checked with `npm view` on 2026-11-22.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | CSR: "all logic, data fetching, templating, and routing are handled on the client"; SSR "generates the full HTML for a page" per navigation | [web.dev: Rendering on the Web](https://web.dev/articles/rendering-on-the-web) (updated 2026-01-05) | verified (quote) |
| 2 | CSR "can be difficult to make and keep fast for mobile devices"; JavaScript "tends to grow as an application grows" | web.dev: Rendering on the Web | verified (quote); replaces the draft's "multi-megabyte JavaScript bundles" (unsourced) |
| 3 | SSR "dynamic nature can have significant compute overhead costs"; "can increase your page's TTFB" | web.dev: Rendering on the Web | verified (quote); replaces "degrades global latency when requests traverse oceans" |
| 4 | web.dev authors "encourage developers to consider server-side rendering or static rendering over a full rehydration approach"; models can be mixed per page | web.dev: Rendering on the Web | verified (quote); added, labelled as the authors' position |
| 5 | Vite builds an SPA by default (`appType` default `'spa'`) | [Vite: Shared Options](https://vite.dev/config/shared-options) | verified |
| 6 | Draft: CSR SEO "Poor without pre-rendering bots" | [Google: JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics); [Google: Dynamic rendering as a workaround](https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering) | corrected: Googlebot renders JavaScript in a render queue; "not all bots can run JavaScript" (quote); Google calls dynamic rendering "a workaround and not a recommended solution" |
| 7 | For "little or no interactivity, server-side rendering can represent a more scalable solution" | web.dev: Rendering on the Web | verified (quote); used as CSR "wrong choice when" |
| 8 | Hydration: React "will 'attach' your components' logic to the initial generated HTML"; "treat mismatches as bugs and fix them" | [react.dev: hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) (React 19.3) | verified (quote) |
| 9 | Static rendering "achieves a consistently fast TTFB"; SSR with rehydration "rarely the best option" per real-site metrics | web.dev: Rendering on the Web | verified (quote); used as SSR "wrong choice when" |
| 10 | ISR: after the window "the next request will still return the cached (now stale) page" and regeneration happens "in the background" | [Next.js: ISR](https://nextjs.org/docs/app/guides/incremental-static-regeneration) | verified (quote) |
| 11 | Draft implied ISR runs on static CDN storage and at the edge | Next.js: ISR ("ISR is only supported when using the Node.js runtime (default)"; "not supported when creating a Static Export") | corrected in mechanism, matrix and decision tree ("ISR or cached SSR") |
| 12 | Static rendering does not suit personalized pages or sites with too many URLs to predict | web.dev: Rendering on the Web | verified (quote) |
| 13 | "If you need real-time data, consider switching to dynamic rendering" | Next.js: ISR | verified (quote) |
| 14 | Islands: Jason Miller, *Islands Architecture*, 2020-08-11; HTML rendered on the server with placeholders "around highly dynamic regions" hydrated into "small self-contained widgets" | [jasonformat.com](https://jasonformat.com/islands-architecture/) | verified (quote); draft title "Islands Architecture Concept Specification" corrected |
| 15 | Islands is also called "partial or selective hydration" | [Astro: Islands architecture](https://docs.astro.build/en/concepts/islands/) | verified (quote); heading kept with both terms, since React and Next.js use "selective hydration" for per-Suspense hydration (row 22) |
| 16 | `client:*` directives; `client:idle` "when the browser becomes idle"; `client:visible` "only once it enters the viewport"; Astro "will only hydrate exactly what's needed" | Astro: Islands architecture; [Astro: Directives reference](https://docs.astro.build/en/reference/directives-reference/) | verified (quote) |
| 17 | Astro server islands via `server:defer` | Astro: Islands architecture | verified |
| 18 | Astro pages "pre-rendered at build time as static pages" by default; on-demand rendering per route | [Astro: On-demand rendering](https://docs.astro.build/en/guides/on-demand-rendering/) | verified (quote) |
| 19 | Astro "Zero JS, by default"; target list of content sites; other frameworks "excel at" app-like experiences such as "logged-in admin dashboards, inboxes" | [Why Astro?](https://docs.astro.build/en/concepts/why-astro/) | verified (quote); labelled advocacy; used as islands "wrong choice when" |
| 20 | Draft: Server Components "execute exclusively on the server" | [react.dev: Server Components](https://react.dev/reference/rsc/server-components) ("once at build time on your CI server" or "for each request using a web server") | corrected |
| 21 | Server Components "are not sent to the browser"; interactivity through `"use client"` Client Components; RSC bundler APIs "do not follow semver" | react.dev: Server Components | verified (quote) |
| 22 | RSC output is "a description of the rendered UI, not HTML"; a framework may combine it with SSR | [RSC RFC](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md) | verified (quote) |
| 23 | Wire format called "Flight" | [react source: packages/react-server/src](https://github.com/facebook/react/tree/main/packages/react-server/src) (`ReactFlightServer.js` and related files, GitHub API) | verified; not named in react.dev or the RFC, so attributed to the source code |
| 24 | Next.js App Router streams HTML "in chunks aligned with `<Suspense>` boundaries"; streaming "enables selective hydration"; without boundaries "React hydrates the entire page in one blocking pass"; component payload embedded in the HTML | [Next.js: Streaming](https://nextjs.org/docs/app/guides/streaming) | verified (quote) |
| 25 | React Router RSC support "experimental and subject to breaking changes" | [React Router: React Server Components](https://reactrouter.com/how-to/react-server-components) (docs for 8.5.2) | verified (quote) |
| 26 | Draft listed Remix as an RSC framework | [Remix blog: Merging Remix and React Router](https://remix.run/blog/merging-remix-and-react-router) ("What we planned to release as Remix v3 is now going to be released as React Router v7") | corrected: React Router named instead |
| 27 | Waku supports Server Components; npm `latest` tag is `1.0.0-rc.5` (published 2026-11-11) | [waku.gg](https://waku.gg/); `npm view waku dist-tags` | verified; labelled pre-stable |
| 28 | Hydration gap: SSR pages "can appear to be loaded and interactive, but can't actually respond to input until" scripts run | web.dev: Rendering on the Web | verified (quote); replaces the draft's "Uncanny Valley" heading and "clicks silently lost" claim |
| 29 | "Server rendering creates an illusion that the app loads faster by showing the HTML snapshot of its output." | react.dev: hydrateRoot | verified (quote) |
| 30 | Client waterfalls: "the child can't start loading any data until the parent component finishes"; RSC moves "sequential round trips to the server" | RSC RFC, "No Client-Server Waterfalls" | verified (quote) |
| 31 | Draft: "cumulative 200ms penalties per request" and "sub-millisecond queries" | none found | removed; rewritten qualitatively with the RFC's reasoning |
| 32 | SSR "avoids additional round trips for data fetching and templating on the client" | web.dev: Rendering on the Web | verified (quote) |
| 33 | Application shell caching with service workers for repeat visits | web.dev: Rendering on the Web | verified |
| 34 | Draft: SSR "Rendered HTML arrives in first packet"; CSR and static TTFB "Instant" | web.dev: Rendering on the Web (SSR "generally produces a fast FCP"; static "consistently fast TTFB") | corrected to sourced qualitative cells |
| 35 | Draft: RSC compute "High (Requires Node / Edge runtime)" | react.dev: Server Components | corrected: no per-request cost when rendered at build time |
| 36 | RSC introduced 2020-12-21 by Dan Abramov, Lauren Tan, Joseph Savona and Sebastian Markbåge; RFC PR #188 opened by Joseph Savona | [react.dev blog](https://react.dev/blog/2020/12/21/data-fetching-with-react-server-components); GitHub API `repos/reactjs/rfcs/pulls/188` (`user.login: josephsavona`) | corrected: draft credited "Dan Abramov & Laurent Tan" with the RFC |
| 37 | Draft reference to `library/methodologies/islands_and_selective_hydration.md` research notes | unverified AI summary | removed; primary sources cited inline |
| 38 | Pinned versions: react 19.3.1, next 16.4.6, astro 7.4.13, vite 8.3.8, react-router 8.5.2, waku 1.0.0-rc.5, solid-js 2.0.3, svelte 5.59.1 | `npm view <name> version`, 2026-11-22 | verified |
| 39 | "Wrong choice when" for RSC (interactive canvas apps; team cannot absorb churn); "wrong" cases in Quick Diagnostic Rules; mental-model friction cells; CSR TTFB and cost cells; the continuum line; the decision tree | none | the book's judgment; labelled "(judgment)" or "the book's reasoning" on the page |
| 40 | Draft: islands matter where JavaScript payload "directly impact[s] conversions" | none found | removed |
| 41 | Code examples | none runnable | the only code block is a text decision tree, tagged `text`; inline snippets are fragments; nothing to run with `node` |

## 2. Independent verifier pass (2026-11-22)

The verifier did not write the page or section 1. Claims were extracted from the page afresh; every cited source was fetched on 2026-11-22 with `curl -sL`, converted to text and searched for each quote. Versions were checked with `npm view <name> version`.

**Verdict: PASS.** 46 claims checked: 36 SUPPORTED, 9 PARTIAL (all reworded to match the source), 0 UNSUPPORTED, and 1 group of labelled judgments (V46). Remaining unsourced statements are labelled as the book's judgment or are uncontroversial background without numbers.

| # | Claim on the page | Source checked | Verdict |
| :--- | :--- | :--- | :--- |
| V1 | CSR "all logic, data fetching, templating, and routing are handled on the client"; SSR generates "the full HTML for a page" per navigation | web.dev: Rendering on the Web (Osmani and Miller; published 2019-02-06, updated 2026-01-05) | SUPPORTED |
| V2 | CSR "can be difficult to make and keep fast for mobile devices"; JavaScript "tends to grow as an application grows" | web.dev | SUPPORTED |
| V3 | SSR "dynamic nature can have significant compute overhead costs"; "can increase your page's TTFB" | web.dev | SUPPORTED |
| V4 | "we encourage developers to consider server-side rendering or static rendering over a full rehydration approach"; "for some pages and not others" | web.dev | SUPPORTED |
| V5 | "Most frameworks let you mix models per route" | none | PARTIAL: vague attribution with no source; reworded to "Models can be mixed per route", which the web.dev quote supports |
| V6 | "Vite 8.3 builds this shape by default (`appType` defaults to `'spa'`)" | Vite: Shared Options (docs v8.3.7) | PARTIAL: `appType` says whether the app is an SPA and controls dev and preview middleware, not the build output; reworded to "treats a project as a single-page application by default" |
| V7 | "Googlebot renders JavaScript in a later queue" | Google: JavaScript SEO basics (updated 2026-03-04) | PARTIAL: Google says "Googlebot queues all pages with a 200 HTTP status code for rendering" and renders "Once Google's resources allow"; reworded to match, and matrix cell "Google renders it later" reworded to "Google queues it for rendering" |
| V8 | server-side or pre-rendering "is still a great idea because it makes your website faster for users and crawlers, and not all bots can run JavaScript" | Google: JavaScript SEO basics | SUPPORTED (verbatim) |
| V9 | CSR wrong "for content pages aimed at low-end phones", where SSR "can represent a more scalable solution" for experiences "with little or no interactivity" | web.dev | PARTIAL: web.dev does not mention low-end phones in that passage; reworded to "pages with little or no interactivity" |
| V10 | React "will 'attach' your components' logic to the initial generated HTML from the server"; "treat mismatches as bugs and fix them" | react.dev: hydrateRoot (React 19.3) | SUPPORTED |
| V11 | Static rendering "achieves a consistently fast TTFB, because the HTML for a page doesn't have to be dynamically generated"; SSR with rehydration "rarely the best option" per metrics from real sites | web.dev | SUPPORTED |
| V12 | Static pages can be served from many CDNs | web.dev ("deploy static renders to multiple CDNs") | SUPPORTED |
| V13 | ISR: "the next request will still return the cached (now stale) page"; "a new version of the page begins generating in the background" | Next.js: ISR (docs v16.4.6, updated 2026-10-15) | SUPPORTED |
| V14 | "ISR therefore needs a running server"; matrix "ISR also needs a Node.js server" | Next.js: ISR ("ISR is only supported when using the Node.js runtime (default)"; "ISR is not supported when creating a Static Export"; platform table lists adapters as "Platform-specific") | PARTIAL: the docs name a runtime, not a server; reworded to "ISR has deployment limits" and "ISR needs the Node.js runtime and is not supported in a static export" |
| V15 | Personalized pages do not suit static rendering; too many URLs to predict | web.dev (verbatim quote; "infeasible when you need to predict those URLs ahead of time") | SUPPORTED |
| V16 | "If you need real-time data, consider switching to dynamic rendering" | Next.js: ISR | SUPPORTED |
| V17 | Jason Miller, *Islands Architecture*, August 11, 2020: "HTML pages on the server", placeholders "around highly dynamic regions", "hydrated" into "small self-contained widgets" | jasonformat.com (title "Islands Architecture", dated Aug 11, 2020) | SUPPORTED; the page says Miller "described" the pattern, which fits his note that Katie Sylor-Miller coined the name |
| V18 | Islands also known as "partial or selective hydration" | Astro: Islands architecture | SUPPORTED |
| V19 | `client:idle` "when the browser becomes idle"; `client:visible` "only once it enters the viewport"; Astro "will only hydrate exactly what's needed on the page" | Astro: Islands architecture | SUPPORTED |
| V20 | Astro pages "pre-rendered at build time as static pages" by default; on-demand per route | Astro: On-demand rendering | SUPPORTED |
| V21 | Server islands (`server:defer`) render a personalized component separately from an otherwise static page | Astro: Islands architecture ("small components of personalized content does not delay the rendering of an otherwise static page") | SUPPORTED |
| V22 | Other frameworks "excel at building more complex, application-like experiences in the browser: logged-in admin dashboards, inboxes, social networks, todo lists"; labelled advocacy | Why Astro? | SUPPORTED |
| V23 | "Zero JS, by default"; target list "marketing sites, publishing sites, ... and e-commerce sites" | Why Astro? | SUPPORTED |
| V24 | Server Components run "once at build time on your CI server" or "for each request using a web server"; "are not sent to the browser"; interactivity via `"use client"` | react.dev: Server Components (React 19.3) | SUPPORTED |
| V25 | Imports stay out of the client bundle | react.dev: Server Components (example comments "Not included in bundle") | SUPPORTED |
| V26 | "React sends 'a description of the rendered UI, not HTML'", which a framework may also server-render to HTML | RSC RFC ("by default React returns a description of the rendered UI, not HTML"; a framework "may choose to combine Server Components with ... SSR") | PARTIAL: "by default" qualifier missing; reworded to "By default React returns" |
| V27 | React's source code calls the wire format "Flight" | `packages/react-server/src` listing (GitHub API: `ReactFlightServer.js` and 14 other `ReactFlight*` files); `ReactFlightServer.js` comment "the Flight protocol" | SUPPORTED; the page attributes the name to source code only, as required (neither react.dev nor the RFC uses it) |
| V28 | Next.js: React's server renderer "produces HTML in chunks aligned with `<Suspense>` boundaries"; streaming "enables selective hydration"; each boundary a hydration unit; "React hydrates the entire page in one blocking pass" without boundaries | Next.js: Streaming (docs v16.4.6) | SUPPORTED |
| V29 | Static shell sent before slow data resolves; component payload embedded in the HTML | Next.js: Streaming ("It is sent immediately"; "it arrives embedded in the HTML stream") | SUPPORTED |
| V30 | React Router RSC support "experimental and subject to breaking changes" | React Router docs (8.5.2): "experimental and subject to breaking changes in minor/patch releases" | SUPPORTED (truncated quote keeps meaning) |
| V31 | RSC bundler/framework APIs "do not follow semver and may break between minors in React 19.x" | react.dev: Server Components | SUPPORTED |
| V32 | Matrix: SSR "Generally produces a fast FCP"; static fast FCP; SSR payload "A complete copy of the UI's implementation" plus data | web.dev | SUPPORTED |
| V33 | Matrix: "ISR serves a cached page while regenerating", attributed by default to web.dev | web.dev does not discuss ISR; Next.js: ISR does | PARTIAL: attribution; the cell now links the Next.js ISR page already cited on the page |
| V34 | Matrix: CSR FCP "Later: content waits for JavaScript and data fetches", attributed by default to web.dev | web.dev gives no CSR FCP statement | PARTIAL: labelled "(judgment)" |
| V35 | Matrix: RSC FCP fast when server-rendered and streamed | web.dev (streaming SSR "speeding up your FCP") | SUPPORTED |
| V36 | Matrix: RSC cost none per request if built at build time | react.dev: Server Components | SUPPORTED |
| V37 | SSR pages "can appear to be loaded and interactive, but can't actually respond to input until ..." | web.dev | SUPPORTED (verbatim) |
| V38 | "The user will spend some time looking at the server-generated HTML ... Server rendering creates an illusion that the app loads faster by showing the HTML snapshot of its output." | react.dev: hydrateRoot | SUPPORTED (verbatim) |
| V39 | Waterfall: "the child can't start loading any data until the parent component finishes loading its data"; "moving sequential round trips to the server. The problem isn't really the round trips, it's that they are from client to server." | RSC RFC, No Client-Server Waterfalls | SUPPORTED (verbatim) |
| V40 | SSR "avoids additional round trips for data fetching and templating on the client" | web.dev | SUPPORTED |
| V41 | Application shell caching with service workers for repeat visits | web.dev | SUPPORTED |
| V42 | "Remix development continues as React Router" plus the quote "What we planned to release as Remix v3 is now going to be released as React Router v7" | Remix blog, May 15, 2024 | PARTIAL: the quote is verbatim and dated, but the post does not say all Remix development continues as React Router; reworded to "The Remix team released its planned next version as React Router" |
| V43 | Waku supports RSC and had not reached stable 1.0 on npm | waku.gg ("supports all the latest React 19 features like server components"); `npm view waku dist-tags` = `latest: 1.0.0-rc.5` | SUPPORTED (not linked on the page; checked) |
| V44 | Attributions: blog *Introducing Zero-Bundle-Size React Server Components*, 2020-12-21, by Dan Abramov, Lauren Tan, Joseph Savona and Sebastian Markbåge; RFC PR #188 opened by Joseph Savona | react.dev blog byline; GitHub API `pulls/188` (`user.login: josephsavona`, created 2020-12-21) | SUPPORTED; the RFC's credits say Sebastian Markbåge "came up with the initial design", and the page does not claim otherwise |
| V45 | Pinned versions: React 19.3 (react 19.3.1), Next.js 16.4 (16.4.6), Astro 7.4 (7.4.13), Vite 8.3 (8.3.8), React Router 8.5 (8.5.2), Waku 1.0.0-rc.5, Solid 2.0 (solid-js 2.0.3), Svelte 5 (5.59.1) | `npm view`, 2026-11-22 | SUPPORTED, all match |
| V46 | Judgment cells, decision tree, RSC "wrong choice when", continuum line, "server far from its database moves the waterfall" | none | labelled as the book's judgment or reasoning on the page; no numbers |

**Edits made to the page (rewording only, no new claims or sources):** V5, V6, V7 (two places), V9, V14 (two places), V26, V33, V34, V42, as listed above. Front matter set to `agent-verified` after the audit passed.

**Code checks.** No runnable JavaScript on the page: the only code block is a `text` decision tree, and the inline snippets (`<div id="root"></div>`, `client:*`, `server:defer`, `"use client"`) are fragments. All eight packages resolve on npm.

**Audit.** `python pipelines/scripts/audit_repo_standards.py` passed after the edits and after the front matter change.

## 3. Known omissions (follow-up content, not errors)

Topics a complete chapter on where code runs could add. Each needs its own sourced entry before it is published:

* Resumability (Qwik 1.x, `@builder.io/qwik` 1.20.4) as an alternative to hydration
* Next.js Partial Prerendering and Cache Components (static shell plus dynamic holes), which the Next.js streaming guide references
* Edge runtime limits (APIs unavailable outside Node.js) and data-locality trade-offs for edge rendering
* Other frameworks' rendering modes: SvelteKit 3 (`@sveltejs/kit` 3.4.0) per-route `prerender` and `ssr` options; Nuxt 4 (4.6.4) route rules
* web.dev's trisomorphic rendering and prerendering versus static rendering distinction
* Field data (CrUX) comparing rendering models, with dataset, month and percentile
* Core Web Vitals links: how each model affects LCP and INP (see Appendix B)

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | N/A | 2 | **19** (17 of 18 applicable, scaled) |

D8 is 1 because the matrix and decision tree depend on the descriptions in section 2. D9 is N/A: the page has no code examples beyond a text decision tree. All gates pass except G8 (human accountability), which the `agent-verified` status would disclose instead.
