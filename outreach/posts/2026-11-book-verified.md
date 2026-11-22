# The whole book is verified (and one short post per page)

**Status:** not posted
**Base URL:** https://blip-cmd.github.io/frontend-engineering-book-of-choices/

Every fact below appears on the linked page with its primary source, and in that page's claim ledger in `reviews/`. Re-check the page before posting if it has changed since 2026-11-22. Post one at a time; a page a week is a good rhythm.

---

## Announcement (LinkedIn, then X)

All 20 pages of **Frontend Engineering as a Book of Choices** are now verified against primary sources.

The first draft was AI-assisted, so every page went through two separate checks. One agent rewrote it against official docs (MDN, web.dev, OWASP, react.dev, framework docs and RFCs), and a second agent, which had not written it, re-checked every claim and could fail the page. More than 900 claims were checked, and each page links a public ledger listing every source.

What the checks caught in the draft:
• invented statistics ("80% to 90% of apps…", "5x to 10x faster")
• references credited to the wrong people, and a blog post title that did not exist
• outdated advice: wrong INP thresholds, the archived Recoil library, Vue grouped with signal frameworks
• a security claim that a third-party script tool isolates trackers from your form fields (its own docs say otherwise)

Each page is labelled "AI-checked" and says it has not yet been reviewed by a human expert. Expert reviews are the next step, and very welcome.

https://blip-cmd.github.io/frontend-engineering-book-of-choices/

#frontend #webdev #opensource

---

## One post per page

Use as a LinkedIn post or an X post (each is under 280 characters without the link).

**Chapter 0, The Calculus of Choices** (`chapters/the-calculus-of-choices/`)
Before picking a framework, write down your constraints. Chapter 0 covers how to make that decision record, and when the checklist is the wrong tool (two-way-door decisions you can cheaply reverse).

**Chapter 1, Where Code Runs** (`chapters/where-code-runs/`)
Google can render JavaScript, but not every crawler can. Chapter 1 compares CSR, SSR, static, islands and Server Components, and when each is the wrong choice.

**Chapter 2, The Reactivity Dilemma** (`chapters/the-reactivity-dilemma/`)
Vue 3.5 still renders through a virtual DOM; Svelte 5's runes are signals under the hood. Chapter 2 sorts the reactivity models by what each framework's own docs say.

**Chapter 3, State and Cache Topologies** (`chapters/state-and-cache-topologies/`)
Do server caches roll back optimistic updates for you? SWR does by default; TanStack Query and RTK Query make you do it. Chapter 3 compares the state options source by source.

**Chapter 4, The Networking Contract** (`chapters/the-networking-contract/`)
React's Server Functions run one at a time per client, and react.dev does not recommend them for data fetching. Chapter 4 compares REST, GraphQL, tRPC and Server Functions.

**Chapter 5, Design Engineering and UI** (`chapters/design-engineering-and-ui/`)
Headless component libraries help with accessibility, but none guarantees it: you still label components and test with assistive technology. Chapter 5, with sources.

**Chapter 6, Styling and Presentation** (`chapters/styling-and-presentation/`)
styled-components is in maintenance mode, not deprecated, and has supported React Server Components since 6.3. Chapter 6 compares CSS approaches without the hype.

**Chapter 7, Delivery and Build Pipeline** (`chapters/delivery-and-build-pipeline/`)
Every bundler speed claim in Chapter 7 is quoted from its vendor and labelled as a vendor claim, next to the Core Web Vitals thresholds (75th percentile) that decide what users feel.

**Chapter 8, Local-First and Offline** (`chapters/local-first-and-offline-resilience/`)
CRDTs converge, but when two people edit the same field at once, only one value survives. Chapter 8 covers local-first storage, quotas and when local-first is the wrong choice.

**Playbook: Content-first publishing** (`playbooks/content-first-publishing/`)
A content site's targets: LCP 2.5 s, INP 200 ms, CLS 0.1 at the 75th percentile, from web.dev, not invented. The playbook builds on Astro 7 islands.

**Playbook: Enterprise B2B SaaS** (`playbooks/enterprise-b2b-saas/`)
TanStack Table has no built-in virtualization; you pair it with TanStack Virtual, and it does not replace server-side pagination. The B2B SaaS playbook, sourced.

**Playbook: Real-time dashboards** (`playbooks/high-frequency-realtime-dashboard/`)
uPlot draws with Canvas 2D, and its README suggests WebGL or WebGPU libraries beyond about 100k points in view. The real-time dashboard playbook.

**Playbook: Collaborative canvas** (`playbooks/collaborative-canvas-workspace/`)
PixiJS 8 marks its WebGPU renderer experimental and recommends WebGL for production. The collaborative canvas playbook covers Yjs, storage and when CRDTs are the wrong tool.

**Playbook: Low-latency e-commerce** (`playbooks/low-latency-ecommerce/`)
In Next.js 16, ISR runs on the Node.js runtime, not the Edge runtime. The e-commerce playbook covers caching, optimistic carts and personalised pages.

**Appendix A, Anti-patterns** (`appendices/architecture-anti-patterns/`)
Throttling scroll handlers with requestAnimationFrame? MDN calls it useless. 15 frontend anti-patterns, each with its fix and a primary source.

**Appendix B, Core Web Vitals triage** (`appendices/core-web-vitals-triage-guide/`)
A CLS score is the largest burst of layout shifts, not the page-lifetime total. A step-by-step Core Web Vitals triage guide.

**Appendix D, Migration playbooks** (`appendices/migration-playbooks/`)
Tailwind 4 needs Safari 16.4+, Chrome 111+ and Firefox 128+. Check your audience before you migrate. Migration playbooks for Vite 8, Rspack and Tailwind 4.

**Essay, The 14 KB Slow-Start Budget** (`essays/the-14kb-tcp-slow-start-budget/`)
The "14 KB rule" rests on RFC 6928, an Experimental RFC whose 10-segment window is optional. The essay works through the arithmetic, the caveats, and QUIC.

**Essay, Server Caches vs Redux** (`essays/why-server-caches-replace-most-redux-stores/`)
TanStack Query's own docs name the apps that still want a client state manager. The essay on when a server cache replaces your Redux store, and when it does not.
