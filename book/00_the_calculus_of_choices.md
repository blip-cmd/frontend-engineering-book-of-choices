---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: Fowler "Who Needs an Architect?" (IEEE Software 2003, PDF), Astro Islands docs, Figma blog (2017-06-08, 2025-09-18), Ink & Switch local-first essay (2019), web.dev Web Vitals, TTFB and Rendering on the Web, Google Search Central JavaScript SEO basics, MDN How browsers work, RFC 6928, Russell Performance Inequality Gap 2026, Jackson Micro Frontends (2019), McKinley Choose Boring Technology (2015), Amazon 2015 shareholder letter (SEC), Nygard ADRs (2011), MADR
review_by: 2027-11
reviewers:
ledger: reviews/the-calculus-of-choices.md
---

# Chapter 0: The Calculus of Choices

> "[A]rchitecture is the decisions that you wish you could get right early in a project, but that you are not necessarily more likely to get them right than any other."
> Ralph Johnson, quoted by Martin Fowler in ["Who Needs an Architect?"](https://martinfowler.com/ieeeSoftware/whoNeedsArchitect.pdf), *IEEE Software*, July/August 2003

This chapter is for a developer or tech lead about to choose a frontend architecture. It sets out the book's method, which is its own reasoning rather than an industry standard: name the constraints first, then pick the options that fit them.

---

## 1. Why No Stack Is Best for Every Product

Framework debates often ask which stack is best. The book's position is that the question has no single answer, because each stack is tuned for a different set of constraints, and a choice that fits one product can hurt another.

Two products show the gap. A storefront that needs fast first page loads fits static or server-rendered HTML with small interactive regions; Astro's islands model renders most of the page as static HTML and adds JavaScript only to the components that need it ([Astro docs: Islands](https://docs.astro.build/en/concepts/islands/)). A collaborative design canvas has the opposite needs: Figma's product is written in C++ and compiled to WebAssembly ([Figma, 2017](https://www.figma.com/blog/webassembly-cut-figmas-load-time-by-3x/)) and renders with WebGPU, falling back to WebGL when needed ([Figma, 2025](https://www.figma.com/blog/figma-rendering-powered-by-webgpu/)). Local-first software, which treats the copy of data on the user's device as the primary copy and for which the essay presents conflict-free replicated data types (CRDTs) as a potential foundational technology ([Kleppmann et al., Ink & Switch, 2019](https://www.inkandswitch.com/essay/local-first/)), suits multi-user editing; the book's judgment is that its sync machinery is more than a marketing site needs.

Fowler reads Johnson's definition as "things that people perceive as hard to change" ([Fowler, 2003](https://martinfowler.com/ieeeSoftware/whoNeedsArchitect.pdf)).

---

## 2. Who Pays for Each Choice: Users, Developers or the Business

The book models each architectural choice as a trade-off among three parties; this model is its own framing, not an established theory.

```text
                          The User
                     (Latency, Battery,
                      Accessibility, INP)
                            /\
                           /  \
                          /    \
                         /      \
                        /        \
                       /          \
                      /____________\
            The Developer             The Business
       (Velocity, Type Safety,    (Hosting Cost,
        Refactoring Ergonomics)     Time to Market, SEO)
```

The diagram is a triangle with the user at the top and the developer and the business at the base corners; each party's concerns are listed below.

1. **The user** wants a fast server response, little main-thread JavaScript, quick responses to input, accessible pages, and pages that work on unreliable mobile connections. Interaction to Next Paint (INP) is a Core Web Vital and is good at 200 milliseconds or less, measured at the 75th percentile of page loads ([web.dev: Web Vitals](https://web.dev/articles/vitals)). Time to First Byte (TTFB) is not a Core Web Vital; web.dev gives 0.8 seconds or less as a rough guide ([web.dev: TTFB](https://web.dev/articles/ttfb)).
2. **The developer** wants fast iteration, type safety from server to client, clear error handling and code that is easy to change.
3. **The business** wants a short time to market, predictable hosting bills, visibility in search results and a large pool of people it can hire.

**Where the costs move.** web.dev's rendering guide shows a choice made for one party landing on another: in client-side rendering "the amount of JavaScript required tends to grow as an application grows, which can impact a page's INP" (the user pays), while server-side rendering "can have significant compute overhead costs" (the business pays) ([web.dev: Rendering on the Web](https://web.dev/articles/rendering-on-the-web)).

---

## 3. Seven Constraints to Settle Before Choosing a Framework

The book recommends settling the following constraints before choosing a library or framework. The list and its order are the book's own checklist, not a standard or a weighted score.

| Constraint | Range to place your product on | What it decides |
| :--- | :--- | :--- |
| **1. SEO and discoverability** | Vital, optional or irrelevant | Whether a client-rendered single-page app is acceptable. Google renders JavaScript, but its docs still call server-side or pre-rendering "a great idea" because "not all bots can run JavaScript" ([Google Search Central](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)). |
| **2. Traffic and latency** | Public traffic with spikes, or a predictable intranet | How much can be cached at a CDN, and how much HTML the first round trip carries before the server waits for an acknowledgment ([MDN](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work); [RFC 6928](https://www.rfc-editor.org/rfc/rfc6928.html)). |
| **3. Hosting budget** | Static files on a CDN, or always-on servers | Whether rendering on every request is affordable, since server-side rendering "can have significant compute overhead costs" ([web.dev: Rendering on the Web](https://web.dev/articles/rendering-on-the-web)). |
| **4. State and mutation complexity** | Simple forms over a server API, or many users editing the same data at once | Whether a server cache is enough or local-first sync with CRDTs is worth its cost ([Ink & Switch, 2019](https://www.inkandswitch.com/essay/local-first/)). |
| **5. Devices and networks** | Fast desktops on broadband, or low-cost Android phones on slow mobile links | How much JavaScript the critical path can afford. Alex Russell's budget estimates, which are advocacy writing, aim to emulate a 75th-percentile user experience and describe the 75th-percentile device as "yesterday's mid-market Android" ([Russell, 2025](https://infrequently.org/2025/11/performance-inequality-gap-2026/)). |
| **6. Team size and hiring** | One developer, one product team, or many teams | Whether one application or several independently released micro-frontends fits. Their documented costs include payload size and "operational and governance complexity" ([Cam Jackson on martinfowler.com, 2019](https://martinfowler.com/articles/micro-frontends.html)). |
| **7. Lifespan** | A short campaign site, or a platform maintained for a decade | How much to rely on young abstractions rather than web standards. Dan McKinley argues that each company gets "about three innovation tokens" to spend on unfamiliar technology ([Choose Boring Technology, 2015](https://mcfunley.com/choose-boring-technology)). |

### When this checklist is the wrong tool

The checklist is for decisions that are hard to reverse. Jeff Bezos's 2015 shareholder letter separates "one-way doors" from reversible "two-way doors", and says the reversible kind "can and should be made quickly" ([Amazon 2015 letter, SEC filing](https://www.sec.gov/Archives/edgar/data/1018724/000119312516530910/d168744dex991.htm)). In the book's judgment, skip the checklist when:

* **the choice is cheap to undo**, such as swapping a library that sits behind a small interface;
* **the constraints are not known yet**, as in a prototype with no field data (Core Web Vitals are assessed at the 75th percentile of real page loads, [web.dev: Web Vitals](https://web.dev/articles/vitals)), so ship and measure first;
* **the current stack already meets the constraints**, since McKinley argues that familiar tools have failure modes that "are well understood" and every new one adds operations work ([Choose Boring Technology](https://mcfunley.com/choose-boring-technology)).

---

## 4. Which Chapter Settles Which Decision

Each chapter covers one decision:

* **Chapter 1, Where Code Runs:** which machine renders each page (client, server, build step, islands or server components).
* **Chapter 2, The Reactivity Dilemma:** how updates reach the DOM (virtual DOM, fine-grained signals or compile-time reactivity).
* **Chapter 3, State and Cache Topologies:** which tool owns each kind of state (server caches, client stores, atomic state or local-first sync).
* **Chapter 4, The Networking Contract:** REST, GraphQL, tRPC or server functions.
* **Chapter 5, Design Engineering and UI Architecture:** design tokens, headless primitives and who owns styling.
* **Chapter 6, Styling and Presentation:** whether styles are generated at build time or at runtime.
* **Chapter 7, Delivery and Build Pipeline:** bundlers, the first round trip, code splitting and Core Web Vitals.
* **Chapter 8, Local-First and Offline Resilience:** CRDTs, browser storage and when local-first is worth it.
* **Decision Playbooks:** worked architectures for five product types, from e-commerce to collaborative canvases.
* **Appendices:** anti-patterns, Core Web Vitals triage, a security checklist and migration playbooks.

Place your product on each row of the table in section 3, then read the chapters for the decisions those rows affect. Record each choice where the next person will find it. An Architecture Decision Record, as Michael Nygard proposed in 2011, is a short text file with a context, the decision, its status and its consequences, listing all of them and "not just the 'positive' ones" ([Nygard, 2011](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)). MADR is a Markdown template for the same record ([adr.github.io/madr](https://adr.github.io/madr/)).
