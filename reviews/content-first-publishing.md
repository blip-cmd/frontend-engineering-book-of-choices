---
page: book/09_decision_playbooks/content_first_publishing.md
verified: 2026-11-21
---

# Claim Ledger: Decision Playbook, Content-First Publishing & Documentation

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead choosing the architecture of a documentation hub, blog, marketing site, news portal or catalog storefront, where most visitors read and few interact. The page helps them pick a rendering model, islands framework, styling, image handling, delivery and search, and decide when to add server rendering. Thesis (unchanged from the draft): ship static HTML by default with Astro islands, add client JavaScript only for the widgets that need it, and avoid client-rendered SPAs, whole-page hydration and runtime CSS-in-JS for content pages.

**History.** Author pass on 2026-11-21 rewrote the AI-generated draft. The draft set unsourced targets stricter than the published thresholds ("LCP < 1.2s", "INP < 50ms", "100/100" Lighthouse SEO), invented a "99% reads, 1% writes" split, a "300 KB" SPA bundle and a Tailwind stylesheet "capped under 15 KB gzipped", said SPAs "penalize search engine crawlers" (Google says it renders JavaScript, though pre-rendering is still recommended), and placed ISR in an Astro stack without saying that Astro gets it only from the Vercel adapter. A "When this playbook is the wrong choice" section was added, and generic headings were replaced with headings that say what each section decides.

**Recommendation changes (rule A1).**
1. The "frequent content updates" checklist item no longer prescribes ISR. Astro has no framework-level ISR; the page now offers rebuilds at each new commit (webhook wording removed by the verifier, see section 2), Astro 7 route caching with stale-while-revalidate, or the Vercel adapter's `isr` option, citing each.
2. The "authentication on every page" item now points to Astro server islands (`server:defer`) for small per-user regions instead of a yes/no rule.
3. The Next.js App Router is named as a reasonable alternative for teams already on Next.js, because the Next.js docs say Server Components reduce client JavaScript. The rejection of whole-page hydration (Pages Router) stands.

---

## 1. Author pass (2026-11-21)

Sources were fetched in the same session (curl with HTML stripped to text, and WebFetch for the Astro directives and route caching pages) and quotes matched against the live page text. Package versions came from `npm view` on 2026-11-21. The page has no code blocks, so there was nothing to run.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | Core Web Vitals "good": LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less, at the 75th percentile of page loads segmented across mobile and desktop | [web.dev: Web Vitals](https://web.dev/articles/vitals) | verified (quote); replaces the draft's unsourced "LCP < 1.2s" and "INP < 50ms" |
| 2 | Lighthouse SEO audits include meta description, valid `rel=canonical`, descriptive link text | [Lighthouse overview](https://developer.chrome.com/docs/lighthouse/overview) | verified; draft's "100/100 SEO scores" target removed |
| 3 | "99% reads, 1% writes" | none found | removed; rewritten qualitatively |
| 4 | Astro renders every UI component "to just HTML & CSS, stripping out all client-side JavaScript automatically" | [Astro: Islands](https://docs.astro.build/en/concepts/islands/) | verified (quote); replaces "100% static HTML" and "exactly 0 KB of client JavaScript" |
| 5 | `client:load`, `client:idle`, `client:visible`, `client:media`, `client:only` behaviours; no directive means no JavaScript | [Astro: Template directives](https://docs.astro.build/en/reference/directives-reference/) | verified (quote) |
| 6 | Content collections validate content and provide TypeScript types | [Astro: Content collections](https://docs.astro.build/en/guides/content-collections/); [Why Astro](https://docs.astro.build/en/concepts/why-astro/) | verified (quote) |
| 7 | Starlight includes site navigation, search, internationalisation and front matter validation | [Starlight](https://starlight.astro.build/) | verified (quote) |
| 8 | Astro supports React, Preact, Svelte, Vue and SolidJS islands; frameworks can be mixed on one page | [Astro: Islands](https://docs.astro.build/en/concepts/islands/) | verified (quote) |
| 9 | Preact: "Fast 3kB alternative to React with the same modern API" | [preactjs.com](https://preactjs.com/) | verified (quote), labelled as a vendor claim |
| 10 | Tailwind generates CSS only for classes found in source files | [Tailwind: Detecting classes](https://tailwindcss.com/docs/detecting-classes-in-source-files) | verified (quote); draft's "capped under 15 KB gzipped" removed |
| 11 | Tailwind's Astro guide installs `tailwindcss` and `@tailwindcss/vite` as a Vite plugin | [Tailwind: Astro](https://tailwindcss.com/docs/installation/framework-guides/astro) | verified |
| 12 | `build.inlineStylesheets` defaults to `'auto'`, inlining stylesheets under `assetsInlineLimit` (default 4kb) | [Astro: Configuration](https://docs.astro.build/en/reference/configuration-reference/) | verified (quote); corrects the draft's "inline critical CSS eliminates render-blocking requests" |
| 13 | Lighthouse recommends inlining critical styles to eliminate render-blocking stylesheets | [Lighthouse: Render-blocking resources](https://developer.chrome.com/docs/lighthouse/performance/render-blocking-resources) | verified |
| 14 | `<Image />`/`<Picture />` optimise `src/` images; output has `loading`, `decoding` and inferred dimensions to avoid CLS; `public/` and plain `<img>` are not processed | [Astro: Images](https://docs.astro.build/en/guides/images/) | verified (quote); added as a table row for the framework's image capability |
| 15 | Astro prerenders the whole site to static HTML by default | [Astro: On-demand rendering](https://docs.astro.build/en/guides/on-demand-rendering/) | verified (quote) |
| 16 | Deploy guides include Cloudflare, Netlify, Vercel, GitHub Pages; Git-connected hosts rebuild at each new commit | [Astro: Deploy](https://docs.astro.build/en/guides/deploy/) | verified (quote); draft's "Fastly" dropped (not in Astro's guides) |
| 17 | Pagefind runs without hosting infrastructure; 10,000-page site searchable with under 300kB total payload | [Pagefind](https://pagefind.app/) | verified (quote), labelled as a vendor claim |
| 18 | Starlight ships Pagefind search by default; Algolia DocSearch documented as an alternative | [Starlight: Site search](https://starlight.astro.build/guides/site-search/) | verified (quote) |
| 19 | Google renders JavaScript; pre-rendering "is still a great idea ... not all bots can run JavaScript" | [Google: JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) | verified (quote); corrects "penalizes search engine crawlers" |
| 20 | "Sending a 300 KB JavaScript bundle" | none found | removed |
| 21 | Pages Router: page JavaScript runs and "makes the page fully interactive" (hydration) | [Next.js: Pages Router rendering](https://nextjs.org/docs/pages/building-your-application/rendering) | verified (quote) |
| 22 | App Router Server Components "reduce the amount of JavaScript sent to the browser"; Next.js 16 | [Next.js: Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components); `npm view next` (16.4.6) | verified (quote) |
| 23 | Hydration "wastes user battery" | none found | removed |
| 24 | Runtime `<style>` injection "forces the browser to recalculate the styles a lot more often" and "can be very slow if it happens at the wrong time in the React lifecycle" | [react.dev: useInsertionEffect](https://react.dev/reference/react/useInsertionEffect) | verified (quote); replaces the draft's unsourced "delays First Contentful Paint" |
| 25 | `server:defer` server islands render the page immediately with fallback content | [Astro: Server islands](https://docs.astro.build/en/guides/server-islands/) | verified (quote) |
| 26 | Route caching added in `astro@7.0.0`; supports stale-while-revalidate and invalidation by tag or path | [Astro: Route caching](https://docs.astro.build/en/guides/caching/) | verified; adapter CDN cache providers are marked experimental (not stated on the page) |
| 27 | Vercel adapter `isr` option caches on-demand pages like prerendered pages after first request | [Astro: Vercel adapter](https://docs.astro.build/en/guides/integrations-guide/vercel/) | verified (quote) |
| 28 | ISR is a Next.js feature | [Next.js: ISR](https://nextjs.org/docs/app/guides/incremental-static-regeneration) | verified |
| 29 | Astro contrasts content sites with frameworks built for "logged-in admin dashboards, inboxes, social networks, todo lists" | [Astro: Why Astro](https://docs.astro.build/en/concepts/why-astro/) | verified (quote) |
| 30 | Versions: astro 7.4.13, @astrojs/starlight 0.43.1, tailwindcss 4.3.5, @tailwindcss/vite 4.3.5, preact 11.2.0, svelte 5.59.1, @astrojs/preact 6.1.6, @astrojs/svelte 9.1.6, pagefind 1.6.0, next 16.4.6 | `npm view` | verified |
| 31 | Static pages turn traffic spikes into bandwidth cost; JavaScript competes with content on slow networks; personalised-everywhere sites gain little from static builds; migration to Astro must earn back its cost | none | unsourced background without numbers (acceptable per the standards); not explicitly labelled as the book's reasoning or position |

## 2. Independent verifier pass (2026-11-22)

A separate agent that did not write the page extracted the claims afresh (43 claims, counting each directive, quote, number and version separately) and checked each against its cited source, fetched with `curl -sL` on 2026-11-21/22 and searched as stripped text. All 25 cited URLs resolved (HTTP 200) to the expected page. Versions were rechecked with `npm view`: astro 7.4.13, @astrojs/starlight 0.43.1, tailwindcss 4.3.5, @tailwindcss/vite 4.3.5, preact 11.2.0, svelte 5.59.1, pagefind 1.6.0, next 16.4.6, @astrojs/preact 6.1.6, @astrojs/svelte 9.1.6, @astrojs/vercel 11.0.22, @emotion/react 11.14.0, styled-components 6.6.0, all matching the page and the author's row 30. The page has no code blocks, so there was nothing to run.

**Verdicts.** 37 SUPPORTED (every quote appears verbatim: Astro islands, Starlight, Preact, Google, Next.js, react.dev, Why Astro; all numbers: 2.5 s, 200 ms, 0.1, 75th percentile, 4 kB, 3kB, 10,000 pages, 300 kB, astro@7.0.0). 4 PARTIAL, 1 UNSUPPORTED, all corrected below. Section 1's traffic-pattern and target-environment bullets have no citation and no numbers; they are uncontroversial background (NO SOURCE, acceptable), though they are not explicitly labelled as the book's reasoning as row 31 says. The Lighthouse render-blocking page now warns that the audit "has moved into the Render-blocking requests insight as of Lighthouse 13"; its advice to inline critical styles still stands, so the claim is SUPPORTED.

**Edits to the page.**
1. Route caching (PARTIAL, the author's known gap): the source says the Netlify, Vercel and Cloudflare adapters each "provide an experimental CDN cache provider". Added that qualifier: "the CDN cache providers in Astro's Netlify, Vercel and Cloudflare adapters are experimental".
2. Rebuild trigger (UNSUPPORTED): "rebuild on each commit or CMS webhook" cited Astro: Deploy, which never mentions webhooks. Reworded to the source's "rebuild and republish at each new commit". This also affects recommendation change 1 above, which mentions webhooks.
3. Pagefind (PARTIAL): "needs a total network payload under 300 kB" reworded to the source's "can run a full-text search on a 10,000-page site with a total network payload under 300 kB, including the Pagefind library itself".
4. ISR (PARTIAL): "ISR as a framework feature belongs to Next.js" implied exclusivity the cited Next.js guide does not state. Reworded to "Next.js documents Incremental Static Regeneration (ISR) as a framework feature; in Astro it is an option of the Vercel adapter".
5. Next.js App Router in section 5 (PARTIAL): "Server Components already keep static parts of the page out of the client bundle" paraphrased beyond the source. Reworded to the source's quote: Server Components "reduce the amount of JavaScript sent to the browser".

**Verdict: PASS.** No UNSUPPORTED claims remain, every PARTIAL was corrected, every number links its source, and `python pipelines/scripts/audit_repo_standards.py` passes (see the final run). Front matter set to `agent-verified`, `review_by: 2027-05`.

## 3. Known omissions (follow-up content, not errors)

* Svelte is recommended alongside Preact, but the page cites only Astro's support for it, not a Svelte primary source on its runtime cost.
* No measured comparison (bundle sizes, field CWV) of Astro against a Next.js App Router build of the same content; any such numbers need a reproducible script in the repo.
* View transitions and `prefetch` options in Astro, both relevant to multi-page reading flows.
* Feeds, sitemaps (`@astrojs/sitemap`) and structured data for news and catalog sites.
* CMS integration and preview workflows for non-developer editors.
* The adapter CDN cache providers for route caching are experimental; a fuller treatment should say so and date it.
* A code example (a `client:visible` island and a content collection schema) would raise D9.

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 0 | 1 | **16** |

D9 is 0 because the playbook has no examples. All gates pass except G8 (human accountability), which an `agent-verified` status would disclose instead.
