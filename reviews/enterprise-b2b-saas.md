---
page: book/09_decision_playbooks/enterprise_b2b_saas.md
verified: 2026-11-21
---

# Claim Ledger: Decision Playbook, Enterprise B2B SaaS & Data Grids

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead or senior frontend developer starting, or re-platforming, a login-gated business app (admin portal, dashboard, billing or CRM tool) built around forms and data tables. The page helps them pick one library per layer: execution boundary, server state, component primitives, tables, forms and API contract. Thesis (unchanged from the draft): a client-rendered React SPA with a server cache, URL state, headless tables, schema-validated forms and a typed API contract fits this archetype, because search indexing does not matter behind a login and type safety across the client/server boundary prevents regressions.

**History.** Author pass on 2026-11-21 rewrote the AI-generated draft. Among other errors, the draft said "90% of state is remote API data" (no source; replaced with TanStack Query's own qualitative statement, labelled as the library's view), set a micro-frontend threshold of "under 50 engineers" (no source; now a labelled position without a number), described shadcn/ui as built on Radix only (since July 2026 shadcn/ui defaults to Base UI, with Radix and React Aria also supported), and implied TanStack Table virtualizes rows itself (TanStack Table has no virtualization built in). It had no "when not to" section; section 5 was added from sourced facts and labelled reasoning.

**Recommendation changes (rule A1).** None to the stack. Two qualifications that primary sources required:
1. Component primitives now read "shadcn/ui on Base UI or Radix" instead of "Radix UI Primitives", because the shadcn/ui changelog makes Base UI the default for projects created since July 2026 while keeping Radix fully supported.
2. "Avoid Redux to cache API entities" now notes RTK Query as the Redux Toolkit route, because Redux's own docs provide a server-cache tool and the draft implied Redux could only be used with hand-written reducers.

---

## 1. Author pass (2026-11-21)

Sources were fetched in the same session (curl, HTML stripped to text, or the TanStack `.md` endpoints) and quotes matched against the page text. Package versions came from `npm view` on 2026-11-21. The page has no code blocks, so there was nothing to run.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | An SPA loads a single document and updates it with JavaScript; MDN lists SEO among its trade-offs | [MDN: SPA](https://developer.mozilla.org/en-US/docs/Glossary/SPA) | verified (quote); replaces the draft's "SEO is completely irrelevant" with the login-gated reasoning |
| 2 | Vite gives built assets hashed file names | [Vite: Static Asset Handling](https://vite.dev/guide/assets) | verified (quote) |
| 3 | A URL that changes with its content "can be cached for a longer period" | [MDN: HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) | verified (quote); replaces the draft's "caches permanently in the browser" |
| 4 | React recommends "starting with a framework"; from-scratch builds with Vite for constraints "not well-served by existing frameworks" | [react.dev: Creating a React App](https://react.dev/learn/creating-a-react-app) | verified (quote); added so the SPA choice is labelled as a position against React's default advice |
| 5 | Next.js App Router is a file-system router using Server Components and Suspense | [Next.js docs: App Router](https://nextjs.org/docs/app) | verified (quote) |
| 6 | TanStack Query handles "fetching, caching, synchronizing and updating server state" | [TanStack Query: Overview](https://tanstack.com/query/latest/docs/framework/react/overview) | verified (quote) |
| 7 | Failed queries are retried 3 times with exponential backoff by default | [TanStack Query: Important Defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults) | verified (quote); draft said "retries" without detail |
| 8 | `placeholderData` with `keepPreviousData` keeps the previous page's data while the next loads | [TanStack Query: Paginated Queries](https://tanstack.com/query/latest/docs/framework/react/guides/paginated-queries) | verified (quote) |
| 9 | "90% of state is remote API data" | none found | removed; replaced with claim 10 |
| 10 | Client-state libraries store async data "albeit inefficiently"; remaining global state is "usually very tiny" | [TanStack Query: Does this replace client state?](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state) | verified (quote); labelled as the library's own view (advocacy) |
| 11 | nuqs `useQueryState` replaces `React.useState` and syncs with the URL | [nuqs: Basic usage](https://nuqs.dev/docs/basic-usage) | verified (quote) |
| 12 | nuqs 2 supports React SPA, Next.js, React Router and TanStack Router | [nuqs: Installation](https://nuqs.dev/docs) | verified |
| 13 | shadcn/ui: "This is not a component library. It is how you build your component library."; hands you the component code | [shadcn/ui docs](https://ui.shadcn.com/docs) | verified (quote) |
| 14 | Since July 2026 new shadcn/ui projects default to Base UI; Radix "is still fully supported" and not deprecated | [shadcn/ui changelog: Base UI as the Default](https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default) | verified (quote); corrects the draft's "Radix UI Primitives + Tailwind" |
| 15 | React Aria is a first-class shadcn/ui base alongside Base UI and Radix | [shadcn/ui changelog: React Aria](https://ui.shadcn.com/docs/changelog/2026-07-react-aria) | verified (quote) |
| 16 | Radix follows WAI-ARIA authoring practices; handles aria and role attributes, focus management, keyboard navigation | [Radix: Accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility) | verified (quote); draft's "high accessibility baseline out of the box" made specific |
| 17 | TanStack Table is headless and renders no markup; features include sorting, filtering, grouping, column resizing, pinning, pagination | [TanStack Table: Overview](https://tanstack.com/table/latest/docs/overview) | verified (quote) |
| 18 | TanStack Table has no built-in virtualization; official examples use TanStack Virtual, which renders visible items plus an overscan buffer | [TanStack Table: Virtualization](https://tanstack.com/table/latest/docs/framework/react/guide/virtualization) | verified (quote); corrects the draft's implication that Table virtualizes |
| 19 | Virtualization "is not a replacement for server-side pagination, filtering, or sorting"; for small tables normal rendering "is simpler and usually preferable" | TanStack Table: Virtualization | verified (quote) |
| 20 | "Powers multi-thousand row data tables" | none | removed (unquantified capacity claim); replaced by claims 18 and 19 |
| 21 | TanStack Table "is NOT a pre-built table component, like you might find from a library like AG Grid" | TanStack Table: Overview | verified (quote); used in "wrong choice" |
| 22 | React Hook Form "uses refs and uncontrolled native inputs by default" | [React Hook Form FAQ](https://react-hook-form.com/faqs) | verified (quote) |
| 23 | React Hook Form says it "Minimizes the number of re-renders" | [react-hook-form.com](https://react-hook-form.com/) | verified (quote), attributed to its authors; draft's "eliminate unnecessary re-renders on every keystroke" softened to the source's wording |
| 24 | `zodResolver` from `@hookform/resolvers/zod` | [resolvers README](https://github.com/react-hook-form/resolvers) | verified |
| 25 | tRPC procedures accept Zod input validators | [tRPC: Validators](https://trpc.io/docs/server/validators) | verified |
| 26 | Orval generates Zod schemas from OpenAPI | [Orval: Zod](https://orval.dev/docs/guides/zod) | verified (quote) |
| 27 | tRPC uses TypeScript inference with no code generation and "catches problems at build time" | [tRPC docs](https://trpc.io/docs) | verified (quote) |
| 28 | Monorepo not mandatory, but without one "you will lose guarantees that your client and server works together" | [tRPC FAQ](https://trpc.io/docs/faq) | verified (quote) |
| 29 | Orval generates typed TanStack Query hooks from OpenAPI | [Orval: React Query](https://orval.dev/docs/guides/react-query) | verified (quote) |
| 30 | openapi-typescript turns OpenAPI 3.0 and 3.1 schemas into TypeScript | [openapi-typescript](https://openapi-ts.dev/introduction) | verified (quote); added as the types-only OpenAPI option |
| 31 | Generated clients catch breaking changes only after regeneration and type-check; run generation in CI | none | book's position, labelled; follows from claims 26, 29, 30 |
| 32 | RTK Query eliminates "the need to hand-write data fetching & caching logic yourself" | [RTK Query overview](https://redux-toolkit.js.org/rtk-query/overview) | verified (quote) |
| 33 | "Do NOT use Micro-Frontends if team size is under 50 engineers" | none found | number removed; rewritten as a labelled position (one team vs independently releasing teams) |
| 34 | pnpm has built-in workspace (monorepo) support | [pnpm: Workspaces](https://pnpm.io/workspaces) | verified (quote) |
| 35 | Turborepo is "designed for scaling monorepos" | [Turborepo docs](https://turborepo.dev/docs) | verified (quote) |
| 36 | With a large DOM the browser "must constantly recompute the position and styling of nodes" | [Chrome for Developers: Avoid an excessive DOM size](https://developer.chrome.com/docs/lighthouse/performance/dom-size) | verified (quote); draft's "1,000 table rows" threshold removed. The source says this audit moved into the Lighthouse 13 "Optimize DOM size" insight; the quoted mechanism still stands, and the page cites no Lighthouse thresholds |
| 37 | `content-visibility: auto` keeps off-screen content in the DOM and accessibility tree, so it can be searched | [web.dev: content-visibility](https://web.dev/articles/content-visibility); [MDN: content-visibility](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/content-visibility) | verified (quote) |
| 38 | `content-visibility` is Baseline 2024 newly available, since September 2024 | MDN: content-visibility | verified (quote) |
| 39 | Find-in-page cannot reach virtualized rows that are not in the DOM | TanStack Table: Virtualization; web.dev: content-visibility | inference from claims 18 and 37 (web.dev contrasts DOM-resident content as searchable) |
| 40 | Versions: vite 8.3.8, react 19.3.1, next 16.4.6, @tanstack/react-query 5.108.2, nuqs 2.10.3, tailwindcss 4.3.5, @tanstack/react-table 9.3.1, @tanstack/react-virtual 3.14.26, react-hook-form 7.92.0, @hookform/resolvers 7.0.8, zod 4.6.7, @trpc/server 11.29.7, orval 8.48.0, openapi-typescript 7.13.0, shadcn 4.23.0, @reduxjs/toolkit 2.15.0, zustand 5.1.0, turbo 2.11.13 | `npm view <name> version` | verified; pinned on the page by major version |
| 41 | Archetype assumptions: desktop browsers, reliable connections, growing team of generalist React developers | none | labelled as assumptions about the audience |
| 42 | Single-monorepo position assumes one release train; micro-frontends exist for independent deployment; offline-first is out of scope | none | labelled as the book's reasoning |

## 2. Independent verifier pass (2026-11-21 to 2026-11-22)

**Verdict: PASS.** The verifier did not write the page or section 1. Claims were extracted afresh from the page (37 factual claims plus 18 pinned versions), and every cited source was fetched with `curl -sL` (TanStack pages via their `.md` endpoints, the resolvers README via raw GitHub), stripped to text and searched for each quote. All quotes appear verbatim, allowing for typographic differences (markdown emphasis in TanStack Table's "**_NOT_** a pre-built table component").

* **shadcn/ui and Base UI:** the changelog entry is titled "July 2026 - Base UI as the Default" (also listed under July 2026 on the changelog index) and says "Run npx shadcn init and Base UI is the default pick", "Radix is still fully supported" and "Radix is not being deprecated". The React Aria entry (July 2026) says "Base UI remains the default, and Radix remains fully supported". SUPPORTED.
* **Other sources:** MDN SPA (single document; "tradeoff disadvantages such as SEO"), MDN HTTP caching, react.dev, Next.js App Router, TanStack Query (overview, defaults "silently retried 3 times, with exponential backoff delay", paginated queries, client state), nuqs (basic usage; nuqs@^2 frameworks list), Radix accessibility, TanStack Table (overview feature list, headless definition, AG Grid quote; virtualization: no built-in virtualization, overscan buffer, "not a replacement for server-side pagination, filtering, or sorting", "simpler and usually preferable"), React Hook Form FAQ and home page, resolvers README, tRPC docs, FAQ and validators, Orval Zod and React Query guides, openapi-typescript, RTK Query, pnpm, Turborepo, Chrome DOM size, web.dev and MDN content-visibility ("Baseline 2024 Newly available", "Since September 2024"). All SUPPORTED except the three PARTIAL claims below, now corrected.
* **Edits (rewording only, no new claims or sources):**
  1. "Vite gives built assets hashed file names" was PARTIAL (the source says *referenced* assets get hashed names; public-directory files do not). Now "Assets referenced in source code get hashed file names in a Vite build".
  2. "syncs the value with the URL, which makes filtered views shareable as links" placed the shareable-link inference inside the nuqs citation, which does not say it. PARTIAL; the citation now covers only the URL sync, and "so a filtered view can be shared as a link" follows as the book's reasoning.
  3. "shadcn/ui copies component source into your repository" was a stretch of "shadcn/ui hands you the actual component code". PARTIAL; now "hands you the component code itself rather than a package".
* **Numbers:** 3 retries, July 2026, September 2024, OpenAPI 3.0 and 3.1, and all major versions are sourced. No unsourced numbers remain.
* **Versions (`npm view <name> version`, 2026-11-22):** vite 8.3.8, react 19.3.1, next 16.4.6, @tanstack/react-query 5.108.2, nuqs 2.10.3, tailwindcss 4.3.5, @tanstack/react-table 9.3.1, @tanstack/react-virtual 3.14.26, react-hook-form 7.92.0, @hookform/resolvers 7.0.8, zod 4.6.7, @trpc/server 11.29.7, orval 8.48.0, openapi-typescript 7.13.0, shadcn 4.23.0, @reduxjs/toolkit 2.15.0, zustand 5.1.0, turbo 2.11.13; all match section 1 and the majors pinned on the page. @base-ui/react (1.9.0) also resolves.
* **Code checks:** the page has no code blocks, so nothing to run in `node`.
* **Gates:** `python pipelines/scripts/audit_repo_standards.py` run after the edits (see the verdict above; it passed).

## 3. Known omissions (follow-up content, not errors)

* RBAC is named as a success metric but the page never says how to implement it; at minimum it should state that UI checks hide controls while the server must enforce authorization (needs an OWASP citation).
* Multi-tenancy (tenant switching, cache keys scoped per tenant in TanStack Query) is in the archetype list but not discussed.
* Accessibility of virtualized tables (`aria-rowcount`, `aria-rowindex` for rows not in the DOM).
* TanStack Form as an alternative to React Hook Form; TanStack Router as a typed router for the Vite SPA option.
* Pre-built grid options (for example AG Grid) with licence and bundle trade-offs.
* Server-side table state: mapping TanStack Table's sorting, filter and pagination state to nuqs and to TanStack Query keys.
* Base UI's own accessibility documentation, to match the Radix claim now that Base UI is the shadcn/ui default.

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | N/A | 1 | **18** (16 of 18, scaled) |

D9 is N/A: the page has no code examples. D3 is 1 because mechanisms (SPA document model, hashed URLs, virtualization windowing) are named in one sentence each rather than explained. D10 is 1 because some terms (headless, overscan, RBAC) are used without definition. All gates pass except G8 (human accountability), which the `agent-verified` status would disclose instead.
