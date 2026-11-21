# Appendix B: Core Web Vitals Production Triage Guide

> An actionable diagnostic and remediation protocol for resolving failing Google Core Web Vitals (LCP, INP, CLS) in production environments.

---

## 1. Largest Contentful Paint (LCP) Triage

**The Target:** LCP must occur within **2.5 seconds** of navigation on real mobile devices.

### Diagnosing the Root Cause:
Open Chrome DevTools -> **Performance** tab -> Record page load -> Check the **Timings** row for the `LCP` marker. Identify which element triggered LCP (typically a hero image, video poster, or large heading block).

### The Remediation Playbook:
1. **LCP Element is an Image:**
   * *Problem:* The browser discovers the image URL late in the document lifecycle.
   * *Fix:* Inject a high-priority preload tag in the `<head>` of your server-rendered HTML:
     ```html
     <link rel="preload" as="image" href="/hero.avif" fetchpriority="high">
     ```
   * *Fix:* Never apply `loading="lazy"` to the LCP hero image. Lazy loading explicitly tells the browser to delay fetching until layout calculation finishes.
2. **Slow Time to First Byte (TTFB):**
   * *Problem:* Origin server database queries delay initial HTML delivery past 800ms.
   * *Fix:* Implement Stale-While-Revalidate edge caching or migrate dynamic queries to streaming SSR where initial `<head>` and critical styles flush immediately.
3. **Render-Blocking CSS:**
   * *Problem:* External stylesheets halt DOM rendering until downloaded.
   * *Fix:* Inline critical CSS directly into `<style>` tags in the HTML `<head>`, and load secondary styles asynchronously.

---

## 2. Interaction to Next Paint (INP) Triage

**The Target:** User interactions (clicks, taps, keypresses) must paint the next frame within **200 milliseconds**.

### Diagnosing the Root Cause:
Open Chrome DevTools -> **Performance** tab -> Enable **CPU Throttling (4x Slowdown)** -> Interact with controls -> Look for red-striped **Long Tasks** exceeding 50 milliseconds.

### The Remediation Playbook:
1. **Heavy Main-Thread Computation:**
   * *Fix:* Break monolithic execution loops into cooperative time-slices using `scheduler.yield()` or `setTimeout(..., 0)`:
     ```javascript
     async function processLargeBatch(items) {
       for (const item of items) {
         processItem(item);
         if (shouldYield()) {
           await scheduler.yield(); // Lets the browser paint user input
         }
       }
     }
     ```
2. **Whole-Tree Re-Rendering Thrash:**
   * *Problem:* Clicking a toggle forces an entire parent component tree to re-execute in React.
   * *Fix:* Transition hot-state variables to fine-grained signals (Preact/Solid) or atomic state (Jotai) to bypass tree diffing.
3. **Third-Party Script Contention:**
   * *Problem:* Analytics trackers, advertising pixels, and customer chat widgets consume main-thread execution time.
   * *Fix:* Offload third-party scripts to run in background Web Workers using `Partytown`.

---

## 3. Cumulative Layout Shift (CLS) Triage

**The Target:** CLS score must remain below **0.1** across the entire page lifecycle.

### Diagnosing the Root Cause:
Open Chrome DevTools -> **Rendering** drawer -> Check **Layout Shift Regions**. Elements that shift during page load will flash in purple.

### The Remediation Playbook:
1. **Images and Embeds Missing Aspect Ratio:**
   * *Fix:* Always set explicit `width` and `height` attributes on `<img>` tags, or define CSS `aspect-ratio`:
     ```css
     .card-thumbnail {
       width: 100%;
       aspect-ratio: 16 / 9;
     }
     ```
2. **Dynamic Content Injected Above the Fold:**
   * *Problem:* A banner or advertisement finishes loading and pushes existing article content downward.
   * *Fix:* Reserve space in advance using a fixed-height container or skeleton placeholder with identical dimensions.
3. **Web Font Swapping Layout Jumps (FOIT/FOUT):**
   * *Problem:* Fallback system font occupies different horizontal character widths than the custom web font, causing paragraphs to re-wrap when the custom font swaps in.
   * *Fix:* Use `font-display: optional`, or calculate fallback font metrics using CSS `size-adjust`, `ascent-override`, and `descent-override` so the fallback font occupies identical geometry.
