# Appendix A: The 15 Deadly Frontend Architectural Anti-Patterns

> The quickest way to build a high-performance frontend system is to systematically eliminate known architectural failure modes.

---

### 1. The Redux as a Server Cache Trap
* **The Anti-Pattern:** Manually dispatching actions (`FETCH_USERS_START`, `FETCH_USERS_SUCCESS`) and storing raw asynchronous database records in global client state stores (Redux, Zustand).
* **The Damage:** Memory duplication, stale data races, manually written retry logic, and hundreds of lines of useless boilerplate.
* **The Refactor:** Delegate all remote API data to a dedicated server cache (TanStack Query, SWR, or RTK Query). Reserve client stores strictly for ephemeral, client-owned UI state.

---

### 2. The `useEffect` Data Fetching Waterfall
* **The Anti-Pattern:** Fetching data inside child component `useEffect` hooks. Component A renders, fetches data, renders child Component B, which then triggers its own `useEffect` fetch.
* **The Damage:** Compounding network waterfalls that multiply round-trip latency over mobile networks.
* **The Refactor:** Parallelize fetches using route-level loaders (Remix / Next.js), pre-fetch in parent routers, or hoist queries using GraphQL fragments.

---

### 3. The Uncanny Valley of Full-Page Hydration
* **The Anti-Pattern:** Using full-page Server-Side Rendering (SSR) to send static HTML, then hydrating the entire document tree with a multi-megabyte JavaScript bundle on budget mobile devices.
* **The Damage:** The page looks clickable immediately, but clicks on buttons and links are dropped or delayed because the main thread is locked parsing hydration bundles.
* **The Refactor:** Transition to Islands Architecture (Astro) or React Server Components (RSC) to ship zero client JavaScript for static sections.

---

### 4. Prop Drilling vs. Context Re-Render Thrashing
* **The Anti-Pattern:** Putting rapidly changing state (e.g., mouse coordinates, scroll positions, form inputs) into a top-level React Context provider to avoid prop drilling.
* **The Damage:** Every state update forces every component consuming that Context (and their entire subtrees) to re-render, destroying frame rates.
* **The Refactor:** Use atomic state (Jotai), fine-grained signals, or pass component state down via composition (`children` slots).

---

### 5. Runtime CSS-in-JS in Modern Rendering Environments
* **The Anti-Pattern:** Adopting Emotion or Styled Components in streaming SSR or Server Component setups.
* **The Damage:** Inserting `<style>` tags during render blocks the browser CSSOM parser, breaks streaming HTML, and causes measurable CPU jank.
* **The Refactor:** Migrate to Utility-First CSS (Tailwind) or compile-time zero-runtime CSS (StyleX, Panda CSS, CSS Modules).

---

### 6. Unsanitized Rich-Text Injection
* **The Anti-Pattern:** Directly mounting CMS or user-generated HTML via `dangerouslySetInnerHTML={{ __html: content }}`.
* **The Damage:** Direct opening for Cross-Site Scripting (XSS) attacks.
* **The Refactor:** Always process HTML through `DOMPurify.sanitize()` prior to mounting.

---

### 7. The Micro-Frontend Premature Optimization
* **The Anti-Pattern:** Splitting a 10-person frontend engineering team's application into 6 federated micro-frontends.
* **The Damage:** Multiplied bundle weight (duplicated React versions), fractured local development loops, CSS style leakage, and organizational overhead with zero business upside.
* **The Refactor:** Consolidate into a well-structured modular monorepo using Turborepo or Nx with pnpm workspaces.

---

### 8. Storing Sensitive Tokens in LocalStorage
* **The Anti-Pattern:** Saving OAuth access tokens or JWTs in `localStorage` for convenience.
* **The Damage:** Any minor third-party script injection or XSS vulnerability can read tokens via `localStorage.getItem()` and exfiltrate accounts.
* **The Refactor:** Store session tokens exclusively in `HttpOnly; Secure; SameSite=Lax` cookies that JavaScript cannot touch.

---

### 9. Omitting Explicit Image and Video Dimensions
* **The Anti-Pattern:** Rendering responsive images without explicit `width`, `height`, or CSS `aspect-ratio` properties.
* **The Damage:** Images load and push subsequent content downward, triggering massive Cumulative Layout Shift (CLS) penalties and user mis-clicks.
* **The Refactor:** Always specify aspect ratios or reserve geometric skeleton boxes before media arrives.

---

### 10. Heavy Main-Thread Computational Tasks
* **The Anti-Pattern:** Parsing 10 MB CSV files, running image filters, or computing complex physics on the browser main thread.
* **The Damage:** Freezes the browser UI, drops Interaction to Next Paint (INP) to hundreds of milliseconds, and causes operating systems to prompt "Page Unresponsive".
* **The Refactor:** Move heavy computations, data processing, and embedded database queries to dedicated Web Workers.

---

### 11. Naive Timestamps in Distributed Offline State
* **The Anti-Pattern:** Relying on client `Date.now()` timestamps (Last-Write-Wins) to merge offline edits.
* **The Damage:** Device clock drift guarantees silent data loss when concurrent offline edits are synchronized.
* **The Refactor:** Adopt mathematically proven Conflict-Free Replicated Data Types (CRDTs) such as Yjs or Automerge.

---

### 12. Uncontrolled DOM Node Sprawl
* **The Anti-Pattern:** Appending 5,000 raw table rows or list items directly into the DOM tree.
* **The Damage:** High browser memory consumption, sluggish scrolling, and slow layout recalculation passes.
* **The Refactor:** Virtualize lists using `TanStack Virtual` so only elements currently inside the visible viewport are mounted.

---

### 13. Synchronous Network Requests on Tab Close
* **The Anti-Pattern:** Using synchronous `fetch()` or `XMLHttpRequest` inside `unload` or `beforeunload` events to log analytics.
* **The Damage:** The browser cancels unfinished requests or freezes tab closure.
* **The Refactor:** Use `navigator.sendBeacon(url, data)` or `fetch(url, { keepalive: true })`.

---

### 14. Blind Type Casting at Network Boundaries
* **The Anti-Pattern:** Using TypeScript `as ApiResponse` casting on raw JSON fetches.
* **The Damage:** TypeScript types disappear at runtime. If the backend schema changes, the application crashes silently in production with undefined property errors.
* **The Refactor:** Parse network responses defensively using runtime validation schemas like `zod` or `valibot`.

---

### 15. Unthrottled High-Frequency Event Listeners
* **The Anti-Pattern:** Attaching raw component re-render triggers to `window.onscroll` or `window.onresize` events.
* **The Damage:** Triggers dozens of re-renders per second, causing severe frame drops.
* **The Refactor:** Throttle listeners using `requestAnimationFrame`, or better, replace scroll checks with the native `IntersectionObserver` API.
