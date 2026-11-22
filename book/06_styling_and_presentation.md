---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: tailwindcss 4.3.5, @stylexjs/stylex 0.19.2, @pandacss/dev 2.6.0, @vanilla-extract/css 1.21.3, styled-components 6.6.0 (6.3.0 release notes), @emotion/react 11.14.0 (emotion#2978), react 19.3.1, typescript 7.0.2, Next.js docs 16.4.6, react.dev useInsertionEffect, MDN Baseline (nesting, container-type, subgrid, color-mix, custom properties)
review_by: 2027-05
reviewers:
ledger: reviews/styling-and-presentation.md
---

# Chapter 6: Styling and Presentation: The CSS Architecture Dilemma

> For a tech lead choosing how a React application writes and ships its CSS. The decision is where styles are generated: at build time (utility classes, CSS Modules, compile-time CSS-in-JS) or in the browser at runtime (runtime CSS-in-JS). Versions were checked against the npm registry on 2026-11-22.

---

## 1. The Core Dilemma

Two problems drive every styling choice in a component-based app:

1. **Global cascade collisions.** In one large global stylesheet, any selector can match any element, so changing a class used on one page can restyle an unrelated page. Every approach in this chapter is a way to scope styles to the component that owns them.
2. **The cost of scoping at runtime.** Runtime CSS-in-JS libraries such as styled-components and Emotion solved scoping by writing styles in JavaScript and generating CSS rules in the browser.

React's own documentation does not recommend the second approach. It lists three ways to apply styles from JavaScript (static CSS files produced by a compiler, inline styles, and runtime injection of `<style>` tags) and says: "We don't recommend runtime `<style>` tag injection", because "Runtime injection forces the browser to recalculate the styles a lot more often" and "can be very slow if it happens at the wrong time in the React lifecycle". React's `useInsertionEffect` hook fixes only the timing problem; the docs call the first problem "not solvable" ([react.dev: useInsertionEffect](https://react.dev/reference/react/useInsertionEffect)). The Next.js 16.4.6 docs add a warning that using CSS-in-JS with Server Components and streaming "requires library authors to support the latest version of React, including concurrent rendering" ([Next.js: CSS-in-JS](https://nextjs.org/docs/app/guides/css-in-js)).

This chapter's position follows from those two sources: for new React projects, generate CSS at build time and handle per-instance values with CSS custom properties. Runtime CSS-in-JS remains a reasonable place to stay for an existing codebase that works, not a starting point.

---

## 2. Choose Where Styles Are Generated: Build Time or Runtime

### Choice A: Utility-First CSS (Tailwind CSS 4.x)

* **Mechanism:** Components compose small single-purpose classes in markup (`flex items-center justify-between p-4 bg-white rounded-lg shadow`). Tailwind "treats all of your source files as plain text" and looks for tokens that could be class names, then generates CSS only for the ones that map to a utility ([Tailwind: Detecting classes in source files](https://tailwindcss.com/docs/detecting-classes-in-source-files)). Tailwind CSS 4.0 (released January 22, 2025) moved configuration from `tailwind.config.js` into CSS, detects template files automatically, and builds on cascade layers, `@property` and `color-mix()` ([Tailwind CSS v4.0 announcement](https://tailwindcss.com/blog/tailwindcss-v4)). The registry version on 2026-11-22 is 4.3.5.
* **Advantage:** The output depends on the set of distinct utilities used, not on the number of components, because a second component using `p-4` adds no CSS (the book's reasoning). Tailwind's own claim is that "most Tailwind projects ship less than 10kB of CSS to the client" ([tailwindcss.com](https://tailwindcss.com/)); this is a vendor statement without a published measurement method.
* **Trade-off:** Long class strings in markup, and a vocabulary of utility names to learn.
* **Wrong choice when:** class names are assembled from runtime strings. Tailwind "has no way of understanding string concatenation or interpolation", so `bg-${color}-600` generates no CSS; the docs require complete class names ([Tailwind: Dynamic class names](https://tailwindcss.com/docs/detecting-classes-in-source-files#dynamic-class-names)). It is also a poor fit for styling HTML you do not author, such as rich text from a CMS, where you cannot add classes to each element (the book's reasoning).

### Choice B: CSS Modules

* **Mechanism:** "A CSS Module is a CSS file where all class names and animation names are scoped locally by default" ([CSS Modules specification](https://github.com/css-modules/css-modules)). The bundler rewrites each class to a unique name and gives the component a map from the original name to the generated one. Next.js supports them in any component in the `app` directory through `.module.css` files ([Next.js: CSS](https://nextjs.org/docs/app/getting-started/css)).
* **Advantage:** The files are ordinary CSS and ship no styling JavaScript beyond the class-name map. Native features work wherever the browser supports them: MDN marks each of these Baseline widely available and gives the date since which it has been available across browsers: CSS nesting since December 2023 ([MDN: nesting selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/Nesting_selector)), size container queries (`container-type`) since February 2023 ([MDN: container-type](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/container-type)), subgrid since September 2023 ([MDN: Subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Subgrid)) and `color-mix()` since May 2023 ([MDN: color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/color-mix)).
* **Trade-off:** Each module emits its own rules, so the same declaration written in two modules ships twice, and output grows with the CSS the team writes (the book's reasoning). Class names are not type-checked without extra tooling.
* **Wrong choice when:** design tokens must be enforced by the compiler (a module can hard-code any colour), or the product must run in browsers released before the dates above and the build tool is not set up to lower newer syntax (the book's reasoning).

### Choice C: Compile-Time CSS-in-JS (StyleX, Panda CSS, vanilla-extract)

* **Mechanism:** Styles are written as TypeScript or JavaScript objects and turned into static CSS by a build step. The three libraries differ in detail:
  * **StyleX** (`@stylexjs/stylex` 0.19.2): a compiler that emits "collision-free atomic CSS", with "No runtime style injection" and a "Tiny and fast runtime for merging class names" ([StyleX: Introduction](https://stylexjs.com/docs/learn/)). Meta reports that at Meta "Atomic classes reduced CSS size by 80%" ([Engineering at Meta, November 2025](https://engineering.fb.com/2025/11/11/web/stylex-a-styling-library-for-css-at-scale/)); this is the vendor's own figure and the post gives no baseline or method.
  * **Panda CSS** (`@pandacss/dev` 2.6.0): "You write styles in TypeScript, and Panda generates plain atomic CSS at build time" by static analysis. Without its opt-in source transforms, "the css call stays in the client bundle and a small runtime joins the class names" ([Panda: Why Panda](https://panda-css.com/docs/overview/getting-started)).
  * **vanilla-extract** (`@vanilla-extract/css` 1.21.3): styles live in `.css.ts` files and "All styles generated at build time" ([vanilla-extract](https://vanilla-extract.style/)). Its class names are locally scoped per style, not atomic; atomic output comes from its separate Sprinkles package ([Sprinkles](https://vanilla-extract.style/documentation/packages/sprinkles/)).
* **Advantage:** Typed tokens and editor autocomplete, with CSS produced before the browser runs. Server Components setups are documented: StyleX has a Vite + React Server Components guide ([StyleX: Vite RSC](https://stylexjs.com/docs/learn/installation/vite/vite-rsc)), and Panda states "Server components get the same result with no transform, since css() runs on the server" ([Panda: Why Panda](https://panda-css.com/docs/overview/getting-started)).
* **Trade-off:** Each needs a bundler plugin, and style values must be visible to the compiler. StyleX allows only statically resolvable values plus arrow functions for dynamic styles, which it compiles to CSS variables set at runtime ([StyleX: Defining styles](https://stylexjs.com/docs/learn/styling-ui/defining-styles/)).
* **Wrong choice when:** many style values are only known at runtime (for example, user-built themes). Panda's docs say "Using a value that is not statically analyzable at build-time will not work" and recommend recipes, CSS variables or `data-*` attributes instead ([Panda: Dynamic styling](https://panda-css.com/docs/guides/dynamic-styling)). It is also the wrong choice when the project's bundler has no maintained plugin for the library.

### Choice D: Runtime CSS-in-JS (styled-components 6.x, Emotion 11.x)

* **Mechanism:** Style templates are evaluated in JavaScript during render; the library hashes the result into a class name and inserts the CSS rule into the document. This is the "runtime injection of `<style>` tags" that React's docs advise against ([react.dev: useInsertionEffect](https://react.dev/reference/react/useInsertionEffect)).
* **Project status (styled-components 6.6.0):** On March 17, 2025 the maintainer wrote that styled-components "as a project is in 'maintenance mode'" and "will continue to be available with occasional bugfixes and misc improvements to support the existing user base", adding: "For new projects, I would not recommend adopting styled-components or most other css-in-js solutions" ([styled-components: Thank you](https://opencollective.com/styled-components/updates/thank-you)). Maintenance mode is not deprecation: the package is still released. Version 6.3.0 (January 10, 2026) added React Server Components support, in which components "emit inline `<style>` tags that React 19 automatically hoists and deduplicates" and `ThemeProvider` becomes a no-op ([6.3.0 release notes](https://github.com/styled-components/styled-components/releases/tag/styled-components%406.3.0)). A March 27, 2026 update says the maintenance-mode post is "still true" while the library "now has a path forward in modern React", and that the author is "the only remaining maintainer" ([styled-components: A Whole New World](https://opencollective.com/styled-components/updates/a-whole-new-world)).
* **Project status (Emotion, `@emotion/react` 11.14.0):** the request for Server Components support has been open since January 2023 ([emotion-js/emotion#2978](https://github.com/emotion-js/emotion/issues/2978), still open on 2026-11-22), and the Next.js docs list Emotion under libraries "working on support" ([Next.js: CSS-in-JS](https://nextjs.org/docs/app/guides/css-in-js)).
* **When it is still the right choice:** a large existing codebase that already works on it, where a rewrite would cost more than the style recalculation it saves (the book's reasoning).
* **Wrong choice when:** starting a new project (the maintainer's and React's advice above), or rendering Emotion-styled components as Server Components.

---

## 3. Comparative Matrix

Each cell summarises the sources linked in Section 2. Cells without a link are the book's reasoning.

| Constraint | Utility-first (Tailwind 4.x) | CSS Modules | Compile-time (StyleX, Panda, vanilla-extract) | Runtime CSS-in-JS (styled-components, Emotion) |
| :--- | :--- | :--- | :--- | :--- |
| **Styling work in the browser** | None: a static stylesheet ([Tailwind docs](https://tailwindcss.com/docs/detecting-classes-in-source-files)) | None beyond the class-name map ([spec](https://github.com/css-modules/css-modules)) | StyleX: small class-merging runtime; Panda: none with transforms, small runtime without; vanilla-extract: static CSS | Rules generated and inserted during render ([react.dev](https://react.dev/reference/react/useInsertionEffect)) |
| **React Server Components** | Yes: the stylesheet is imported in the root layout ([Next.js: CSS](https://nextjs.org/docs/app/getting-started/css)) | Yes: importable "into any component inside the app directory" ([Next.js: CSS](https://nextjs.org/docs/app/getting-started/css)) | Documented for StyleX and Panda ([StyleX](https://stylexjs.com/docs/learn/installation/vite/vite-rsc), [Panda](https://panda-css.com/docs/overview/getting-started)) | styled-components since 6.3.0; Emotion not yet ([#2978](https://github.com/emotion-js/emotion/issues/2978)) |
| **CSS growth as the app grows** | Tracks distinct utilities used (book's reasoning) | Tracks authored rules (book's reasoning) | StyleX: "CSS size plateaus as the codebase grows" ([StyleX](https://stylexjs.com/docs/learn/)) | Rules generated per distinct style value at runtime |
| **Type safety** | Editor tooling only | None without extra tooling | TypeScript APIs and token contracts ([vanilla-extract](https://vanilla-extract.style/)) | Typed theme objects |
| **Dynamic values** | Complete class names, or custom properties | Custom properties | Custom properties (StyleX compiles dynamic styles to them) | Interpolated props |

---

## 4. Dynamic Styles Without Runtime Injection

The main argument for runtime CSS-in-JS was passing props straight into styles. This styled-components fragment (it needs `import styled from 'styled-components'` and a React app around it) generates a CSS rule for each distinct `$width` value at render time (the book's reading of how interpolation works). The `$` prefix makes it a transient prop, which styled-components does not pass to the DOM ([styled-components API: transient props](https://styled-components.com/docs/api)).

```tsx
// Fragment. Runtime pattern: each distinct $width inserts a new rule in the browser.
const Box = styled.div<{ $width: number }>`
  width: ${(props) => props.$width}px;
`;
```

For CSS-in-JS users, React's documentation recommends a combination of "CSS files for static styles, inline styles for dynamic styles" ([react.dev: useInsertionEffect](https://react.dev/reference/react/useInsertionEffect)). With Tailwind CSS 4.x, the static rule reads a custom property and the component sets only the property's value inline. `w-(--box-width)` is Tailwind 4 syntax for `width: var(--box-width)`:

```tsx
import type { CSSProperties } from 'react';

export function Box({ width }: { width: number }) {
  return (
    <div
      className="h-10 w-(--box-width) rounded bg-blue-500"
      style={{ '--box-width': `${width}px` } as CSSProperties}
    />
  );
}
```

This example was type-checked with TypeScript 7.0.2 in strict mode, rendered with React 19 on Node 24 (output: `<div class="h-10 w-(--box-width) rounded bg-blue-500" style="--box-width:240px"></div>`), and compiled with `@tailwindcss/cli` 4.3.5, which emitted `.w-\(--box-width\) { width: var(--box-width); }`.

What the browser does differently: no stylesheet rule is added. Changing `width` changes one element's `style` attribute. Custom properties "inherit their value from their parent" ([MDN: Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties)), so the browser still recomputes style for that element and the descendants that use the variable; the saving is that no new rules enter the cascade for every element to match against (the book's reasoning, consistent with React's "recalculate the styles a lot more often" warning). Custom properties are Baseline widely available, available across browsers since April 2017 ([MDN: custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/--*)). StyleX uses the same technique for its dynamic styles, and the styled-components 6.3.0 release notes list custom properties "set via inline `style`" among their Server Components best practices.

---

## 5. Decision Playbook

```text
Is this an existing app that already works on runtime CSS-in-JS?
├── Yes ──> Stay for now; move new or hot components to build-time CSS.
│           (Emotion + Server Components: not supported, see #2978)
└── No
    │
    Do you want to write styles as utility classes in markup?
    ├── Yes ──> Tailwind CSS 4.x
    │           (shadcn/ui components are updated for Tailwind v4)
    └── No: styles in objects or separate files
        │
        Must design tokens be enforced by the TypeScript compiler?
        ├── Yes ──> StyleX, Panda CSS or vanilla-extract
        └── No  ──> CSS Modules
```

The same tree as a table:

| If | Then |
| :--- | :--- |
| The app already runs on styled-components or Emotion and works | Keep it; write new components with build-time CSS. Do not move Emotion components into Server Components. |
| New project, styles written in markup | Tailwind CSS 4.x. shadcn/ui's components are updated "for Tailwind v4 and React 19" ([shadcn/ui: Tailwind v4](https://ui.shadcn.com/docs/tailwind-v4)). |
| New project, typed tokens required | StyleX, Panda CSS or vanilla-extract, if the bundler has a supported plugin and style values are known at build time. |
| New project, plain CSS preferred | CSS Modules. |

---

## 6. References

* React: [useInsertionEffect, "Injecting dynamic styles from CSS-in-JS libraries"](https://react.dev/reference/react/useInsertionEffect)
* Next.js: [How to use CSS-in-JS libraries](https://nextjs.org/docs/app/guides/css-in-js) and [CSS](https://nextjs.org/docs/app/getting-started/css)
* Tailwind CSS: [v4.0 announcement](https://tailwindcss.com/blog/tailwindcss-v4) (January 22, 2025) and [Detecting classes in source files](https://tailwindcss.com/docs/detecting-classes-in-source-files)
* [CSS Modules specification](https://github.com/css-modules/css-modules)
* [StyleX documentation](https://stylexjs.com/docs/learn/); Melissa Liu, [StyleX: A Styling Library for CSS at Scale](https://engineering.fb.com/2025/11/11/web/stylex-a-styling-library-for-css-at-scale/), Engineering at Meta (2025)
* [Panda CSS documentation](https://panda-css.com/docs/overview/getting-started); [vanilla-extract documentation](https://vanilla-extract.style/)
* styled-components: [Thank you](https://opencollective.com/styled-components/updates/thank-you) (March 17, 2025), [A Whole New World](https://opencollective.com/styled-components/updates/a-whole-new-world) (March 27, 2026), [6.3.0 release notes](https://github.com/styled-components/styled-components/releases/tag/styled-components%406.3.0)
* Adam Wathan, [CSS Utility Classes and "Separation of Concerns"](https://adamwathan.me/css-utility-classes-and-separation-of-concerns/) (August 7, 2017)
* MDN: [Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties)
