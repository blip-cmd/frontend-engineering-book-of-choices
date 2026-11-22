---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: radix-ui 1.8.1, react-aria-components 1.22.1, @ark-ui/react 5.40.0, @base-ui/react 1.9.0, shadcn 4.23.0 (changelog July 2026), class-variance-authority 0.7.1, tailwindcss 4.3.5, @pandacss/dev 2.6.0, style-dictionary 5.8.0, @mui/material 9.5.0, antd 6.7.1, @mantine/core 9.8.2, react 19.3.1; DTCG Format and Resolver 2025.10; WAI-ARIA APG; WCAG 2.2; CSS Custom Properties Level 1; web.dev CLS and Optimize CLS; NN/g Skeleton Screens 101
review_by: 2027-05
reviewers:
ledger: reviews/design-engineering-and-ui.md
---

# Chapter 5: Design Engineering & UI Architecture: Tokens, Primitives, and Performance

> Design engineering decides where each design decision lives in code: in a token file, in a behaviour primitive tested against assistive technology, or in style code your team owns.

---

## 1. Decide Who Owns Behaviour and Who Owns Styling

This chapter is for a tech lead or front-end developer choosing how a React app gets its components. Versions checked with `npm view` on 2026-11-22: radix-ui 1.8.1, react-aria-components 1.22.1, @ark-ui/react 5.40.0, @base-ui/react 1.9.0, shadcn (CLI) 4.23.0, class-variance-authority 0.7.1, tailwindcss 4.3.5, @pandacss/dev 2.6.0, style-dictionary 5.8.0, @mui/material 9.5.0, antd 6.7.1, @mantine/core 9.8.2, react 19.3.1.

Two failure modes frame the choice:

* **Building every widget by hand.** Each custom menu, combobox or dialog has to reimplement the keyboard behaviour and ARIA semantics described in the W3C ARIA Authoring Practices Guide (APG). The APG warns that "Incorrect ARIA misrepresents visual experiences, with potentially devastating effects" for screen reader users ([APG: Read Me First](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/)).
* **Fighting a pre-styled suite.** MUI, Ant Design and Mantine all theme through a token or theme object ([MUI theming](https://mui.com/material-ui/customization/theming/); [Ant Design: Customize Theme](https://ant.design/docs/react/customize-theme); [Mantine theme object](https://mantine.dev/theming/theme-object/)). The book's judgment: the friction starts when a brand needs a component structure or interaction the theme does not expose as a parameter, and the team ends up overriding the suite's own styles.

The approach this chapter describes splits the work three ways: design decisions go into tokens, keyboard and ARIA behaviour comes from a headless primitive library, and visual styling lives in code the team owns.

---

## 2. Split the Design System into Tokens, Behaviour Primitives and Owned Styles

```text
┌────────────────────────────────────────────────────────┐
│  Tier 1: Design Tokens (DTCG JSON / CSS custom props)  │
│  - Colors, typography scale, spacing, border radii     │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  Tier 2: Headless Primitives (Radix / React Aria /     │
│          Ark UI / Base UI)                             │
│  - Keyboard behaviour, focus, ARIA roles, portals      │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  Tier 3: Owned Recipes (Tailwind / Panda / cva)        │
│  - Visual styles, variants, animations, hover states   │
└────────────────────────────────────────────────────────┘
```

The diagram shows three layers stacked top to bottom. Tokens feed values into the primitives' styling; primitives supply behaviour; recipes apply the visual design to the primitives. Each layer can change without editing the others.

### Tier 1: Design Tokens (DTCG Format 2025.10)

* **Mechanism:** A token is a named design value stored in a platform-neutral file and compiled to CSS custom properties or other platform formats. The W3C Design Tokens Community Group (DTCG) published the [Design Tokens Format Module 2025.10](https://www.designtokens.org/TR/2025.10/format/) as a Final Community Group Report on 28 October 2025; it "is not a W3C Standard nor is it on the W3C Standards Track". In that format, "An object with a `$value` property is a token", and one token references another with curly braces (`{group.token}`). A companion [Resolver Module 2025.10](https://www.designtokens.org/TR/2025.10/resolver/) describes how to work with tokens "in multiple contexts (such as 'light mode' and 'dark mode' color themes)".
* **Tooling:** Style Dictionary has had "first-class support for the DTCG format" since version 4, but its docs state that format 2025.10 "does not have full support yet" in Style Dictionary 5.x ([Style Dictionary: DTCG](https://styledictionary.com/info/dtcg/)). In Tailwind CSS 4.x, design tokens live in "theme variables", defined with the `@theme` directive, which also generate the utility classes ([Tailwind: Theme variables](https://tailwindcss.com/docs/theme)).
* **Token layers (the book's convention):**
  * *Primitive tokens:* raw palette values (`blue-500: #3b82f6`). Components do not reference them directly.
  * *Semantic tokens:* intent-based aliases (`color-bg-interactive` points at `blue-500`).
  * *Component tokens:* element-specific aliases (`button-primary-bg` points at `color-bg-interactive`).

  Ant Design 5+ uses a similar idea under different names: a three-layer derivation in which Map Tokens are derived from Seed Tokens and Alias Tokens from Map Tokens, plus a Component Token for each component ([Ant Design: Customize Theme](https://ant.design/docs/react/customize-theme)).
* **The benefit:** A theme or brand swap replaces the semantic layer, and components pick up the change without edits.

The CSS below is a fragment showing that swap, and the one cascade rule that breaks it:

```css
/* Fragment: theme switching through the semantic layer */
:root {
  --blue-400: #60a5fa;
  --blue-500: #3b82f6;
  --color-bg-interactive: var(--blue-500);   /* semantic token */
}
[data-theme="dark"] {
  --color-bg-interactive: var(--blue-400);
}
/* Declare component tokens on the component, not on :root */
.button-primary {
  --button-primary-bg: var(--color-bg-interactive);
  background: var(--button-primary-bg);
}
```

Custom properties "inherit their value from their parent" ([MDN: Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties)), and their computed value is the "specified value with variables substituted" ([CSS Custom Properties Level 1](https://www.w3.org/TR/css-variables-1/)). If `--button-primary-bg` were declared on `:root`, its `var()` would be resolved once at `:root`. When `[data-theme="dark"]` sits on an element below `:root`, that resolves to `blue-500`, and the button inside the dark element would inherit that resolved colour, so the dark theme would not reach it.

**When tokens are the wrong investment (the book's reasoning):** a single-brand product with no dark mode and one platform gets little from a three-layer token build; plain CSS custom properties or Tailwind theme variables are enough until a second theme or platform appears.

### Tier 2: Headless Primitives (Radix, React Aria, Ark UI, Base UI)

* **Mechanism:** Unstyled components that implement keyboard handling, focus management and ARIA state attributes (`aria-expanded`, `aria-haspopup`) for patterns such as dialog, menu and combobox. For a modal dialog, for example, the APG specifies that Tab and Shift + Tab "do not move focus outside the dialog" and Escape closes it ([APG: Dialog (Modal) Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)).
* **Options:**
  * **Radix Primitives** (`radix-ui` 1.8.x): "follow the WAI-ARIA authoring practices guidelines and are tested in a wide selection of modern browsers and commonly used assistive technologies"; the package "is tree-shakeable" ([Radix: Accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility); [Radix: Introduction](https://www.radix-ui.com/primitives/docs/overview/introduction)).
  * **React Aria Components** (`react-aria-components` 1.22.x, from Adobe): "style-free out of the box" with "internationalization out of the box" ([React Aria](https://react-spectrum.adobe.com/react-aria/)).
  * **Ark UI** (`@ark-ui/react` 5.x): built on Zag.js state machines, with the same components for React, Solid, Vue and Svelte ([Ark UI README](https://github.com/chakra-ui/ark)).
  * **Base UI** (`@base-ui/react` 1.9.x, maintained in the [mui/base-ui](https://github.com/mui/base-ui) repository): the package was renamed from `@base-ui-components/react` (per its npm deprecation notice) and is "tree-shakable" ([Base UI: Quick start](https://base-ui.com/react/overview/quick-start)).
* **What primitives do not do:** They do not make a page conformant. Radix says users "should be able to use our components as-is in most contexts" (most, not all), and accessible labels remain the developer's job: "Ultimately it's up to you to provide those labels" ([Radix: Accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility)). The APG states that "Testing assistive technology interoperability is essential before using code from this guide in production" ([APG: Read Me First](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/)), and WCAG 2.2 conformance "is defined only for web pages", not for component libraries ([WCAG 2.2, W3C Recommendation 12 December 2024](https://www.w3.org/TR/WCAG22/)).

**When headless primitives are the wrong choice (the book's reasoning):** a team with no designer and no time to style every state (hover, focus, disabled, error) ends up rebuilding a pre-styled suite one component at a time.

### Tier 3: Owned Recipes (shadcn/ui, cva, Panda Recipes)

* **Mechanism:** A recipe maps variant names (size, intent) to classes. `class-variance-authority` (cva 0.7.x; 1.0 is in beta) is "a tiny library for building type-safe, variant-driven class names with Tailwind CSS or any other styling approach" ([cva docs](https://cva.style/docs)). Panda CSS ships the same idea as a built-in `cva` recipe function ([Panda: Recipes](https://panda-css.com/docs/concepts/recipes)).
* **shadcn/ui:** "This is not a component library. It is how you build your component library." Its CLI copies component source into your repository, and "The top layer of your component code is open for modification" ([shadcn/ui: Introduction](https://ui.shadcn.com/docs)). Projects initialised since July 2026 default to Base UI, while Radix "is still fully supported" (`shadcn init -b radix`) ([changelog: Base UI as the Default](https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default)); React Aria became a third base the same month ([changelog: React Aria](https://ui.shadcn.com/docs/changelog/2026-07-react-aria)).
* **What ownership does not remove:** the copied code still imports a primitive library from npm. shadcn/ui's own FAQ says "the core of your app can receive fixes by updating your dependencies, for instance, @base-ui/react" ([shadcn/ui: Introduction](https://ui.shadcn.com/docs)). Only the styled top layer is yours.

**When copy-in code is the wrong choice (the book's reasoning):** if several product teams need the same components, copies in each repository drift apart, and upstream fixes to the styled layer arrive only when someone merges them by hand. A shared, versioned internal package is easier to keep consistent.

---

## 3. Compare a Pre-Styled Suite, Headless Primitives and Hand-Built Components

Ratings below are the book's judgment unless a source is linked.

| Evaluation | Pre-styled suite (MUI 9.x / Ant Design 6.x / Mantine 9.x) | Headless + owned styles (shadcn/ui on Base UI, Radix or React Aria) | Hand-built (HTML/CSS/JS) |
| :--- | :--- | :--- | :--- |
| **Time to first screen** | Fastest: components arrive styled | Fast: CLI copies styled defaults to adjust | Slow: every widget written from scratch |
| **Brand differentiation** | Within the theme's parameters (MUI theme object, Ant Design tokens) | Full: you edit the component source | Full |
| **Accessibility starting point** | Built into each component; check its docs | Primitives tested against assistive technologies ([Radix](https://www.radix-ui.com/primitives/docs/overview/accessibility)); labels and page-level checks still yours | Depends on reimplementing each [APG pattern](https://www.w3.org/WAI/ARIA/apg/) correctly |
| **Code ownership** | Dependency upgrades bring fixes and breaking changes | Styled layer in your repo; primitive library stays an npm dependency ([shadcn/ui](https://ui.shadcn.com/docs)) | Fully internal |
| **Bundle cost** | Pay per imported component plus the suite's styling layer; "Modern bundlers already tree-shake unused code in production builds" ([MUI: Minimizing bundle size](https://mui.com/material-ui/guides/minimizing-bundle-size/)) | Pay per imported primitive (Radix and Base UI are tree-shakeable) plus your CSS | Only what you write |
| **Wrong choice when** | The brand needs structures or interactions the theme cannot express | No one has time to design and style every component state | The product needs complex widgets (combobox, date picker, menu) and no one can test them with assistive technology |

The draft of this page gave bundle sizes per strategy; no measured source was found, so the figures were removed. Measure your own build before deciding on bundle grounds.

---

## 4. Reserve Space and Show Progress Without Shifting the Layout

1. **Cumulative Layout Shift (CLS):**
   * A good CLS score is "0.1 or less", measured at "the 75th percentile of page loads, segmented across mobile and desktop devices" ([web.dev: CLS](https://web.dev/articles/cls)).
   * CLS counts *unexpected* shifts. "Layout shifts that occur within 500 milliseconds of user input will have the `hadRecentInput` flag set, so they can be excluded" ([web.dev: CLS](https://web.dev/articles/cls)). An accordion that expands within 500 milliseconds of a click can be excluded this way; an ad that loads late and pushes text down cannot.
   * "Always include width and height size attributes on your images and video elements. Alternatively, reserve the required space with CSS aspect-ratio", and reserve space for ads, embeds and iframes ([web.dev: Optimize CLS](https://web.dev/articles/optimize-cls)). `aspect-ratio` is Baseline widely available since September 2021 ([MDN: aspect-ratio](https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio)).
   * Animate with `transform`: "Composited animations using translate can't impact other elements, and so don't count toward CLS" ([web.dev: Optimize CLS](https://web.dev/articles/optimize-cls)).
2. **Skeletons, spinners and progress bars:**
   * NN/g recommends skeleton screens for full-page loads, where they reduce perceived loading time, and for waits under 10 seconds; spinners suit waits of 2 to 10 seconds; progress bars are "strongly recommended" above 10 seconds; and below 1 second, skeletons or spinners "aren't necessary" ([NN/g: Skeleton Screens 101](https://www.nngroup.com/articles/skeleton-screens/)).
   * A skeleton that matches the final layout's dimensions also avoids a layout shift when content arrives (the book's reasoning from the CLS guidance above).
3. **Optimistic UI updates:**
   * For low-risk, reversible actions (a "Like" toggle, a task status), update the UI immediately and roll back if the request fails. React 19+ provides `useOptimistic` for this; its reference shows "the UI automatically rolls back" when a delete fails ([react.dev: useOptimistic](https://react.dev/reference/react/useOptimistic)). Tell the user the change failed; a silent rollback looks like a bug.
   * **When optimistic UI is the wrong choice (the book's reasoning):** payments, irreversible deletes and anything with side effects outside the app. Showing success before the server confirms it misleads the user if the request fails.

---

## 5. Decision Playbook: Pick a Component Strategy by Brand Requirement

```text
                  [What are the product's brand and velocity priorities?]
                                             │
           Is custom, distinctive visual branding a hard commercial requirement?
                         ├── Yes
                         │     └── Choose Headless Primitives + Design Tokens
                         │         (shadcn/ui on Base UI, Radix or React Aria;
                         │          Ark UI; styled with Tailwind or Panda)
                         │
                         └── No (internal admin tool, operator dashboard)
                               └── Choose a Pre-Styled UI Suite
                                   (MUI, Ant Design, Mantine)
```

The tree reads: if a distinctive brand is a hard requirement, pick headless primitives with tokens; if not (for example an internal admin tool), pick a pre-styled suite. This branching is the book's judgment. Two conditions override it:

* **Pick the suite even with a strong brand** when the team has no designer to specify every component state, and the suite's theme tokens cover the brand's colours, type and radii.
* **Pick headless primitives even for an internal tool** when the tool will be embedded in a branded product later, or when it needs widgets the suite does not offer.

---

## 6. References

* [Further reading: *Frontend Architecture for Design Systems* (Micah Godbolt)](../library/reading_list.md)
* W3C: [ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/) and [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
* Design Tokens Community Group: [Format Module 2025.10](https://www.designtokens.org/TR/2025.10/format/)
* web.dev: [Cumulative Layout Shift](https://web.dev/articles/cls) and [Optimize CLS](https://web.dev/articles/optimize-cls)
* Adam Wathan and Steve Schoger: [*Refactoring UI*](https://www.refactoringui.com/)
