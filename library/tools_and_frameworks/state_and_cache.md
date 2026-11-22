# State and Cache Topologies: Client State Stores vs. Remote Server Caches

> **Unverified background notes.** This file is an AI-generated research summary from the book's first draft. It has not been checked against the [content standards](../../CONTENT_STANDARDS.md) and is not part of the book. The verified chapters in `book/` cite primary sources directly; rely on those instead.

* **Category:** `state_and_cache`
* **Status:** Industry Standard
* **Core Comparison:** Global Store (Zustand, Redux Toolkit, Pinia) vs. Server Cache (TanStack Query, SWR, Apollo/Relay) vs. Atomic State (Jotai, Nano Stores) vs. Fine-Grained Signals

---

## 1. The Fundamental Decomposition of State

The single greatest conceptual breakthrough in modern frontend architecture was the separation of **Server State** from **Client State**:

1. **Server State (Remote Cache):**
   * *Characteristics:* Asynchronous, shared with other users, owned by a remote database, potentially out-of-date immediately after fetching, requires caching, deduplication, polling, and optimistic updates.
   * *Examples:* User profiles, product catalogs, order histories, notification feeds.
   * *Optimal Tooling:* TanStack Query (React Query), SWR, RTK Query, Apollo Client.

2. **Client State (Ephemeral UI State):**
   * *Characteristics:* Synchronous, owned exclusively by the local browser session, transient, requires immediate feedback, vanishes on tab reload unless persisted.
   * *Examples:* Active modal flags, accordion toggles, selected form tabs, draft filter selections, canvas zoom coordinates.
   * *Optimal Tooling:* Component local state (`useState`), atomic state (Jotai), or lightweight stores (Zustand).

*Architectural Anti-Pattern:* Storing raw asynchronous API responses in global Redux or Zustand stores and manually writing reducer actions for `FETCH_START`, `FETCH_SUCCESS`, and `FETCH_ERROR`. This duplicates browser memory, produces stale data race conditions, and adds hundreds of lines of boilerplate.

---

## 2. Comparative Matrix

| Solution | Primary Archetype | Bundle Size | Mental Model | Best Use Case | Primary Hazard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TanStack Query** | Server State Cache | ~12 KB | Declarative stale-while-revalidate cache | 90% of web application data fetching and mutations | Over-fetching if query keys are poorly structured |
| **Zustand** | Centralized Client Store | ~1 KB | Unidirectional store with hook selectors | Complex client UI coordination (audio player, canvas tools) | Misusing it to manually cache backend API entities |
| **Redux Toolkit (RTK)**| Centralized Immutable Store | ~11 KB (without RTK Query) | Predictable action dispatchers & immutable state | Massive enterprise apps with rigorous state action auditing | Verbosity and ceremonial structure for small-to-medium teams |
| **Jotai** | Atomic State | ~3 KB | Bottom-up atom composition | Highly dynamic, fine-grained UI trees with complex derived state | Orphaned atoms and difficult debugging without DevTools |
| **Signals (Preact/Solid)**| Reactive Observable Primitives | ~1-3 KB | Direct subscriber updates without re-rendering | High-frequency telemetry, live financial streams, games | Leaking subscriptions across component lifecycles |

---

## 3. Decision Playbook

```
                  [Does this data originate from an API / Backend?]
                                   │
                   ├── Yes ───────> Adopt TanStack Query / SWR / RTK Query
                   │                (Treat data as a server cache with stale timers)
                   │
                   └── No (Pure Local UI State)
                           │
             Is it confined to one component tree?
                   ├── Yes ───────> Local Component State (useState / useReducer)
                   └── No
                           │
             Does it require high-frequency updates across detached leaves?
                   ├── Yes ───────> Atomic State (Jotai) or Signals
                   └── No  ───────> Lightweight Global Store (Zustand)
```

### Definitive Guidelines:
* **The 80/20 Reality:** In most standard business web applications, 80% to 90% of state is actually server cache. Adopting TanStack Query or SWR frequently eliminates the need for any global client store entirely.
* **Avoid Multi-Store Chaos:** When using Zustand, prefer a single unified store or small slice-based stores over dozens of scattered uncoordinated instances.
