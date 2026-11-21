---
status: draft
ai_involvement: drafted
last_verified:
verified_against:
review_by:
reviewers:
---

# Decision Playbook: Enterprise B2B SaaS & Data Grids

> Recommended Architecture for: Internal Admin Portals, Enterprise Dashboards, Billing & CRM Platforms, and Complex Multi-Tenant Workspaces.

---

## 1. The Archetype Profile

* **Primary Success Metric:** Developer velocity, rapid feature iteration, bulletproof form validation, rich data-table manipulation (sorting, filtering, pagination, virtualization), and robust role-based access control (RBAC).
* **Traffic Pattern:** Authenticated corporate intranet or subscription SaaS. SEO is completely irrelevant. Users access via modern desktop browsers with stable broadband connections.
* **Team Profile:** Fast-growing engineering team hiring from the general frontend talent pool; maintaining high type safety is essential to prevent regressions.

---

## 2. The Recommended Architectural Stack

| Layer | Recommended Choice | Rationale |
| :--- | :--- | :--- |
| **Execution Boundary** | **Vite + React SPA (or Next.js App Router if full-stack)** | An authenticated SPA shell caches permanently in the browser. Users log in once and experience fluid client-side page transitions without server rendering round trips. |
| **State & Cache** | **TanStack Query (React Query) + URL State** | 90% of state is remote API data (customer records, invoices). TanStack Query manages caching, retries, and pagination. Table filters, search terms, and active tabs are stored directly in URL query parameters via `nuqs` for shareable deep links. |
| **Component Primitives** | **shadcn/ui (Radix UI Primitives + Tailwind CSS)** | High accessibility baseline out of the box, full source code ownership in your repo, and easy customization without third-party CSS battles. |
| **Data Tables** | **TanStack Table (Headless) + TanStack Virtual** | Powers multi-thousand row data tables with sorting, grouping, and column resizing while keeping the DOM lightweight via DOM node virtualization. |
| **Form & Validation** | **React Hook Form + Zod** | Uncontrolled form inputs eliminate unnecessary re-renders on every keystroke. Zod schemas enforce type-safe validation matching backend API contracts. |
| **API Contract** | **tRPC (in TypeScript Monorepo) or OpenAPI / Orval** | End-to-end type safety ensures frontend forms catch backend schema regressions immediately at build time. |

---

## 3. What to Explicitly Avoid

* **Do NOT use a centralized global store (Redux / Zustand) to cache API entities:**
  Do not manually write reducers and actions for API requests. Rely on TanStack Query to manage server cache lifecycles.
* **Do NOT use Micro-Frontends if team size is under 50 engineers:**
  A monolithic repository managed with Turborepo or pnpm workspaces provides superior development speed, unified typing, and instant refactoring without runtime orchestration tax.
* **Do NOT render 1,000 table rows without DOM virtualization:**
  Appending thousands of table nodes directly into the DOM degrades memory and causes scroll stutter. Always virtualize large lists.

---

## 4. Constraint Checklist
* Are users frequently bookmarking and sharing filtered reports? Store all filter, search, and page state in URL query parameters.
* Do forms feature complex interdependent fields? Leverage `react-hook-form` with a declarative Zod resolver.
