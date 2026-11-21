# Roadmap

> What is done, what is next, and where help is most welcome. Pick anything marked open and say so in an issue so work is not duplicated.

---

## Phase 1: Public Launch (Done)

* [x] Website on GitHub Pages (Astro Starlight): one page per chapter, search, sitemap, social previews, "Edit page" links
* [x] Architecture calculator rebuilt with reasoning, chapter links, and shareable URLs
* [x] Removed summaries of third-party books; added an original [further-reading list](library/reading_list.md)
* [x] Licenses: CC BY-NC-ND 4.0 for writing, AGPL-3.0 for code, MIT for starter recipes; Contributor License Agreement
* [x] Contribution guide, issue templates, and CI (tests, standards audit, site build)

---

## Phase 2: Quality Pass on Every Page (In progress, help wanted)

Every page is reviewed against [CONTENT_STANDARDS.md](CONTENT_STANDARDS.md): ten pass/fail gates (sourced numbers, working code, no invented packages or experience, a named human reviewer...) and ten scored dimensions. Each page's status lives in its front matter (`status: draft | reviewed | gold`) and is shown on the website. Run `npm run audit` to see the current count.

Review order (highest risk first, because readers copy examples and act on numbers):

1. [ ] Appendix C: Frontend Security Hardening Checklist
2. [ ] Appendix B: Core Web Vitals Triage Guide
3. [ ] Appendix D: Migration Playbooks
4. [ ] Chapter 3: State and Cache Topologies, and the essay "Why Server Caches Replace Most Redux Stores"
5. [ ] Essay: The 14 KB TCP Slow-Start Budget, and Chapter 7: Delivery and Build Pipeline
6. [ ] Decision playbooks (5)
7. [ ] Chapters 0, 1, 2, 4, 5, 6, 8 and Appendix A

Known issues across the draft: unsourced percentages and multipliers, no verification dates, and generic headings ("The Landscape of Choices") repeated across chapters.

### Content-standards tooling

* [x] Page status front matter, shown on the website
* [x] Audit: front matter, `UNVERIFIED` markers, stale facts, unsourced numbers (warning on drafts, error on reviewed pages)
* [ ] External link checker
* [ ] Code-block extraction and type-check
* [ ] `npm view` existence check for packages named in code

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
