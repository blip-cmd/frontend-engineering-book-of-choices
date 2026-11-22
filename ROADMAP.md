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

## Phase 2: Quality Pass on Every Page (Done 2026-11-22; human review welcome)

All 20 pages are **agent-verified**: an author pass checked every claim against primary sources, and an independent verifier pass re-checked it (roughly 900 claims in total). Each page links its claim ledger; the index is [reviews/README.md](reviews/README.md). The first draft's most common faults were unsourced percentages and multipliers, outdated versions, misattributed references, and claims that official docs contradict. All are fixed or removed.

Next for content quality:

* [ ] Human expert review of any page (status `reviewed`, then `gold`): see the [expert review issue](https://github.com/blip-cmd/frontend-engineering-book-of-choices/issues/3)
* [ ] Verified entries for the known omissions listed in each ledger's section 3
* [ ] Re-verification as `review_by` dates arrive (automated weekly)

### Content-standards tooling

* [x] Page status front matter, shown on the website
* [x] Audit: front matter, `UNVERIFIED` markers, stale facts, unsourced numbers (warning on drafts, error on reviewed pages)
* [x] External link checker, library version watch and overdue-review check (weekly freshness report)
* [x] Weekly automated agent verification with an independent verifier pass
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

## Phase 4: Calculator, CLI and Recipes (In progress)

* [x] Calculator explanations aligned with the verified chapters (2026-11-22)
* [ ] One shared rules file used by both the web calculator and the CLI, so they never disagree
* [ ] More questions: team size and experience, hosting budget, device and network spectrum
* [ ] Export an Architectural Decision Record from the browser
* [ ] Tests for the calculator's recommendations
* [x] Recipes rebuilt as buildable starters on current versions, built in CI on every pull request, and watched by the weekly freshness report (2026-11-22)
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
