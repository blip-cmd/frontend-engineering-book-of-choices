---
page: book/02_the_reactivity_dilemma.md
verified: 2026-11-22
---

# Claim Ledger: Chapter 2, The Reactivity Dilemma

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead or senior frontend developer choosing a UI framework or deciding how to structure state inside one. The page helps them decide which reactivity model (Virtual DOM reconciliation, fine-grained signals, or compile-time reactivity) fits their update pattern, ecosystem needs and team. Thesis (unchanged from the draft): the model decides how much work runs per state change; signals suit many updates to a few values, React suits ecosystem- and hiring-driven projects, and Svelte suits teams that want a compiler to handle reactivity wiring.

**History.** The AI-generated draft was rewritten by the author pass on 2026-11-22. Main corrections: the draft grouped Angular, Vue 3 and Preact with Solid as fine-grained signal frameworks whose components run once (Vue 3.5 renders through a Virtual DOM, Preact re-renders a component that reads `.value` unless the signal is passed into JSX, Angular marks components for change detection); it said Svelte 5 eliminates "observable graph libraries" (Svelte's own announcement says Svelte 5's reactivity "is powered by signals"); it described signals generically as `.value` reads (Solid and Angular use getter calls). Removed as unsourced: "even when 95% of the rendered nodes did not change", "periodic frame drops on low-powered mobile processors", the runtime sizes (~40 KB, ~3 KB, ~12 KB, ~2 KB to 8 KB), "Handles 60fps streaming updates effortlessly", "Vastest library catalog in software history", "High Developer Satisfaction", the "10-100 updates/sec" threshold, "zero-overhead memory consumption", "the main thread remains completely idle", and the qualitative speed ratings in the matrix ("Extremely Low", "Moderate to High"). The library/ research-note link was removed. Two references were misattributed: "Rethinking Reactivity and Svelte 5 Runes (2023)" by Rich Harris is actually "Introducing runes" by the Svelte team (2023-09-20), and the Fiber overview is Andrew Clark's repository, not a "React Core Team" document. Recommendation changes, each forced by a source: the final branch of the decision tree no longer offers Vue as a fine-grained signal choice (Vue's docs say its rendering uses a Virtual DOM), and the high-frequency branch now names Preact only with signals passed directly into JSX (Preact's docs). The worked scenario is no longer called a benchmark, since no benchmark was run.

---

## 1. Author pass (2026-11-22)

Sources were fetched in the same session with `curl` and searched as text; package versions were checked with `npm view` on 2026-11-22. The page contains no runnable JavaScript; the only code block is a text decision tree, now tagged `text`.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | Imperative UI "works well enough for isolated examples, but it gets exponentially more difficult to manage in more complex systems" | [react.dev: Reacting to Input with State](https://react.dev/learn/reacting-to-input-with-state) | verified (quote); replaces the draft's unsourced "decays into spaghetti code" |
| 2 | React calls the component whose state update triggered the render; "This process is recursive" | [react.dev: Render and Commit](https://react.dev/learn/render-and-commit) | verified (quote); corrects "re-executes the component function" (it is the component and its children) |
| 3 | React elements are objects with `type`, `props` and other fields | [react.dev: createElement](https://react.dev/reference/react/createElement) | verified (quote) |
| 4 | Commit applies "the minimal necessary operations"; React only changes DOM nodes that differ | react.dev: Render and Commit | verified (quote) |
| 5 | Reconciliation is a "heuristic O(n) algorithm" | [legacy.reactjs.org: Reconciliation](https://legacy.reactjs.org/docs/reconciliation.html) | verified (quote); labelled as archived docs |
| 6 | React Fiber architecture document by Andrew Clark, 2016 | [acdlite/react-fiber-architecture](https://github.com/acdlite/react-fiber-architecture); GitHub API `created_at` 2016-07-19 | verified; draft credited "React Core Team" |
| 7 | React batches state updates from one event handler | [react.dev: Queueing a Series of State Updates](https://react.dev/learn/queueing-a-series-of-state-updates) | verified |
| 8 | "React normally re-renders a component whenever its parent re-renders"; memoization "is a performance optimization, not a guarantee" | [react.dev: memo](https://react.dev/reference/react/memo) | verified (quote) |
| 9 | Draft: diffing costs CPU "even when 95% of the rendered nodes did not change" | none found | removed; rewritten qualitatively from #8 |
| 10 | Draft: VDOM garbage causes "periodic frame drops on low-powered mobile processors" | none found | removed; kept only the allocation mechanism (#3) and advice to profile |
| 11 | React Compiler 1.0 released 2025-10-07; automates memoization at build time; package `babel-plugin-react-compiler` 1.0.0 | [React Compiler v1.0](https://react.dev/blog/2025/10/07/react-compiler-1); [Introduction](https://react.dev/learn/react-compiler/introduction); `npm view` | verified; added (draft predates it) |
| 12 | Solid 2.0 `createSignal` returns a getter and a setter; components run once; only expressions that read a value re-run; JSX, memos and effects are tracking scopes | [Solid docs: Reactivity](https://docs.solidjs.com/concepts/reactivity) | verified (quote) |
| 13 | "There is no virtual DOM value that Solid repeatedly rebuilds and compares" | [Solid docs: Components and JSX](https://docs.solidjs.com/concepts/components-and-jsx) | verified (quote) |
| 14 | Solid stages writes and applies them in a microtask; tests and read-after-write code are "the two places where the delay shows up" | Solid docs: Reactivity | verified (quote) |
| 15 | Solid: component body is not a tracking scope; "destructuring reads once" | Solid docs: Reactivity; Components and JSX | verified (quote) |
| 16 | Preact: reading `.value` in a component re-renders it; passing the signal into JSX updates text "without re-rendering the component" | [Preact: Signals (v11 guide)](https://preactjs.com/guide/v11/signals/) | verified (quote); corrects the draft's "component runs only once" for Preact |
| 17 | `@preact/signals` 2.x supports Preact 11 | `npm view @preact/signals peerDependencies` (`>=11.0.0-0`) | verified |
| 18 | Angular signals are getter functions; reading one in an `OnPush` template marks the component for the next change detection | [Angular: Signals](https://angular.dev/guide/signals) | verified (quote); corrects the draft's "surgical DOM node" description for Angular |
| 19 | Zoneless is the default in Angular v21+ | [Angular: Zoneless](https://angular.dev/guide/zoneless) | verified (quote) |
| 20 | Vue renders through a Virtual DOM; the render effect re-runs and the new tree is compared with the old one | [Vue: Rendering Mechanism](https://vuejs.org/guide/extras/rendering-mechanism.html) | verified; corrects the draft's grouping of Vue 3 with fine-grained signals |
| 21 | Vapor Mode "does not rely on Virtual DOM"; in 3.6 release candidates only (`3.6.0-rc.16`, 2026-11-20); stable is 3.5.46 | [Vue: Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth.html); [Vue changelog](https://github.com/vuejs/core/blob/minor/CHANGELOG.md); `npm view vue dist-tags` | verified |
| 22 | Destructuring a `reactive()` object loses reactivity | [Vue: Reactivity Fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html) | verified |
| 23 | TC39 Signals proposal is at Stage 1 with a polyfill | [proposal-signals](https://github.com/tc39/proposal-signals); [tc39/proposals stage 1 list](https://github.com/tc39/proposals/blob/main/stage-1-proposals.md) | verified; added one line |
| 24 | Svelte "uses a compiler to turn declarative components written in HTML, CSS and JavaScript" into JavaScript | [Svelte docs: Overview](https://svelte.dev/docs/svelte/overview) | verified (quote) |
| 25 | Runes are compiler keywords used in `.svelte` and `.svelte.js` / `.svelte.ts` files; "you can't assign them to a variable or pass them as arguments to a function" | [Svelte docs: What are runes?](https://svelte.dev/docs/svelte/what-are-runes) | verified (quote) |
| 26 | "Svelte 5's reactivity is powered by signals", "an under-the-hood implementation detail" | [Svelte blog: Introducing runes](https://svelte.dev/blog/runes) (The Svelte team, 2023-09-20) | verified (quote); corrects the draft's claim that Svelte has no observable graph |
| 27 | Svelte does not use a Virtual DOM | [Virtual DOM is pure overhead](https://svelte.dev/blog/virtual-dom-is-pure-overhead) (Rich Harris, 2018-12-27) | verified; labelled advocacy and Svelte 3 era |
| 28 | `$state` on objects and arrays creates a "deeply reactive state proxy"; destructured references are not reactive | [Svelte docs: $state](https://svelte.dev/docs/svelte/$state) | verified (quote) |
| 29 | A Svelte `<script>` block "runs when a component instance is created" | [Svelte docs: .svelte files](https://svelte.dev/docs/svelte/svelte-files) | verified (quote) |
| 30 | Draft: Svelte produces larger cumulative bundles on very large apps | none found | rewritten as the book's reasoning (output scales with component count; compare real builds) |
| 31 | Draft: runtime sizes ~40 KB React, ~3 KB Solid, ~12 KB Preact, ~2 KB to 8 KB Svelte | none fetched with measurement details | removed; matrix row replaced |
| 32 | Draft matrix speed ratings ("Extremely Low", "Moderate to High", "60fps") and "High Developer Satisfaction" | none | removed; matrix now describes per-update work from the docs in rows 2 to 29; points to [js-framework-benchmark](https://github.com/krausest/js-framework-benchmark) for measured comparisons |
| 33 | Weekly npm downloads 2026-11-14 to 2026-11-20: react 275,461,240; solid-js 12,570,158; svelte 10,392,751 | [npm downloads API](https://api.npmjs.org/downloads/point/last-week/react,solid-js,svelte) | verified; replaces "Vastest library catalog in software history"; labelled as including transitive installs |
| 34 | Draft: "10-100 updates/sec" threshold; "main thread remains completely idle" | none | removed; signal path now says the handler and one expression still run |
| 35 | INP as the field metric for responsiveness | [web.dev: INP](https://web.dev/articles/inp) | verified (link only, no threshold quoted) |
| 36 | Ryan Carniato, "A Hands-on Introduction to Fine-Grained Reactivity", February 2021 | [dev.to](https://dev.to/ryansolid/a-hands-on-introduction-to-fine-grained-reactivity-3ndf) (posted 2021-02-09) | verified; link added |
| 37 | Pinned versions: react 19.3.1, solid-js 2.0.3 (2.0.0 published 2026-11-17), preact 11.2.0, @preact/signals 2.11.4, @angular/core 22.3.0, vue 3.5.46, svelte 5.59.1, babel-plugin-react-compiler 1.0.0 | `npm view <name> version`, 2026-11-22 | verified |
| 38 | "When this is the wrong choice" for each model | Solid docs: Reactivity (test delay); Svelte docs: What are runes? (file restriction); otherwise labelled the book's reasoning | verified or labelled |

## 2. Independent verifier pass (2026-11-22)

The verifier did not write the page or section 1. It extracted the claims from the page itself (51 claims, including every quote, version, date, attribution, table cell and number) and fetched all 29 cited URLs with `curl -sL` on 2026-11-22, searching the text of each. Versions were re-checked with `npm view` and the download figures with the npm downloads API.

**Verdict: PASS.** 45 claims SUPPORTED as written; 6 PARTIAL, all corrected below; 0 UNSUPPORTED remaining. Every number on the page has a source.

Spot checks of the claims the coordinator flagged:

* React Compiler 1.0: blog post dated Oct 7, 2025 (Lauren Tan, Joe Savona, Mofei Zhang); `babel-plugin-react-compiler` 1.0.0 published 2025-10-07 and is still `latest`. SUPPORTED.
* Vue: `latest` is 3.5.46; `rc` is 3.6.0-rc.16 (changelog entry dated 2026-11-20, with `compiler-vapor` and `runtime-vapor` fixes); `alpha` and `beta` tags also exist. Reactivity in Depth says the team is "exploring" Vapor Mode. PARTIAL, corrected (edit 1).
* Svelte 5: the runes post says "Svelte 5's reactivity is powered by signals" and "signals are an under-the-hood implementation detail rather than something you interact with directly". SUPPORTED. The Overview's sentence ends "...into lean, tightly optimized JavaScript" (checked in the page's llms.txt). SUPPORTED.
* Solid 2.0: the docs site is labelled "solid 2.0"; every quote is verbatim; `solid-js` 2.0.0 was published 2026-11-17 and `latest` is 2.0.3. SUPPORTED.
* Preact 11: the v11 guide (site shows v11.2.0) has the `{count.value}` re-render vs `{count}` "Text automatically updates without re-rendering the component" contrast; the `@preact/signals` peer range includes `>=11.0.0-0`. SUPPORTED.
* Angular: signals are "getter functions"; the OnPush quote is verbatim; "Zoneless is the default in Angular v21+". `@angular/core` 21.0.0 was published 2025-11-19 and `latest` is 22.3.0. SUPPORTED.
* TC39 Signals: the README header says "Stage 1"; tc39/proposals lists it among the Stage 1 proposals; the README says "Try it for yourself, using a polyfill". SUPPORTED.
* Attributions: "Introducing runes" is bylined "The Svelte team", dated `2023-09-20`. The Fiber repository is `acdlite/react-fiber-architecture`; GitHub API owner name is Andrew Clark, `created_at` 2016-07-19, and the README speaks in the first person ("notes I took"). SUPPORTED. "Virtual DOM is pure overhead" is by Rich Harris, Dec 27 2018, and never mentions Svelte 3 (Svelte 3 had not been released then). Section 1 row 27's "Svelte 3 era" label was wrong (edit 3).
* npm: `last-week` and `2026-11-14:2026-11-20` both return react 275,461,240, solid-js 12,570,158 and svelte 10,392,751. SUPPORTED. Every pinned version in row 37 matches `npm view` on 2026-11-22.
* Ryan Carniato's post: "Posted on Feb 9, 2021". SUPPORTED.

Edits to the page:

1. Vue Vapor Mode: "Vue's docs describe Vapor Mode, a compilation strategy" became "Vue's docs say the team is exploring Vapor Mode, a Solid-inspired compilation strategy", which matches the source. "ships only in 3.6 release candidates (`3.6.0-rc.16`" became "ships only in 3.6 pre-releases (the latest is `3.6.0-rc.16`", because the alpha and beta dist-tags also carry Vapor.
2. Signals tax 1: "every signal, memo and effect keeps a list of subscribers in memory for as long as it lives" had no source and was inaccurate for effects, which have no readers. It now quotes the Solid docs: a signal "knows who reads it", so the runtime keeps a record of readers alongside each value.
3. Svelte VDOM post: "(2018, written for Svelte 3)" became "(December 2018, before Svelte 5)". The post does not mention Svelte 3.
4. Matrix, Svelte column: deleted ", and signal-driven updates re-run ([Svelte blog])", because the cited post does not say this. "Re-run the effects that read the changed signal" became "Granular updates triggered by the changed state ([Svelte docs: $state])"; no cited source talks about effects re-running for template updates.
5. Worked scenario, signals path: "Only the JSX expression that reads it re-runs" was wrong for Preact, where the bound text updates without any expression re-running. It became "Solid re-runs only the JSX expression that reads it; Preact updates the text bound to the signal; in both, no component function runs again".
6. npm links (two places): `.../point/last-week/...` became `.../point/2026-11-14:2026-11-20/...`. It is the same API, and the cited figures stay reproducible after the rolling week moves on.

Code checks: the page has no runnable JavaScript. The only code block is the decision tree, tagged `text`. Every package named on the page resolves with `npm view`.

## 3. Known omissions (follow-up content, not errors)

* Qwik's resumability model (`@builder.io/qwik` 1.20.4; `@qwik.dev/core` 2.0 is at release candidate) is a fourth reactivity approach the page does not cover.
* React 19 concurrent features (`useTransition`, `useDeferredValue`) as a way to keep input responsive under frequent updates.
* Measured js-framework-benchmark results with named run and versions, and measured gzip runtime sizes for each framework from a reproducible script.
* Vue 3.5 reactive props destructure and Vapor Mode once it reaches a stable release.
* Angular's `OnPush` and zoneless trade-offs in more depth, and Solid 2.0 async reactivity.
* A small runnable signal example (for example with `@preact/signals-core`) to show dependency tracking.

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | **19** |

D9 is 1 because the worked scenario is described in prose with no runnable code. Gate G8 (human accountability) is not met; the `agent-verified` status, if granted, discloses this.
