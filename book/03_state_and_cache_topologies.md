# Chapter 3: State and Cache Topologies: Client State Stores vs. Remote Server Caches

> Most bugs in modern frontend applications do not stem from rendering logic; they stem from attempting to manage remote, asynchronous network data as if it were local synchronous memory.

---

## 1. The Core Dilemma

In the early days of modern frontend frameworks, state management was treated monolithically. Frameworks like Redux, Vuex, and MobX encouraged developers to store all application data in a single, centralized global store.

This unified approach created subtle, systemic architectural bugs:
* Developers wrote hundreds of lines of boilerplate reducers, actions, and thunks just to handle network states: `IS_LOADING`, `FETCH_SUCCESS`, `FETCH_ERROR`.
* Data fetched from the server lived in the client store indefinitely, silently growing stale while backend databases updated.
* Race conditions emerged when two components dispatched requests with unpredictable network response arrival times.
* Manually deduplicating requests, retrying failed fetches, and invalidating related records became a massive maintenance burden.

The breakthrough in modern state architecture is the formal bifurcation of state into two fundamentally distinct categories: **Server State (Remote Cache)** and **Client State (Ephemeral UI State)**.

---

## 2. The Landscape of Choices

### Category 1: Remote Server Caches (TanStack Query, SWR, RTK Query)
* **Mental Model:** The client does not "own" this data. It merely holds an asynchronous, temporary snapshot of data that belongs to a remote database.
* **Core Responsibilities:**
  * Declarative caching with customizable stale-while-revalidate windows (`staleTime`, `gcTime`).
  * Automatic request deduplication across multiple mounted components.
  * Window focus and network reconnection background re-fetching.
  * Optimistic mutations with automatic rollback on server errors.
* **Enabling Libraries:** `@tanstack/react-query`, `swr`, `@reduxjs/toolkit/query`.

### Category 2: Centralized Client Stores (Zustand, Pinia, Redux Toolkit)
* **Mental Model:** A single or slice-based synchronous state store owned exclusively by the browser session.
* **Core Responsibilities:**
  * Complex multi-step wizard state.
  * Audio/video playback queues, timeline scrubbers, and active canvas coordinates.
  * Cross-component selection states (e.g., selecting 15 rows in a data table to trigger bulk actions).
* **Enabling Libraries:** `zustand`, `pinia`, `@reduxjs/toolkit`.

### Category 3: Atomic State Primitives (Jotai, Nano Stores)
* **Mental Model:** Decomposed, bottom-up state "atoms" that reside outside the React component tree. Components subscribe only to the specific atoms they read.
* **Core Responsibilities:**
  * Fine-grained UI trees where isolated child components need to share state without triggering full parent component re-renders.
  * Canvas-style applications with hundreds of independently draggable elements.
* **Enabling Libraries:** `jotai`, `nanostores`. (Recoil, the library from Meta that popularised this model, was archived in early 2025 and should not be used for new projects.)

### Category 4: Local-First Persistent Synchronizers (ElectricSQL, Replicache, Yjs)
* **Mental Model:** State lives in a local embedded client database (SQLite in Wasm, IndexedDB, or CRDT doc). All reads and writes happen synchronously against local disk, synchronizing in the background via event logs.
* **Core Responsibilities:**
  * Offline-capable applications with instant interaction feedback and collaborative multiplayer syncing.
* **Enabling Libraries:** `electric-sql`, `replicache`, `yjs`, `automerge`, `tinybase`.

---

## 3. Comparative Synthesis Matrix

| Dimension | Server Cache (TanStack Query) | Client Store (Zustand) | Atomic State (Jotai) | Local-First Sync (Replicache/Yjs) |
| :--- | :--- | :--- | :--- | :--- |
| **Data Origin** | Remote Backend API / Database | Local Browser Memory | Local Browser Memory | Local Database synced with Cloud |
| **Network Model**| Asynchronous HTTP / REST / GraphQL | Synchronous In-Memory | Synchronous In-Memory | Asynchronous Event Log / CRDT Sync |
| **Staleness Handling**| Automatic (Stale-while-revalidate) | Manual (Developer must manage) | Manual (Developer must manage) | Real-time continuous replication |
| **Offline Writes**| Queue or fail on error | Ephemeral memory only | Ephemeral memory only | Full native offline write support |
| **Bundle Footprint**| ~12 KB | ~1 KB | ~3 KB | ~25 KB to 80 KB |
| **Primary Risk** | Over-fetching via bad query keys | Misused as an ad-hoc server cache | Scattered atoms; difficult traceability | High architectural and operational overhead |

---

## 4. The 80/20 Rule of Modern State

In 80% to 90% of business applications, developers who believe they need a global state manager (like Redux or Zustand) actually only need a server cache (like TanStack Query). 

When you adopt a server cache:
1. All network fetching, caching, loading spinners, and error alerts are managed declaratively.
2. The remaining client state is usually trivial: a modal visibility boolean, an active tab identifier, a search input string. This remaining state can comfortably reside in local component state (`useState`) or URL query parameters.
3. The need for a global client store often drops to zero.

---

## 5. Decision Playbook

```
                  [Where does the data canonically live?]
                                    │
               ├── On a Remote Database / API Backend
               │      └── Use a Server Cache: TanStack Query or SWR
               │          (Do not duplicate raw API data into global stores)
               │
               ├── On the Local Client Device Exclusively
               │      │
               │      Is it shared across multiple detached component trees?
               │            ├── No  ──> Local Component State (useState / useReducer)
               │            │           or URL Query Parameters
               │            └── Yes
               │                  │
               │                  Does it require atomic, fine-grained leaf subscriptions?
               │                        ├── Yes ──> Atomic State (Jotai)
               │                        └── No  ──> Lightweight Store (Zustand)
               │
               └── On Both (Instant local writes + offline + multi-client sync)
                      └── Use Local-First Sync Engine (ElectricSQL / Replicache / Yjs)
```

---

## 6. References & Library Audits
* [State and Cache Topologies (research notes)](../library/tools_and_frameworks/state_and_cache.md)
* [Further reading: *Designing Data-Intensive Applications* (Martin Kleppmann)](../library/reading_list.md)
* Tanner Linsley: *Inside React Query: The State Separation Revolution* (2020)
* Martin Kleppmann et al.: *Local-First Software: You Own Your Data, in spite of the Cloud* (2019)
