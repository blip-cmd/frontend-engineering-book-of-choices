---
page: book/06_styling_and_presentation.md
verified: 2026-11-22
---

# Claim Ledger: Chapter 6, Styling and Presentation

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead choosing how a React application writes and ships its CSS. The page helps them decide whether styles are generated at build time (Tailwind CSS, CSS Modules, StyleX, Panda CSS, vanilla-extract) or at runtime (styled-components, Emotion), and how to handle per-instance dynamic values. Thesis (unchanged from the draft): runtime style injection has a cost that build-time approaches avoid, so new projects should generate CSS at build time and pass dynamic values through CSS custom properties. The recommendation is kept; it now rests on react.dev and the styled-components maintainer's own advice instead of unsourced numbers.

**History.** The AI-generated draft gave an unsourced Tailwind size range ("12 KB to 25 KB gzipped"), an unsourced runtime cost ("15-40 ms per heavy render"), "Exactly 0 ms" for all build-time options (StyleX and Panda both document a small runtime), called runtime CSS-in-JS "Incompatible with React Server Components" (styled-components added RSC support in 6.3.0, January 2026), described vanilla-extract as producing atomic class names (it does not, except through Sprinkles), claimed custom properties are recalculated "on the compositor thread" (no source supports this; removed), shipped a dynamic-style example whose class never read the custom property it set, linked an unverified library research note, and cited a Meta article title ("StyleX: A Stylistic Evolution at Meta", 2023) that could not be found.

---

## 1. Author pass (2026-11-22)

Sources were fetched in this session with `curl` (text extracted and searched) and with WebSearch to locate URLs. Package versions were checked with `npm view <name> version`. Quotes were matched against the extracted page text, allowing for typographic apostrophes.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | React lists three approaches (compiled CSS files, inline styles, runtime `<style>` injection); "We don't recommend runtime `<style>` tag injection"; it "forces the browser to recalculate the styles a lot more often" and "can be very slow if it happens at the wrong time in the React lifecycle"; first problem "not solvable"; recommends "CSS files for static styles, inline styles for dynamic styles" | [react.dev: useInsertionEffect](https://react.dev/reference/react/useInsertionEffect) | verified (quote); replaces draft's "stalls the browser's CSSOM parser, blocks the main thread, and breaks streaming HTML pipelines" |
| 2 | Next.js warns CSS-in-JS with Server Components and streaming needs library support for concurrent rendering; Emotion listed as "working on support"; pandacss, styled-components, stylex, vanilla-extract listed as supported in Client Components; docs version 16.4.6 | [Next.js: CSS-in-JS](https://nextjs.org/docs/app/guides/css-in-js) | verified (quote) |
| 3 | "Edge Workers" break runtime CSS-in-JS | none found | removed |
| 4 | Tailwind "treats all of your source files as plain text" and generates CSS only for tokens that map to utilities | [Tailwind: Detecting classes](https://tailwindcss.com/docs/detecting-classes-in-source-files) | verified (quote); draft's "Tailwind oxide compiler" name removed (not used on the cited pages) |
| 5 | Tailwind cannot understand "string concatenation or interpolation"; use complete class names | Tailwind: Detecting classes (`#dynamic-class-names` anchor present) | verified (quote); added as "wrong choice when" |
| 6 | Tailwind 4.0 released January 22, 2025; CSS-first configuration instead of `tailwind.config.js`; automatic content detection; built on cascade layers, `@property`, `color-mix()` | [Tailwind v4.0 announcement](https://tailwindcss.com/blog/tailwindcss-v4); `npm view tailwindcss time` (4.0.0 published 2025-01-21 UTC) | verified (quote) |
| 7 | tailwindcss 4.3.5 | `npm view tailwindcss version` | verified |
| 8 | Draft: CSS "flattens to a constant ceiling (typically 12 KB to 25 KB gzipped)" | none found | removed; replaced with Tailwind's vendor claim (row 9) and labelled reasoning |
| 9 | "most Tailwind projects ship less than 10kB of CSS to the client" | [tailwindcss.com](https://tailwindcss.com/) | verified (quote); labelled as vendor statement with no method |
| 10 | "A CSS Module is a CSS file where all class names and animation names are scoped locally by default" | [CSS Modules spec](https://github.com/css-modules/css-modules) | verified (quote); draft's fixed name format `.button_a7b9x` generalised, since the format is bundler-specific |
| 11 | Next.js supports `.module.css` imports in any component in the `app` directory; Tailwind setup documented | [Next.js: CSS](https://nextjs.org/docs/app/getting-started/css) | verified (quote) |
| 12 | CSS nesting Baseline widely available since December 2023 | [MDN: nesting selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/Nesting_selector) | verified (Baseline banner) |
| 13 | `container-type` Baseline widely available since February 2023 | [MDN: container-type](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/container-type) | verified (Baseline banner) |
| 14 | Subgrid Baseline widely available since September 2023 | [MDN: Subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Subgrid) | verified (Baseline banner) |
| 15 | `color-mix()` Baseline widely available since May 2023 | [MDN: color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/color-mix) | verified (Baseline banner); replaces draft's vague "modern color functions" |
| 16 | Custom properties Baseline widely available since April 2017; they "inherit their value from their parent" | [MDN: --*](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/--*); [MDN: Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties) | verified (Baseline banner; quote) |
| 17 | Draft: CSS Modules "100% native CSS syntax with zero runtime JavaScript overhead"; "bundle size grows linearly" | CSS Modules spec | reworded: "ordinary CSS", no styling JavaScript beyond the class-name map; growth claim labelled as book's reasoning |
| 18 | StyleX: "collision-free atomic CSS", "No runtime style injection", "Tiny and fast runtime for merging class names", "CSS size plateaus as the codebase grows" | [StyleX: Introduction](https://stylexjs.com/docs/learn/) | verified (quote); **corrects** draft's "Exactly 0 ms" runtime |
| 19 | StyleX allows only statically resolvable values plus arrow functions for dynamic styles, compiled to CSS variables set at runtime | [StyleX: Defining styles](https://stylexjs.com/docs/learn/styling-ui/defining-styles/) | verified (quote) |
| 20 | StyleX has a Vite + React Server Components setup | [StyleX: Vite RSC](https://stylexjs.com/docs/learn/installation/vite/vite-rsc) | verified |
| 21 | Meta: "Atomic classes reduced CSS size by 80%"; StyleX open sourced end of 2023; author Melissa Liu, November 2025 | [Engineering at Meta](https://engineering.fb.com/2025/11/11/web/stylex-a-styling-library-for-css-at-scale/) | verified (quote); labelled as vendor figure without baseline; replaces draft's unfindable 2023 title |
| 22 | Panda: "You write styles in TypeScript, and Panda generates plain atomic CSS at build time"; without transforms "a small runtime joins the class names"; "Server components get the same result with no transform" | [Panda: Why Panda](https://panda-css.com/docs/overview/getting-started) | verified (quote) |
| 23 | Panda: "Using a value that is not statically analyzable at build-time will not work"; recommends recipes, CSS variables or `data-*` attributes | [Panda: Dynamic styling](https://panda-css.com/docs/guides/dynamic-styling) | verified (quote); added as "wrong choice when" |
| 24 | vanilla-extract: `.css.ts` files; "All styles generated at build time"; type-safe token contracts; class names locally scoped (e.g. `.app_myStyle__sznanj0`) | [vanilla-extract](https://vanilla-extract.style/); [Styling docs](https://vanilla-extract.style/documentation/styling/) | verified (quote); **corrects** draft's "atomic class names" for all three libraries |
| 25 | Sprinkles is "A zero-runtime atomic CSS framework for vanilla-extract" | [Sprinkles](https://vanilla-extract.style/documentation/packages/sprinkles/) | verified (quote) |
| 26 | Versions: @stylexjs/stylex 0.19.2, @pandacss/dev 2.6.0, @vanilla-extract/css 1.21.3, styled-components 6.6.0, @emotion/react 11.14.0, react 19.3.1 | `npm view <name> version` | verified |
| 27 | styled-components "in 'maintenance mode'" (March 17, 2025, Evan Jacobs); "will continue to be available with occasional bugfixes and misc improvements"; "For new projects, I would not recommend adopting styled-components or most other css-in-js solutions" | [OpenCollective: Thank you](https://opencollective.com/styled-components/updates/thank-you) | verified (quote); maintenance mode kept distinct from deprecation; replaces draft's "Obsolete for greenfield architectures" |
| 28 | styled-components 6.3.0 (January 10, 2026) added RSC support: inline `<style>` tags "that React 19 automatically hoists and deduplicates"; `ThemeProvider` a no-op in RSC; custom properties "can be set via inline `style`" | [6.3.0 release notes](https://github.com/styled-components/styled-components/releases/tag/styled-components%406.3.0); `npm view styled-components time` | verified (quote); **corrects** draft's "Incompatible with React Server Components" |
| 29 | March 27, 2026: maintenance-mode post "still true"; "now has a path forward in modern React"; "the only remaining maintainer" | [OpenCollective: A Whole New World](https://opencollective.com/styled-components/updates/a-whole-new-world) | verified (quote) |
| 30 | Emotion RSC support issue open since January 2023 | [emotion-js/emotion#2978](https://github.com/emotion-js/emotion/issues/2978) (GitHub API, state "open", created 2023-01-30) | verified |
| 31 | Draft: runtime CSS-in-JS "15-40 ms per heavy render"; "measurable CPU jank on mobile devices" | none found | removed; replaced by React's qualitative statement (row 1) |
| 32 | Transient props: `$` prefix keeps a prop from reaching the DOM | [styled-components API](https://styled-components.com/docs/api) | verified (quote); fragment changed from `width` to `$width` and labelled as fragment |
| 33 | Draft: custom property change is recalculated "instantly on the compositor thread" by "native C++ styling engine" | none found | removed; replaced by MDN inheritance fact and labelled reasoning |
| 34 | Draft example set `--box-width` but no class read it | Tailwind 4.3.5 CLI run | **corrected**: added `w-(--box-width)`; the CLI emitted `.w-\(--box-width\) { width: var(--box-width); }` |
| 35 | `Box` example type-checks and renders | TypeScript 7.0.2 `--strict`; React 19 `renderToString` on Node 24.18.1 | verified (run); output `<div class="h-10 w-(--box-width) rounded bg-blue-500" style="--box-width:240px"></div>`; added `import type { CSSProperties }` so it compiles without the global `React` namespace |
| 36 | shadcn/ui components updated "for Tailwind v4 and React 19" | [shadcn/ui: Tailwind v4](https://ui.shadcn.com/docs/tailwind-v4) | verified (quote); draft's "massive community" removed (no source) |
| 37 | Adam Wathan, "CSS Utility Classes and 'Separation of Concerns'", August 7, 2017 | [adamwathan.me](https://adamwathan.me/css-utility-classes-and-separation-of-concerns/) | verified; URL added |
| 38 | Link to `library/tools_and_frameworks/styling_paradigms.md` | n/a | removed (unverified AI research note) |
| 39 | Global stylesheets let one change restyle unrelated pages; atomic output tracks distinct utilities; module output tracks authored rules; inline custom property avoids adding rules to the cascade; runtime libraries generate a rule per distinct value; keep working runtime CSS-in-JS codebases | none | explanatory background, labelled on the page as the book's reasoning |

## 2. Independent verifier pass (2026-11-22)

A separate agent that did not write the page extracted 67 claims from it independently (quotes, dates, versions, Baseline statuses, API behaviour and code output) and checked each against its cited source, fetched in this session with `curl -sL` (HTML stripped to text, quotes searched with typographic quotes normalised). Versions were checked with `npm view <name> version` and publish dates with `npm view <name> time`; the Emotion issue state with the GitHub API.

**Verdict: PASS.** 0 UNSUPPORTED remain; 6 PARTIAL claims were corrected; every number on the page has a source; `python pipelines/scripts/audit_repo_standards.py` passes (its one warning is on another page).

Spot results for the items flagged for special attention:

* styled-components 6.3.0: release page says "released this 10 Jan"; `npm view styled-components time` gives 6.3.0 at 2026-01-10. RSC quotes ("emit inline `<style>` tags that React 19 automatically hoists and deduplicates", `ThemeProvider` a no-op in RSC, custom properties "can be set via inline `style`" under "RSC best practices") verbatim. SUPPORTED.
* Maintenance mode: "Thank you", published March 17, 2025 by Evan Jacobs; "as a project is in \"maintenance mode\"", "will continue to be available with occasional bugfixes and misc improvements to support the existing user base", "For new projects, I would not recommend adopting styled-components or most other css-in-js solutions" verbatim. "A Whole New World", published March 27, 2026: "still true", "now has a path forward in modern React", "the only remaining maintainer" verbatim. SUPPORTED.
* Emotion: issue #2978 "Emotion in React Server Components?", state open, created 2023-01-30, not closed on 2026-11-22; Next.js 16.4.6 CSS-in-JS docs list emotion under "currently working on support". SUPPORTED.
* StyleX runtime ("No runtime style injection", "Tiny and fast runtime for merging class names") and Panda runtime ("a small runtime joins the class names" without transforms; "Server components get the same result with no transform") verbatim. SUPPORTED.
* Vendor figures: tailwindcss.com "most Tailwind projects ship less than 10kB of CSS to the client" and Meta "Atomic classes reduced CSS size by 80%" verbatim; neither states a method, and the Meta post's only implied baseline is the earlier `cx` system, so "no baseline or method" stands. Meta post "POSTED ON NOVEMBER 11, 2025", by Melissa Liu. SUPPORTED.
* Versions, all matching the page: tailwindcss 4.3.5, @tailwindcss/cli 4.3.5, @stylexjs/stylex 0.19.2, @pandacss/dev 2.6.0, @vanilla-extract/css 1.21.3, styled-components 6.6.0, @emotion/react 11.14.0, react 19.3.1, typescript 7.0.2; Next.js docs show "Latest v16.4.6". Tailwind v4.0 blog dated January 22, 2025 (npm 4.0.0 at 2025-01-21 UTC).

Edits made (all rewordings to match the source; nothing added):

| # | Where | Verdict | Edit |
| :--- | :--- | :--- | :--- |
| V1 | Section 1, Next.js warning | PARTIAL: "only works when the library supports React's concurrent rendering" stretched the source | Replaced with the exact quote: "requires library authors to support the latest version of React, including concurrent rendering" |
| V2 | Section 2B, Baseline dates (nesting, `container-type`, subgrid, `color-mix()`) | PARTIAL: MDN's date is when each feature became "available across browsers" (newly available), not the date it became widely available | Reworded: MDN marks each Baseline widely available and gives the date since which it has been available across browsers |
| V3 | Section 4, custom properties Baseline | PARTIAL: same date misreading as V2 | Reworded to "Baseline widely available, available across browsers since April 2017" |
| V4 | Section 2B, "browsers released before the Baseline dates above" | PARTIAL: followed from V2 | Changed to "before the dates above" |
| V5 | Section 3, RSC row for Tailwind and CSS Modules | PARTIAL: the Next.js CSS page never mentions Server Components; it shows the Tailwind stylesheet imported in the root layout and CSS Modules imported "into any component inside the app directory" | Cells now say exactly that, after "Yes" |
| V6 | Section 4, React recommendation; Section 5 tree, shadcn/ui | PARTIAL: React's recommendation is addressed to CSS-in-JS users ("If you use CSS-in-JS, we recommend a combination of..."); shadcn says components are "updated for", not "built for", Tailwind v4 | Added the source's own qualifier "For CSS-in-JS users ... a combination of"; "built for" changed to "updated for" |

Claims accepted as NO SOURCE explanatory background (no numbers): runtime libraries hash evaluated styles into a class name; bundlers rewrite CSS Module classes to unique names with a name map; all other cells and sentences labelled on the page as the book's reasoning.

Code checks (temp folder outside the repo, Node 24.18.1):

* `Box` component: `tsc` 7.0.2 `--strict --jsx react-jsx` passes; `renderToString` with react-dom 19.3.1 prints `<div class="h-10 w-(--box-width) rounded bg-blue-500" style="--box-width:240px"></div>` (also checked `width={0}`, giving `--box-width:0px`); `@tailwindcss/cli` 4.3.5 emits `.w-\(--box-width\) { width: var(--box-width); }`. Matches the page.
* styled-components fragment (with the stated import, styled-components 6.6.0): type-checks under `--strict` with `--skipLibCheck` (without it, TypeScript 7.0.2 reports an error inside styled-components' own `ServerStyleSheet.d.ts`, not in the fragment); rendering `$width={100}` and `$width={200}` gives two different generated class names and no `$width` attribute in the HTML, consistent with the page's description.

## 3. Known omissions (follow-up content, not errors)

Topics a complete styling chapter could add, each needing its own sourced entry:

* Native scoping and ordering as an alternative to tooling: `@layer` (Baseline widely available since March 2022 per MDN), `@scope` (Baseline 2026, newly available since March 2026 per MDN) and `:has()` (Baseline widely available since December 2023 per MDN) were checked in this pass but are not discussed on the page.
* Sass and plain global CSS with a naming convention (BEM), which Next.js still documents.
* Measured comparisons of runtime CSS-in-JS cost (no primary benchmark with stated tool and versions was found in this pass).
* Migration guidance from styled-components or Emotion to a build-time approach.
* Other compile-time libraries Next.js lists (Linaria, Kuma UI, Pigment CSS) and component libraries' styling engines (MUI, Chakra).
* Design tokens across platforms and theming (dark mode) with custom properties.

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | **18** |

D3 is 1 because the style-recalculation mechanism rests on React's statement and the book's reasoning, not a rendering-engine source. D9 is 1 because the only examples are a short fragment and one small tested component. G8 (human accountability) is not met; the page is a draft until the verifier pass.
