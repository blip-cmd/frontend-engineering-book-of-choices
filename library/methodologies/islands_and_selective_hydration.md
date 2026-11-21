# Architectural Methodology: Islands Architecture and Selective Hydration

* **Identifier:** `islands-and-selective-hydration`
* **Pioneers & Key Implementers:** Jason Miller, Astro Core Team, Fresh (Deno), Marko (eBay)
* **Core Mechanisms:** Static HTML default, partial hydration, independent component roots, client directives (`client:load`, `client:visible`, `client:idle`)

---

## 1. Mechanics and Mental Model
In traditional Single Page Applications (SPAs) and conventional Server-Side Rendering (SSR), the server renders the entire page into HTML, and the browser must then download, parse, and execute JavaScript for the entire page to attach event handlers. This process (full page hydration) incurs a severe CPU cost on mobile devices.

Islands Architecture inverts this paradigm:
1. **The Ocean of Static HTML:** By default, 100% of the rendered page is pure, static HTML and CSS with zero client-side JavaScript sent to the browser.
2. **Interactive Islands:** Dynamic widgets (e.g., an interactive search bar, an image carousel, an authenticated user menu) are explicitly defined as isolated, independent root components ("islands").
3. **Selective & Deferred Hydration:** Each island loads its JavaScript independently based on configurable triggers:
   * `client:load`: Hydrate immediately on page load.
   * `client:idle`: Hydrate only when main thread activity drops.
   * `client:visible`: Hydrate only when an IntersectionObserver detects the element in the viewport.
   * `client:media`: Hydrate only when a responsive media query matches.

## 2. Comparative Trade-offs

### What You Gain:
* **Near-Zero Baseline JavaScript:** Content-heavy sites ship 80-95% less JavaScript than equivalent Next.js or Nuxt setups.
* **Immunity to Top-Level Hydration Failures:** A runtime crash or hydration mismatch in one island does not break the rest of the page.
* **Component Framework Agnosticism:** Different islands on the same page can run React, Vue, Svelte, or vanilla web components.

### What You Forfeit:
* **Global Interactive Shell State:** Sharing client state across disparate islands requires decoupled mechanisms (such as `nanostores`, browser custom events, or shared broadcast channels) rather than standard React context providers.
* **Seamless SPA-Style Page Transitions:** Traditional document navigation causes full page refreshes unless coupled with View Transitions API or lightweight router shims.

## 3. Decision Bounds: When to Choose and Avoid

### Choose Islands When:
* Content-to-interactivity ratio is high (marketing sites, content portals, e-commerce catalog pages, documentation sites).
* Core Web Vitals (specifically Largest Contentful Paint and Interaction to Next Paint) directly impact business revenue and SEO ranking.
* The application runs on budget mobile devices across developing markets.

### Avoid Islands When:
* The application is an interconnected desktop-class web app (e.g., Figma, linear issue trackers, digital audio workstations, complex analytics dashboards) where almost every pixel is interactive and bound to a single centralized state graph.

## 4. Enabling Ecosystem & Tooling
* **Frameworks:** Astro, Deno Fresh, Marko, îles.
* **State Bridges:** Nano Stores, URL query params, LocalStorage sync, custom events.
