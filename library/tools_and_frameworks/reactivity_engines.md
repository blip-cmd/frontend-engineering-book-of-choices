# Reactivity Engines: Virtual DOM vs. Signals vs. Direct AST Compilation

> **Unverified background notes.** This file is an AI-generated research summary from the book's first draft. It has not been checked against the [content standards](../../CONTENT_STANDARDS.md) and is not part of the book. The verified chapters in `book/` cite primary sources directly; rely on those instead.

* **Category:** `reactivity_engine`
* **Status:** Industry Standard & Emerging Production
* **Core Comparison:** React (Virtual DOM) vs. Solid / Preact / Angular / Vue (Fine-Grained Signals) vs. Svelte (Compile-Time AST Reactive Transformation)

---

## 1. Mechanics Overview

### Virtual DOM (VDOM)
* **How it works:** When state updates, the framework executes the entire component function again, creating a lightweight in-memory tree representing the desired UI state. The runtime performs a diffing algorithm (reconciliation) against the previous tree and calculates the minimal set of real DOM mutations.
* **Mental Model:** Functional purity. UI is a pure projection of state: `UI = f(State)`.
* **The Cost:** Memory churn from ephemeral VDOM objects, CPU cycles spent diffing nodes that did not change, and the necessity of manual memoization hooks (`useMemo`, `useCallback`, `React.memo`) to suppress redundant re-renders.

### Fine-Grained Signals
* **How it works:** A signal is an observable primitive wrapping a value and a subscriber set. When a component initializes, access to `.value` registers the calling DOM node or compute effect as a subscriber. When the signal mutates, it notifies only its exact subscribers. The component function never executes again; only the specific text node or DOM attribute is updated directly.
* **Mental Model:** A reactive dependency graph. UI binds directly to observable cells: `DOM_Node = Signal.listen()`.
* **The Cost:** Graph management overhead, subtle timing/batching complexities, and proxy/accessor wrappers.

### Compile-Time AST Compilation
* **How it works:** Instead of shipping a runtime reconciliation or graph library to the client, the compiler analyzes assignments and dependencies during build time. It generates imperative JavaScript code (e.g., `if (changed.x) node.data = x`) that updates the DOM directly.
* **Mental Model:** Disappearing runtime. The compiler transforms high-level reactive declarations into surgical vanilla JavaScript mutations.
* **The Cost:** Tighter compiler lock-in, non-standard JavaScript semantics, and bundle growth if boilerplate generated per component outpaces a shared runtime library.

---

## 2. Comparative Matrix

| Evaluation Vector | Virtual DOM (React) | Fine-Grained Signals (Solid, Preact, Vue, Angular) | Compile-Time (Svelte 5 Runes) |
| :--- | :--- | :--- | :--- |
| **Component Re-execution** | High (Entire tree re-executes on state shift) | None (Component runs once as setup function) | None (Compiled reactive statements run selectively) |
| **Memory Footprint** | Moderate to High (Ephemeral VDOM node allocation) | Very Low (Persistent graph pointers, zero VDOM) | Minimal (No runtime virtual trees) |
| **Runtime Library Weight** | ~40 KB (React + ReactDOM) | ~3 KB to 16 KB (Preact / Solid) | ~2 KB to 8 KB base runtime |
| **Optimization Burden** | Developer-driven (Manual memoization and dependency arrays) | Automatic (Dependencies tracked at access time) | Automatic (Static dependency analysis by compiler) |
| **Ecosystem & Market Share**| Massive (Dominant hiring pool and component libraries) | Rapidly Growing (Supported by Angular, Vue, Solid, Preact) | Strong in developer satisfaction, smaller enterprise market share |

---

## 3. Decision Playbook

### Choose Virtual DOM When:
* Ecosystem scale and ready-made component libraries (e.g., AG Grid, rich text editors, 3D Canvas bindings) are top priorities.
* Team composition consists predominantly of existing React developers where hiring velocity outweighs micro-benchmarks.
* Cross-platform targets (React Native for mobile/desktop) share component and state primitives.

### Choose Signals When:
* The application features high-frequency data streams (financial tickers, real-time telemetry, live collaborative canvases, heavy dashboards).
* Memory efficiency on low-powered consumer electronics or embedded browsers is a hard engineering constraint.
* You desire declarative component syntax without the cognitive overhead of manual dependency arrays and stale closures.

### Choose Compile-Time When:
* Rapid prototyping, developer ergonomics, and minimal bundle footprint are paramount.
* The team prefers idiomatic web standards and concise markup without runtime framework weight.
