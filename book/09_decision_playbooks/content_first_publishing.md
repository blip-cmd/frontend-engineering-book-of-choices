---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: astro 7.4.13, @astrojs/starlight 0.43.1, @astrojs/vercel 11.0.22, tailwindcss 4.3.5, preact 11.2.0, svelte 5.59.1, pagefind 1.6.0, next 16.4.6; docs.astro.build, starlight.astro.build, web.dev, developer.chrome.com, developers.google.com, nextjs.org, react.dev, tailwindcss.com, pagefind.app (fetched 2026-11)
review_by: 2027-05
reviewers:
ledger: reviews/content-first-publishing.md
---

# Decision Playbook: Content-First Publishing & Documentation

> The book's recommended architecture for documentation hubs, tech blogs, marketing sites, news portals and catalog storefronts: sites where most visitors read and few interact. Checked against Astro 7.4, Starlight 0.43, Tailwind CSS 4.3, Preact 11.2 and Pagefind 1.6 (npm registry, November 2026).

---

## 1. What a Content-First Site Must Achieve

* **Primary success metric (the book's position):** pass all three Core Web Vitals at the 75th percentile of page loads, segmented across mobile and desktop: LCP of 2.5 seconds or less, INP of 200 milliseconds or less, and CLS of 0.1 or less ([web.dev: Web Vitals](https://web.dev/articles/vitals)). These are field thresholds; a Lighthouse run in the lab does not prove them. Alongside them, pass Lighthouse's SEO audits, which check items such as a meta description, a valid `rel=canonical` and descriptive link text ([Lighthouse overview](https://developer.chrome.com/docs/lighthouse/overview)).
* **Traffic pattern:** reads far outnumber writes, and traffic arrives in spikes from social sharing and search. Pages that are the same for every visitor can be built once and served as files, so a spike costs bandwidth rather than server rendering.
* **Target environment:** any device and network, including low-end phones on slow mobile connections. Every byte of JavaScript a reader downloads competes with the article itself.

---

## 2. The Recommended Stack, Layer by Layer

Each row is the book's recommendation; the rationale column states what the official docs say.

| Layer | Recommended choice | Rationale |
| :--- | :--- | :--- |
| **Rendering** | **Astro 7+ with islands** (Starlight for documentation) | By default Astro renders every UI component "to just HTML & CSS, stripping out all client-side JavaScript automatically" ([Astro: Islands](https://docs.astro.build/en/concepts/islands/)). A component ships JavaScript only when you add a `client:*` directive: `client:load` hydrates on page load, `client:idle` once the page finishes its initial load, `client:visible` when the component enters the viewport, `client:media` when a CSS media query matches, and `client:only` skips server rendering ([Astro: Template directives](https://docs.astro.build/en/reference/directives-reference/)). Content collections validate Markdown content against a schema and give it TypeScript types ([Astro: Content collections](https://docs.astro.build/en/guides/content-collections/)). For documentation, [Starlight](https://starlight.astro.build/) adds site navigation, search, internationalisation and front matter validation on top of Astro. |
| **Islands framework** | **Preact or Svelte**, only inside islands | Astro supports React, Preact, Svelte, Vue and SolidJS islands, and several frameworks can share one page ([Astro: Islands](https://docs.astro.build/en/concepts/islands/)). Preact describes itself as a "Fast 3kB alternative to React with the same modern API" ([preactjs.com](https://preactjs.com/)), a vendor claim. Choosing it over React for a few widgets is the book's position; a team with React components to reuse can use React islands instead. |
| **Styling** | **Tailwind CSS 4+** through `@tailwindcss/vite` | Tailwind scans your source files and generates CSS only for the classes you use ([Tailwind: Detecting classes](https://tailwindcss.com/docs/detecting-classes-in-source-files)); its Astro guide installs it as a Vite plugin ([Tailwind: Astro](https://tailwindcss.com/docs/installation/framework-guides/astro)). Astro's `build.inlineStylesheets` defaults to `'auto'`, which inlines stylesheets smaller than Vite's `assetsInlineLimit` (default 4 kB) into `<style>` tags ([Astro: Configuration](https://docs.astro.build/en/reference/configuration-reference/)). That removes a render-blocking request when the CSS is small; Lighthouse recommends inlining critical styles for the same reason ([Lighthouse: Render-blocking resources](https://developer.chrome.com/docs/lighthouse/performance/render-blocking-resources)). |
| **Images** | **Astro `<Image />` and `<Picture />`** | Local images in `src/` are transformed, optimised and bundled; the output `<img>` carries `loading` and `decoding` attributes and inferred dimensions to avoid Cumulative Layout Shift. Files in `public/` and plain `<img>` tags are not processed ([Astro: Images](https://docs.astro.build/en/guides/images/)). |
| **Delivery** | **Static build on a CDN host** | Astro prerenders the whole site to static HTML by default ([Astro: On-demand rendering](https://docs.astro.build/en/guides/on-demand-rendering/)). Astro's deploy guides cover Cloudflare, Netlify, Vercel, GitHub Pages and others, and Git-connected hosts rebuild and republish the site at each new commit ([Astro: Deploy](https://docs.astro.build/en/guides/deploy/)). |
| **Search** | **Pagefind**, or Algolia DocSearch | Pagefind indexes the built HTML and runs search in the browser without hosting any infrastructure; its docs say it can run a full-text search on a 10,000-page site with a total network payload under 300 kB, including the Pagefind library itself ([Pagefind](https://pagefind.app/)), a vendor claim. Starlight includes Pagefind search by default and documents Algolia DocSearch as an alternative ([Starlight: Site search](https://starlight.astro.build/guides/site-search/)). |

---

## 3. Patterns This Playbook Rejects, and Why

* **A client-rendered single-page app (for example Vite with React) for article pages.** The reader waits for JavaScript to download and run before the article appears. Google does render JavaScript pages, but its own guidance says server-side or pre-rendering "is still a great idea because it makes your website faster for users and crawlers, and not all bots can run JavaScript" ([Google: JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)).
* **Whole-page hydration for static text (for example the Next.js Pages Router).** In the Pages Router, the page's JavaScript runs in the browser and "makes the page fully interactive" through hydration ([Next.js: Pages Router rendering](https://nextjs.org/docs/pages/building-your-application/rendering)), so components that only render paragraphs and headings still download and run on the client. The Next.js 16 App Router addresses this with Server Components, which "reduce the amount of JavaScript sent to the browser" ([Next.js: Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)); it is a reasonable alternative for a team already on Next.js.
* **Runtime CSS-in-JS that injects `<style>` tags (for example Emotion or styled-components).** The React docs advise against runtime injection because it "forces the browser to recalculate the styles a lot more often" and "can be very slow if it happens at the wrong time in the React lifecycle" ([react.dev: useInsertionEffect](https://react.dev/reference/react/useInsertionEffect)). Build-time CSS such as Tailwind avoids that cost.

---

## 4. Constraint Checklist: When to Add Server Rendering

* **Does every page need per-user content (logged-in state, prices, carts)?** If only a small region does, keep the page static and turn that region into a server island with `server:defer`: Astro renders the rest of the page immediately with fallback content and fetches the island's content afterwards ([Astro: Server islands](https://docs.astro.build/en/guides/server-islands/)). If most of the page is per-user, see section 5.
* **Does content change faster than full rebuilds can keep up?** Options, in the book's order of preference: rebuild and republish at each new commit ([Astro: Deploy](https://docs.astro.build/en/guides/deploy/)); render the changing routes on demand with an adapter and cache them with route caching (Astro 7+), which supports stale-while-revalidate and invalidation by tag or path; the CDN cache providers in Astro's Netlify, Vercel and Cloudflare adapters are experimental ([Astro: Route caching](https://docs.astro.build/en/guides/caching/)); or, on Vercel, the adapter's `isr` option, which caches on-demand pages like prerendered ones after the first request ([Astro: Vercel adapter](https://docs.astro.build/en/guides/integrations-guide/vercel/)). Next.js documents Incremental Static Regeneration (ISR) as a framework feature ([Next.js: ISR](https://nextjs.org/docs/app/guides/incremental-static-regeneration)); in Astro it is an option of the Vercel adapter.

---

## 5. When This Playbook Is the Wrong Choice

* **The product is an application, not a publication.** Astro's docs contrast content sites with frameworks designed for "logged-in admin dashboards, inboxes, social networks, todo lists" and other app-like experiences ([Astro: Why Astro](https://docs.astro.build/en/concepts/why-astro/)). If most screens are interactive, almost every component becomes an island and the static default stops paying for itself (the book's reasoning). See the [Enterprise B2B SaaS](enterprise_b2b_saas.md) or [Collaborative Canvas](collaborative_canvas_workspace.md) playbooks.
* **Most of every page is personalised.** Server islands suit a few per-user regions. When the whole page depends on the visitor, a static build saves little and the site is in effect server-rendered (the book's reasoning, not a documented limit).
* **The team already publishes with the Next.js App Router.** Server Components already "reduce the amount of JavaScript sent to the browser" ([Next.js: Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)). The book's position: migrating to Astro has to earn back its cost, so start from field data that shows a Core Web Vitals failure rather than from the framework choice.
