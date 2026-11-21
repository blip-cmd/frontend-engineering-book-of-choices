# Frontend Engineering as a Book of Choices: Complete Volume

> A practical architectural reference and constraint-driven decision engine for modern web applications.

---

## Table of Contents

### Part I: Foundations & The Core Dilemma
* [Chapter 0: The Calculus of Choices](00_the_calculus_of_choices.md)
  The philosophy of constraint-based architecture, the Iron Triangle of Frontend (User vs. Developer vs. Business), and the seven-point evaluation criteria.

### Part II: The Core Architectural Axes
* [Chapter 1: Where Code Runs: The Execution Boundary](01_where_code_runs.md)
  Client-Side Rendering (CSR), Server-Side Rendering (SSR), Static Generation (SSG/ISR), Islands Architecture, and React Server Components (RSC).
* [Chapter 2: The Reactivity Dilemma: Virtual DOM vs. Signals vs. Compilers](02_the_reactivity_dilemma.md)
  How changes in memory map to DOM pixels. Re-rendering heuristic diffs (React) vs. reactive dependency graphs (Solid/Preact) vs. compile-time AST transformations (Svelte).
* [Chapter 3: State and Cache Topologies: Client State Stores vs. Remote Server Caches](03_state_and_cache_topologies.md)
  The fundamental bifurcation of state: Ephemeral UI state vs. asynchronous remote server cache. Why a dedicated server cache removes the need for most global stores.
* [Chapter 4: The Networking Contract: REST vs. GraphQL vs. tRPC vs. Server Actions](04_the_networking_contract.md)
  Transport efficiency vs. schema governance. OpenAPI code generation, GraphQL fragments, tRPC end-to-end inference, and runtime Zod validation.
* [Chapter 5: Design Engineering & UI Architecture: Tokens, Primitives, and Performance](05_design_engineering_and_ui.md)
  The three-tier design system architecture: Design Tokens, Headless Primitives (Radix / Ark), and Composed Recipes (shadcn/ui / Tailwind). Accessibility contracts and perceived performance.
* [Chapter 6: Styling and Presentation: The CSS Architecture Dilemma](06_styling_and_presentation.md)
  Utility-First CSS (Tailwind) vs. CSS Modules vs. Zero-Runtime compilation (StyleX / Panda) vs. the decline of runtime CSS-in-JS.
* [Chapter 7: Delivery & Build Pipeline: Bundlers, Streaming, and Core Web Vitals](07_delivery_and_build_pipeline.md)
  Build tools (Vite, Turbopack, Rspack, Bun), the 14 KB TCP initial congestion window budget, route chunking, and Core Web Vitals (LCP, INP, CLS) optimization.
* [Chapter 8: Local-First and Offline Resilience: CRDTs and Client Databases](08_local_first_and_offline_resilience.md)
  Inverting data ownership. Embedded SQLite in Wasm over OPFS, Conflict-Free Replicated Data Types (Yjs / Automerge), and zero-latency offline writes.

### Part III: Archetype Decision Playbooks
Ready-to-implement architecture blueprints tailored to specific product profiles:
* [Content-First Publishing & Documentation](09_decision_playbooks/content_first_publishing.md)
* [Enterprise B2B SaaS & Data Grids](09_decision_playbooks/enterprise_b2b_saas.md)
* [High-Frequency Real-Time Telemetry & Financial Dashboards](09_decision_playbooks/high_frequency_realtime_dashboard.md)
* [Collaborative Canvas & Document Workspaces](09_decision_playbooks/collaborative_canvas_workspace.md)
* [Low-Latency Global E-Commerce Storefronts](09_decision_playbooks/low_latency_ecommerce.md)

### Part IV: Technical Appendices & Production Guides
* [Appendix A: The 15 Deadly Frontend Architectural Anti-Patterns](10_appendices/architecture_anti_patterns.md)
* [Appendix B: Core Web Vitals Production Triage Guide](10_appendices/core_web_vitals_triage_guide.md)
* [Appendix C: Production Frontend Security Hardening Checklist](10_appendices/frontend_security_checklist.md)
* [Appendix D: Zero-Downtime Migration Playbooks](10_appendices/migration_playbooks.md)

---

## Interactive Decision Tooling & Starter Recipes
* **Interactive Evaluation CLI:** Run `python pipelines/cli/choice_engine.py` to evaluate your constraints interactively.
* **Production Starter Configurations:** Ready-made starter templates under [recipes/](../recipes/).
* **Interactive Calculator:** Try the [web calculator](https://blip-cmd.github.io/frontend-engineering-book-of-choices/calculator/) to map your constraints to a recommended stack.
* **Further Reading:** Books that shaped this volume are listed in the [reading list](../library/reading_list.md).
