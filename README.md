# Frontend Engineering as a Book of Choices

> There is no best framework, only trade-offs. A free, open reference that maps your real constraints to the frontend architecture that fits, and shows what each choice costs.

**Read it online:** [blip-cmd.github.io/frontend-engineering-book-of-choices](https://blip-cmd.github.io/frontend-engineering-book-of-choices/) · **Try the calculator:** [Architecture Calculator](https://blip-cmd.github.io/frontend-engineering-book-of-choices/calculator/)

---

## What This Is

Most frontend guides tell you which tool to use. This book asks what you are building, for whom, and under which limits (search visibility, team size, latency, data ownership, budget, devices) and then walks through the options that fit and the price of each one.

It covers:

* **Where code runs:** CSR, SSR, static generation, islands and server components ([Chapter 1](book/01_where_code_runs.md))
* **Reactivity:** Virtual DOM vs. signals vs. compilers ([Chapter 2](book/02_the_reactivity_dilemma.md))
* **State:** server caches vs. client stores vs. local-first ([Chapter 3](book/03_state_and_cache_topologies.md))
* **API contracts:** REST, GraphQL, tRPC and server actions ([Chapter 4](book/04_the_networking_contract.md))
* **Design engineering and styling:** tokens, headless primitives, CSS architectures ([Chapters 5](book/05_design_engineering_and_ui.md) and [6](book/06_styling_and_presentation.md))
* **Delivery:** bundlers, Core Web Vitals and the first-14 KB budget ([Chapter 7](book/07_delivery_and_build_pipeline.md))
* **Offline and local-first:** client databases and CRDTs ([Chapter 8](book/08_local_first_and_offline_resilience.md))
* **Five decision playbooks** for common product types, and **four appendices** (anti-patterns, Core Web Vitals triage, security checklist, migrations)

The full table of contents is in [book/README.md](book/README.md).

---

## Project Status: Help Wanted

This is a living, community-reviewed book. The first draft was written with the help of AI tools. It is now being reviewed, sourced, and extended chapter by chapter, in the open. Expect rough edges, and please point them out.

The most useful contributions right now:

* **Corrections:** outdated libraries, wrong numbers, missing caveats. [Open an issue](https://github.com/blip-cmd/frontend-engineering-book-of-choices/issues/new/choose).
* **Real-world experience:** "we chose X and this is what it cost us."
* **Sources:** links to official docs, specs and benchmarks for claims that lack them.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to help and [ROADMAP.md](ROADMAP.md) for what is planned.

---

## Tools

### Architecture Calculator (web)

Answer six questions about your project and get a recommended starting architecture, with the reasoning and a link to the relevant chapter. Answers are saved in the URL so you can share a result with your team. [Open the calculator](https://blip-cmd.github.io/frontend-engineering-book-of-choices/calculator/).

### Decision CLI and Starter Recipes

```bash
git clone https://github.com/blip-cmd/frontend-engineering-book-of-choices.git
cd frontend-engineering-book-of-choices

node bin/choices.js list                         # list the five archetypes
node bin/choices.js init enterprise_b2b_saas --target ./my-app   # copy a starter recipe
node bin/choices.js export --format=markdown     # write an Architectural Decision Record
```

The starter configurations live in [recipes/](recipes/).

---

## Repository Structure

```text
├── book/          # The book: chapters 0-8, decision playbooks, appendices (the single source of truth)
├── docs/essays/   # Standalone essays drawn from the chapters
├── library/       # Research notes behind the chapters, plus a further-reading list
├── site/          # The website (Astro Starlight), generated from book/ and deployed to GitHub Pages
├── recipes/       # Starter configurations for each playbook
├── bin/           # Node.js decision CLI
├── pipelines/     # Python CLI, PDF (Typst) and EPUB builders, quality audit, schemas
├── tests/         # Node and Python test suites
└── skills/        # Prompts used to research and draft chapters (kept for transparency)
```

### Running Locally

```bash
# Website: http://localhost:4321/frontend-engineering-book-of-choices/
cd site && npm install && npm run dev

# Tests and standards audit (from the repository root)
npm test
python -m unittest discover -s tests -p "test_*.py"
npm run audit
```

---

## License

* **Writing** (everything in `book/`, `docs/`, `library/`, and the website's page text) is licensed under [Creative Commons BY-NC-ND 4.0](LICENSE-CONTENT.md). You may read it, share it, and quote it with credit. You may not sell it or publish modified versions. To improve it, contribute here.
* **Code** (the calculator, CLI, recipes, scripts, and site code) is licensed under the [MIT License](LICENSE), so you can use the recipes and tools in your own projects.

Copyright (c) 2026 blip-cmd and contributors.
