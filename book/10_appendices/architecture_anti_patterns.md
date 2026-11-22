---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: react.dev (React 19.3.1), web.dev, MDN and OWASP as of 2026-11; Next.js docs 16.4.6; TanStack Query 5.108.2, SWR 2.5.1, Redux Toolkit 2.15.0, React Router 8.5.2, Astro 7.4.13, Jotai 3.0.2 (GitHub docs), Tailwind CSS 4.3.5, StyleX 0.19.2, Panda CSS 2.6.0, DOMPurify 3.4.18, Turborepo 2.11.13, Yjs 13.6.33, Automerge 3.5.0, TanStack Virtual 3.14.26, Zod 4.6.7, Valibot 1.5.0
review_by: 2027-05
reviewers:
ledger: reviews/architecture-anti-patterns.md
---

# Appendix A: 15 Frontend Architecture Anti-Patterns and Their Fixes

> For a tech lead reviewing a frontend codebase or a design proposal. Each entry names a pattern, the mechanism that makes it fail, the usual fix, and, where one exists, the case in which the warning does not apply. Package versions were checked on npm on 2026-11-22. Statements marked "the book's reasoning" are this book's judgment, not a sourced finding.

---

### 1. Do not use a client store (Redux, Zustand) as a server cache
* **The anti-pattern:** Hand-writing the fetch lifecycle as actions (`FETCH_USERS_START`, `FETCH_USERS_SUCCESS`) and keeping copies of server records in a global client store such as Redux or Zustand.
* **Why it fails:** Every screen then needs its own loading, error, caching and refetch code. Redux's own data layer, RTK Query, exists to remove exactly this: it is "designed to simplify common cases for loading data in a web application, eliminating the need to hand-write data fetching & caching logic yourself" ([RTK Query overview](https://redux-toolkit.js.org/rtk-query/overview)). TanStack Query's docs list the wiring it replaces: connectors, action creators, middlewares, reducers, and loading/error/result states ([TanStack Query: Does this replace client state?](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state)).
* **The fix:** Keep server data in a server cache: TanStack Query 5 (`@tanstack/react-query` 5.108.2), SWR 2 (`swr` 2.5.1) or RTK Query (part of `@reduxjs/toolkit` 2.15.0). Keep the client store for state the client owns, such as open panels or a draft that has not been saved. [Chapter 3](../03_state_and_cache_topologies.md) compares these options.
* **Exception:** Some applications, "like a visual designer or music production application", hold a large amount of synchronous client-only state, and TanStack Query's docs say "TanStack Query is not a replacement for local/client state management" (same source).

---

### 2. Do not chain data fetches through child `useEffect` hooks (React 19)
* **The anti-pattern:** Each component fetches its own data in `useEffect`. The parent renders and fetches; only after its data arrives does it render a child, which then starts its own fetch.
* **Why it fails:** react.dev: "Fetching directly in Effects makes it easy to create 'network waterfalls'. You render the parent component, it fetches some data, renders the child components, and then they start fetching their data. If the network is not very fast, this is significantly slower than fetching all data in parallel." Effects also "don't run on the server", so server-rendered HTML contains only a loading state ([react.dev: useEffect](https://react.dev/reference/react/useEffect)).
* **The fix:** react.dev recommends: "If you use a framework, use its built-in data fetching mechanism", and otherwise a client-side cache such as TanStack Query, SWR or React Router (same source). React Router 8 (`react-router` 8.5.2) in framework mode "runs matched route loaders in parallel" ([React Router: Data Loading](https://reactrouter.com/start/framework/data-loading)). With GraphQL, Relay fragments "let each component declare its own data needs independently, while retaining the efficiency of a single query" ([Relay: Fragments](https://relay.dev/docs/tutorial/fragments-1/)). See also [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect).
* **Exception:** react.dev says "You can continue fetching data directly in Effects if neither of these approaches suit you". If you do, ignore stale responses in the Effect's cleanup function, as in react.dev's `let ignore = false` example (same source).

---

### 3. Do not hydrate a whole server-rendered page when most of it is static
* **The anti-pattern:** Server-rendering a page, then shipping and running the JavaScript for every component on it so the whole document hydrates, including text that never changes.
* **Why it fails:** web.dev: "Server-side rendered pages can appear to be loaded and interactive, but can't actually respond to input until the client-side scripts for components are executed and event handlers have been attached", and the "primary downside" of server rendering with rehydration is that it "can have a significant negative impact on TBT and INP, even if it improves FCP" ([web.dev: Rendering on the Web](https://web.dev/articles/rendering-on-the-web)).
* **The fix:** Send JavaScript only for the parts that are interactive. Astro 7 (`astro` 7.4.13) renders every UI component "to just HTML & CSS, stripping out all client-side JavaScript automatically" unless you opt a component in as an island ([Astro: Islands](https://docs.astro.build/en/concepts/islands/)). In React 19, Server Components render ahead of time in a separate environment, and libraries they import, such as a Markdown parser, are "Not included in bundle" ([react.dev: Server Components](https://react.dev/reference/rsc/server-components)).
* **Exception:** When nearly every component on the page is interactive (an editor, a dense dashboard), there is little static content to leave out, and the gain shrinks (the book's reasoning).

---

### 4. Do not put fast-changing state in a top-level React Context
* **The anti-pattern:** Storing values that change many times a second (pointer position, scroll position, each keystroke in a form) in one Context provider at the top of the tree, to avoid passing props.
* **Why it fails:** "React automatically re-renders all the children that use a particular context starting from the provider that receives a different value", and "Skipping re-renders with memo does not prevent the children receiving fresh context values" ([react.dev: useContext](https://react.dev/reference/react/useContext)). Every consumer runs again on every change, whether or not the part of the value it uses changed.
* **The fix:** Before reaching for context, react.dev suggests you "Extract components and pass JSX as children to them" ([react.dev: Passing Data Deeply with Context](https://react.dev/learn/passing-data-deeply-with-context)). Keep fast-changing values in local state next to the components that read them, or in a store that subscribes per value. Jotai 3 (`jotai` 3.0.2) was "born to solve extra re-render issues in React" and optimizes "renders based on atom dependency" ([Jotai docs: Comparison](https://github.com/pmndrs/jotai/blob/main/docs/basics/comparison.mdx)). With Preact Signals, a signal passed through the tree "can be updated without re-rendering any components", and only components that read `.value` update ([Preact: Signals](https://preactjs.com/guide/v10/signals/)).
* **Exception:** Context suits values that change rarely. react.dev lists theming, the current account, routing and managing state as use cases for context (same react.dev source).

---

### 5. Do not start a new project on runtime CSS-in-JS
* **The anti-pattern:** Choosing a library that injects `<style>` tags at runtime (styled-components, Emotion) for a new React project, especially one that uses streaming or Server Components.
* **Why it fails:** React does not recommend runtime `<style>` injection, because it "forces the browser to recalculate the styles a lot more often" and "can be very slow if it happens at the wrong time in the React lifecycle"; React calls the first problem "not solvable" ([react.dev: useInsertionEffect](https://react.dev/reference/react/useInsertionEffect)). Next.js 16 (docs for 16.4.6) warns that CSS-in-JS with Server Components and streaming needs library support for concurrent rendering, and lists Emotion among the libraries still working on that support ([Next.js: CSS-in-JS](https://nextjs.org/docs/app/guides/css-in-js)). On March 17, 2025 the styled-components maintainer wrote that styled-components "as a project is in 'maintenance mode'", adding: "For new projects, I would not recommend adopting styled-components or most other css-in-js solutions" ([styled-components on OpenCollective](https://opencollective.com/styled-components/updates/thank-you)).
* **The fix:** Generate CSS at build time with Tailwind CSS 4 (`tailwindcss` 4.3.5), CSS Modules, StyleX (`@stylexjs/stylex` 0.19.2) or Panda CSS (`@pandacss/dev` 2.6.0), and pass per-instance values through inline styles. For CSS-in-JS users, React recommends "a combination of the first two approaches (CSS files for static styles, inline styles for dynamic styles)" (react.dev, same source). [Chapter 6](../06_styling_and_presentation.md) compares these options.
* **Exception:** The maintainer's post says styled-components "will continue to be available with occasional bugfixes and misc improvements to support the existing user base" (same source). A working runtime CSS-in-JS codebase is not by itself a reason to migrate (the book's reasoning).

---

### 6. Do not render untrusted HTML without sanitizing it
* **The anti-pattern:** Mounting CMS or user-generated HTML directly with `dangerouslySetInnerHTML={{ __html: content }}`.
* **Why it fails:** react.dev: "If the HTML inside isn't trusted (for example, if it's based on user data), you risk introducing an XSS vulnerability" ([react.dev: Common components](https://react.dev/reference/react-dom/components/common)).
* **The fix:** Sanitize the string with DOMPurify 3 (`dompurify` 3.4.18), `const clean = DOMPurify.sanitize(dirty)`, immediately before mounting it, and do not change the markup afterwards: the README warns that post-processing and changing the markup context defeat sanitization. On the server, DOMPurify "requires a DOM to be present", and the README recommends jsdom ([DOMPurify README](https://github.com/cure53/DOMPurify)). [Appendix C](frontend_security_checklist.md) covers the rest of the XSS checklist.

---

### 7. Do not split one team's application into micro-frontends
* **The anti-pattern:** Splitting an application that one team owns into several independently built and deployed micro-frontends, for example with Module Federation.
* **Why it fails:** The martinfowler.com article that describes the approach lists its costs. Independently built bundles "can cause duplication of common dependencies": "if every micro frontend includes its own copy of React, then we're forcing our customers to download React n times". A standalone development container that differs from production risks a micro-frontend that "is broken, or behaves differently when we deploy to production". CSS "is inherently global", so selectors written by different teams clash on one page. And the architecture brings "more repositories, more tools, more build/deploy pipelines, more servers, more domains" ([Cam Jackson, Micro Frontends](https://martinfowler.com/articles/micro-frontends.html)). Module Federation can load one shared copy of a dependency with `singleton: true` ([Module Federation: shared](https://module-federation.io/configure/shared)).
* **The fix:** Keep one application in a monorepo: pnpm "has built-in support for monorepos" through workspaces ([pnpm: Workspaces](https://pnpm.io/workspaces)), and Turborepo 2 (`turbo` 2.11.13) "is designed for scaling monorepos" ([Turborepo docs](https://turborepo.dev/docs)). Shared types and cross-package refactors then land in one commit, with no runtime composition layer to operate (the book's reasoning, as in the [enterprise B2B playbook](../09_decision_playbooks/enterprise_b2b_saas.md)).
* **Exception:** Several teams that must ship parts of one UI on separate release schedules are the case micro-frontends exist for. The article opens with that problem: "Scaling frontend development so that many teams can work simultaneously on a large and complex product is even harder" (same martinfowler.com source).

---

### 8. Do not store session tokens in `localStorage`
* **The anti-pattern:** Saving OAuth access tokens or JWTs in `localStorage` for convenience.
* **Why it fails:** OWASP: "Do not store session identifiers in local storage as the data is always accessible by JavaScript" ([OWASP HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)). Any script that runs on the page, including an XSS payload or a compromised third-party tag, can read the token and send it elsewhere.
* **The fix:** Have the server set the session in a cookie with `HttpOnly`, `Secure` and an explicit `SameSite` (`Strict` preferred; see [Appendix C](frontend_security_checklist.md)). `HttpOnly` "Forbids JavaScript from accessing the cookie" ([MDN: Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)). Know its limit: MDN notes that such a cookie "will still be sent with JavaScript-initiated requests", so injected script can still act as the user while the page is open, though it cannot copy the token out. XSS prevention and CSRF protection are still needed.

---

### 9. Set dimensions on every image and video
* **The anti-pattern:** Rendering `<img>` or `<video>` elements without `width` and `height` attributes or a CSS `aspect-ratio`.
* **Why it fails:** The browser cannot reserve space for media it has not measured, so content below it moves when the file arrives. web.dev lists "images or videos with unknown dimensions" as a cause of layout shifts, which can make users "click the wrong link or button". A good Cumulative Layout Shift (CLS) is 0.1 or less at the 75th percentile of page loads ([web.dev: CLS](https://web.dev/articles/cls)).
* **The fix:** "Always include width and height size attributes on your images and video elements. Alternatively, reserve the required space with CSS aspect-ratio or similar" ([web.dev: Optimize CLS](https://web.dev/articles/optimize-cls)). The [Core Web Vitals triage guide](core_web_vitals_triage_guide.md) covers ads, embeds and fonts.

---

### 10. Do not run heavy computation on the main thread
* **The anti-pattern:** Parsing large CSV files, applying image filters or running physics simulations on the browser's main thread.
* **Why it fails:** "The main thread can only process one task at a time." Any task longer than 50 ms is a long task, and with many long tasks "the user interface will feel unresponsive" ([web.dev: Optimize long tasks](https://web.dev/articles/optimize-long-tasks)). This shows up as poor Interaction to Next Paint (INP): good INP is 200 ms or less at the 75th percentile of page loads ([web.dev: INP](https://web.dev/articles/inp)).
* **The fix:** Run the computation in a dedicated Web Worker. Workers run on "background threads" and "can perform tasks without interfering with the user interface", but "can't directly manipulate the DOM", so they post results back to the main thread ([MDN: Using Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers)). Work that must touch the DOM can instead be split into smaller tasks that yield to the main thread between steps (web.dev, same long-tasks source).

---

### 11. Do not merge offline edits by client wall-clock timestamp
* **The anti-pattern:** Stamping each record or document with the client's `Date.now()` and letting the newest timestamp win when offline edits sync (whole-record last-write-wins).
* **Why it fails:** When two people edit different fields of the same record while offline, one person's edit disappears without an error, and a client whose clock runs fast wins every conflict (the book's reasoning; the [collaborative canvas playbook](../09_decision_playbooks/collaborative_canvas_workspace.md) shows the same failure).
* **The fix:** Use a CRDT library that merges concurrent changes. Yjs 13 (`yjs` 13.6.33) is a CRDT framework that "supports ... offline editing" ([Yjs README](https://github.com/yjs/yjs)). Automerge 3 (`@automerge/automerge` 3.5.0) merges edits to different properties, and for conflicting writes to the same property it picks a winner by "the internal ID of the operation, not a wall clock time", keeping the other value available through `Automerge.getConflicts()` ([Automerge: Conflicts](https://automerge.org/docs/reference/documents/conflicts/)).
* **Exception:** Data with a single writer (one user on one device) has no concurrent edits to merge, so a CRDT adds machinery with nothing to resolve (the book's reasoning).

---

### 12. Do not render thousands of rows into the DOM at once
* **The anti-pattern:** Appending every row of a large table or list to the DOM.
* **Why it fails:** With a large DOM, "the browser must constantly recompute the position and styling of nodes" as users and scripts interact, and broad selectors such as `document.querySelectorAll('li')` can hold references to a very large number of nodes. Lighthouse warns when the body element has more than about 800 nodes; since Lighthouse 13 the audit is part of the "Optimize DOM size" insight ([Chrome for Developers: Avoid an excessive DOM size](https://developer.chrome.com/docs/lighthouse/performance/dom-size)).
* **The fix:** Virtualize with TanStack Virtual 3 (`@tanstack/react-virtual` 3.14.26), "a headless UI utility for virtualizing long lists" ([TanStack Virtual](https://tanstack.com/virtual/latest/docs/introduction)). Virtualization "keeps the DOM small by only rendering the items that are visible in the scroll viewport", plus an overscan buffer ([TanStack Table: Virtualization](https://tanstack.com/table/latest/docs/framework/react/guide/virtualization)).
* **Exception:** TanStack's docs: "Virtualization is not a replacement for server-side pagination, filtering, or sorting", since the data still has to be in the browser, and "For small tables, normal rendering is simpler and usually preferable" (same TanStack Table source). Rows outside the viewport are not in the DOM, so the browser's find-in-page cannot reach them.

---

### 13. Send exit analytics with `sendBeacon` on `visibilitychange`, not in `unload`
* **The anti-pattern:** Sending analytics from an `unload` or `beforeunload` handler, for example with a synchronous `XMLHttpRequest` that holds the page open until it finishes.
* **Why it fails:** MDN: these workarounds "block unloading the document, which slows down navigation to the next page", and the events themselves are unreliable: "In many situations, especially on mobile, the browser will not fire these events" ([MDN: sendBeacon](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon)). Chrome "has stopped firing unload events by default", and `unload` listeners can keep pages out of the back/forward cache ([MDN: unload event](https://developer.mozilla.org/en-US/docs/Web/API/Window/unload_event)).
* **The fix:** Listen for `visibilitychange` and, when `document.visibilityState === "hidden"`, call `navigator.sendBeacon(url, data)`. The data is sent asynchronously "without delaying unload or the next navigation", as a POST of up to about 64 KiB (MDN sendBeacon, Baseline widely available, available across browsers since April 2018). For other methods or headers, use `fetch(url, { method: 'POST', body, keepalive: true })`: the browser "will not abort the associated request if the page that initiated it is unloaded", and keepalive bodies are limited to 64 kibibytes ([MDN: RequestInit keepalive](https://developer.mozilla.org/en-US/docs/Web/API/RequestInit)).

---

### 14. Validate API responses instead of casting them (TypeScript)
* **The anti-pattern:** Writing `const user = (await res.json()) as User` and trusting the type.
* **Why it fails:** The TypeScript handbook: "Because type assertions are removed at compile-time, there is no runtime checking associated with a type assertion. There won't be an exception or null generated if the type assertion is wrong" ([TypeScript: Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)). If the backend changes a field's type, the wrong value travels through the app and fails later, far from the network call. In the example below, a cast would let `user.id + 1` evaluate to the string `"71"` with no error.
* **The fix:** Parse responses at the boundary with a runtime schema. In Zod 4 (`zod` 4.6.7), `.parse()` returns "a strongly-typed deep clone of the input" or throws a `ZodError`, and `.safeParse()` returns a result object instead of throwing ([Zod: Basic usage](https://zod.dev/basics)). Valibot 1 (`valibot` 1.5.0) is a schema library with "no dependencies" that "can run in any JavaScript environment" ([Valibot: Introduction](https://valibot.dev/guides/introduction/)).

This runs as an ES module with Node 24 and `zod` 4.6.7, and prints `Bad API response at id: Invalid input: expected number, received string`:

```js
import { z } from 'zod'

const User = z.object({ id: z.number(), name: z.string() })

// The backend started sending id as a string.
const body = JSON.parse('{"id":"7","name":"Ada"}')

const result = User.safeParse(body)
if (result.success) {
  console.log(result.data.id + 1)
} else {
  const issue = result.error.issues[0]
  console.error(`Bad API response at ${issue.path.join('.')}: ${issue.message}`)
}
```

---

### 15. Do not re-render on every `scroll` or `resize` event
* **The anti-pattern:** Setting React state from a `window` `scroll` or `resize` listener, so components re-render on every event.
* **Why it fails:** MDN: "Since scroll events can fire at a high rate, the event handler shouldn't execute computationally expensive operations such as DOM modifications" ([MDN: scroll event](https://developer.mozilla.org/en-US/docs/Web/API/Document/scroll_event)).
* **The fix:** To know when an element enters or leaves the viewport (lazy loading, infinite scroll, visibility tracking), use `IntersectionObserver` (Baseline widely available, available across browsers since March 2019), which reports intersections asynchronously instead of event handlers calling `getBoundingClientRect()` on the main thread; its callback still runs on the main thread, so keep it short ([MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)). To react to an element's size, use `ResizeObserver` (Baseline widely available, available across browsers since July 2020) ([MDN: ResizeObserver](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver)). When you need the scroll position itself, throttle with a timer such as `setTimeout()`. Do not throttle with `requestAnimationFrame()`: MDN calls that "useless because animation frame callbacks are fired at the same rate as scroll event handlers" (MDN scroll event, same source).
