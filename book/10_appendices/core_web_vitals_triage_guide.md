---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: web.dev (Web Vitals, LCP, Optimize LCP, TTFB, Optimize TTFB, INP, Optimize long tasks, CLS, Optimize CLS, Extract critical CSS); Chrome DevTools Performance and Rendering docs; MDN (fetchpriority, Cache-Control, Scheduler.yield, aspect-ratio, font-display, size-adjust, ascent-override); react.dev Render and Commit; Preact Signals v10 guide; Solid README; Partytown docs, @qwik.dev/partytown 1.0.5; Node.js 24.18.1
review_by: 2027-05
reviewers:
ledger: reviews/core-web-vitals-triage-guide.md
---

# Appendix B: Core Web Vitals Production Triage Guide

> For a developer whose field data shows a failing Core Web Vital (LCP, INP or CLS): how to find the cause in Chrome DevTools and which fix matches each cause.

All three thresholds below are "good" values measured at the 75th percentile of page loads, segmented across mobile and desktop devices ([web.dev: Web Vitals](https://web.dev/articles/vitals)). DevTools gives you a lab reproduction on your own machine; the pass or fail verdict comes from field data.

---

## 1. Largest Contentful Paint (LCP) Triage

**The Target:** an LCP of 2.5 seconds or less at the 75th percentile ([web.dev: LCP](https://web.dev/articles/lcp)).

### Find the LCP element and its slow subpart

Open Chrome DevTools > **Performance**. The Live metrics screen names the LCP element and highlights it on the page when you hover over it. Record a page load: the LCP marker appears in the trace overlay next to FCP and DOMContentLoaded ([DevTools Performance reference](https://developer.chrome.com/docs/devtools/performance/reference)).

The LCP element can be an `<img>`, a `<video>` (its poster image or first frame), an element with a CSS `url()` background image, or a block-level element containing text ([web.dev: LCP](https://web.dev/articles/lcp)). web.dev splits LCP into four subparts: time to first byte, resource load delay, resource load duration and element render delay ([web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp)). Fix whichever subpart is largest.

### Fix by cause

1. **LCP element is an image the browser finds late:**
   * *Problem:* The image URL appears only in CSS or JavaScript, so the browser's preload scanner cannot discover it in the HTML.
   * *Fix:* Put the image in the HTML as an `<img>` where possible. If it must come from CSS or JavaScript, preload it with a high fetch priority in the HTML markup ([web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp)):
     ```html
     <link rel="preload" as="image" href="/hero.avif" type="image/avif" fetchpriority="high">
     ```
   * *Fix:* For an `<img>` already in the HTML, add `fetchpriority="high"`, because browsers do not load images at the highest priority by default. Setting a high priority on more than one or two images stops it helping ([web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp)). The `fetchpriority` attribute is Baseline newly available since October 2024 ([MDN: fetchpriority](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/fetchpriority)).
   * *Fix:* Never set `loading="lazy"` on the LCP image. A lazy image does not load until layout confirms it is in the viewport, which always adds resource load delay ([web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp)).
2. **Slow Time to First Byte (TTFB):**
   * *Problem:* The server takes too long to send the first byte of HTML. TTFB is not a Core Web Vitals metric; as a rough guide, web.dev suggests most sites aim for 0.8 seconds or less ([web.dev: TTFB](https://web.dev/articles/ttfb)).
   * *Fix:* Serve the HTML from a CDN edge cache with appropriate `Cache-Control` headers; this does not suit personalized pages ([web.dev: Optimize TTFB](https://web.dev/articles/optimize-ttfb)). The `stale-while-revalidate` directive lets a cache reuse a stale response while it revalidates in the background ([MDN: Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)).
   * *Fix:* Stream the HTML so the browser can parse the first chunks, including the `<head>`, before the rest of the response arrives. Node.js and Deno support streaming server rendering, and React has server APIs that stream markup as it renders ([web.dev: Optimize TTFB](https://web.dev/articles/optimize-ttfb)).
3. **Render-blocking CSS:**
   * *Problem:* The browser does not render the page until external stylesheets in the `<head>` have downloaded.
   * *Fix:* Inline the CSS needed for the first view in a `<style>` tag and defer the rest. Inline only small amounts: inlined CSS cannot be cached across page loads, and a stylesheet that loads slower than the LCP resource is a poor candidate ([web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp); [web.dev: Extract critical CSS](https://web.dev/articles/extract-critical-css)).

---

## 2. Interaction to Next Paint (INP) Triage

**The Target:** an INP of 200 milliseconds or less at the 75th percentile; above 500 milliseconds is poor. INP measures the time from a click, tap or key press until the next frame is painted, and reports the longest interaction observed during the visit, ignoring outliers ([web.dev: INP](https://web.dev/articles/inp)).

### Find the slow interaction and the long task behind it

Open Chrome DevTools > **Performance**, set **CPU** throttling in the capture settings, record, and interact with the slow control. Throttling is relative to your own CPU and cannot truly simulate a mobile device; DevTools can calibrate a preset for low- and mid-tier phones. The **Interactions** track marks interactions over 200 milliseconds with a red triangle, and the tooltip splits each into input delay, processing time and presentation delay. On the **Main** track, long tasks have a red triangle, with the part over 50 milliseconds shaded red ([DevTools Performance reference](https://developer.chrome.com/docs/devtools/performance/reference)).

### Fix by cause

1. **Heavy Main-Thread Computation:**
   * *Problem:* Any task longer than 50 milliseconds is a long task, and the browser cannot respond to input while it runs ([web.dev: Optimize long tasks](https://web.dev/articles/optimize-long-tasks)).
   * *Fix:* Break the loop into chunks and yield to the main thread between them. With `scheduler.yield()`, the continuation of your task runs before any other similar tasks are started, but MDN lists it as limited availability, not Baseline, so feature-detect it and fall back to `setTimeout`, which puts the rest of the work at the back of the task queue ([MDN: Scheduler.yield()](https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield); [web.dev: Optimize long tasks](https://web.dev/articles/optimize-long-tasks)). The example below yields only after about 50 milliseconds of work, the deadline web.dev uses. It runs as written in Node.js 24, which takes the `setTimeout` path:
     ```javascript
     // Yield to the main thread: scheduler.yield() where supported, setTimeout otherwise.
     function yieldToMain() {
       if (globalThis.scheduler?.yield) {
         return globalThis.scheduler.yield();
       }
       return new Promise((resolve) => setTimeout(resolve, 0));
     }

     // Process items in chunks, yielding once each chunk has run past the deadline.
     async function processLargeBatch(items, processItem, deadline = 50) {
       let lastYield = performance.now();
       for (const item of items) {
         processItem(item);
         if (performance.now() - lastYield > deadline) {
           await yieldToMain(); // the browser can handle input and paint here
           lastYield = performance.now();
         }
       }
     }

     // Usage: double 200,000 numbers without one long task.
     const items = Array.from({ length: 200_000 }, (_, i) => i);
     const results = [];
     processLargeBatch(items, (n) => results.push(n * 2)).then(() => {
       console.log(`processed ${results.length} items`);
     });
     ```
2. **Whole-Tree Re-Rendering in React:**
   * *Problem:* When a component's state changes, React re-renders that component and every component nested inside it by default, which is costly when the state lives high in the tree ([react.dev: Render and Commit](https://react.dev/learn/render-and-commit)).
   * *Fix:* Move frequently changing state somewhere only its readers subscribe to it. With Preact Signals, a signal passed through the tree can update without re-rendering the components it passes through; only components that read `.value` re-render ([Preact: Signals](https://preactjs.com/guide/v10/signals/)). Solid compiles to real DOM updates with no virtual DOM diff, but adopting it means changing frameworks ([Solid README](https://github.com/solidjs/solid)).
3. **Third-Party Script Contention:**
   * *Problem:* Analytics, ad and chat scripts compete with your code for the main thread.
   * *Fix:* Partytown (`@qwik.dev/partytown`, 1.0.x) runs opted-in third-party scripts in a web worker ([Partytown](https://partytown.qwik.dev/)). It suits scripts that mostly send events, such as Google Tag Manager. It may not be best suited for UI-intensive scripts that build a mini-app within your page; DOM operations within the worker are purposely throttled; and `event.preventDefault()` called by a third-party script has no effect ([Partytown: Trade-Offs](https://partytown.qwik.dev/trade-offs)).

---

## 3. Cumulative Layout Shift (CLS) Triage

**The Target:** a CLS of 0.1 or less at the 75th percentile; above 0.25 is poor. CLS is not a sum over the whole visit: it is the largest burst (session window) of unexpected layout shifts, where shifts are less than 1 second apart and the window lasts at most 5 seconds ([web.dev: CLS](https://web.dev/articles/cls)).

### See which elements shift

Open Chrome DevTools > **Rendering** tab > check **Layout Shift Regions**, then reload. Areas that shift are briefly highlighted in purple ([DevTools: Rendering](https://developer.chrome.com/docs/devtools/rendering/performance)). In a Performance recording, click a layout shift to see its score and potential culprits ([DevTools Performance reference](https://developer.chrome.com/docs/devtools/performance/reference)).

### Fix by cause

1. **Images and Embeds Missing Dimensions:**
   * *Fix:* Set `width` and `height` attributes on `<img>` and `<video>` elements; browsers derive an aspect ratio from them and reserve the space before the file loads. Alternatively, reserve the space with CSS `aspect-ratio` ([web.dev: Optimize CLS](https://web.dev/articles/optimize-cls)), which is Baseline widely available since September 2021 ([MDN: aspect-ratio](https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio)):
     ```css
     .card-thumbnail {
       width: 100%;
       aspect-ratio: 16 / 9;
     }
     ```
2. **Content Injected Above Existing Content:**
   * *Problem:* A banner or advertisement finishes loading and pushes the article down.
   * *Fix:* Reserve the space in advance with `min-height`, `aspect-ratio` or a placeholder. When an ad's size varies, size the slot for the smallest or most likely ad and accept some shift for larger ones; keep the placeholder if no ad arrives, because collapsing the space shifts content too ([web.dev: Optimize CLS](https://web.dev/articles/optimize-cls)).
3. **Web Font Swaps (FOIT and FOUT):**
   * *Problem:* The fallback font takes up a different amount of space than the web font. Both a flash of unstyled text and a flash of invisible text shift content, because invisible text is still laid out in the fallback font ([web.dev: Optimize CLS](https://web.dev/articles/optimize-cls)).
   * *Fix:* `font-display: optional` uses the web font only if it is ready by initial layout, so no re-layout happens ([web.dev: Optimize CLS](https://web.dev/articles/optimize-cls)); it is Baseline widely available since January 2020 ([MDN: font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display)).
   * *Fix:* Match the fallback font's metrics to the web font with `size-adjust`, `ascent-override`, `descent-override` and `line-gap-override` in a fallback `@font-face` rule ([web.dev: Optimize CLS](https://web.dev/articles/optimize-cls)). `size-adjust` is Baseline widely available since September 2023 ([MDN: size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust)); `ascent-override` is limited availability, so some browsers will ignore it ([MDN: ascent-override](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/ascent-override)).
