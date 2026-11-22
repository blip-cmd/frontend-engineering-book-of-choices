---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: react 19.3.1, babel-plugin-react-compiler 1.0.0, solid-js 2.0.3, preact 11.2.0, @preact/signals 2.11.4, @angular/core 22.3.0, vue 3.5.46 (3.6.0-rc.16), svelte 5.59.1, TC39 Signals proposal Stage 1, npm downloads API 2026-11-14 to 2026-11-20, react.dev, docs.solidjs.com, preactjs.com v11, angular.dev, vuejs.org, svelte.dev docs and blog
review_by: 2027-05
reviewers:
ledger: reviews/the-reactivity-dilemma.md
---

# Chapter 2: The Reactivity Dilemma: Virtual DOM vs. Signals vs. Compilers

> How does a change in memory become a pixel update on screen? The answer decides how much work a framework does on every state change, and which kinds of mistakes your team will make.

---

## 1. What the Reactivity Model Decides

Every frontend application has a synchronization problem: when an event (a keystroke, a WebSocket message, an HTTP response) changes a variable in memory, the browser's Document Object Model (DOM) must show that change.

Updating the DOM by hand (`document.getElementById(...).textContent = ...`) works for small examples. The React docs put it this way: manipulating the UI imperatively "works well enough for isolated examples, but it gets exponentially more difficult to manage in more complex systems" ([react.dev: Reacting to Input with State](https://react.dev/learn/reacting-to-input-with-state)). Frameworks offer declarative UI instead: you describe what the interface should look like for a given state, and the framework keeps the DOM in sync.

The mechanism a framework uses for that sync is the architectural choice this chapter covers:
* Re-run component functions, build a new tree of plain objects and compare it with the previous one (Virtual DOM)?
* Track which expressions read which values, and re-run only those expressions when a value changes (fine-grained signals)?
* Use a compiler to turn component code into direct DOM operations wired to a reactive runtime (compile-time reactivity)?

---

## 2. Choose How Updates Reach the DOM: Three Models

### Choice A: Virtual DOM Reconciliation (React 19)
* **Mechanism:** When state changes, React calls the function component whose state update triggered the render, and "this process is recursive": every component it returns renders too ([react.dev: Render and Commit](https://react.dev/learn/render-and-commit)). Each render returns React elements, which are plain objects with `type`, `props` and other fields ([react.dev: createElement](https://react.dev/reference/react/createElement)). React compares the new output with the previous render and, in the commit phase, applies "the minimal necessary operations" to the DOM. The comparison is the "heuristic O(n) algorithm" described in the archived [legacy reconciliation docs](https://legacy.reactjs.org/docs/reconciliation.html); the reconciler behind it is React Fiber ([Andrew Clark, React Fiber Architecture, 2016](https://github.com/acdlite/react-fiber-architecture)). State updates inside one event handler are batched into a single render ([react.dev: Queueing a Series of State Updates](https://react.dev/learn/queueing-a-series-of-state-updates)).
* **The Inherent Tax:**
  1. *Render work for unchanged output:* "React normally re-renders a component whenever its parent re-renders" ([react.dev: memo](https://react.dev/reference/react/memo)), so a state change high in the tree re-runs every child function below it, including those whose output turns out identical.
  2. *Allocation per render:* every render creates new element objects that the JavaScript engine must later garbage-collect. How much this costs depends on tree size and device; measure it in a profiler rather than assuming it.
  3. *Optimization burden:* skipping work has meant wrapping components in `memo` and values in `useMemo` and `useCallback`, and React notes memoization "is a performance optimization, not a guarantee" ([react.dev: memo](https://react.dev/reference/react/memo)). React Compiler 1.0 (released October 7, 2025, package `babel-plugin-react-compiler` 1.0.0) applies this memoization automatically at build time ([React Compiler v1.0](https://react.dev/blog/2025/10/07/react-compiler-1); [Introduction](https://react.dev/learn/react-compiler/introduction)).
* **When this is the wrong choice (the book's reasoning):** a screen where a few values change many times per second inside a large component tree, and the team cannot move that state into small leaf components. Each update then re-renders a subtree that mostly did not change.

### Choice B: Fine-Grained Signals (Solid 2.0; Preact, Angular and Vue in part)
* **Mechanism:** A signal holds one value and records who reads it. In Solid 2.0, `createSignal` returns a getter and a setter. Solid "runs each component once, records which reactive values each expression reads, and re-runs only those expressions when the values they read change"; JSX expressions, memos and effects are the tracking scopes ([Solid docs: Reactivity](https://docs.solidjs.com/concepts/reactivity)). "There is no virtual DOM value that Solid repeatedly rebuilds and compares" ([Solid docs: Components and JSX](https://docs.solidjs.com/concepts/components-and-jsx)). Writes are staged and applied together in a microtask ([Solid docs: Reactivity](https://docs.solidjs.com/concepts/reactivity)).
* **Other frameworks use signals differently**, so check which rendering model sits underneath:
  * *Preact 11 with `@preact/signals` 2.x:* reading `signal.value` inside a component re-renders that component through the Virtual DOM. Passing the signal itself into JSX (`{count}` instead of `{count.value}`) binds it to a text node that updates "without re-rendering the component" ([Preact: Signals](https://preactjs.com/guide/v11/signals/)).
  * *Angular 22:* signals are getter functions (`count()`). Reading one in an `OnPush` component's template makes Angular mark that component so "it gets updated the next time change detection runs" ([Angular: Signals](https://angular.dev/guide/signals)). Zoneless change detection is the default from Angular v21 ([Angular: Zoneless](https://angular.dev/guide/zoneless)).
  * *Vue 3.5:* refs work like signals, but a component's render effect produces a new Virtual DOM tree that the renderer compares with the old one ([Vue: Rendering Mechanism](https://vuejs.org/guide/extras/rendering-mechanism.html)). Vue's docs say the team is exploring Vapor Mode, a Solid-inspired compilation strategy "that does not rely on Virtual DOM" ([Vue: Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth.html)); as of November 2026 it ships only in 3.6 pre-releases (the latest is `3.6.0-rc.16`, [Vue changelog](https://github.com/vuejs/core/blob/minor/CHANGELOG.md)), while the stable release is 3.5.46.
  * *A JavaScript standard:* the [TC39 Signals proposal](https://github.com/tc39/proposal-signals) is at Stage 1, with a polyfill for experiments; it is not part of the language.
* **The Inherent Tax:**
  1. *Graph bookkeeping:* a signal "knows who reads it" ([Solid docs: Reactivity](https://docs.solidjs.com/concepts/reactivity)), so the runtime keeps a record of readers in memory alongside each value.
  2. *Read placement:* a read outside a tracking scope runs once and never updates. Solid's component body is not a tracking scope, and "destructuring reads once" when applied to props ([Solid docs: Components and JSX](https://docs.solidjs.com/concepts/components-and-jsx)). Vue documents the same loss when you destructure a `reactive()` object ([Vue: Reactivity Fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)).
* **When this is the wrong choice:** when the product depends on React-only component libraries (data grids, charting, 3D) that have no equivalent, because Solid components are not React components (the book's reasoning). Also when tests and imperative code read a value right after writing it: Solid's docs name tests and such code as "the two places where the delay shows up" ([Solid docs: Reactivity](https://docs.solidjs.com/concepts/reactivity)).

### Choice C: Compile-Time Reactivity (Svelte 5)
* **Mechanism:** Svelte "uses a compiler to turn declarative components written in HTML, CSS and JavaScript" into JavaScript ([Svelte docs: Overview](https://svelte.dev/docs/svelte/overview)). Runes such as `$state` and `$derived` are compiler keywords, valid only in `.svelte` and `.svelte.js` / `.svelte.ts` files ([Svelte docs: What are runes?](https://svelte.dev/docs/svelte/what-are-runes)). The compiler does not remove the reactive graph: "Svelte 5's reactivity is powered by signals", which are "an under-the-hood implementation detail rather than something you interact with directly" ([Svelte blog: Introducing runes, 2023](https://svelte.dev/blog/runes)). Svelte does not build a Virtual DOM; Rich Harris's advocacy post [Virtual DOM is pure overhead](https://svelte.dev/blog/virtual-dom-is-pure-overhead) (December 2018, before Svelte 5) gives the reasoning. `$state` on an object or array creates a "deeply reactive state proxy" that triggers granular updates ([Svelte docs: $state](https://svelte.dev/docs/svelte/$state)).
* **The Inherent Tax:**
  1. *Compiler semantics:* runes look like functions but are not values; "you can't assign them to a variable or pass them as arguments to a function" ([Svelte docs: What are runes?](https://svelte.dev/docs/svelte/what-are-runes)). Destructuring a reactive value gives non-reactive references ([Svelte docs: $state](https://svelte.dev/docs/svelte/$state)).
  2. *Output grows with component count:* the compiler emits code per component on top of a shared runtime, so total output scales with the number of components. Whether that ends up larger or smaller than another framework depends on the app; compare real builds (the book's reasoning).
* **When this is the wrong choice (the book's reasoning):** when reactive logic must live in plain `.js` or `.ts` modules shared with non-Svelte code, since runes work only in Svelte files; or when the project cannot add a compile step for its UI code.

---

## 3. What Each Model Does on One State Change

The rows describe the work each model performs, taken from the docs cited in Section 2. They are not speed rankings. To compare speed, run a reproducible benchmark such as [js-framework-benchmark](https://github.com/krausest/js-framework-benchmark) against pinned versions, then profile your own screens.

| Constraint | Virtual DOM (React 19) | Fine-Grained Signals (Solid 2.0) | Compile-Time (Svelte 5) |
| :--- | :--- | :--- | :--- |
| **Component function re-runs** | The updated component and its children, unless memoized ([react.dev](https://react.dev/learn/render-and-commit)) | None after mount ([Solid docs](https://docs.solidjs.com/concepts/reactivity)) | None; the `<script>` block "runs when a component instance is created" ([Svelte docs](https://svelte.dev/docs/svelte/svelte-files)) |
| **Per-update work** | Build new elements, compare, commit the differences | Re-run the expressions that read the changed signal | Granular updates triggered by the changed state ([Svelte docs](https://svelte.dev/docs/svelte/$state)) |
| **Memory held between updates** | Previous render output for comparison | Subscriber graph | Subscriber graph (signals at runtime) |
| **Main source of mistakes** | Missing or broken memoization ([react.dev](https://react.dev/reference/react/memo)) | Reads outside tracking scopes; destructured props ([Solid docs](https://docs.solidjs.com/concepts/components-and-jsx)) | Rune placement rules; destructured state ([Svelte docs](https://svelte.dev/docs/svelte/$state)) |
| **npm downloads, week of 2026-11-14 to 2026-11-20** | `react`: 275,461,240 | `solid-js`: 12,570,158 | `svelte`: 10,392,751 |

Download counts come from the [npm downloads API](https://api.npmjs.org/downloads/point/2026-11-14:2026-11-20/react,solid-js,svelte) and include automated and transitive installs, so they indicate ecosystem reach, not the number of developers.

---

## 4. Worked Scenario: A Live Telemetry Grid

Consider a dashboard grid that receives a stream of WebSocket updates, several per second for each tile. Each message changes one metric in one tile.

1. **Virtual DOM (React 19):**
   If the metrics live in state at the top of the grid, each message re-renders the grid component and every tile below it, then React compares the output and commits the one changed text node ([react.dev: Render and Commit](https://react.dev/learn/render-and-commit)). Moving each metric's state into its own tile component, or memoizing tiles, limits the re-render to one tile. Whether the unlimited version hurts depends on grid size and device; check [Interaction to Next Paint (INP)](https://web.dev/articles/inp) in the field to find out.
2. **Fine-grained signals (Solid 2.0, or Preact 11 with the signal passed into JSX):**
   The message sets the tile's signal. Solid re-runs only the JSX expression that reads it; Preact updates the text bound to the signal; in both, no component function runs again ([Solid docs: Reactivity](https://docs.solidjs.com/concepts/reactivity); [Preact: Signals](https://preactjs.com/guide/v11/signals/)). The message handler and that one expression still run on the main thread.

---

## 5. Decision Playbook

The tree is the book's reasoning, built from the mechanisms above.

```text
                  [How often does your state change?]
                                        │
           ├── Many updates per second to a few values (telemetry, tickers, games)
           │      └── Choose Fine-Grained Signals (Solid 2.0, or Preact 11 + signals in JSX)
           │
           └── Ordinary web UI frequency (form inputs, clicks, page navigations)
                  │
                  Are ecosystem size and hiring the top priority?
                        ├── Yes ──> Choose Virtual DOM (React 19)
                        │           (add React Compiler 1.0 instead of hand-written memoization)
                        │
                        └── No
                              │
                              Do you want compiled components with little framework syntax?
                                    ├── Yes ──> Choose Compile-Time (Svelte 5)
                                    └── No  ──> Choose Fine-Grained Signals (Solid 2.0)
```

### Quick Diagnostic Rules
* **Choose React 19 (Virtual DOM):** when the product relies on React-only third-party libraries (enterprise data grids, charting, 3D canvas), or hiring needs the largest framework ecosystem; `react` has by far the most npm downloads of the three ([npm downloads API](https://api.npmjs.org/downloads/point/2026-11-14:2026-11-20/react,solid-js,svelte)). Wrong when a few fast-changing values sit high in a large tree and cannot be moved down.
* **Choose Solid 2.0 or Preact 11 with signals (fine-grained):** when frequent updates to a few values must not re-run component code. Wrong when the React-only libraries above are required, or when the team is not ready to learn where reads must happen.
* **Choose Svelte 5 (compiler):** when a team wants a compile step to handle reactivity wiring and is comfortable with rune rules. Wrong when reactive logic must be shared through plain JavaScript modules outside Svelte files.

---

## 6. References
* react.dev: [Render and Commit](https://react.dev/learn/render-and-commit), [memo](https://react.dev/reference/react/memo), [React Compiler v1.0](https://react.dev/blog/2025/10/07/react-compiler-1)
* Andrew Clark: [React Fiber Architecture](https://github.com/acdlite/react-fiber-architecture) (2016)
* Solid docs: [Reactivity](https://docs.solidjs.com/concepts/reactivity), [Components and JSX](https://docs.solidjs.com/concepts/components-and-jsx)
* Ryan Carniato: [A Hands-on Introduction to Fine-Grained Reactivity](https://dev.to/ryansolid/a-hands-on-introduction-to-fine-grained-reactivity-3ndf) (February 2021)
* The Svelte team: [Introducing runes](https://svelte.dev/blog/runes) (September 2023)
* Vue: [Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth.html); Angular: [Signals](https://angular.dev/guide/signals); Preact: [Signals](https://preactjs.com/guide/v11/signals/)
* [TC39 Signals proposal](https://github.com/tc39/proposal-signals)
