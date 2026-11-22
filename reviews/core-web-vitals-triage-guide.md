---
page: book/10_appendices/core_web_vitals_triage_guide.md
verified: 2026-11-21
---

# Claim Ledger: Appendix B, Core Web Vitals Production Triage Guide

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a frontend developer or tech lead whose field data shows a failing Core Web Vital. The page helps them decide which fix to apply by first finding the cause in Chrome DevTools. Thesis: each failing metric has a small set of common causes (late-discovered LCP image, slow TTFB, render-blocking CSS; long main-thread tasks, wide React re-renders, third-party scripts; unsized media, injected content, font swaps), and each cause has a specific, documented fix.

**History.** The author pass (2026-11-21) rewrote the AI-generated draft. The draft's thresholds were stated without the 75th-percentile rule and as "on real mobile devices" (web.dev segments mobile and desktop); it described CLS as a whole-lifecycle total (it is the largest session window); it placed the LCP marker in the Timings track (it is in the trace overlay); and it claimed Jotai bypasses tree diffing and that ad placeholders can always match the final size. No recommendation was reversed; the preload advice was narrowed to images not discoverable in the HTML, as web.dev recommends.

---

## 1. Author pass (2026-11-21)

All sources were fetched in this session (curl, HTML stripped to text) and each claim was matched against the page text. Package versions checked with `npm view` on 2026-11-21.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | Core Web Vitals are LCP, INP and CLS; "good" thresholds are measured at the 75th percentile of page loads, segmented across mobile and desktop | [web.dev: Web Vitals](https://web.dev/articles/vitals) | verified (quote); draft's "on real mobile devices" corrected |
| 2 | Good LCP is 2.5 seconds or less | [web.dev: LCP](https://web.dev/articles/lcp) | verified (quote) |
| 3 | Live metrics screen shows the LCP element and highlights it on hover; LCP marker appears in the trace overlay with FCP and DCL | [DevTools Performance reference](https://developer.chrome.com/docs/devtools/performance/reference) | corrected: draft said "Timings row"; the Timings track holds custom `performance.mark()`/`measure()` entries |
| 4 | LCP candidate element types: `<img>`, `<video>` poster or first frame, `url()` background image, block-level text | web.dev: LCP | verified; replaces draft's "typically a hero image" |
| 5 | LCP subparts: TTFB, resource load delay, resource load duration, element render delay | [web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp) | verified |
| 6 | LCP resource should be discoverable by the preload scanner; if referenced only from CSS or JS, preload it with `fetchpriority="high"` | web.dev: Optimize LCP | verified (quote); draft applied preload to all images, narrowed |
| 7 | Browsers do not load images at the highest priority by default; `fetchpriority="high"` on more than one or two images stops helping | web.dev: Optimize LCP | verified (quote) |
| 8 | `fetchpriority` Baseline newly available since October 2024 | [MDN: fetchpriority](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/fetchpriority) | verified |
| 9 | Never lazy-load the LCP image; lazy images wait until layout confirms they are in the viewport | web.dev: Optimize LCP; [MDN img](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img) | verified (quote: "Never lazy-load your LCP image") |
| 10 | TTFB is diagnostic, not a Core Web Vital; "as a rough guide" 0.8 seconds or less | [web.dev: TTFB](https://web.dev/articles/ttfb) | verified; draft's "800ms" kept with the source's hedge |
| 11 | CDN edge caching with `Cache-Control`; not appropriate for personalized content | [web.dev: Optimize TTFB](https://web.dev/articles/optimize-ttfb) | verified (quote) |
| 12 | `stale-while-revalidate` lets a cache reuse a stale response while revalidating | [MDN: Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control) | verified (quote) |
| 13 | Streaming markup; Node.js and Deno support streaming SSR; React has streaming server APIs | web.dev: Optimize TTFB | verified |
| 14 | Inline critical CSS, defer the rest; inline only small stylesheets because inlined CSS is not cached | web.dev: Optimize LCP; [web.dev: Extract critical CSS](https://web.dev/articles/extract-critical-css) | verified; caveat added from source |
| 15 | Good INP is 200 ms or less; poor above 500 ms; p75 | [web.dev: INP](https://web.dev/articles/inp) | verified (quote) |
| 16 | INP covers click, tap and keyboard interactions; reports the longest interaction, ignoring outliers | web.dev: INP | verified (quote) |
| 17 | CPU throttling is relative to your CPU, cannot truly simulate mobile; Calibrate option for low- and mid-tier devices | DevTools Performance reference | verified (quote); draft's "4x" preset not found in the docs, removed |
| 18 | Interactions track: red triangle over 200 ms; input delay, processing time, presentation delay | DevTools Performance reference | verified |
| 19 | Long tasks: red triangle, part over 50 ms shaded red | DevTools Performance reference | verified (quote); draft's "red-striped" matches web.dev wording too |
| 20 | Long task is any task over 50 ms; the browser cannot respond to input while it runs | [web.dev: Optimize long tasks](https://web.dev/articles/optimize-long-tasks) | verified (quote) |
| 21 | `scheduler.yield()` continuation is prioritized; `setTimeout` puts work at the back of the queue | web.dev: Optimize long tasks | verified (quote) |
| 22 | `scheduler.yield()` is limited availability, not Baseline; needs a fallback | [MDN: Scheduler.yield()](https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield); web.dev | verified; fallback added |
| 23 | 50 ms yield deadline in the batch example | web.dev: Optimize long tasks | verified ("A common deadline is 50 milliseconds") |
| 24 | `processLargeBatch` example runs | Node.js 24.18.1 | verified (run): printed `processed 200000 items`; also run with a stub `scheduler.yield` and a 5 ms deadline (77 yields, all 3,000,000 items processed). Draft called an undefined `shouldYield()`; rewritten as runnable |
| 25 | React re-renders the updated component and all nested components by default | [react.dev: Render and Commit](https://react.dev/learn/render-and-commit) | verified (quote) |
| 26 | Preact Signals update without re-rendering pass-through components; components reading `.value` re-render | [Preact: Signals](https://preactjs.com/guide/v10/signals/) | verified (quote) |
| 27 | Jotai renders are optimized by atom dependency, avoiding React context's extra re-renders | [Jotai](https://jotai.org/) (home page source in the pmndrs/jotai repo) | verified; draft's "bypass tree diffing" corrected |
| 28 | Solid uses fine-grained updates to the real DOM, no virtual DOM diff | [Solid README](https://github.com/solidjs/solid) | verified (quote) |
| 29 | Partytown runs opted-in third-party scripts in a web worker; package `@qwik.dev/partytown` 1.0.5 | [Partytown](https://partytown.qwik.dev/); [How it works](https://partytown.qwik.dev/how-does-partytown-work); `npm view` | verified |
| 30 | Partytown suits GTM-style event scripts, not UI-heavy scripts; DOM operations throttled; `preventDefault()` has no effect | [Partytown: Trade-Offs](https://partytown.qwik.dev/trade-offs) | verified (quote); caveats added |
| 31 | Good CLS is 0.1 or less, poor above 0.25; p75 | [web.dev: CLS](https://web.dev/articles/cls) | verified; draft's "below 0.1" corrected |
| 32 | CLS is the largest session window; shifts less than 1 s apart, window at most 5 s | web.dev: CLS | verified (quote); draft's "across the entire page lifecycle" corrected |
| 33 | Layout Shift Regions highlights shifts in purple | [DevTools: Rendering](https://developer.chrome.com/docs/devtools/rendering/performance) | verified (quote) |
| 34 | Clicking a layout shift in a recording shows scores and potential culprits | DevTools Performance reference | verified (quote) |
| 35 | Set `width`/`height` on images and video; browsers derive an aspect ratio; or use CSS `aspect-ratio` | [web.dev: Optimize CLS](https://web.dev/articles/optimize-cls) | verified (quote) |
| 36 | `aspect-ratio` Baseline widely available since September 2021 | [MDN: aspect-ratio](https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio) | verified |
| 37 | Reserve space with `min-height`/`aspect-ratio`/placeholder; size for smallest or most likely ad; do not collapse the space | web.dev: Optimize CLS | verified; draft's "identical dimensions" corrected |
| 38 | Both FOUT and FOIT shift layout because invisible text is laid out in the fallback font | web.dev: Optimize CLS | verified (quote) |
| 39 | `font-display: optional` avoids re-layout; Baseline widely since January 2020 | web.dev: Optimize CLS; [MDN: font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display) | verified |
| 40 | `size-adjust`, `ascent-override`, `descent-override`, `line-gap-override` reduce fallback differences | web.dev: Optimize CLS | verified; `line-gap-override` added from source |
| 41 | `size-adjust` Baseline widely since September 2023; `ascent-override` limited availability | [MDN: size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust); [MDN: ascent-override](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/ascent-override) | verified |
| 42 | Package versions: `jotai` 3.0.2, `@preact/signals` 2.11.4, `solid-js` 2.0.3, `@qwik.dev/partytown` 1.0.5 | `npm view` | verified; only Partytown's major is pinned on the page |

Removed: the "4x Slowdown" preset (not in the fetched DevTools docs), "Lazy loading tells the browser to delay fetching until layout calculation finishes" (replaced by web.dev's wording), and "Origin server database queries" as the stated cause of slow TTFB (unsourced specific cause; made general). The HTML and CSS snippets are fragments by nature; the JavaScript example is runnable.

## 2. Independent verifier pass (2026-11-21)

A separate agent that did not write the page or section 1 extracted the claims from the page itself (41 factual claims, plus 4 package checks and 1 runnable example), fetched every cited source with `curl` (HTML stripped to text) and WebFetch, and searched the text for each claim.

**Verdict: PASS** after the edits below. No UNSUPPORTED claim remains, every PARTIAL claim was reworded to its source, and every number on the page sits next to its source link.

| # | Claim on the page | Source | Verdict | Edit |
| :--- | :--- | :--- | :--- | :--- |
| V1 | "Jotai ... re-renders components based on the atoms they use, which avoids the extra re-renders of React context" | [jotai.org](https://jotai.org/) | UNSUPPORTED: on 2026-11-21 jotai.org serves a Namecheap "Domain registration has expired" parking page (curl and WebFetch both), so the citation does not resolve (G2) | Sentence deleted. No replacement source added, per the protocol |
| V2 | "TTFB is a diagnostic metric, not a Core Web Vital" | [web.dev: TTFB](https://web.dev/articles/ttfb) | PARTIAL: the page says TTFB "isn't a Core Web Vitals metric"; the word "diagnostic" is not on it | Reworded to "TTFB is not a Core Web Vitals metric; as a rough guide, web.dev suggests most sites aim for 0.8 seconds or less" |
| V3 | "`scheduler.yield()` resumes your work ahead of other queued tasks" | [web.dev: Optimize long tasks](https://web.dev/articles/optimize-long-tasks) | PARTIAL: the source says the continuation "will run before any other similar tasks are started", and higher-priority work such as input still runs first | Reworded to the source's wording |
| V4 | Partytown "does not suit scripts that build UI in your page" | [Partytown: Trade-Offs](https://partytown.qwik.dev/trade-offs) | PARTIAL: the source hedges ("may not be best suited" for UI-intensive scripts that build "a mini-app within your page") | Reworded to the source's hedge; "worker script" corrected to "third-party script" for `preventDefault()` |
| V5 | Preload the CSS/JS-referenced LCP image "in the `<head>` of the server-rendered HTML" | [web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp) | PARTIAL: the source says to preload it "using `<link rel="preload">` in the HTML markup (or using a Link header)"; it does not specify server rendering or the `<head>` | Reworded to "in the HTML markup" |

All other claims were SUPPORTED, matching section 1 rows 1 to 23 and 25 to 41 (Jotai row 27 excepted). Checked in particular: the 75th-percentile and mobile/desktop wording; the LCP, INP, CLS and TTFB thresholds (2.5 s; 200 ms and 500 ms; 0.1 and 0.25; 0.8 s); the four LCP subparts; the DevTools live metrics, overlay markers, Interactions track (red triangle over 200 ms), long-task shading over 50 ms, CPU throttling caveats and Calibrate option; the session-window definition (less than 1 second apart, at most 5 seconds); and the MDN Baseline statuses and dates (fetchpriority newly available October 2024; aspect-ratio September 2021; font-display January 2020; size-adjust September 2023; ascent-override and `Scheduler.yield()` limited availability).

**Code checks.** The `processLargeBatch` example was extracted from the page and run in Node.js 24.18.1 (where `globalThis.scheduler` is undefined, so it takes the `setTimeout` path): printed `processed 200000 items`. Edge cases: a stubbed `scheduler.yield` with 3,000,000 items and a 5 ms deadline (116 yields through the stub, all items processed); an empty array (`processed 0 items`); a `processItem` that throws (the returned promise rejects with the error). The HTML and CSS blocks are fragments. `npm view`: `@qwik.dev/partytown` 1.0.5 (repository QwikDev/partytown), `@preact/signals` 2.11.4, `solid-js` 2.0.3, `jotai` 3.0.2 (the package exists; only its documentation site's domain has lapsed).

## 3. Known omissions (follow-up content, not errors)

Topics a complete triage guide could add, each needing its own sourced entry:

* Field data sources: CrUX, PageSpeed Insights and the `web-vitals` library for attributing slow interactions in production
* LCP: image CDNs, responsive `srcset`/`sizes`, client-side rendering delays, `103 Early Hints`, bfcache
* INP: `content-visibility`, reducing DOM size, React 18+ `startTransition`/`useDeferredValue` and `memo` as alternatives to changing state libraries
* Third-party scripts: `async`/`defer`, facades for embeds, and loading after interaction, as lighter options than Partytown
* CLS: animations that trigger layout instead of `transform`, and bfcache restores

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | **17** |

D1 and D2 are 1: each cause has one main fix with limits stated (inline only small CSS, Partytown not for UI scripts, signals require a library change), but few alternatives are compared. D9 is 1: one runnable example; the other snippets are short fragments. Gate G8 (human accountability) is not met by this pass, as expected for an agent-verified page.
