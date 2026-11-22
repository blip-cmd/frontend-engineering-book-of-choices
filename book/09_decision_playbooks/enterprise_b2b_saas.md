---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: vite 8.x, react 19.x, next 16.x, tanstack-query 5.x, nuqs 2.x, shadcn 4.x (Base UI default changelog July 2026), tailwindcss 4.x, tanstack-table 9.x, tanstack-virtual 3.x, react-hook-form 7.x, hookform-resolvers 7.x, zod 4.x, trpc 11.x, orval 8.x, openapi-typescript 7.x, redux-toolkit 2.x, MDN, web.dev, Chrome for Developers
review_by: 2027-05
reviewers:
ledger: reviews/enterprise-b2b-saas.md
---

# Decision Playbook: Enterprise B2B SaaS & Data Grids

> Recommended Architecture for: Internal Admin Portals, Enterprise Dashboards, Billing & CRM Platforms, and Complex Multi-Tenant Workspaces.

This playbook is the book's recommendation for one archetype: a login-gated, data-heavy React app for business users. The stack choices are positions, labelled as such; the facts behind them link to official documentation. Package versions were checked against the npm registry on 2026-11-21.

---

## 1. Who This Playbook Assumes

* **Primary success metric:** shipping features quickly without regressions. That means correct form validation, data tables that sort, filter, paginate and scroll through large result sets, and role-based access control (RBAC) in the UI.
* **Traffic pattern:** users sign in before they see any product screen (corporate intranet or subscription SaaS), so search indexing of those screens does not matter. MDN lists SEO as one of the trade-offs of a single-page application ([MDN: SPA](https://developer.mozilla.org/en-US/docs/Glossary/SPA)); behind a login, that trade-off costs nothing. The playbook also assumes desktop browsers on reliable office connections. That is an assumption about the audience, not a measured fact.
* **Team profile:** a growing team hiring generalist React developers, where TypeScript types shared between client and server catch contract mistakes before release.

---

## 2. The Recommended Stack, Layer by Layer

| Layer | Recommended choice (position) | What it does, with sources |
| :--- | :--- | :--- |
| **Execution boundary** | **Vite 8 + React 19 single-page app**; Next.js 16 App Router if the same team also owns server code or public pages | An SPA loads one HTML document and then updates it with JavaScript, so moving between screens does not load a new page from the server ([MDN: SPA](https://developer.mozilla.org/en-US/docs/Glossary/SPA)). Assets referenced in source code get hashed file names in a Vite build ([Vite: Static Asset Handling](https://vite.dev/guide/assets)), and a URL that changes whenever its content changes "can be cached for a longer period" ([MDN: HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)). The React team recommends "starting with a framework" and offers building from scratch with a tool like Vite for apps whose "constraints [are] not well-served by existing frameworks" ([react.dev: Creating a React App](https://react.dev/learn/creating-a-react-app)); this playbook's position is that a login-gated admin app with no public pages can be such a case. The App Router is Next.js's file-system router built on Server Components and Suspense ([Next.js docs](https://nextjs.org/docs/app)). |
| **State and cache** | **TanStack Query 5** for server data; **URL search params via nuqs 2** for filters, search terms and tabs | TanStack Query handles "fetching, caching, synchronizing and updating server state" ([TanStack Query: Overview](https://tanstack.com/query/latest/docs/framework/react/overview)). By default, failed queries are retried 3 times with exponential backoff ([Important Defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)), and `placeholderData: keepPreviousData` keeps the last page on screen while the next one loads ([Paginated Queries](https://tanstack.com/query/latest/docs/framework/react/guides/paginated-queries)). nuqs's `useQueryState` replaces `React.useState` and syncs the value with the URL ([nuqs: Basic usage](https://nuqs.dev/docs/basic-usage)), so a filtered view can be shared as a link; nuqs 2 supports React SPAs, Next.js, React Router and TanStack Router ([nuqs: Installation](https://nuqs.dev/docs)). |
| **Component primitives** | **shadcn/ui with Tailwind CSS 4**, on Base UI or Radix | shadcn/ui hands you the component code itself rather than a package: "This is not a component library. It is how you build your component library." ([shadcn/ui docs](https://ui.shadcn.com/docs)). Since July 2026, `npx shadcn init` defaults to Base UI; Radix "is still fully supported" and is not deprecated ([shadcn/ui changelog: Base UI as the Default](https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default)), and React Aria is a third option ([changelog: React Aria](https://ui.shadcn.com/docs/changelog/2026-07-react-aria)). Radix Primitives follow the WAI-ARIA authoring practices and handle aria and role attributes, focus management and keyboard navigation ([Radix: Accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility)). |
| **Data tables** | **TanStack Table 9 (headless) + TanStack Virtual 3** | TanStack Table is a headless library: it provides state and APIs for sorting, filtering, grouping, column resizing, pinning and pagination, and renders no markup of its own ([TanStack Table: Overview](https://tanstack.com/table/latest/docs/overview)). It has no virtualization built in; its docs pair it with TanStack Virtual, which renders only the rows in the scroll viewport plus a small overscan buffer ([TanStack Table: Virtualization](https://tanstack.com/table/latest/docs/framework/react/guide/virtualization)). Virtualized rows still have to be loaded into the browser, so virtualization does not replace server-side pagination, filtering or sorting (same source). |
| **Forms and validation** | **React Hook Form 7 + Zod 4**, joined by `@hookform/resolvers` | React Hook Form "uses refs and uncontrolled native inputs by default" ([React Hook Form FAQ](https://react-hook-form.com/faqs)), which its authors say minimizes re-renders ([react-hook-form.com](https://react-hook-form.com/)). `zodResolver` from `@hookform/resolvers/zod` plugs a Zod schema into `useForm` ([resolvers README](https://github.com/react-hook-form/resolvers)). The same Zod schema can validate tRPC procedure inputs ([tRPC: Validators](https://trpc.io/docs/server/validators)), or Orval can generate Zod schemas from an OpenAPI spec ([Orval: Zod](https://orval.dev/docs/guides/zod)), so client and server validate against one definition. |
| **API contract** | **tRPC 11** in a TypeScript monorepo; **OpenAPI with Orval 8 or openapi-typescript 7** otherwise | tRPC uses TypeScript's type inference with no code generation step and "catches problems at build time" ([tRPC docs](https://trpc.io/docs)). Its FAQ says a monorepo is not mandatory, but without one "you will lose guarantees that your client and server works together" ([tRPC FAQ](https://trpc.io/docs/faq)). For other backends, Orval generates typed TanStack Query hooks from an OpenAPI spec ([Orval: React Query](https://orval.dev/docs/guides/react-query)) and openapi-typescript generates types from OpenAPI 3.0 and 3.1 schemas ([openapi-typescript](https://openapi-ts.dev/introduction)). Generated code catches a breaking API change only after it is regenerated from the updated spec and type-checked, so the book's position is to run generation in CI. |

---

## 3. What to Avoid (Positions)

* **Do not hand-write Redux or Zustand reducers to cache API entities.**
  TanStack's docs say client-state libraries can store async data, "albeit inefficiently when compared to a tool like TanStack Query" ([TanStack Query: Does this replace client state?](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state)); that is the library's own view of itself. Redux's docs make the same point for Redux apps: RTK Query exists to eliminate "the need to hand-write data fetching & caching logic yourself" ([RTK Query overview](https://redux-toolkit.js.org/rtk-query/overview)). A team already on Redux Toolkit can use RTK Query instead of adding TanStack Query, and keep Redux or Zustand for client-only state that is truly global.
* **Do not split one product team's app into micro-frontends.**
  The book's position: micro-frontends address separate teams that must release parts of one UI independently. For a single team, a monorepo with pnpm workspaces ([pnpm: Workspaces](https://pnpm.io/workspaces)) and Turborepo, which is "designed for scaling monorepos" ([Turborepo docs](https://turborepo.dev/docs)), keeps shared types and cross-package refactors in one commit, with no runtime composition layer to run.
* **Do not render large tables without virtualization or server-side pagination.**
  Every rendered row adds DOM nodes, and with a large DOM the browser "must constantly recompute the position and styling of nodes" as users interact ([Chrome for Developers: Avoid an excessive DOM size](https://developer.chrome.com/docs/lighthouse/performance/dom-size)). Virtualize long client-side tables with TanStack Virtual, and page or filter on the server when the full dataset is too large to load. For small tables, TanStack's docs say normal rendering "is simpler and usually preferable" ([TanStack Table: Virtualization](https://tanstack.com/table/latest/docs/framework/react/guide/virtualization)).

---

## 4. Constraint Checklist

* Do users bookmark and share filtered reports? Keep filter, search, sort and page state in URL search params with nuqs `useQueryState`.
* Do forms have many interdependent fields? Write one Zod schema for the whole form and pass it to React Hook Form with `zodResolver`.
* Is the backend TypeScript and in the same repository? Use tRPC. Otherwise, generate the client from an OpenAPI spec with Orval or openapi-typescript.
* Do tables hold more rows than a page can render comfortably? Virtualize with TanStack Virtual if the data fits in the browser; use server-side pagination if it does not.

---

## 5. When This Playbook Is the Wrong Choice

* **Public pages need search traffic.** Marketing pages, documentation or public listings lose the SEO trade-off that MDN attributes to SPAs ([MDN: SPA](https://developer.mozilla.org/en-US/docs/Glossary/SPA)). Render those pages on the server or at build time; see the [content-first publishing playbook](content_first_publishing.md).
* **The backend is not TypeScript, or lives in another team's repository.** tRPC's guarantee depends on sharing types between client and server ([tRPC FAQ](https://trpc.io/docs/faq)); use an OpenAPI contract instead.
* **Several teams must ship parts of one UI on separate release schedules.** The single-monorepo position in section 3 assumes one release train. Independent deployment is the case micro-frontends exist for (book's reasoning, not a sourced finding).
* **Users must find any row with the browser's find-in-page.** Virtualization renders only the rows in the scroll viewport plus an overscan buffer ([TanStack Table: Virtualization](https://tanstack.com/table/latest/docs/framework/react/guide/virtualization)), so find-in-page cannot reach rows that are not in the DOM. CSS `content-visibility: auto` keeps off-screen content in the DOM and the accessibility tree, so it stays searchable ([web.dev: content-visibility](https://web.dev/articles/content-visibility)); it has been Baseline newly available since September 2024 ([MDN: content-visibility](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/content-visibility)).
* **The team wants a finished grid, not a grid toolkit.** TanStack Table "is NOT a pre-built table component, like you might find from a library like AG Grid" ([TanStack Table: Overview](https://tanstack.com/table/latest/docs/overview)); you write the markup, styles and interactions yourself. A pre-built grid component trades that control for less code to write.
* **Users work on poor or offline connections.** The connectivity assumption in section 1 no longer holds, and this playbook does not cover offline-first design.
