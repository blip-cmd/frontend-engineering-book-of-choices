# Roadmap

> What is done, what is next, and where help is most welcome. Pick anything marked open and say so in an issue so work is not duplicated.

---

## Phase 1: Public Launch (Done)

* [x] Website on GitHub Pages (Astro Starlight): one page per chapter, search, sitemap, social previews, "Edit page" links
* [x] Architecture calculator rebuilt with reasoning, chapter links, and shareable URLs
* [x] Removed summaries of third-party books; added an original [further-reading list](library/reading_list.md)
* [x] Licenses: CC BY-NC-ND 4.0 for writing, MIT for code
* [x] Contribution guide, issue templates, and CI (tests, standards audit, site build)

---

## Phase 2: Quality Pass on Every Chapter (Open, help wanted)

The first draft was written with AI assistance. Each page needs a human review before it can be called reliable. For every chapter and appendix:

1. Link every factual claim to an official doc, specification, or primary source.
2. Check every library is current and not deprecated (one fix so far: Recoil, archived in early 2025, was removed from Chapter 3).
3. Replace or source unsupported numbers (bundle sizes, "80% to 90%" style claims, latency figures).
4. Add at least one small, runnable code example per major choice.
5. Add a "When this is the wrong choice" section if it is missing.

| Page | Reviewed | Sourced | Code examples |
| :--- | :---: | :---: | :---: |
| Chapter 0: The Calculus of Choices | [ ] | [ ] | n/a |
| Chapter 1: Where Code Runs | [ ] | [ ] | [ ] |
| Chapter 2: The Reactivity Dilemma | [ ] | [ ] | [ ] |
| Chapter 3: State and Cache Topologies | [ ] | [ ] | [ ] |
| Chapter 4: The Networking Contract | [ ] | [ ] | [ ] |
| Chapter 5: Design Engineering and UI | [ ] | [ ] | [ ] |
| Chapter 6: Styling and Presentation | [ ] | [ ] | [ ] |
| Chapter 7: Delivery and Build Pipeline | [ ] | [ ] | [ ] |
| Chapter 8: Local-First and Offline | [ ] | [ ] | [ ] |
| Playbooks (5) | [ ] | [ ] | [ ] |
| Appendices (4) | [ ] | [ ] | [ ] |
| Essays (2) | [ ] | [ ] | [ ] |

---

## Phase 3: New Chapters (Open)

Topics a complete frontend reference still lacks:

* [ ] Testing strategy: unit vs. component vs. end-to-end, and what each one catches
* [ ] Accessibility in depth: semantics, focus management, testing with assistive technology
* [ ] Forms and validation: controlled vs. uncontrolled, schema validation, server actions
* [ ] Routing and navigation: file-based vs. config routing, data loading, view transitions
* [ ] Internationalisation: message formats, right-to-left layouts, locale-aware routing
* [ ] Observability: error tracking, real-user monitoring, performance budgets in CI
* [ ] AI in the frontend: streaming responses, optimistic UI for slow models, safety of rendered output
* [ ] Authentication on the client: sessions vs. tokens, where to store what

---

## Phase 4: Calculator and CLI (Open)

* [ ] One shared rules file used by both the web calculator and the CLI, so they never disagree
* [ ] More questions: team size and experience, hosting budget, device and network spectrum
* [ ] Export an Architectural Decision Record from the browser
* [ ] Tests for the calculator's recommendations
* [ ] Publish the CLI to npm as `@blip-cmd/choices`

---

## Phase 5: Reach (Open)

* [ ] Submit the sitemap to Google Search Console and Bing Webmaster Tools
* [ ] A social preview image per chapter
* [ ] Free PDF and EPUB downloads attached to each GitHub release (the build pipeline already exists: `.github/workflows/compile_books.yml`)
* [ ] Share the essays on dev.to, Hashnode and relevant communities, linking back to the site

---

## Later Ideas

Companion volumes using the same "book of choices" format (UI/UX design, backend, DevOps, data engineering) once this volume is reviewed and stable.
