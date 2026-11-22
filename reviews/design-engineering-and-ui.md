---
page: book/05_design_engineering_and_ui.md
verified: 2026-11-22
---

# Claim Ledger: Chapter 5, Design Engineering & UI Architecture

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead or front-end developer choosing how a React app gets its UI components. The page helps them decide between a pre-styled suite (MUI, Ant Design, Mantine), headless primitives with owned styles (shadcn/ui on Base UI, Radix or React Aria; Ark UI), and hand-built components, and how to handle layout stability and loading feedback. Thesis (unchanged from the draft): split the design system into tokens, headless behaviour primitives and owned style recipes; choose headless primitives when distinctive branding is a hard requirement and a pre-styled suite when it is not.

**History.** The AI-generated draft said headless primitives "guarantee compliance" with the WAI-ARIA authoring practices and that developers "write zero lines of complex accessibility logic" (Radix itself says labels are the developer's job and that components work "in most contexts"; the APG says assistive-technology testing is essential; WCAG conformance applies to pages, not libraries). It claimed shadcn/ui has "no third-party npm package lock-in" (shadcn/ui's FAQ says the primitive library stays a dependency), that full suites inflate bundles "with unused components" (MUI's docs say production builds tree-shake unused code), and gave bundle sizes ("~50 KB to 120 KB gzipped", "~2 KB to 8 KB per primitive") with no source. It did not mention the DTCG format, Base UI, or shadcn/ui's July 2026 switch to Base UI as its default.

---

## 1. Author pass (2026-11-22)

Sources were fetched in the same session with `curl -sL`, converted to text, and quotes matched against the extracted text. Package versions were checked with `npm view <name> version`.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | Versions: radix-ui 1.8.1, react-aria-components 1.22.1, @ark-ui/react 5.40.0, @base-ui/react 1.9.0, shadcn 4.23.0, class-variance-authority 0.7.1, tailwindcss 4.3.5, @pandacss/dev 2.6.0, style-dictionary 5.8.0, @mui/material 9.5.0, antd 6.7.1, @mantine/core 9.8.2, react 19.3.1 | `npm view <name> version` | verified; pinned on the page |
| 2 | `@base-ui-components/react` was renamed to `@base-ui/react`; repository is mui/base-ui | `npm view @base-ui-components/react deprecated` ("Package was renamed to @base-ui/react"); `npm view @base-ui/react repository.url` | verified |
| 3 | "Incorrect ARIA misrepresents visual experiences, with potentially devastating effects" | [APG: Read Me First](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) | verified (quote) |
| 4 | MUI, Ant Design and Mantine theme through a theme object or tokens | [MUI theming](https://mui.com/material-ui/customization/theming/); [Ant Design: Customize Theme](https://ant.design/docs/react/customize-theme); [Mantine theme object](https://mantine.dev/theming/theme-object/) | verified |
| 5 | Draft: full suites inflate bundles "with unused components" | [MUI: Minimizing bundle size](https://mui.com/material-ui/guides/minimizing-bundle-size/): "Modern bundlers already tree-shake unused code in production builds" | **contradicted; corrected** |
| 6 | DTCG Format Module 2025.10 is a Final Community Group Report dated 28 October 2025; "is not a W3C Standard nor is it on the W3C Standards Track" | [DTCG Format 2025.10](https://www.designtokens.org/TR/2025.10/format/); [designtokens.org](https://www.designtokens.org/) ("First stable version 2025.10") | verified (quote); added |
| 7 | "An object with a `$value` property is a token"; aliases use `{group.token}` | DTCG Format 2025.10, sections 5.1 and 6.6 | verified (quote) |
| 8 | Resolver Module 2025.10 works with tokens "in multiple contexts (such as 'light mode' and 'dark mode' color themes)" | [DTCG Resolver 2025.10](https://www.designtokens.org/TR/2025.10/resolver/) | verified (quote; source uses typographic double quotes inside) |
| 9 | Style Dictionary: "first-class support for the DTCG format" as of version 4; format 2025.10 "does not have full support yet" | [Style Dictionary: DTCG](https://styledictionary.com/info/dtcg/) | verified (quote) |
| 10 | Tailwind CSS 4.x stores design tokens in "theme variables" defined with `@theme`, which generate utility classes | [Tailwind: Theme variables](https://tailwindcss.com/docs/theme) | verified |
| 11 | Ant Design 5+ token chain: Seed, Map, Alias and Component tokens | [Ant Design: Customize Theme](https://ant.design/docs/react/customize-theme) ("Since 5.0") | verified |
| 12 | Primitive / semantic / component token layers | none | labelled on the page as the book's convention |
| 13 | Custom properties "inherit their value from their parent"; computed value is "specified value with variables substituted", so a component token declared on `:root` does not pick up a theme override deeper in the tree | [MDN: Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties); [CSS Custom Properties Level 1](https://www.w3.org/TR/css-variables-1/) | verified (quotes); the consequence is derived from the spec's computed-value rule. Added as the mechanism behind the theming claim |
| 14 | Modal dialog: Tab and Shift + Tab "do not move focus outside the dialog"; Escape closes it | [APG: Dialog (Modal) Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | verified (quote) |
| 15 | Radix "follow the WAI-ARIA authoring practices guidelines and are tested in a wide selection of modern browsers and commonly used assistive technologies"; package "is tree-shakeable" | [Radix: Accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility); [Radix: Introduction](https://www.radix-ui.com/primitives/docs/overview/introduction) | verified (quote) |
| 16 | React Aria is "style-free out of the box" with "internationalization out of the box"; published by Adobe | [React Aria](https://react-spectrum.adobe.com/react-aria/) (adobe.com domain) | verified (quote) |
| 17 | Ark UI is built on Zag.js state machines with parity across React, Solid, Vue and Svelte | [Ark UI README](https://github.com/chakra-ui/ark) (the ark-ui.com docs page returned a client-side error page to `curl`) | verified |
| 18 | Base UI is "tree-shakable" | [Base UI: Quick start](https://base-ui.com/react/overview/quick-start) | verified (quote) |
| 19 | Draft: "Developers write zero lines of complex accessibility logic. The primitives guarantee compliance with W3C WAI-ARIA authoring practices" | Radix: Accessibility ("as-is in most contexts"; "Ultimately it's up to you to provide those labels"); APG: Read Me First ("Testing assistive technology interoperability is essential before using code from this guide in production") | **contradicted; corrected** (quotes added) |
| 20 | WCAG 2.2 is a W3C Recommendation of 12 December 2024; conformance "is defined only for web pages" | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | verified (quote) |
| 21 | cva is "a tiny library for building type-safe, variant-driven class names with Tailwind CSS or any other styling approach"; cva 1.0 is in beta | [cva docs](https://cva.style/docs) ("cva@1.0 is now in beta") | verified (quote) |
| 22 | Panda CSS recipes use a built-in `cva` function | [Panda: Recipes](https://panda-css.com/docs/concepts/recipes) | verified |
| 23 | shadcn/ui: "This is not a component library. It is how you build your component library."; "The top layer of your component code is open for modification" | [shadcn/ui: Introduction](https://ui.shadcn.com/docs) | verified (quote) |
| 24 | Base UI became shadcn/ui's default in July 2026; Radix "is still fully supported"; `shadcn init -b radix` | [changelog: Base UI as the Default](https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default) (dated July 2026) | verified (quote); added |
| 25 | React Aria became a shadcn/ui component base in July 2026 (`--base aria`) | [changelog: React Aria](https://ui.shadcn.com/docs/changelog/2026-07-react-aria) | verified; added |
| 26 | Draft: shadcn/ui has "no third-party npm package lock-in" | shadcn/ui FAQ: "the core of your app can receive fixes by updating your dependencies, for instance, @base-ui/react" | **contradicted; corrected** |
| 27 | Draft matrix: headless accessibility "Highest (Audited WAI-ARIA primitives)" | none found for "audited" | replaced with Radix's documented "tested" claim |
| 28 | Draft matrix: "~50 KB to 120 KB gzipped" (suites) and "~2 KB to 8 KB per primitive" | none found | **removed**; row rewritten qualitatively with MUI, Radix and Base UI tree-shaking statements |
| 29 | Good CLS is "0.1 or less" at "the 75th percentile of page loads, segmented across mobile and desktop devices" | [web.dev: CLS](https://web.dev/articles/cls) | verified (quote); added |
| 30 | Shifts "within 500 milliseconds of user input" get `hadRecentInput` and can be excluded | web.dev: CLS | verified (quote); added; narrows the draft's "Never render content that pushes existing DOM nodes downward" to unexpected shifts |
| 31 | "Always include width and height size attributes ... Alternatively, reserve the required space with CSS aspect-ratio"; ads, embeds and iframes without dimensions cause CLS | [web.dev: Optimize CLS](https://web.dev/articles/optimize-cls) | verified (quote) |
| 32 | `aspect-ratio` Baseline widely available since September 2021 | [MDN: aspect-ratio](https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio) | verified (quote) |
| 33 | "Composited animations using translate can't impact other elements, and so don't count toward CLS" | web.dev: Optimize CLS | verified (quote); added |
| 34 | Draft: "Full-screen loading spinners create high cognitive friction and make wait times feel longer" | [NN/g: Skeleton Screens 101](https://www.nngroup.com/articles/skeleton-screens/) | not supported as worded; replaced with NN/g's guidance: skeletons for full-page loads reduce perceived loading time and suit waits under 10 seconds; spinners 2 to 10 seconds; progress bars "strongly recommended" above 10 seconds; under 1 second, skeletons or spinners "aren't necessary" |
| 35 | React 19 introduces `useOptimistic`; its reference shows "the UI automatically rolls back" when a delete fails | [react.dev: useOptimistic](https://react.dev/reference/react/useOptimistic); [React 19 release post](https://react.dev/blog/2024/12/05/react-19) | verified (quote); added |
| 36 | Book judgments: suite friction starts where the theme stops; tokens are overkill for one brand, one theme, one platform; headless is wrong without design capacity; copy-in code drifts across teams; optimistic UI is wrong for payments and irreversible actions; decision-tree overrides | none | labelled on the page as the book's judgment or reasoning |
| 37 | Draft: "subtle focus traps break keyboard navigation" | APG: Dialog (Modal) Pattern | removed: the APG requires modal dialogs to contain focus, so "focus trap" as a defect was imprecise; replaced with the APG's warning about incorrect ARIA |
| 38 | Draft epigraph and "Modern frontend architecture resolves this tension" | none | rewritten: rule-of-three epigraph and unsourced generalisation replaced with a specific statement of the chapter's approach |
| 39 | References: APG "(2024)" and web.dev CLS had no URL; *Refactoring UI* "(2018)" | [APG](https://www.w3.org/WAI/ARIA/apg/); [web.dev: CLS](https://web.dev/articles/cls); [refactoringui.com](https://www.refactoringui.com/) (names Adam Wathan and Steve Schoger) | URLs added; years dropped (APG is a living document; the *Refactoring UI* year was not confirmed on the fetched page). The `library/reading_list.md` link for Godbolt stays |

**Headings.** "The Core Dilemma", "The Three-Tier Design Architecture", "Comparative Matrix" and "Decision Playbook" were replaced with headings that state what each section decides. The ASCII diagrams now have a `text` language tag and a prose description. A "Wrong choice when" row was added to the matrix, and each tier has a "when this is the wrong choice" paragraph labelled as the book's reasoning.

**Code.** The page has one CSS block, labelled as a fragment. There is no runnable JavaScript, so nothing was run with `node`. The CSS behaviour it illustrates (row 13) follows from the CSS Custom Properties computed-value rule; it was not executed in a browser in this session.

**Research-note links.** The draft linked only to `library/reading_list.md`, which stays; no other `library/` links were present.

**Audit.** `python pipelines/scripts/audit_repo_standards.py` passed, with no G1 warning for this page.

## 2. Independent verifier pass (2026-11-22)

A separate agent that did not write the page or section 1 extracted the claims from the page itself, fetched every cited URL with `curl -sL`, stripped the HTML and matched each quote with a script that normalises only whitespace and typographic quotes.

**Claims checked:** 61 (13 pinned versions, 1 package rename, 40 sourced quotes or paraphrases, 7 statements labelled as the book's judgment or reasoning).

**Versions.** `npm view <name> version` returned exactly the 13 versions pinned on the page. `npm view @base-ui-components/react deprecated` returned "Package was renamed to @base-ui/react"; the repository is `mui/base-ui`. The cva 1.0 beta is published as `cva@1.0.0-beta.12` (`class-variance-authority` latest stays 0.7.1), consistent with the cva docs banner "cva@1.0 is now in beta".

**Points of particular attention, all SUPPORTED as worded:** DTCG Format and Resolver 2025.10 are each a "Final Community Group Report" dated 28 October 2025 that "is not a W3C Standard nor is it on the W3C Standards Track" (not a W3C Standard); Style Dictionary says 2025.10 "does not have full support yet ... This is a work in progress in v5"; Base UI package `@base-ui/react`; shadcn/ui FAQ quote (present verbatim in the Introduction page's FAQ accordion, which continues "or input-otp"); July 2026 changelog ("New projects now use Base UI by default. Radix is still fully supported", `shadcn init -b radix`; React Aria via `--base aria`); Radix "tested in ... commonly used assistive technologies", "as-is in most contexts", "up to you to provide those labels"; APG "Incorrect ARIA ..." (said of screen reader users' non-visual experience) and "Testing assistive technology interoperability is essential ..."; WCAG 2.2 Recommendation of 12 December 2024, "Conformance is defined only for web pages"; NN/g spinners 2 to 10 s, skeletons under 10 s and for full-page loads, progress bars "strongly recommended" above 10 s, under 1 s "aren't necessary"; MUI "Modern bundlers already tree-shake unused code in production builds"; web.dev CLS "0.1 or less" at the 75th percentile and the 500 ms `hadRecentInput` rule; Optimize CLS quotes; MDN `aspect-ratio` Baseline since September 2021; react.dev `useOptimistic` (docs header react@19.3; React 19 release post: "In React 19, we're adding a new hook").

**Verdicts:** 51 SUPPORTED, 7 labelled judgments (acceptable, no numbers), 3 PARTIAL (all corrected below), 0 UNSUPPORTED, 0 unsourced numbers.

**Edits made:**

1. *PARTIAL, Ant Design token chain.* The page called Seed, Map, Alias and Component Token one chain. The source describes a "three-layer derivation" (Map from Seed, Alias from Map) and says each component has its own Component Token "in addition to Design Token", not derived from Seed Token by default. Reworded to match.
2. *PARTIAL, CSS fragment reasoning.* The claim that a component token declared on `:root` resolves to `blue-500` holds only when `[data-theme="dark"]` is on an element below `:root`. If the attribute is on `<html>` itself, both rules match the root element, `[data-theme="dark"]` wins on source order at equal specificity, and the `:root` declaration resolves to `blue-400`. Reworded to state that condition.
3. *PARTIAL, accordion example.* "Does not hurt CLS" stretched the source, which says shifts within 500 ms of discrete input "can be excluded". Reworded to "expands within 500 milliseconds of a click can be excluded this way".

**Code checks.** No JavaScript on the page. The CSS fragment was rendered in headless Chrome (`--dump-dom`, `getComputedStyle`): the page's pattern gives `rgb(96, 165, 250)` (blue-400) inside a `[data-theme="dark"]` div; the anti-pattern (component token on `:root`) gives `rgb(59, 130, 246)` (blue-500) inside the dark div, as the page says; with `data-theme="dark"` on `<html>` the anti-pattern gives blue-400, which is why edit 2 adds the condition. This follows the spec: custom properties are "Inherited: yes" with computed value "specified value with variables substituted".

**Ledger correction (section 1, row 7).** The curly-brace alias syntax is DTCG Format section 7.1.1, not 6.6; the claim itself is supported.

**Verdict: PASS.**

## 3. Known omissions (follow-up content, not errors)

Each needs its own sourced, verified entry before it is published:

* View Transitions for UI animation (`document.startViewTransition()` is Baseline 2025, newly available since October 2025, per [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Document/startViewTransition)) and `prefers-reduced-motion`
* WCAG 2.2 criteria that design systems own: 2.1.2 No Keyboard Trap, 2.4.7 Focus Visible, 2.4.11 Focus Not Obscured (Minimum), 2.5.8 Target Size (Minimum), and 1.4.3 contrast checks on token pairs
* Web fonts as a CLS cause (listed in web.dev's Optimize CLS)
* Syncing tokens between design tools and code (DTCG adopters such as Figma and Tokens Studio are listed on designtokens.org)
* Testing primitives in your own app: automated checks plus manual screen-reader passes
* Non-React options (Ark UI's Vue, Solid and Svelte bindings; Web Components)
* Right-to-left layouts (shadcn/ui and Base UI both document RTL support)

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 1 | **18** |

D9 is 1: the page has one illustrative CSS fragment and no worked scenario. D10 is 1: terms such as "portal" and "headless" are used without definition. All gates pass except G8 (human accountability), which the `agent-verified` status would disclose if granted.
