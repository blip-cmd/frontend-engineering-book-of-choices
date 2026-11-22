---
page: book/07_delivery_and_build_pipeline.md
verified: 2026-11-21
---

# Claim Ledger: Chapter 7, Delivery & Build Pipeline

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a developer or tech lead choosing a bundler and a code-splitting strategy for a web app. The page helps them decide which bundler fits their framework, how to size the first HTML response, how finely to split code, and which field thresholds to hold the result to. Thesis (unchanged from the draft): delivery is limited by TCP slow start and a single main thread, so the build pipeline (bundling, chunking) and the transport pipeline (what arrives in the first round trip) must both be managed, and Core Web Vitals judge the outcome.

**History.** The AI-generated draft had seven passages with unsourced numbers. It described Bun as written in Zig (Bun's docs now say Rust), stated vendor speed multipliers as fact ("5x to 10x faster" for Rspack, where Rspack's own page says "more than 10 times"), claimed HTML that fits in 14 KB paints in "a single network round trip" (it ignores the TCP handshake, and MDN says the browser renders incrementally beyond 14 KB), gave Core Web Vitals thresholds as strict "<" bounds without the 75th percentile, and cited two references with no URL that could not be matched to a published source.

---

## 1. Author pass (2026-11-21)

Sources were fetched in the same session with `curl` and quotes matched against the extracted page text. Package versions were checked with `npm view`.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | "The browser blocks interactions from occurring while a task of any length is running"; the main thread processes one task at a time | [web.dev: Optimize long tasks](https://web.dev/articles/optimize-long-tasks) | verified (quote) |
| 2 | "By default, CSS is treated as a render-blocking resource" until the CSSOM is built | [web.dev: Render-blocking CSS](https://web.dev/articles/critical-rendering-path/render-blocking-css) | verified (quote); draft's "inlined or preloaded" fix corrected, since preloading a stylesheet does not stop it blocking render |
| 3 | "A 2 MB JavaScript bundle" causes "seconds of frozen interactivity" on mobile | none found | removed; rewritten qualitatively (long parse/compile/execute tasks hurt INP) |
| 4 | Versions: vite 8.3.8, next 16.4.6, @rspack/core 2.3.3, webpack 5.113.0, bun 1.4.5 | `npm view <name> version` | verified |
| 5 | Vite 8 "ships with Rolldown as its single, unified, Rust-based bundler" | [Vite 8 announcement](https://vite.dev/blog/announcing-vite8) | verified (quote); draft's limitation "transitions to Rolldown" was stale and is replaced |
| 6 | Vite dev server serves source "on-demand over native ESM" | [Why Vite](https://vite.dev/guide/why) | verified (quote) |
| 7 | Vite vendor claim: "up to 10-30x faster builds" | Vite 8 announcement | verified (quote), labelled as vendor claim |
| 8 | "Most existing Vite plugins work out of the box with Vite 8" | Vite 8 announcement | verified (quote) |
| 9 | Vite 8 lists "more flexible chunk splitting" among Rolldown features | Vite 8 announcement | verified (quote) |
| 10 | Turbopack is "an incremental bundler optimized for JavaScript and TypeScript, written in Rust, and built into Next.js"; works with Pages and App Router | [Turbopack docs](https://nextjs.org/docs/app/api-reference/turbopack) | verified (quote) |
| 11 | Turbopack is the default bundler in Next.js 16 | Turbopack docs; [Next.js 16 blog](https://nextjs.org/blog/next-16) | verified |
| 12 | Next.js vendor claim: "up to 5-10x faster Fast Refresh, and 2-5x faster builds" | Next.js 16 blog | verified (quote), labelled as vendor claim |
| 13 | WASM-binding platforms do not support Turbopack; use `--webpack` | Turbopack docs | verified |
| 14 | `turbopack` npm package is at version 0.0.1 (no standalone release) | `npm view turbopack` | verified; replaces draft's "tightly integrated into Vercel", which no source supported |
| 15 | Rspack is "a high-performance web bundler written in Rust" with "a modernized webpack API" | [Rspack introduction](https://rspack.rs/guide/start/introduction) | verified (quote) |
| 16 | Rspack vendor claim: "more than 10 times faster than webpack" | Rspack introduction | verified (quote); corrects draft's "5x to 10x faster", which was stated as fact |
| 17 | Rspack is compatible with "the vast majority of webpack's configuration options and APIs" | Rspack introduction | verified (quote) |
| 18 | Bun is "written in Rust and powered by JavaScriptCore"; single executable with test runner, script runner, package manager | [Bun docs](https://bun.com/docs); [GitHub repo languages API](https://api.github.com/repos/oven-sh/bun/languages) | verified (quote); **corrects** draft's "Zig / JavaScriptCore" |
| 19 | Bun has a bundler (`Bun.build`) | [Bun bundler docs](https://bun.com/docs/bundler) | verified |
| 20 | RFC 6928 raises the initial window upper bound "to 10 segments (maximum 14600 B)" | [RFC 6928](https://www.rfc-editor.org/rfc/rfc6928.txt) | verified (quote) |
| 21 | During slow start the window "grows rapidly, roughly doubling every round trip" | [MDN: How browsers work](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work); [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681.txt) | verified (quote) |
| 22 | QUIC initial window limited "to the larger of 14,720 bytes or twice the maximum datagram size" | [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.txt) | verified (quote); added so the rule is stated for HTTP/3 too |
| 23 | MDN: include what the browser needs to start rendering "in the first 14KB" | MDN: How browsers work | verified (quote) |
| 24 | After the first window the server "must stop and wait for an acknowledgment" | [High Performance Browser Networking, ch. 2](https://hpbn.co/building-blocks-of-tcp/) | verified (quote); replaces draft's "wait for an ACK packet to return across the ocean" |
| 25 | HTML larger than 14 KB is still parsed and rendered incrementally | MDN: How browsers work | verified (quote); **corrects** draft's implication that the page cannot paint until the rest arrives |
| 26 | "All TCP connections begin with a three-way handshake" before data flows, so 14 KB is not a one-round-trip load | High Performance Browser Networking, ch. 2 | verified (quote); **corrects** draft's "single network round trip" |
| 27 | React `lazy` "lets you defer loading component's code until it is rendered for the first time" | [react.dev: lazy](https://react.dev/reference/react/lazy) | verified (quote); React 19.3.1 per `npm view react version` |
| 28 | Lazy-loading the LCP image "will always lead to unnecessary resource load delay" | [web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp) | verified (quote) |
| 29 | Over-splitting into "hundreds of tiny 1 KB chunks causes HTTP/2 request congestion" | none found | removed; replaced with webpack's documented overhead statement (row 30) |
| 30 | Extra chunks "still add scheduling, header, cache lookup, parsing, and evaluation overhead"; defaults `minSize` 20000 bytes (20 KB before min+gz in production) and at most 30 parallel requests on demand and at initial load | [webpack SplitChunksPlugin](https://webpack.js.org/plugins/split-chunks-plugin/) | verified (quote) |
| 31 | LCP good is within 2.5 s; INP 200 ms or less; CLS 0.1 or less | [web.dev: Web Vitals](https://web.dev/articles/vitals) | verified (quote); draft's "< 2.5 s", "< 200 ms", "< 0.1" corrected to "or less" |
| 32 | Assess at "the 75th percentile of page loads, segmented across mobile and desktop devices" | web.dev: Web Vitals | verified (quote); added |
| 33 | INP replaced First Input Delay as a Core Web Vital in March 2024 | [web.dev: INP is a Core Web Vital](https://web.dev/blog/inp-cwv-launch) (page dated 2024-03-12) | verified |
| 34 | Good Core Web Vitals align "with what our core ranking systems seek to reward" | [Google Search Central: Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals) | verified (quote); replaces draft's "the industry benchmark for ... search engine ranking" |
| 35 | LCP fixes: make the LCP image discoverable in HTML, `fetchpriority="high"`, `rel="preload"` for CSS-referenced images, reduce TTFB (redirects, CDN edge caching) | web.dev: Optimize LCP | verified; **corrects** draft's blanket "preload hero images" |
| 36 | INP measures interaction latency across all interactions | [web.dev: INP](https://web.dev/articles/inp) | verified (quote) |
| 37 | Yield with `setTimeout(fn, 0)` or `scheduler.yield()` | web.dev: Optimize long tasks | verified |
| 38 | `scheduler.yield()` is not Baseline: Chrome and Edge 129, Firefox 142, no Safari | [MDN: Scheduler.yield()](https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield); web.dev support table | verified ("Limited availability. This feature is not Baseline") |
| 39 | A Web Worker "can perform tasks without interfering with the user interface" | [MDN: Using Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) | verified (quote) |
| 40 | "Transition to fine-grained signals to eliminate whole-tree reconciliation" | none found | removed as unsourced; replaced with the qualitative "reduce how much of the page re-renders on each interaction" (recommendation narrowed, not reversed) |
| 41 | "Always include width and height size attributes on your images and video elements", or CSS `aspect-ratio`; reserve space for dynamically injected content | [web.dev: Optimize CLS](https://web.dev/articles/optimize-cls) | verified (quote) |
| 42 | References "Optimizing Content Delivery for TCP Slow Start" (Grigorik) and "The Evolution of Core Web Vitals: INP Deep Dive" (Walton) | none found | removed: no URL given and no matching published article located; replaced with fetched primary sources |
| 43 | Book judgments: Rspack keeps webpack's configuration complexity; choose Bun's bundler when Bun is already the runtime; do not switch bundlers without measuring | none | labelled on the page as the book's judgment |

**Code.** The page has no runnable code blocks; inline snippets (`lazy()`, `scheduler.yield()`, HTML attributes) are API names checked against the sources above.

**Research-note links.** The draft linked only to `library/reading_list.md`, which is allowed to stay; no other `library/` links were present.

## 2. Independent verifier pass (2026-11-21 to 2026-11-22)

A separate agent that did not write the page or section 1 extracted the claims from the page itself, fetched all 24 cited URLs with `curl -sL` and searched the extracted text for each quote, and re-ran `npm view` for every package.

**Claims checked: about 65** (every quoted phrase, number, version, API name and attribution on the page, including the five pinned versions and three Core Web Vitals thresholds). Result: 2 PARTIAL (both corrected below), 0 UNSUPPORTED, all others SUPPORTED or explanatory background. The remaining unsourced sentences are explanatory background with no numbers (for example "Chains are worse than counts") or are labelled as the book's judgment.

Points checked with particular care:

* **Bun "written in Rust".** Supported by three independent primary texts. bun.com/docs: "It's written in Rust and powered by JavaScriptCore, reducing startup time and memory usage." The oven-sh/bun GitHub README: "It's written in Rust and powered by JavaScriptCore under the hood". `gh api repos/oven-sh/bun/languages` lists Rust as the largest language (90,574,949 bytes, then C++ 13,968,248 and TypeScript 10,617,803) and lists no Zig; the repo's primary language field is Rust. The bundled test runner, package manager and bundler match bun.com/docs: "Bun ships as a single, dependency-free binary and includes a runtime, package manager, test runner, and bundler." Latest release `bun-v1.4.5`, matching `npm view bun version`.
* **Vendor speed claims.** All three are verbatim and sit in the column headed "Maintainers' speed claim", under a sentence calling them vendor claims: Vite "up to 10-30x faster builds" (Vite 8 announcement), Next.js "up to 5-10x faster Fast Refresh, and 2-5x faster builds" (Next.js 16 blog), Rspack "more than 10 times faster than webpack" (Rspack introduction). Bun's row quotes none.
* **Core Web Vitals.** web.dev/articles/vitals: LCP "within 2.5 seconds", INP "200 milliseconds or less", CLS "0.1. or less" (sic), and "the 75th percentile of page loads, segmented across mobile and desktop devices", with a page passing when it meets the targets "at the 75th percentile for all three". The INP launch post is dated 2024-03-12 and says "INP has replaced FID as a Core Web Vital metric", so "March 2024" holds.
* **`scheduler.yield()` support.** MDN marks it "Limited availability. This feature is not Baseline"; browser-compat-data (via the MDN BCD API) gives Chrome 129, Edge 129, Firefox 142, Safari and Safari iOS unsupported.
* **Versions.** `npm view`: vite 8.3.8, next 16.4.6, @rspack/core 2.3.3, webpack 5.113.0, bun 1.4.5, turbopack 0.0.1, react 19.3.1. All match the page.
* **Networking numbers.** RFC 6928 "to 10 segments (maximum 14600 B)"; RFC 9002 "the larger of 14,720 bytes or twice the maximum datagram size"; webpack `minSize: 20000`, "bigger than 20kb (before min+gz ...)" and at most 30 parallel requests on demand and at initial load in production. All verbatim.

**Edits made (2):**

1. Section 3: "so on high-latency mobile links the first 14 KB decide how early rendering can start" was attributed to High Performance Browser Networking ch. 2, which does not say it (PARTIAL: an extrapolation). Reworded to the source's own sentence: the performance of small transfers "is often limited by the roundtrip time between server and client".
2. Section 5, LCP fix: "remove render-blocking CSS" stretched web.dev: Optimize LCP, whose heading is "Reduce or inline render-blocking stylesheets" (PARTIAL). Reworded to "reduce or inline render-blocking stylesheets".

**Code checks.** The page has no fenced code blocks. Inline API names (`lazy`, `Bun.build`, `scheduler.yield()`, `setTimeout(fn, 0)`, `fetchpriority="high"`, `<link rel="preload" as="image">`, `next build --webpack`, `minSize`) were each found in the cited source. Every package named exists on npm under the expected name.

**Verdict: PASS.** No UNSUPPORTED claims remain, both PARTIAL claims were corrected, and every number links to its source. Front matter set to `agent-verified`, `last_verified: 2026-11`, `review_by: 2027-05` (build tooling: six months), `reviewers` left empty.

## 3. Known omissions (follow-up content, not errors)

Topics a complete delivery chapter could add, each needing its own sourced entry:

* **Streaming.** The chapter title promises streaming, but no section covers streamed SSR (for example React 19 `renderToReadableStream`, Next.js streaming) or HTTP chunked delivery.
* `103 Early Hints`, `preconnect` and resource priority beyond `fetchpriority`
* Compression choices (gzip, Brotli, Zstandard) and their Baseline status
* Other bundlers named in the ecosystem: webpack 5 itself, esbuild, Parcel, standalone Rolldown
* Where field data comes from (CrUX, RUM libraries such as `web-vitals`) and how to read the 75th percentile per device type
* Production source maps, cache-busting file names and long-term caching headers
* bfcache and Speculation Rules for navigation speed
* Image formats and responsive images for LCP

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | N/A | 2 | **17** (15 of 18 points, scaled) |

D1 and D2 are 1 because the bundler table gives fit and limitation per tool and one "when not to switch" case, but few concrete counter-scenarios. D8 is 1 because section 1 points to later sections. D9 is N/A: the page has no worked example. All gates pass except G8 (human accountability), which the `agent-verified` status would disclose instead.
