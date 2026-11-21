---
status: draft
ai_involvement: drafted
last_verified:
verified_against:
review_by:
reviewers:
---

# Chapter 7: Delivery & Build Pipeline: Bundlers, Streaming, and Core Web Vitals

> The finest architecture fails if the delivery pipeline ships a bloated, unoptimized payload that stalls on the user's network.

---

## 1. The Core Dilemma

Frontend delivery is a game of constraints governed by network physics:
* A mobile device on a cellular network cannot download and execute a 2 MB JavaScript bundle without experiencing seconds of frozen interactivity.
* The browser's main thread is single-threaded. When parsing huge scripts, user interactions are queued or dropped, causing Interaction to Next Paint (INP) scores to fail.
* If critical CSS is not inlined or preloaded, the browser stalls rendering entirely until external stylesheets arrive, destroying Largest Contentful Paint (LCP).

To deliver world-class performance, frontend engineers must master both the build pipeline (how assets are compiled and chunked) and the transport pipeline (how assets are streamed and prioritized over HTTP).

---

## 2. The Landscape of Build Tools

| Bundler / Engine | Language Core | Primary Strength | Best Use Case | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| **Vite (Rollup / Rolldown)** | Rust + JavaScript | Blazing instant dev server via native ESM; universal plugin ecosystem | Standard web apps, SPAs, library authors | Production bundling transitions to native Rust engine (Rolldown) |
| **Turbopack** | Rust | High-speed incremental caching tailored for Next.js | Large Next.js App Router applications | Tightly integrated into Vercel and Next.js; limited standalone usage |
| **Rspack** | Rust | Drop-in replacement for Webpack with 5x to 10x faster build speeds | Massive legacy enterprise Webpack migrations | Retains some Webpack configuration complexities |
| **Bun** | Zig / JavaScriptCore | All-in-one bundler, test runner, and package manager | Fast scripting, microservices, local tooling | Younger ecosystem for complex multi-page asset manifests |

---

## 3. The 14 KB Rule: Optimizing for TCP Slow Start

As documented in [High Performance Browser Networking](../library/reading_list.md), new TCP connections begin with an initial congestion window (initcwnd) of 10 packets, which equals approximately **14 KB of compressed data**.

### The Rule:
If your initial server-rendered HTML payload, critical inline CSS, and essential document head tags fit within **14 KB**, the browser can parse and paint the first screen in a **single network round trip**. If your initial HTML exceeds 14 KB, the connection must pause, wait for an ACK packet to return across the ocean, and double the congestion window before delivering the remainder of the page.

---

## 4. Code Splitting Strategies: Avoiding the Monolith and the Waterfall

Splitting application code into chunks is necessary, but naive code splitting introduces dangerous request waterfalls:

1. **Route-Level Splitting (Essential Baseline):**
   * Dynamically import page routes using `React.lazy()` or framework file routers. Users visiting `/dashboard` never download the JavaScript for `/settings` or `/billing`.
2. **Component-Level Lazy Loading (Strategic):**
   * Defer heavy, below-the-fold, or conditional components: rich-text editors, charting libraries (Recharts, Chart.js), 3D canvas viewers, and modal dialogues.
3. **The Anti-Pattern (Micro-Chunk Waterfalls):**
   * Over-splitting code into hundreds of tiny 1 KB chunks causes HTTP/2 request congestion and waterfall chains where chunk A imports chunk B, which imports chunk C.
   * *Optimal Balance:* Group related utilities into coherent shared vendor chunks with modern bundlers.

---

## 5. Core Web Vitals: The Engineering Metric Scorecard

Google's Core Web Vitals are the industry benchmark for real-world user experience and search engine ranking:

1. **Largest Contentful Paint (LCP) - Target: < 2.5 seconds:**
   * *Metric:* How quickly the main content block (hero image, heading, video poster) becomes visible.
   * *Fix:* Preload hero images using `<link rel="preload" as="image">`, eliminate render-blocking CSS, and utilize edge-cached SSR or static HTML.
2. **Interaction to Next Paint (INP) - Target: < 200 milliseconds:**
   * *Metric:* The latency of user interactions (clicks, taps, keypresses) from input to the next painted frame.
   * *Fix:* Break long-running JavaScript tasks using `scheduler.yield()` or `setTimeout(0)`, transition to fine-grained signals to eliminate whole-tree reconciliation, and offload heavy computations to Web Workers.
3. **Cumulative Layout Shift (CLS) - Target: < 0.1:**
   * *Metric:* Visual stability of the page during loading.
   * *Fix:* Explicitly set `width` and `height` attributes on images and video embeds, and reserve skeleton bounding boxes for dynamic content.

---

## 6. References & Library Audits
* [Further reading: *High Performance Browser Networking* (Ilya Grigorik)](../library/reading_list.md)
* Ilya Grigorik: *Optimizing Content Delivery for TCP Slow Start*
* Philip Walton: *The Evolution of Core Web Vitals: INP Deep Dive* (Google Chrome Team)
