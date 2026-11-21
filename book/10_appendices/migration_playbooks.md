---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: rspack 2.3 docs, vite 8.3 docs, @vitejs/plugin-react 6.3, tailwindcss 4.3 docs, styled-components 6.6 docs, next.js app router docs, panda-css 2.6 docs, class-variance-authority 0.7, astro 7.4 and @astrojs/react 7.1 docs, react.dev, MDN view transitions (2026-11), cloudflare workers routes, nginx proxy module, martinfowler.com
review_by: 2027-05
reviewers:
ledger: reviews/migration-playbooks.md
---

# Appendix D: Zero-Downtime Migration Playbooks

> Three incremental migrations for a tech lead who has to modernize a live frontend without stopping feature work or shipping a big-bang rewrite. Each playbook names the versions it was checked against.

---

## 1. Playbook 1: Leave Webpack for Rspack (Keep the Config) or Vite (Change the Model)

### The Problem
A large codebase on Webpack 5 has a dev server that takes minutes to start and CI builds that block every merge. The team wants faster feedback without a long freeze.

### Choose Rspack When the Webpack Config Is the Asset
1. **Option A: Rspack 2 as a near drop-in replacement.**
   * Rspack's docs say it "is compatible with the vast majority of webpack's configuration options and APIs, allowing you to reuse existing loaders and plugins" ([Rspack introduction](https://rspack.rs/guide/start/introduction)). That makes it the lower-risk choice when the build depends on custom loaders and plugins.
   * Speed: Rspack describes itself as "more than 10 times faster than webpack" ([Rspack introduction](https://rspack.rs/guide/start/introduction)). This is the vendor's own claim; measure your own build before and after.
   * Install `@rspack/core` (2.x) plus `@rspack/cli` if you used `webpack-cli` and `@rspack/dev-server` if you used `webpack-dev-server`, then change `webpack serve` / `webpack build` to `rspack dev` / `rspack build` ([Rspack: Migrate from webpack](https://rspack.rs/guide/migration/webpack)). `@rspack/core@2` requires Node.js `^20.19.0 || >=22.12.0` (same source).
   * **When not to:** the migration guide targets webpack 5, because Rspack's API and configuration align with webpack 5. A Webpack 4 project should read webpack's own v4 to v5 migration notes first ([Rspack: Migrate from webpack](https://rspack.rs/guide/migration/webpack)). Check every plugin against the [community plugin compatibility list](https://rspack.rs/plugins/community-plugin-compatibility): some, such as `@ngtools/webpack` and `critters-webpack-plugin`, are listed as incompatible.

### Choose Vite When You Can Rewrite the Build Entry Points
2. **Option B: Move to Vite 8.**
   * *Phase 1: environment variables.* Replace `process.env.X` reads in client code with `import.meta.env.VITE_X`. By default, Vite only exposes variables prefixed with `VITE_` to client code, and their values are bundled in at build time, so they must not hold secrets ([Vite: Env Variables and Modes](https://vite.dev/guide/env-and-mode)). For React, add `@vitejs/plugin-react`, which provides Fast Refresh and the automatic JSX runtime ([plugin README](https://github.com/vitejs/vite-plugin-react/tree/main/packages/plugin-react)); it does not handle environment variables.
   * *Phase 2: `index.html` as the entry.* In Vite, `index.html` sits at the project root and is "the entry point to your application"; Vite resolves the `<script type="module" src="...">` tags inside it ([Vite: Getting Started](https://vite.dev/guide/)). Replace the webpack `entry` setting and the HTML plugin template with this file.
   * *Phase 3: path aliases.* Either set `resolve.alias` in `vite.config.ts`, or set `resolve.tsconfigPaths: true` to reuse the `paths` in `tsconfig.json`. Vite's docs note that the tsconfig option "has a performance cost" ([Vite: Features](https://vite.dev/guide/features); [Vite: Shared Options](https://vite.dev/config/shared-options)).
   * *Result:* in development, Vite serves source files over native ES modules and its HMR updates only the edited module without a full page reload ([Why Vite](https://vite.dev/guide/why)). Vite 8 uses Rolldown and Oxc based tools instead of esbuild and Rollup ([Vite: Migration from v7](https://vite.dev/guide/migration)).
   * **When not to:** the Vite team itself notes that "exceptionally large codebases can experience slow page loads due to the high number of unbundled network requests" in dev ([Why Vite](https://vite.dev/guide/why)). For a very large app with heavy webpack customization, Option A is the smaller change.

---

## 2. Playbook 2: Replace Runtime CSS-in-JS with Build-Time Styles (Tailwind CSS 4 or Panda CSS)

### The Problem
A React application uses `styled-components` or `@emotion/styled`, which inject `<style>` tags at runtime. The React docs advise against runtime injection because it "forces the browser to recalculate the styles a lot more often" ([react.dev: useInsertionEffect](https://react.dev/reference/react/useInsertionEffect)). Rewriting every component at once is not an option.

**Check the motivation first.** If the goal is React Server Components alone, styled-components 6.3+ "natively supports React Server Components (RSC) with zero configuration" ([styled-components: Advanced](https://styled-components.com/docs/advanced)), so a migration is not required for that reason. Emotion is different: the Next.js App Router docs list Emotion under libraries still "working on support" ([Next.js: CSS-in-JS](https://nextjs.org/docs/app/guides/css-in-js)).

### Step-by-Step Incremental Migration
1. **Phase 1: Co-existence setup.**
   * Install Tailwind CSS 4 alongside the existing library. Tailwind's Preflight base styles can restyle existing components. Tailwind 4 has no `preflight: false` setting (the v3 `corePlugins` option "is no longer supported in v4"); instead, import `tailwindcss/theme.css` and `tailwindcss/utilities.css` without `tailwindcss/preflight.css` ([Tailwind: Preflight](https://tailwindcss.com/docs/preflight); [Tailwind: Upgrade guide](https://tailwindcss.com/docs/upgrade-guide)).
   * **When not to choose Tailwind 4:** it "is designed for Safari 16.4+, Chrome 111+, and Firefox 128+"; projects that must support older browsers should stay on v3.4 ([Tailwind: Upgrade guide](https://tailwindcss.com/docs/upgrade-guide)).
2. **Phase 2: New components only.**
   * Set a team rule (this book's recommendation, not a tool requirement) that new UI components use Tailwind classes or Panda CSS. Panda "generates plain atomic CSS at build time" from styles written in TypeScript, so no style engine ships to users ([Panda CSS: Why Panda](https://panda-css.com/docs/overview/why-panda)).
3. **Phase 3: Leaf-to-root conversion.**
   * Migrate leaf components first: buttons, badges, avatars, inputs. They have no styled children, so each one can ship on its own.
   * Replace props-based styled components with Tailwind classes and `cva` from the `class-variance-authority` package (0.7.x) for variant mapping ([cva docs](https://cva.style/docs)).
4. **Phase 4: Remove the runtime dependency.**
   * Once the top-level layout containers are migrated and no imports remain, uninstall `styled-components` or `@emotion/react` and `@emotion/styled`, so the styling runtime leaves the production bundle.

---

## 3. Playbook 3: Strangle a Monolithic SPA Route by Route into Astro Islands

### The Problem
A monolithic single-page application has weak search visibility and fails Core Web Vitals on content pages, but the business cannot take the site offline for a rewrite. The Strangler Fig approach, named by Martin Fowler, replaces a legacy system gradually instead of in one cutover ([Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html)).

### Step-by-Step Incremental Migration
1. **Put a path-based reverse proxy in front.**
   * Use an edge or proxy layer that can route by URL path: for example, a Cloudflare Worker on a [route](https://developers.cloudflare.com/workers/configuration/routing/routes/) that calls `fetch()` toward the right origin, or NGINX [`proxy_pass`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) in separate `location` blocks.
2. **Carve out content routes.**
   * Stand up an Astro 7 project serving `/blog`, `/docs` and marketing pages.
   * Route those paths to the Astro app and every other path (`/app`, `/dashboard`) to the legacy SPA. Both stay on one hostname.
3. **Port content-heavy pages first.**
   * Move product catalog and public pages into Astro. Reuse existing React components through [`@astrojs/react`](https://docs.astro.build/en/guides/integrations-guide/react/), which "enables rendering and client-side hydration for your React components", and hydrate only the interactive ones as islands. With `client:visible`, a component loads "only once it enters the viewport"; the rest of the page stays static HTML ([Astro: Islands architecture](https://docs.astro.build/en/concepts/islands/)).
4. **Smooth navigation between the two apps with cross-document view transitions.**
   * Cross-document view transitions work only when both documents are on the same origin and both opt in with `@view-transition { navigation: auto; }` in their CSS ([MDN: Using the View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using)). The path-based proxy above keeps one origin, which makes this possible.
   * The `@view-transition` at-rule has Limited availability in Baseline terms ("not Baseline because it does not work in some of the most widely-used browsers") as checked on MDN in November 2026 ([MDN: @view-transition](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@view-transition)). Treat it as progressive enhancement: navigation still works without it.
