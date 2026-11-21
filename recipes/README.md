# Architecture Recipes and Starter Configurations

> Production-grade configurations directly instantiating the archetypes and playbooks from Frontend Engineering as a Book of Choices.

---

## Catalog of Starter Recipes

| Recipe Directory | Target Archetype | Core Stack | Relevant Book Chapters |
| :--- | :--- | :--- | :--- |
| [content_first_astro/](content_first_astro/) | Content Publishing and Documentation | Astro + Preact Islands + Tailwind CSS | [Chapter 1](../book/01_where_code_runs.md), [Playbook 1](../book/09_decision_playbooks/content_first_publishing.md) |
| [enterprise_b2b_saas/](enterprise_b2b_saas/) | B2B SaaS, Admin Portals, Data Grids | Vite + React + TanStack Query/Table/Virtual + Radix UI + Zod | [Chapter 3](../book/03_state_and_cache_topologies.md), [Playbook 2](../book/09_decision_playbooks/enterprise_b2b_saas.md) |
| [realtime_dashboard/](realtime_dashboard/) | Real-Time Telemetry and Financial Consoles | Vite + Solid.js Signals + uPlot + Web Worker Offload | [Chapter 2](../book/02_the_reactivity_dilemma.md), [Playbook 3](../book/09_decision_playbooks/high_frequency_realtime_dashboard.md) |
| [collaborative_canvas/](collaborative_canvas/) | Collaborative Canvas and Document Workspaces | Vite + React + Yjs (CRDT) + OPFS / IndexedDB | [Chapter 8](../book/08_local_first_and_offline_resilience.md), [Playbook 4](../book/09_decision_playbooks/collaborative_canvas_workspace.md) |
| [low_latency_ecommerce/](low_latency_ecommerce/) | Low-Latency Global E-Commerce Storefronts | Next.js 15 Streaming SSR + Edge Headers + Tailwind CSS | [Chapter 1](../book/01_where_code_runs.md), [Playbook 5](../book/09_decision_playbooks/low_latency_ecommerce.md) |
| [shared_configs/](shared_configs/) | Base Monorepo Configurations | Shared TypeScript `tsconfig.base.json`, Design Tokens Tailwind Config | [Chapter 5](../book/05_design_engineering_and_ui.md), [Chapter 6](../book/06_styling_and_presentation.md) |

---

## How to Use These Recipes

1. Identify your constraint profile using the interactive CLI: `node bin/choices.js` or `python pipelines/cli/choice_engine.py`.
2. Scaffold a recipe directly into your project:
   ```bash
   node bin/choices.js init enterprise_b2b_saas --target ./my-app
   ```
   Or using Python:
   ```bash
   python pipelines/cli/choice_engine.py --init enterprise_b2b_saas --target ./my-app
   ```
3. Export an Architectural Decision Record (ADR) documenting your decision:
   ```bash
   node bin/choices.js export --format=markdown --output ./docs/adr/0001-frontend-architecture.md
   ```
