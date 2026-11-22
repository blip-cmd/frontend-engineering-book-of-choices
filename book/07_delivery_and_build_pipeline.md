---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: vite 8.3.8, next 16.4.6 (Turbopack docs, Next.js 16 blog), @rspack/core 2.3.3, webpack 5.113.0 (SplitChunksPlugin docs), bun 1.4.5 (bun.com docs, oven-sh/bun README and languages API), react 19.3.1, RFC 6928, RFC 5681, RFC 9002, MDN, web.dev Web Vitals and INP launch post, Google Search Central, hpbn.co ch. 2
review_by: 2027-05
reviewers:
ledger: reviews/delivery-and-build-pipeline.md
---

# Chapter 7: Delivery & Build Pipeline: Bundlers, Streaming, and Core Web Vitals

> A delivery pipeline decides how many bytes reach the user before the first paint, and how much JavaScript the main thread must run before the page can respond to input.

---

## 1. What the Network and the Main Thread Limit

This chapter is for a developer or tech lead choosing a bundler and a code-splitting strategy for a web app. Two physical limits shape every delivery decision:

* **The main thread runs one task at a time.** Almost all page JavaScript runs there, and "the browser blocks interactions from occurring while a task of any length is running" ([web.dev: Optimize long tasks](https://web.dev/articles/optimize-long-tasks)). Large bundles mean long parse, compile and execution tasks, which show up as poor Interaction to Next Paint (INP).
* **CSS blocks rendering.** "By default, CSS is treated as a render-blocking resource", so the browser renders nothing until the CSSOM is built ([web.dev: Render-blocking CSS](https://web.dev/articles/critical-rendering-path/render-blocking-css)). A stylesheet that arrives late delays the first paint and Largest Contentful Paint (LCP).

The build pipeline (how assets are compiled and chunked) controls how much code the main thread receives. The transport pipeline (how bytes are ordered and sent over HTTP) controls when the first useful bytes arrive. Sections 2 and 4 cover the first, section 3 covers the second, and section 5 gives the field metrics that judge both.

---

## 2. Choose a Bundler by the Framework and Config You Already Have

Versions checked with `npm view` on 2026-11-21: vite 8.3.8, next 16.4.6, @rspack/core 2.3.3, webpack 5.113.0, bun 1.4.5. Speed figures in this table are **vendor claims** quoted from each project's own documentation; none is an independent benchmark.

| Bundler | Implementation (from its docs) | Maintainers' speed claim | Fits | Limitation |
| :--- | :--- | :--- | :--- | :--- |
| **Vite 8.x (Rolldown)** | Vite 8 "ships with Rolldown as its single, unified, Rust-based bundler"; in development, source code "is served on-demand over native ESM" ([Vite 8 announcement](https://vite.dev/blog/announcing-vite8); [Why Vite](https://vite.dev/guide/why)) | "up to 10-30x faster builds" ([Vite 8 announcement](https://vite.dev/blog/announcing-vite8)) | SPAs, libraries, and frameworks built on Vite | "Most existing Vite plugins work out of the box with Vite 8": most, not all, so check each plugin when upgrading ([Vite 8 announcement](https://vite.dev/blog/announcing-vite8)) |
| **Turbopack (inside Next.js 16.x)** | "an incremental bundler optimized for JavaScript and TypeScript, written in Rust, and built into Next.js"; the default bundler in Next.js 16 ([Turbopack docs](https://nextjs.org/docs/app/api-reference/turbopack)) | "up to 5-10x faster Fast Refresh, and 2-5x faster builds" ([Next.js 16 blog](https://nextjs.org/blog/next-16)) | Next.js apps (App Router and Pages Router) | Usable only through Next.js (the `turbopack` npm package is at version 0.0.1); on platforms that fall back to WASM bindings, Turbopack is unsupported and you run `next build --webpack` ([Turbopack docs](https://nextjs.org/docs/app/api-reference/turbopack)) |
| **Rspack 2.x** | "a high-performance web bundler written in Rust" with "a modernized webpack API" ([Rspack introduction](https://rspack.rs/guide/start/introduction)) | "more than 10 times faster than webpack" ([Rspack introduction](https://rspack.rs/guide/start/introduction)) | Moving an existing webpack 5 configuration off webpack | Compatible with "the vast majority of webpack's configuration options and APIs" ([Rspack introduction](https://rspack.rs/guide/start/introduction)), not all of them; it also keeps webpack's configuration model, and with it that model's complexity (the book's judgment) |
| **Bun 1.4.x (`Bun.build`)** | A runtime "written in Rust and powered by JavaScriptCore" whose single binary also includes a test runner, package manager and bundler ([Bun docs](https://bun.com/docs); [Bun bundler](https://bun.com/docs/bundler)) | none quoted here | Projects that already run on Bun | The book's judgment: choose it when Bun is already the runtime; for framework apps, the framework's own bundler (Vite or Turbopack) is the one the framework documents and tests |

**When not to switch.** If a webpack 5 build is fast enough and its plugins are stable, a migration costs plugin checks and CI changes for a speed gain you have not measured on your own code. Measure your own build before trusting any row's speed claim.

---

## 3. TCP Slow Start: Fit the Critical Bytes in the First Round Trip

TCP does not send a whole response at once. [RFC 6928](https://www.rfc-editor.org/rfc/rfc6928.txt) raises the upper bound on a new connection's initial congestion window "to 10 segments (maximum 14600 B)", and during slow start the window "grows rapidly, roughly doubling every round trip" ([MDN: How browsers work](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work); [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681.txt)). HTTP/3 runs over QUIC, which follows the same analysis: [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.txt) limits the initial window "to the larger of 14,720 bytes or twice the maximum datagram size". That first window is the origin of the "14 KB rule".

### What the rule says, and what it does not

MDN advises including "everything the browser needs to start rendering a page, or at least the HTML and CSS template for the basic page structure, in the first 14KB" ([MDN: How browsers work](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work)). The window counts bytes on the wire, so the budget applies to the compressed HTML, inlined critical CSS and head tags. After the first window the server "must stop and wait for an acknowledgment" before sending more, which is why the performance of small transfers "is often limited by the roundtrip time between server and client" ([High Performance Browser Networking, ch. 2](https://hpbn.co/building-blocks-of-tcp/)).

The rule is not a cliff. MDN states that "even if the requested page's HTML is larger than the initial 14KB packet, the browser will begin parsing and attempt to render content based on the data it has." The first window also arrives only after the connection is set up: "All TCP connections begin with a three-way handshake" before any application data flows ([High Performance Browser Networking, ch. 2](https://hpbn.co/building-blocks-of-tcp/)), so a 14 KB page still needs more than one round trip from a cold start.

---

## 4. Code Splitting Strategies: Avoiding the Monolith and the Waterfall

Splitting application code into chunks keeps unused code off the main thread, but splitting too finely creates request waterfalls.

1. **Route-level splitting (the baseline):**
   * In React 19.x, `lazy` "lets you defer loading component's code until it is rendered for the first time" ([react.dev: lazy](https://react.dev/reference/react/lazy)). Wrapping each route's component in `lazy()` means users who visit `/dashboard` do not download the code for `/settings` or `/billing`.
2. **Component-level lazy loading (selective):**
   * Defer heavy components that are below the fold or shown on demand: rich-text editors, charting libraries, 3D canvas viewers and modal dialogs. Do not lazy-load the LCP element: web.dev warns that lazy-loading the LCP image "will always lead to unnecessary resource load delay" ([web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp)).
3. **The anti-pattern (micro-chunk waterfalls):**
   * HTTP/2 multiplexing does not make extra chunks free. webpack's documentation says browsers and HTTP/2 "can handle many parallel requests, but extra chunks still add scheduling, header, cache lookup, parsing, and evaluation overhead" ([webpack SplitChunksPlugin](https://webpack.js.org/plugins/split-chunks-plugin/)). Its production defaults reflect this: a new chunk must be at least 20 KB before minification and gzip (`minSize: 20000`), and loading should need at most 30 parallel requests, both on demand and at initial page load ([webpack SplitChunksPlugin](https://webpack.js.org/plugins/split-chunks-plugin/)).
   * Chains are worse than counts: when chunk A dynamically imports B, which imports C, each download starts only after the previous one has arrived and run.
   * *Balance:* group related modules into shared chunks with the bundler's chunking options, then measure. Vite 8 lists "more flexible chunk splitting" among the features Rolldown enables ([Vite 8 announcement](https://vite.dev/blog/announcing-vite8)).

---

## 5. Core Web Vitals: The Field Thresholds the Pipeline Must Meet

Core Web Vitals measure loading, interactivity and visual stability from real-user data. A page passes when it meets all three thresholds at "the 75th percentile of page loads, segmented across mobile and desktop devices" ([web.dev: Web Vitals](https://web.dev/articles/vitals)). INP replaced First Input Delay as a Core Web Vital in March 2024 ([web.dev: INP is a Core Web Vital](https://web.dev/blog/inp-cwv-launch)). For search, Google says that good Core Web Vitals, along with other page experience aspects, align "with what our core ranking systems seek to reward" ([Google Search Central](https://developers.google.com/search/docs/appearance/core-web-vitals)).

1. **Largest Contentful Paint (LCP): good is 2.5 seconds or less** ([web.dev: Web Vitals](https://web.dev/articles/vitals)).
   * *Measures:* when the largest content element in the viewport (hero image, heading, video poster) is rendered.
   * *Fix:* put the LCP image in the initial HTML so the preload scanner finds it, and mark it `fetchpriority="high"`; use `<link rel="preload" as="image">` when the image is only referenced from CSS; reduce or inline render-blocking stylesheets; and cut Time to First Byte by minimizing redirects and serving cached HTML from CDN edge servers rather than the origin ([web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp)).
2. **Interaction to Next Paint (INP): good is 200 milliseconds or less** ([web.dev: Web Vitals](https://web.dev/articles/vitals)).
   * *Measures:* the latency of clicks, taps and key presses until the next frame is painted, observed across all of a user's interactions with the page ([web.dev: INP](https://web.dev/articles/inp)).
   * *Fix:* break long tasks by yielding to the main thread with `setTimeout(fn, 0)` or `await scheduler.yield()` ([web.dev: Optimize long tasks](https://web.dev/articles/optimize-long-tasks)). `scheduler.yield()` is not Baseline (Chrome and Edge 129, Firefox 142, no Safari support), so feature-detect it and fall back to `setTimeout` ([MDN: Scheduler.yield()](https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield)). Move heavy computation to a Web Worker, which "can perform tasks without interfering with the user interface" ([MDN: Using Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers)), and reduce how much of the page re-renders on each interaction.
3. **Cumulative Layout Shift (CLS): good is 0.1 or less** ([web.dev: Web Vitals](https://web.dev/articles/vitals)).
   * *Measures:* unexpected layout shifts during the page's life.
   * *Fix:* "Always include width and height size attributes on your images and video elements", or reserve the space with CSS `aspect-ratio`, and reserve space for ads, embeds and other dynamically injected content ([web.dev: Optimize CLS](https://web.dev/articles/optimize-cls)).

---

## 6. References

* [Further reading: *High Performance Browser Networking* (Ilya Grigorik)](../library/reading_list.md); the TCP chapter is free online at [hpbn.co](https://hpbn.co/building-blocks-of-tcp/)
* [RFC 6928: Increasing TCP's Initial Window](https://www.rfc-editor.org/rfc/rfc6928.txt)
* [MDN: Populating the page: how browsers work](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work)
* [web.dev: Web Vitals](https://web.dev/articles/vitals) and [Interaction to Next Paint is officially a Core Web Vital](https://web.dev/blog/inp-cwv-launch)
