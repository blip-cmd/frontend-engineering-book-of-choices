---
page: book/10_appendices/migration_playbooks.md
verified: 2026-11-21
---

# Claim Ledger: Appendix D, Zero-Downtime Migration Playbooks

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead who has to modernize a live frontend without a feature freeze. The page helps them pick an incremental route for three common migrations: Webpack to Rspack or Vite, runtime CSS-in-JS to build-time styling, and a monolithic SPA to Astro islands behind a path-based proxy. Thesis (unchanged from the draft): migrate in small, reversible steps that run alongside the legacy system rather than through a big-bang rewrite.

**History.** Author pass on 2026-11-21 rewrote the AI-generated draft. Among other errors, the draft claimed Rspack "replicates 90% of Webpack's API surface" with "5x to 10x faster builds" (Rspack's docs say "the vast majority" of options and APIs and "more than 10 times faster", as a vendor claim); told readers to set Tailwind `preflight: false` (Tailwind 4 has no such option); and said `@vitejs/plugin-react` handles environment variables (it provides Fast Refresh and the JSX runtime).

**Recommendation changes (rule A1).**
1. Playbook 2 no longer presents React Server Components as a reason to leave styled-components: styled-components 6.3+ supports RSC natively. The migration motivation is now runtime style injection, which the React docs advise against. Emotion still lacks App Router support per the Next.js docs.
2. Playbook 1 no longer offers Rspack as a direct path from Webpack 4: Rspack's migration guide targets webpack 5 and sends v4 users to webpack's v4 to v5 notes first.

---

## 1. Author pass (2026-11-21)

Sources were fetched in the same session (curl, HTML stripped to text) and quotes matched against the page text. Package versions came from `npm view` on 2026-11-21. The page has no code blocks, so there was nothing to run.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | Rspack "is compatible with the vast majority of webpack's configuration options and APIs, allowing you to reuse existing loaders and plugins" | [Rspack introduction](https://rspack.rs/guide/start/introduction) | verified (quote); draft's "90% of Webpack's API surface" removed |
| 2 | Rspack claims to be "more than 10 times faster than webpack" | [Rspack introduction](https://rspack.rs/guide/start/introduction) | verified (quote), labelled as the vendor's claim; draft's "5x to 10x" corrected |
| 3 | Install `@rspack/core`, plus `@rspack/cli` only if using `webpack-cli` and `@rspack/dev-server` only if using `webpack-dev-server`; scripts become `rspack dev` / `rspack build` | [Rspack: Migrate from webpack](https://rspack.rs/guide/migration/webpack) | verified; draft named only `@rspack/cli` |
| 4 | `@rspack/core@2` requires Node.js `^20.19.0 \|\| >=22.12.0` | Rspack: Migrate from webpack | verified (quote) |
| 5 | Migration guide targets webpack 5; webpack 4 projects should read webpack's v4 to v5 notes | Rspack: Migrate from webpack | verified; draft's "Webpack 4 or 5" corrected |
| 6 | `@ngtools/webpack` and `critters-webpack-plugin` listed as incompatible | [Rspack: Community plugin compatibility](https://rspack.rs/plugins/community-plugin-compatibility) | verified |
| 7 | Vite exposes env under `import.meta.env`; only `VITE_` variables reach client code; values are bundled at build time and must not hold API keys | [Vite: Env Variables and Modes](https://vite.dev/guide/env-and-mode) | verified (quote) |
| 8 | `@vitejs/plugin-react` provides Fast Refresh and the automatic JSX runtime | [plugin-react README](https://github.com/vitejs/vite-plugin-react/tree/main/packages/plugin-react) | verified; draft's claim that it replaces `import.meta.env` migration corrected |
| 9 | `index.html` is "the entry point to your application"; Vite resolves its module script tags | [Vite: Getting Started](https://vite.dev/guide/) | verified (quote) |
| 10 | `resolve.alias`; `resolve.tsconfigPaths: true` reuses tsconfig `paths` and "has a performance cost" | [Vite: Features](https://vite.dev/guide/features); [Vite: Shared Options](https://vite.dev/config/shared-options) | verified (quote) |
| 11 | Vite dev serves source over native ESM; HMR updates the edited module without a full reload | [Why Vite](https://vite.dev/guide/why) | verified; draft's "HMR under 50ms" removed (no source) |
| 12 | Vite 8 uses Rolldown and Oxc instead of esbuild and Rollup | [Vite: Migration from v7](https://vite.dev/guide/migration) | verified (quote) |
| 13 | "exceptionally large codebases can experience slow page loads due to the high number of unbundled network requests" | Why Vite | verified (quote); added as "when not to" |
| 14 | Runtime `<style>` injection "forces the browser to recalculate the styles a lot more often" | [react.dev: useInsertionEffect](https://react.dev/reference/react/useInsertionEffect) | verified (quote); replaces the draft's unsourced INP claim |
| 15 | styled-components 6.3+ "natively supports React Server Components (RSC) with zero configuration" | [styled-components: Advanced](https://styled-components.com/docs/advanced) | verified (quote); contradicts the draft's premise (see recommendation change 1) |
| 16 | Next.js App Router docs list Emotion under libraries "working on support" | [Next.js: CSS-in-JS](https://nextjs.org/docs/app/guides/css-in-js) | verified; Emotion issue [#2928](https://github.com/emotion-js/emotion/issues/2928) also open |
| 17 | Tailwind 4: `corePlugins` "is no longer supported in v4"; disable Preflight by importing `theme.css` and `utilities.css` without `preflight.css` | [Tailwind: Preflight](https://tailwindcss.com/docs/preflight); [Tailwind: Upgrade guide](https://tailwindcss.com/docs/upgrade-guide) | verified; draft's `preflight: false` corrected |
| 18 | Tailwind 4 "is designed for Safari 16.4+, Chrome 111+, and Firefox 128+"; older targets stay on v3.4 | Tailwind: Upgrade guide | verified (quote); added as "when not to" |
| 19 | Panda "generates plain atomic CSS at build time" with no style engine shipped to users | [Panda CSS: Why Panda](https://panda-css.com/docs/overview/why-panda) | verified (quote) |
| 20 | `cva` is the `class-variance-authority` package, used for variants | [cva docs](https://cva.style/docs) | verified |
| 21 | Strangler Fig, named by Martin Fowler, describes gradual legacy modernization | [Fowler: Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html) | verified |
| 22 | Cloudflare Workers routes map URL patterns to a Worker that can `fetch()` to an origin | [Cloudflare: Routes](https://developers.cloudflare.com/workers/configuration/routing/routes/) | verified |
| 23 | NGINX `proxy_pass` proxies to another server | [NGINX proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) | verified |
| 24 | `@astrojs/react` "enables rendering and client-side hydration for your React components" | [Astro: @astrojs/react](https://docs.astro.build/en/guides/integrations-guide/react/) | verified (quote) |
| 25 | `client:visible` loads a component "only once it enters the viewport"; rest of the page stays static | [Astro: Islands architecture](https://docs.astro.build/en/concepts/islands/) | verified (quote) |
| 26 | Cross-document view transitions need same-origin documents that both opt in with `@view-transition { navigation: auto; }` | [MDN: Using the View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using) | verified; draft's "across the independent applications" now states the same-origin condition |
| 27 | `@view-transition` has Limited availability ("not Baseline") | [MDN: @view-transition](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@view-transition) | verified (quote), dated November 2026 |
| 28 | Major versions named on the page (Rspack 2, Vite 8, Tailwind CSS 4, Astro 7, cva 0.7.x, styled-components 6.3+, Webpack 5) match the registry: `@rspack/core` and `@rspack/cli` 2.3.3, `vite` 8.3.8, `@vitejs/plugin-react` 6.3.0, `webpack` 5.113.0, `tailwindcss` 4.3.5, `@pandacss/dev` 2.6.0, `class-variance-authority` 0.7.1, `styled-components` 6.6.0, `@emotion/styled` 11.14.1, `@emotion/react` 11.14.0, `astro` 7.4.13, `@astrojs/react` 7.1.9 | `npm view` | verified |
| 29 | Draft numbers "3-5 minutes", "15+ minutes", "500 components" | none (illustrative scenario) | removed; problem statements made qualitative |
| 30 | Leaf-first conversion order; "new components only" rule; uninstalling the library removes its runtime from the bundle | none | book's position or explanatory background, labelled as a recommendation on the page |

## 2. Independent verifier pass (2026-11-21)

A separate agent that did not write the page extracted the claims itself and checked them. All 24 cited URLs were fetched with `curl -sL` on 2026-11-21 (each returned HTTP 200), stripped to text, and searched for each quote and paraphrase. The plugin-react README was read from the raw GitHub copy of `packages/plugin-react/README.md`.

**Claims checked: 34** (every sourced statement, quote, version and package on the page, plus the unsourced background statements).

* **SUPPORTED: 30.** All quotes appear verbatim: Rspack "vast majority" and "more than 10 times faster" (labelled vendor claim); Rspack install list, optional `@rspack/cli` and `@rspack/dev-server`, `rspack dev` / `rspack build`, Node.js `^20.19.0 || >=22.12.0`, webpack 5 target and v4 referral; `@ngtools/webpack` and `critters-webpack-plugin` marked "Incompatible"; Vite secrets warning; plugin-react Fast Refresh and automatic JSX runtime; "the entry point to your application"; `resolve.alias`, `resolve.tsconfigPaths` and "has a performance cost"; HMR over native ESM "without a full page reload"; "exceptionally large codebases..."; react.dev "forces the browser to recalculate the styles a lot more often"; styled-components "v6.3.0+ ... natively supports React Server Components (RSC) with zero configuration"; Next.js "currently working on support: emotion"; Tailwind `corePlugins` "no longer supported in v4", Preflight import split, "designed for Safari 16.4+, Chrome 111+, and Firefox 128+", v3.4; Panda "plain atomic CSS at build time" and "without shipping a style engine to your users"; cva is `class-variance-authority`; Fowler's gradual-replacement metaphor; Cloudflare routes and `fetch()` subrequests; NGINX `proxy_pass` in `location` context; `@astrojs/react` quote; `client:visible` quote; MDN same-origin and `@view-transition { navigation: auto; }` opt-in; MDN "Limited availability ... not Baseline".
* **PARTIAL, corrected: 2.**
  1. "Vite only exposes variables prefixed with `VITE_`": the source notes the prefix can be customized with `envPrefix`, so the default qualifier was missing. Edit: now "By default, Vite only exposes variables prefixed with `VITE_`...".
  2. "Vite 8 builds with Rolldown and Oxc instead of esbuild and Rollup": the source says "Vite 8 uses Rolldown and Oxc based tools instead of esbuild and Rollup" (not only for builds). Edit: reworded to match the source.
* **UNSUPPORTED: 0.**
* **NO SOURCE: 2**, both acceptable explanatory background with no numbers: "`@vitejs/plugin-react` does not handle environment variables" (the README lists no such feature) and "navigation still works without" view transitions (consistent with MDN's note that transitions still work in non-supporting browsers without the animation).

**Numbers.** Every number on the page (10 times, Node.js versions, Safari 16.4 / Chrome 111 / Firefox 128, v3.4, v6.3, major versions) is linked to its source in the same paragraph.

**Code and packages.** The page has no code blocks, so nothing was run. `npm view <name> version` on 2026-11-21: `@rspack/core` 2.3.3, `@rspack/cli` 2.3.3, `@rspack/dev-server` 2.2.2, `vite` 8.3.8, `@vitejs/plugin-react` 6.3.0, `webpack` 5.113.0, `webpack-cli` 7.3.1, `webpack-dev-server` 6.1.0, `tailwindcss` 4.3.5, `@pandacss/dev` 2.6.0, `class-variance-authority` 0.7.1, `styled-components` 6.6.0, `@emotion/styled` 11.14.1, `@emotion/react` 11.14.0, `astro` 7.4.13, `@astrojs/react` 7.1.9, `@ngtools/webpack` 22.3.0, `critters-webpack-plugin` 3.0.2. All exist and match the majors the page names.

**Verdict: PASS** (no UNSUPPORTED claims, both PARTIAL claims corrected, every number sourced, repo audit passes).

## 3. Known omissions (follow-up content, not errors)

Topics a complete set of migration playbooks could add. Each needs its own sourced entry:

* Measuring success and rolling back: baseline build times and field Core Web Vitals before the switch, and a revert path for each phase
* `rolldown-vite` as an intermediate step from Vite 7 to Vite 8; Rsbuild as a higher-level option on top of Rspack
* Other build-time styling options (CSS Modules, vanilla-extract, StyleX) and Tailwind's `prefix()` to avoid class collisions during co-existence
* Visual regression testing during a styling migration
* Proxy-based strangler details: shared cookies and auth across the two apps, canonical URLs, sitemaps and redirects
* Astro's own client router for transitions inside the Astro app

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | **18** |

D3 is 1 because the page states mechanisms (unbundled ESM, runtime style recalculation, same-origin view transitions) without explaining them in depth. D9 is 1 because the playbooks are step lists with no code or config examples. G8 (human accountability) is not met; no human has reviewed the page.
