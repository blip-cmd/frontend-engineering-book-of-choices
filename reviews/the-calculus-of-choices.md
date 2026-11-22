---
page: book/00_the_calculus_of_choices.md
verified: 2026-11-22
---

# Claim Ledger: Chapter 0, The Calculus of Choices

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a developer or tech lead about to choose a frontend architecture for a product. The page helps them decide which constraints to settle before choosing rendering, state, networking and styling options, and which chapter of the book covers each decision. Thesis (kept from the draft): no stack is best for every product; the right architecture follows from stated constraints, and each choice moves cost between the user, the developer and the business. The author pass kept this thesis and the seven-constraint table, labelled the three-party model, the checklist and its ordering as the book's own scheme (not data), and added a sourced "When this checklist is the wrong tool" subsection and a closing pointer to Architecture Decision Records. One recommendation changed because a primary source contradicts it: the draft said SEO makes SSR or islands "mandatory"; Google Search Central says Google renders JavaScript and calls server-side or pre-rendering "a great idea", so the row now says SEO decides whether a client-rendered app is acceptable.

**History.** The AI-generated draft misquoted Ralph Johnson (it ended the quote with "but that are not necessarily easy to change later"; Johnson's words, as printed in Fowler's 2003 column, end "but that you are not necessarily more likely to get them right than any other"). It also asked for "near-zero" TTFB as a user demand without a source (web.dev says TTFB is not a Core Web Vital and gives 0.8 seconds as a rough guide), gave an unsourced "sub-14KB HTML" figure, team sizes of 5 and 200 engineers, "6-month" and "10-year" horizons and "budget Android on 3G" as unsourced specifics, called its own three-party model "the Iron Triangle" (a project-management term for scope, time and cost), said developer ergonomics "frequently" shifts cost to users with no source, and promised "decision trees" in every chapter (only some chapters have one). The code fence for the diagram had no language tag.

---

## 1. Author pass (2026-11-22)

Sources were fetched in this session with `curl` (HTML converted to text; Fowler's column as PDF converted with `pdftotext`) and quotes were matched against the fetched text. Chapter, playbook and appendix names were checked against the files in `book/`. The page has no runnable code; its one code block is an ASCII diagram tagged `text` and described in prose.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | Johnson: "architecture is the decisions that you wish you could get right early in a project, but that you are not necessarily more likely to get them right than any other" | [Fowler, "Who Needs an Architect?", IEEE Software, July/August 2003](https://martinfowler.com/ieeeSoftware/whoNeedsArchitect.pdf) | verified (quote); draft misquote corrected |
| 2 | Fowler: architecture as "things that people perceive as hard to change" | same | verified (quote) |
| 3 | Astro islands render most of the page as static HTML and add JavaScript only where interactivity is needed | [Astro docs: Islands](https://docs.astro.build/en/concepts/islands/) | verified |
| 4 | Figma's product is written in C++ and compiled to WebAssembly | [Figma blog, Evan Wallace, 2017-06-08](https://www.figma.com/blog/webassembly-cut-figmas-load-time-by-3x/) | verified (quote: "our product is written in C++") |
| 5 | Figma renders with WebGPU and falls back to WebGL as needed | [Figma blog, 2025-09-18](https://www.figma.com/blog/figma-rendering-powered-by-webgpu/) | verified (quote) |
| 6 | Local-first treats the device's copy as the primary copy and uses CRDTs; authors Kleppmann, Wiggins, van Hardenberg, McGranaghan, April 2019 | [Ink & Switch: Local-first software](https://www.inkandswitch.com/essay/local-first/) | verified (quote) |
| 7 | Local-first sync is more than a marketing site needs | none | labelled as the book's judgment |
| 8 | INP is a Core Web Vital, good at 200 ms or less, measured at the 75th percentile of page loads | [web.dev: Web Vitals](https://web.dev/articles/vitals) | verified (quote) |
| 9 | TTFB is not a Core Web Vital; 0.8 seconds or less as a rough guide | [web.dev: TTFB](https://web.dev/articles/ttfb) | verified (quote); replaces "near-zero TTFB" |
| 10 | Client-side rendering: "the amount of JavaScript required tends to grow as an application grows, which can impact a page's INP" | [web.dev: Rendering on the Web](https://web.dev/articles/rendering-on-the-web) (updated 2026-01-05) | verified (quote) |
| 11 | Server-side rendering "can have significant compute overhead costs" | same | verified (quote) |
| 12 | Google renders JavaScript; server-side or pre-rendering is "a great idea" because "not all bots can run JavaScript" | [Google Search Central: JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) | verified (quote); draft's "SSR/Islands are mandatory" corrected |
| 13 | The server sends a number of segments before waiting for an ACK; TCP's initial window sets the first flight (RFC 6928 raises it to 10 segments, Experimental) | [MDN: How browsers work](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work); [RFC 6928](https://www.rfc-editor.org/rfc/rfc6928.html) | verified (quote); "14KB" figure removed from this page |
| 14 | Russell's budgets emulate a 75th-percentile experience; the P75 device is "yesterday's mid-market Android" | [Russell, The Performance Inequality Gap, 2026 (posted 2025-11-24)](https://infrequently.org/2025/11/performance-inequality-gap-2026/) | verified (quote); labelled as advocacy |
| 15 | Micro-frontends are deployed independently; downsides include payload size and "operational and governance complexity" | [Cam Jackson, Micro Frontends, martinfowler.com, 2019-06-19](https://martinfowler.com/articles/micro-frontends.html) | verified (section headings) |
| 16 | "about three innovation tokens"; essay dated 2015 | [McKinley, Choose Boring Technology, 2015-03-30](https://mcfunley.com/choose-boring-technology) | verified (quote) |
| 17 | Boring technology's failure modes "are well understood"; each technology adds operations work | same | verified (quote: "their failure modes are well understood"; "We call the baggage 'operations'") |
| 18 | Bezos: "one-way doors" vs "two-way doors"; Type 2 decisions "can and should be made quickly" | [Amazon 2015 shareholder letter, SEC exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1018724/000119312516530910/d168744dex991.htm) | verified (quote) |
| 19 | When to skip the checklist (cheap-to-undo choices, unknown constraints, a stack that already fits) | Bezos letter; web.dev Web Vitals; McKinley | applications labelled as the book's judgment |
| 20 | ADRs (Nygard, 2011-11-15): a short text file with context, decision, status and consequences, "not just the 'positive' ones" | [Nygard, Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | verified (quote) |
| 21 | MADR is a Markdown template for decision records | [adr.github.io/madr](https://adr.github.io/madr/) | verified |
| 22 | Three-party model, seven-constraint checklist and its order | none | labelled as the book's own scheme, not data |
| 23 | Chapter 1 to 8 titles and topics; five decision playbooks; four appendices | files in `book/` (2026-11-22) | verified against repo; chapters 1 and 2 were being edited by other passes at the time |
| 24 | "Iron Triangle", "sub-14KB HTML", "5-person squad", "200-engineer org", "6-month", "10-year", "3G", "memory allocation", "serverless bill shocks", "frequently shifts the cost", "decision trees" in every chapter | none found | removed or made qualitative |

## 2. Independent verifier pass (2026-11-22)

All 17 cited sources were fetched fresh with `curl -sL` (HTML converted to text; Fowler's PDF with `pdftotext`) and every claim was re-extracted from the page and matched against the fetched text. 32 claims checked: 29 SUPPORTED, 2 PARTIAL (corrected), 1 sentence deleted as adding no checkable claim, 0 UNSUPPORTED. The page has no runnable code and names no npm packages; its one code block is a `text` diagram described in prose.

| # | Claim | Verdict | Note |
| :--- | :--- | :--- | :--- |
| 1 | Johnson quote, "[A]rchitecture is the decisions that you wish you could get right early in a project, but that you are not necessarily more likely to get them right than any other." | SUPPORTED | Verbatim in the PDF, inside the passage introduced by "Johnson responded:"; column printed "July/August 2003 IEEE SOFTWARE" |
| 2 | Fowler: "things that people perceive as hard to change", derived from "Johnson's secondary definition" | SUPPORTED | Verbatim, section "Getting rid of software architecture" |
| 3 | Astro islands: most of the page static HTML, JavaScript only for components that need it | SUPPORTED | "JavaScript is only loaded for the individual components that need it" |
| 4 | Figma's product written in C++ and compiled to WebAssembly (2017) | SUPPORTED | Evan Wallace, June 8, 2017 |
| 5 | Figma renders with WebGPU, falling back to WebGL when needed (2025) | SUPPORTED | September 18, 2025: "fall back to WebGL-based rendering later as needed" |
| 6 | Local-first "keeps the primary copy of data on the user's device and merges edits with CRDTs" | PARTIAL | Essay says "we treat the copy of the data on your local device ... as the primary copy" and that CRDTs "have the potential to be a foundational technology"; it does not define local-first as using CRDTs, and verified Chapter 3 (CRDT updates or queued mutations) and Chapter 8 ("a merge model such as a CRDT") agree. Reworded |
| 7 | Local-first sync is more than a marketing site needs | SUPPORTED as labelled judgment | |
| 8 | Three-party model, seven-constraint checklist and order are the book's own | SUPPORTED as labelled scheme | Labels present in sections 2 and 3 |
| 9 | INP is a Core Web Vital, good at 200 ms or less, at the 75th percentile of page loads | SUPPORTED | web.dev Web Vitals; matches verified Chapter 7 |
| 10 | TTFB not a Core Web Vital; 0.8 seconds or less as a rough guide | SUPPORTED | "TTFB isn't a Core Web Vitals metric"; "As a rough guide, most sites should strive to have a TTFB of 0.8 seconds or less" |
| 11 | CSR: "the amount of JavaScript required tends to grow as an application grows, which can impact a page's INP" | SUPPORTED | Verbatim |
| 12 | SSR "can have significant compute overhead costs" (used twice) | SUPPORTED | Verbatim |
| 13 | Google renders JavaScript; server-side or pre-rendering "a great idea" because "not all bots can run JavaScript" | SUPPORTED | Verbatim ("is still a great idea"); matches verified Chapter 1 |
| 14 | First round trip: the server sends a number of segments before waiting for an acknowledgment | SUPPORTED | MDN: "the server decides what number of segments to send before waiting for an ACK"; RFC 6928 (Experimental) raises the initial window to 10 segments; consistent with verified Chapter 7 |
| 15 | Russell's budgets "aim at the 75th-percentile device and network" | PARTIAL | Source: "The goal of these recommendations is to emulate a 75th percentile user experience"; "today's P75 device is yesterday's mid-market Android". Reworded; advocacy label kept |
| 16 | Micro-frontends released independently; costs include payload size and "operational and governance complexity" | SUPPORTED | Section headings "Independent deployment", "Payload size", "Operational and governance complexity"; Cam Jackson, 19 June 2019 |
| 17 | McKinley: "about three innovation tokens" (2015) | SUPPORTED | "every company gets about three innovation tokens"; March 30th, 2015 |
| 18 | McKinley: failure modes "are well understood"; each new tool adds operations work | SUPPORTED | "their failure modes are well understood"; "We call the baggage 'operations'" |
| 19 | Bezos 2015 letter: "one-way doors" vs reversible "two-way doors"; the reversible kind "can and should be made quickly" | SUPPORTED | SEC exhibit 99.1: "Type 2 decisions can and should be made quickly" |
| 20 | Core Web Vitals assessed at the 75th percentile of real page loads | SUPPORTED | "75th percentile of page loads"; Core Web Vitals are "measurable in the field" |
| 21 | When to skip the checklist (three bullets) | SUPPORTED as labelled judgment | |
| 22 | Nygard 2011: ADR is a short text file with context, decision, status, consequences, "not just the 'positive' ones" | SUPPORTED | November 15, 2011; "An architecture decision record is a short text file" |
| 23 | MADR is a Markdown template for the same record | SUPPORTED | "MADR is a streamlined template for recording architectural significant decisions" |
| 24 to 32 | Chapter 1 to 8 topics, five playbooks, four appendices (section 4) | SUPPORTED | Checked against headings of the files in `book/`; no contradiction with agent-verified Chapters 1 to 7, the playbooks or the appendices. Storefront sentence in section 1 ("static or server-rendered HTML") is consistent with the verified e-commerce playbook (server-rendered HTML cached at a CDN) |

**Edits made to the page.**

1. Section 1, local-first sentence: "keeps the primary copy of data on the user's device and merges edits with conflict-free replicated data types (CRDTs)" became "treats the copy of data on the user's device as the primary copy and for which the essay presents conflict-free replicated data types (CRDTs) as a potential foundational technology".
2. Section 3, row 5: "aim at the 75th-percentile device and network and describe that device as" became "aim to emulate a 75th-percentile user experience and describe the 75th-percentile device as".
3. Section 1: deleted "The skill this book tries to build is judging those decisions against stated constraints." (no checkable claim).
4. Front matter set to `agent-verified` after the audit passed.

**Verdict: PASS.** No UNSUPPORTED claims remain, both PARTIAL claims were corrected, every number on the page (200 ms, 75th percentile, 0.8 seconds, three tokens, dates) links to its source.

## 3. Known omissions (follow-up content, not errors)

* Security, privacy and regulatory requirements (data residency, accessibility law) are not among the seven constraints.
* Accessibility is named as a user concern without a WCAG reference or target.
* No guidance on how to measure each constraint (for example field data from CrUX, hosting cost estimates).
* Reversibility techniques (strangler-fig migrations, adapters) that make a one-way decision cheaper; Appendix D covers migrations.
* Organisation shape and Conway's law as a driver of micro-frontends.
* A worked ADR example for a frontend decision.
* Internationalisation and content-editing workflows as constraints.

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 1 | 2 | 2 | 1 | 2 | 1 | 1 | 2 | **16** |

D3 is 1 because the introduction names mechanisms (hydration cost, the TCP first flight) without explaining them; the chapters do. D6 is 1 because the chapter pins no framework versions, which suits an introduction but leaves the dimension partly unmet. D8 is 1 because section 4 points back to the section 3 table. D9 is 1: Astro and Figma are real examples but brief. The page is about twice the draft's length because of the sourcing and the added "when not to" subsection; the verifier may want it trimmed further.
