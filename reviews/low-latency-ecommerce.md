---
page: book/09_decision_playbooks/low_latency_ecommerce.md
verified: 2026-11-21
---

# Claim Ledger: Decision Playbook, Low-Latency Global E-Commerce Storefronts

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead choosing the rendering, caching and third-party-script strategy of a consumer storefront whose catalog pages are public and the same for most shoppers, with traffic spikes during promotions. The page helps them choose where HTML is rendered and cached, how the cart updates, how images and CSS are delivered, how cached pages are invalidated, and what to do with marketing tags. Thesis (kept from the draft): serve server-rendered catalog HTML from a CDN cache close to the shopper, invalidate it by tag with stale-while-revalidate, update the cart optimistically, size every image, and keep third-party tags off the main thread.

**History.** The author pass (2026-11-21) rewrote the AI-generated draft. The draft had an unsourced "Every 100ms of latency reduction directly correlates with 1% to 2% higher conversion rates", replaced with the exact finding of the Google-commissioned Deloitte study (8.4% retail conversion increase associated with a 0.1 s mobile speed improvement), labelled as correlational and sponsor-commissioned. It set targets of "LCP < 1.0s", "CLS = 0.0" and "sub-100ms checkout initiation" with no source; these became web.dev's "good" thresholds at the 75th percentile. Removed with no source found: "70% to 80% mobile shoppers", "within 16ms", "400 KB bundle", "purge ... globally in milliseconds" (now Cloudflare's own word "instantly"), and "pre-warmed HTML in a single network round trip" (connection setup takes round trips of its own). Two recommendations were changed because primary sources contradict them: (1) "Edge-Rendered SSR with Selective ISR" became CDN-cached server rendering on the Node.js runtime, because Next.js 16 docs say the Edge Runtime does not support ISR; (2) "Remix / Next.js / Hydrogen" became Next.js 16 or React Router 8, with Hydrogen 2026-10 described as a Shopify layer that runs inside those frameworks, because Hydrogen's docs say it leaves routing and rendering to the framework and `remix` 3.x is a different non-React-hooks framework. "Tailwind CSS" was said to inline critical CSS; Tailwind only generates used classes, so inlining is described as a separate step with web.dev's caveats. Partytown is now described as a performance tool, not a security boundary, matching the wording verified in Appendix C, with its documented trade-offs (exit events, `preventDefault`, UI-heavy scripts). Added: a shared-cache warning for personalized responses, a cache-key note for country pricing, and a "When this playbook is the wrong choice" section. No links to `library/` research notes were on the page.

---

## 1. Author pass (2026-11-21)

Sources were downloaded with `curl` on 2026-11-21 and 2026-11-22, converted to text, and quotes matched against the page. Package versions come from `npm view` on 2026-11-21. The page has no runnable code.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | LCP good at 2.5 s or less, measured at the 75th percentile, segmented mobile and desktop | [web.dev LCP](https://web.dev/articles/lcp) | verified (quote); draft's "LCP < 1.0s" removed |
| 2 | CLS good at 0.1 or less at p75 | [web.dev CLS](https://web.dev/articles/cls) | verified (quote); draft's "CLS = 0.0" removed |
| 3 | INP good at 200 ms or less; poor above 500 ms | [web.dev INP](https://web.dev/articles/inp) | verified (quote); draft's "sub-100ms checkout initiation" removed |
| 4 | TTFB "rough guide" 0.8 s or less | [web.dev TTFB](https://web.dev/articles/ttfb) | verified (quote) |
| 5 | Draft: "Every 100ms of latency reduction directly correlates with 1% to 2% higher conversion rates" | none found | removed; replaced by claim 6 |
| 6 | Deloitte, commissioned by Google, 37 brands, about four weeks, Europe and US: "an 8.4% increase in conversions" for retail with a 0.1 s mobile speed improvement; correlational, speed changes "natural and not artificially controlled"; report promotes Google's Test My Site | [Deloitte: Milliseconds Make Millions (PDF), ©2020](https://www.thinkwithgoogle.com/_qs/documents/9757/Milliseconds_Make_Millions_report_hQYAbZJ.pdf) | verified (quote, methodology and disclaimer pages) |
| 7 | Draft: "70% to 80% mobile shoppers" | none found | removed; reader told to check own analytics |
| 8 | CDN puts servers close to users; distance and origin cache misses raise TTFB; large TTFB-to-FCP gap signals client-side rendering | [web.dev Optimize LCP](https://web.dev/articles/optimize-lcp) | verified (quote) |
| 9 | Draft: edge SSR delivers HTML "in a single network round trip" | none found | removed |
| 10 | Next.js 16: ISR "only supported when using the Node.js runtime (default)"; Edge Runtime "does not support Incremental Static Regeneration" and not all Node.js APIs | [Next.js ISR](https://nextjs.org/docs/app/guides/incremental-static-regeneration); [Next.js Edge Runtime](https://nextjs.org/docs/app/api-reference/edge) (docs v16.4.6) | verified (quote); recommendation changed from edge rendering to CDN-cached Node rendering |
| 11 | Hydrogen 2026-10 handles cart, Storefront API and checkout routes and "works with frameworks that run server code, like Next.js, React Router, Nuxt, Astro, and SvelteKit"; cart "updates optimistically, and works without JavaScript"; "one way to build a headless storefront" | [Shopify Hydrogen docs](https://shopify.dev/docs/storefronts/headless/hydrogen) | verified (quote); draft listed Hydrogen as a rendering framework, corrected |
| 12 | `remix` 3.3.0 keeps component state in plain JavaScript "rather than hooks" | [remix.run](https://remix.run/); `npm view remix` | verified (quote); Remix dropped from the stack, React Router named instead |
| 13 | Versions: `next` 16.4.6, `react` 19.3.1, `react-router` 8.5.2, `@shopify/hydrogen` 2026.10.3, `tailwindcss` 4.3.5, `@qwik.dev/partytown` 1.0.5, `remix` 3.3.0 | `npm view <name> version` | verified |
| 14 | `@builder.io/partytown` deprecated: "Use @qwik.dev/partytown instead" | `npm view @builder.io/partytown deprecated` | verified |
| 15 | `useOptimistic` shows optimistic state while an Action is pending; on throw, the UI shows the pre-update value | [react.dev useOptimistic](https://react.dev/reference/react/useOptimistic) | verified (quote) |
| 16 | Draft: optimistic update "within 16ms" | none found | removed |
| 17 | "Until September 2024" Server Functions were called Server Actions; one passed to an action prop is a Server Action | [react.dev Server Functions](https://react.dev/reference/rsc/server-functions) | verified (quote) |
| 18 | Tailwind generates CSS for "the classes you've actually used" | [Tailwind v4.3 docs](https://tailwindcss.com/docs/detecting-classes-in-source-files) | verified (quote); draft implied Tailwind inlines critical CSS, corrected |
| 19 | Inlining critical CSS saves a request; inlining a lot "delays the transmission of the rest of the HTML document" and prevents caching | [web.dev Extract critical CSS](https://web.dev/articles/extract-critical-css) | verified (quote) |
| 20 | Set `width`/`height` or CSS `aspect-ratio` to reserve image space; "Images without dimensions" heads the most-common-causes list | [web.dev Optimize CLS](https://web.dev/articles/optimize-cls) | verified (quote) |
| 21 | AVIF Baseline widely available (high date 2026-07-25); MDN advises a `<picture>` fallback | [webstatus.dev AVIF](https://webstatus.dev/features/avif) (API `api.webstatus.dev/v1/features/avif`); [MDN Image types](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types) | verified |
| 22 | `stale-while-revalidate`: cache may serve stale while revalidating "without blocking" | [RFC 5861 section 3](https://www.rfc-editor.org/rfc/rfc5861); [MDN Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control) | verified (quote) |
| 23 | Fastly `Surrogate-Key` tags content for purge and is stripped before delivery | [Fastly surrogate keys](https://www.fastly.com/documentation/guides/full-site-delivery/purging/working-with-surrogate-keys/) | verified (quote) |
| 24 | Cloudflare `Cache-Tag` header; purge "instantly"; header removed before the visitor sees it | [Cloudflare purge by cache-tags](https://developers.cloudflare.com/cache/how-to/purge-cache/purge-by-tags/) | verified (quote); draft's "globally in milliseconds" replaced by the vendor's word, attributed |
| 25 | Next.js 16 `revalidateTag(tag, 'max')` uses stale-while-revalidate semantics | [Next.js revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) | verified (quote) |
| 26 | Partytown relocates third-party scripts to a web worker, dedicating the main thread to your code | [Partytown introduction](https://partytown.qwik.dev/) | verified (quote) |
| 27 | Partytown best suited to Google Tag Manager or Facebook Pixel; UI-heavy scripts "may not be the best candidates"; `preventDefault()` has no effect; exit-event handlers unreliable, GA4 `user_engagement` not sent | [Partytown Trade-offs](https://partytown.qwik.dev/trade-offs) | verified (quote) |
| 28 | Partytown gives worker code synchronous DOM access through proxies; not a security boundary | [Partytown: How does it work?](https://partytown.qwik.dev/how-does-partytown-work); wording matches [Appendix C](../book/10_appendices/frontend_security_checklist.md) | verified (quote) |
| 29 | Tasks over 50 ms are long tasks that delay input | [web.dev Optimize long tasks](https://web.dev/articles/optimize-long-tasks) | verified (quote) |
| 30 | Draft: "400 KB bundle" and content "on the first incoming packet" | none found | removed; replaced by claim 8 |
| 31 | Draft: tags "causing cart clicks to fail" | none found | changed to "respond late", which follows from claims 3 and 29 |
| 32 | Personalized responses need `private`, otherwise "can be stored in a shared cache and end up being reused for multiple users" | [MDN Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control) | verified (quote); added |
| 33 | `CF-IPCountry` carries the visitor's two-letter country code; Vercel sends `x-vercel-ip-country` | [Cloudflare HTTP headers](https://developers.cloudflare.com/fundamentals/reference/http-headers/); [Vercel request headers](https://vercel.com/docs/headers/request-headers) | verified (quote) |
| 34 | `Vary` is used to build a cache key from request headers | [MDN Vary](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Vary) | verified (quote) |
| 35 | React Router 8 streams loader data returned as an un-awaited promise | [React Router: Streaming with Suspense](https://reactrouter.com/how-to/suspense) (docs 8.5.2) | verified (quote) |
| 36 | Next.js 16 streaming sends parts of a route "as soon as they're ready" via `loading.tsx` (wrapped in `<Suspense>`) or `<Suspense>` | [Next.js Linking and Navigating](https://nextjs.org/docs/app/getting-started/linking-and-navigating) | verified (quote) |
| 37 | Positions: meet all three thresholds on catalog pages; plan for mid-range phones; audit tags quarterly; country in the URL path; re-check stock server-side; small catalogs and per-buyer pricing are counter-cases | none | labelled on the page as position or reasoning |

## 2. Independent verifier pass (2026-11-22)

Every cited source was downloaded again with `curl -sL` on 2026-11-22 and searched as text (the Deloitte PDF with `pdftotext`; AVIF through `api.webstatus.dev/v1/features/avif`). Claims were extracted from the page independently: 41 claims checked (36 sourced facts, 5 labelled positions or reasoning). Versions re-checked with `npm view` on 2026-11-22: `next` 16.4.6, `react` 19.3.1, `react-router` 8.5.2, `@shopify/hydrogen` 2026.10.3, `tailwindcss` 4.3.5, `@qwik.dev/partytown` 1.0.5, `remix` 3.3.0; `@builder.io/partytown` deprecated with "Use @qwik.dev/partytown instead". All match the page. The page has no code blocks, so there was nothing to run.

Focus checks:

* **Deloitte, Milliseconds Make Millions:** SUPPORTED. Key Findings page: "An 8.4% increase in conversions with retail consumers was observed" for a 0.1 s mobile site speed improvement; 37 brands, "over a four week period", "across Europe and the US"; disclaimer: "commissioned by Google", the study "examined the correlation", and "Site speed fluctuations were natural and not artificially controlled"; the Recommendations section promotes Google's Test My Site tool; ©2020 (PDF created 2020-03-13). The page labels it correlational and commissioned.
* **Next.js 16 ISR and Edge Runtime:** SUPPORTED (docs show "Latest v16.4.6"). ISR page: "ISR is only supported when using the Node.js runtime (default)"; Edge Runtime page: "does not support all Node.js APIs" and "does not support Incremental Static Regeneration (ISR)".
* **Hydrogen and Remix naming:** SUPPORTED. Shopify docs "cover Hydrogen version 2026-10" and say it "works with frameworks that run server code, like Next.js, React Router, Nuxt, Astro, and SvelteKit"; the cart store "updates optimistically, and works without JavaScript" through "native HTML forms". remix.run calls Remix "The fully-stacked web framework" and says to keep state in ordinary JavaScript "rather than hooks".
* **Cache-Control:** SUPPORTED. RFC 5861 section 3: revalidate "while still serving stale responses (i.e., without blocking)"; MDN describes `stale-while-revalidate` and warns that without `private` a personalized response "can be stored in a shared cache and end up being reused for multiple users".

Other sources, all SUPPORTED as worded after the edits below: web.dev LCP, CLS, INP, TTFB thresholds (75th percentile, mobile and desktop); web.dev Optimize LCP (CDN, distance, origin round trips); useOptimistic; Server Functions; Tailwind; web.dev critical CSS and Optimize CLS; webstatus.dev AVIF (Baseline widely, high date 2026-07-25) and MDN Image types; Fastly surrogate keys (removed before delivery unless `Fastly-Debug`); Cloudflare cache-tags ("instantly", end users "never see Cache-Tag HTTP headers"); `revalidateTag(tag, 'max')`; Partytown introduction, trade-offs and how-it-works; web.dev long tasks; `CF-IPCountry`; `x-vercel-ip-country`; React Router 8.5.2 streaming.

**Verdict: PASS.** No UNSUPPORTED claims; five PARTIAL claims corrected; every number has a source.

Edits made (rewording to match the source; no claims or sources added):

1. Section 3, client-rendered SPA: "web.dev describes a large gap between TTFB and First Contentful Paint as 'a classic sign...'" was PARTIAL (web.dev says the gap "could indicate" render-blocking assets, or "can also be a sign" of heavy rendering work, which is the classic sign). Reworded to give both causes.
2. Section 4, streaming: "parts of a route" became "parts of a dynamic route", the source's wording.
3. Section 5, Partytown UI scripts: the page attached "may not be the best candidates" to dialog pop-ups, but the source uses that phrase only for scripts inserting many DOM nodes, and says "may not be best suited" for UI-intensive scripts such as dialogs. Reworded to quote each correctly.
4. Section 4, `Vary`: "the standard way to add request headers to a cache key" stretched MDN, which says responses are "separately cached based on the headers listed" and that this is most often used to create a cache key for content negotiation. Reworded to MDN's wording.
5. Section 3, tags and INP: "makes ... respond late and pushes INP past" stated an inference as certain; changed to "can make ... and push".

Remaining note (not an error): the Rendering row still mentions "The draft also named Remix", which explains the naming choice but refers to an earlier draft readers have not seen. A human editor may want to rephrase it.

## 3. Known omissions (follow-up content, not errors)

Each needs its own sourced entry before it is added:

* Next.js 16 Cache Components and Partial Prerendering as an alternative to ISR for mixing static and dynamic parts of a product page
* `fetchpriority="high"` and preloading the LCP product image (web.dev Optimize LCP covers both)
* Responsive images (`srcset`, `sizes`) and image CDNs, including web.dev's note that a third-party image domain adds a connection cost
* Speculation Rules or prefetching for collection-to-product navigation
* Bot and scraper traffic during sales, and request collapsing at the CDN when a hot page's cache entry expires
* Search engine requirements for product pages (structured data, canonical URLs for country paths)
* Payment and checkout pages hosted by the platform (for example Shopify checkout) and their effect on what the storefront can optimize
* Measuring with field data (CrUX, `web-vitals` library) rather than lab runs

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | N/A | 2 | **19** (17 of 18 points, scaled) |

D3 is 1: the page explains why the CDN cache, rather than edge rendering, delivers the speed, and why stale-while-revalidate hides revalidation, but the cache-key and streaming mechanisms are stated, not worked through. D9 is N/A: the playbook has no code example. G8 (human accountability) is not met until a human reviews the page.
