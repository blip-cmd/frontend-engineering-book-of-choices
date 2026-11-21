---
status: draft
ai_involvement: drafted
last_verified:
verified_against:
review_by:
reviewers:
---

# Decision Playbook: Low-Latency Global E-Commerce Storefronts

> Recommended Architecture for: Direct-to-Consumer (DTC) Brands, Global Retail Storefronts, and High-Conversion Marketplaces.

---

## 1. The Archetype Profile

* **Primary Success Metric:** Sub-second global Largest Contentful Paint (LCP < 1.0s), zero layout shift (CLS = 0.0), instant product variant switching, and sub-100ms checkout initiation. Every 100ms of latency reduction directly correlates with 1% to 2% higher conversion rates.
* **Traffic Pattern:** Global consumer traffic with sudden massive promotional surges (Black Friday, flash sales, influencer campaigns).
* **Network & Device Spectrum:** 70% to 80% mobile shoppers navigating on erratic cellular connections and mid-tier smartphones.

---

## 2. The Recommended Architectural Stack

| Layer | Recommended Choice | Rationale |
| :--- | :--- | :--- |
| **Execution Boundary** | **Edge-Rendered SSR with Selective ISR (Remix / Next.js / Hydrogen)** | Pre-renders product pages and collections at CDN edge nodes adjacent to the consumer. Delivers pre-warmed HTML in a single network round trip. |
| **Dynamic Cart State** | **Optimistic Local Cache + Server Action Reconciliation** | Adding an item to the shopping bag updates the local UI immediately (within 16ms), updating the cart drawer without waiting for network confirmation. Background sync validates inventory. |
| **Styling & Assets** | **Tailwind CSS + AVIF / WebP Image Optimization** | Critical CSS is inlined into the document head to avoid render-blocking requests. Product imagery is automatically resized and delivered in modern AVIF formats with explicit `aspect-ratio` to eliminate Cumulative Layout Shift (CLS). |
| **Edge Cache Strategy** | **Stale-While-Revalidate with Tagged Cache Invalidation** | Product pages are served instantly from the edge cache. When inventory or pricing changes in the backend PIM/ERP, targeted cache tags (`surrogate-key` / `cache-tags`) purge only the modified SKU globally in milliseconds. |
| **Third-Party Script Isolation**| **Partytown / Web Worker Offloading** | Marketing tags, analytics trackers, and advertising pixels (Facebook Pixel, Google Tag Manager) are offloaded to run inside a Web Worker, freeing the browser main thread for seamless user interactions. |

---

## 3. What to Explicitly Avoid

* **Do NOT use a purely client-rendered Single Page Application (SPA):**
  A blank screen while downloading a 400 KB bundle directly loses shoppers. E-commerce requires immediate, rendered visual content on the first incoming packet.
* **Do NOT let third-party marketing tags execute directly on the main thread:**
  Analytics trackers and chat widgets are notorious for blocking the JavaScript event loop, driving Interaction to Next Paint (INP) into the red zone and causing cart clicks to fail.
* **Do NOT omit explicit image bounding boxes:**
  Allowing product images to load without predefined dimensions pushes description text and "Add to Cart" buttons downward, failing CLS audits and causing accidental taps.

---

## 4. Constraint Checklist
* Are product prices personalized per user or currency? Use edge geolocation headers to localize prices at the edge before serving the HTML.
* Is inventory volatile during flash sales? Render the product description and media from static edge cache, and stream the live inventory counter asynchronously via a lightweight micro-fetch.
