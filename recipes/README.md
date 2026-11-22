# Architecture Recipes and Starter Configurations

> Small, buildable starter projects that implement the book's decision playbooks. Each one installs from its lockfile and builds in CI on every pull request, so it cannot silently fall behind. Licensed MIT: copy them freely.

---

## Catalog of Starter Recipes

| Recipe Directory | Target Archetype | Core Stack | Relevant Book Chapters |
| :--- | :--- | :--- | :--- |
| [content_first_astro/](content_first_astro/) | Content Publishing and Documentation | Astro 7 + Preact 11 islands + Tailwind 4 | [Chapter 1](../book/01_where_code_runs.md), [Playbook 1](../book/09_decision_playbooks/content_first_publishing.md) |
| [enterprise_b2b_saas/](enterprise_b2b_saas/) | B2B SaaS, Admin Portals, Data Grids | Vite 8 + React 19 + TanStack Query 5 / Table 9 + Zod 4 + Tailwind 4 | [Chapter 3](../book/03_state_and_cache_topologies.md), [Playbook 2](../book/09_decision_playbooks/enterprise_b2b_saas.md) |
| [realtime_dashboard/](realtime_dashboard/) | Real-Time Telemetry and Financial Consoles | Vite 8 + Solid 2 signals + uPlot + Web Worker | [Chapter 2](../book/02_the_reactivity_dilemma.md), [Playbook 3](../book/09_decision_playbooks/high_frequency_realtime_dashboard.md) |
| [collaborative_canvas/](collaborative_canvas/) | Collaborative Canvas and Document Workspaces | Vite 8 + React 19 + Yjs 13 (CRDT) + IndexedDB, optional y-websocket sync | [Chapter 8](../book/08_local_first_and_offline_resilience.md), [Playbook 4](../book/09_decision_playbooks/collaborative_canvas_workspace.md) |
| [low_latency_ecommerce/](low_latency_ecommerce/) | Low-Latency Global E-Commerce Storefronts | Next.js 16 on Node.js + ISR revalidation + useOptimistic cart + Tailwind 4 | [Chapter 1](../book/01_where_code_runs.md), [Playbook 5](../book/09_decision_playbooks/low_latency_ecommerce.md) |
| [shared_configs/](shared_configs/) | Base Monorepo Configurations | Shared `tsconfig.base.json`, Tailwind 4 design tokens (`tokens.css`, DTCG `tokens.json`) | [Chapter 5](../book/05_design_engineering_and_ui.md), [Chapter 6](../book/06_styling_and_presentation.md) |

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

---

## Keeping Recipes Current

* Every recipe has its own `README.md` with the versions it was last built with (2026-11-22).
* CI runs `npm ci`, the type check and the production build for each recipe on every pull request.
* The weekly freshness report lists recipe dependencies that are a major version behind npm.
* To run one locally: `cd recipes/<name> && npm ci && npm run build`.
