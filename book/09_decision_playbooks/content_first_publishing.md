---
status: draft
ai_involvement: drafted
last_verified:
verified_against:
review_by:
reviewers:
---

# Decision Playbook: Content-First Publishing & Documentation

> Recommended Architecture for: Documentation Hubs, Tech Blogs, Marketing Sites, News Portals, and Catalog Storefronts.

---

## 1. The Archetype Profile

* **Primary Success Metric:** Sub-second Largest Contentful Paint (LCP < 1.2s), near-zero Interaction to Next Paint (INP < 50ms), and 100/100 Google Lighthouse SEO scores.
* **Traffic Pattern:** Highly asymmetrical: 99% reads, 1% writes. Massive traffic spikes from social sharing or search indexing.
* **Target Environment:** Global consumer devices ranging from modern desktop gigabit connections to low-end smartphones on high-latency 3G/4G networks.

---

## 2. The Recommended Architectural Stack

| Layer | Recommended Choice | Rationale |
| :--- | :--- | :--- |
| **Execution Boundary** | **Astro (Islands Architecture)** | Delivers 100% static HTML by default. Sends exactly 0 KB of client JavaScript for static articles, hydrating only dynamic widgets (search modals, theme toggles, comment feeds) on demand. |
| **Reactivity Engine** | **Lightweight Preact or Svelte Islands** | Embedded only within dynamic islands; avoids loading full React runtime bundles on content pages. |
| **Styling Paradigm** | **Tailwind CSS (Utility-First)** | Compiles down to an atomic stylesheet capped under 15 KB gzipped. Inline critical CSS eliminates render-blocking network requests. |
| **Asset Delivery** | **Global Edge CDN (Cloudflare / Fastly / Vercel)** | Pages pre-rendered via Static Site Generation (SSG) or Incremental Static Regeneration (ISR), served directly from edge points adjacent to users. |
| **Search Engine** | **Pagefind (Static Search) or Algolia** | Pagefind runs client-side search against pre-built static indexes with zero server infrastructure cost. |

---

## 3. What to Explicitly Avoid

* **Do NOT use a heavy Single Page Application (Vite + React SPA):**
  Sending a 300 KB JavaScript bundle to render an article causes blank screens on slow mobile networks and penalizes search engine crawlers.
* **Do NOT use full-page hydration SSR (Traditional Next.js Pages Router):**
  Hydrating static paragraphs and headings wastes user battery and CPU cycles with zero user benefit.
* **Do NOT use runtime CSS-in-JS (Emotion / Styled Components):**
  Injecting runtime `<style>` tags delays the browser's First Contentful Paint.

---

## 4. Constraint Checklist
* Is dynamic user authentication required on every page? If no, stay strictly with Islands Architecture.
* Are there frequent content updates? Implement Incremental Static Regeneration (ISR) or webhook-triggered edge builds.
