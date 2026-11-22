---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: tanstack-query 5.108.2, swr 2.5.1, redux-toolkit 2.15.0, zustand 5.1.0, pinia 4.1.0, jotai 3.0.2, nanostores 1.5.5, yjs 13.6.33, automerge 3.5.0, tinybase 10.1.0, replicache 15.3.0, electric-sql client 1.5.28; official docs of each, react.dev, Bundlephobia API (2026-11-21)
review_by: 2027-05
reviewers:
ledger: reviews/state-and-cache-topologies.md
---

# Chapter 3: State and Cache Topologies: Client State Stores vs. Remote Server Caches

> Data fetched from a server is a cached copy that other people can change. Handling it as if it were local, synchronous memory produces stale screens, duplicate requests and race conditions. This chapter is for a tech lead choosing a state approach: it separates the two kinds of state and names the tools that fit each.

---

## 1. Why One Global Store for All Data Causes Bugs

Redux and Vuex were built around one central store. Redux's first principle is that "the global state of your application is stored in an object tree within a single store" ([Redux: Three Principles](https://redux.js.org/understanding/thinking-in-redux/three-principles)), and Vuex "uses a single state tree" ([Vuex: State](https://vuex.vuejs.org/guide/state.html)). MobX is different: its docs describe one or several domain stores ([MobX: Defining data stores](https://mobx.js.org/defining-data-stores.html)). For new Vue projects, the Vuex docs themselves recommend Pinia instead ([What is Vuex?](https://vuex.vuejs.org/)).

When server responses go into such a store, the application has to solve by hand the problems a cache library solves for it:
* **Request bookkeeping.** The RTK Query docs list "tracking loading state in order to show UI spinners", "avoiding duplicate requests for the same data", optimistic updates and "managing cache lifetimes" as behaviors applications need, and note that with `createAsyncThunk` alone, users "still have to write significant amounts of reducer logic to manage the loading state and the cached data" ([RTK Query overview](https://redux-toolkit.js.org/rtk-query/overview)).
* **Staleness.** Data copied from the server sits in the store while the database changes underneath it. TanStack Query notes that server state can be changed by other people without the client knowing, so the client copy can go out of date ([TanStack Query overview](https://tanstack.com/query/latest/docs/framework/react/overview)).
* **Race conditions.** When two requests are in flight, "there is no guarantee about which order the responses will arrive in", so an older response can overwrite a newer one ([react.dev: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)).
* **Deduplication, background updates and invalidation.** TanStack Query's overview lists deduping requests and updating out-of-date data in the background among the challenges server state adds ([TanStack Query overview](https://tanstack.com/query/latest/docs/framework/react/overview)).

The fix is to split state into two categories with different owners. **Server state** is a remote cache: TanStack Query describes it as "persisted remotely in a location you may not control or own", requiring "asynchronous APIs" and implying "shared ownership" ([TanStack Query overview](https://tanstack.com/query/latest/docs/framework/react/overview)). **Client state** is UI state that only the browser session owns.

---

## 2. Which Tool Owns Each Kind of State

### Category 1: Remote Server Caches (TanStack Query 5, SWR 2, RTK Query in Redux Toolkit 2)
* **Mental model:** the client does not own this data. It holds a temporary snapshot of data that belongs to a remote database.
* **What these libraries handle:**
  * Caching with configurable freshness. TanStack Query treats cached data as stale by default; `staleTime` sets how long data stays fresh and `gcTime` (renamed from `cacheTime` in v5) sets when inactive queries are removed ([Important defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults); [Migrating to v5](https://tanstack.com/query/latest/docs/framework/react/guides/migrating-to-v5)). SWR is named after the stale-while-revalidate cache strategy from HTTP RFC 5861 ([SWR](https://swr.vercel.app/)). In RTK Query, `keepUnusedDataFor` sets how long data stays cached after the last component unsubscribes ([RTK Query createApi](https://redux-toolkit.js.org/rtk-query/api/createApi)).
  * Request deduplication. Components that use the same key (SWR) or the same query arguments (RTK Query) share one request ([SWR](https://swr.vercel.app/); [RTK Query: Queries](https://redux-toolkit.js.org/rtk-query/usage/queries)).
  * Refetching when the window regains focus or the network reconnects. This is on by default in TanStack Query and SWR ([Important defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults); [SWR: Revalidation](https://swr.vercel.app/docs/revalidation)) and off by default in RTK Query, where `refetchOnFocus` and `refetchOnReconnect` default to `false` ([RTK Query createApi](https://redux-toolkit.js.org/rtk-query/api/createApi)).
  * Optimistic updates with rollback. SWR rolls back on error by default (`rollbackOnError = true`) ([SWR: Mutation](https://swr.vercel.app/docs/mutation)). In TanStack Query you snapshot the previous value in `onMutate` and restore it in `onError` ([Optimistic updates](https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates)). In RTK Query you call `.undo()` on the result of the earlier patch ([Manual cache updates](https://redux-toolkit.js.org/rtk-query/usage/manual-cache-updates)).
* **Packages:** `@tanstack/react-query`, `swr`, and `@reduxjs/toolkit` (RTK Query is imported from `@reduxjs/toolkit/query`, or `@reduxjs/toolkit/query/react` for generated React hooks).

### Category 2: Centralized Client Stores (Zustand 5, Pinia for Vue, Redux Toolkit 2)
* **Mental model:** a single or slice-based synchronous store owned by the browser session. In Zustand the store is a hook used without providers, and a component re-renders when the state it selects changes ([Zustand README](https://github.com/pmndrs/zustand)).
* **Typical uses (the book's judgment):**
  * Multi-step wizard state.
  * Audio or video playback queues, timeline scrubbers and canvas coordinates.
  * Selections shared across components, such as table rows selected for a bulk action.
* **Packages:** `zustand`, `pinia`, `@reduxjs/toolkit`.

### Category 3: Atomic State (Jotai 3, Nano Stores 1)
* **Mental model:** state split into small atoms defined outside components, with each component subscribing to the atoms it reads. In Jotai an atom is a config object that "doesn't hold a value"; "the atom value exists in a store" ([Jotai: atom](https://github.com/pmndrs/jotai/blob/main/docs/core/atom.mdx)). Nano Stores "uses many atomic stores" and works with React, Vue, Svelte and other frameworks ([Nano Stores README](https://github.com/nanostores/nanostores)).
* **Typical uses (the book's judgment):**
  * Component trees where distant children share state without re-rendering a common parent.
  * Canvas editors with many independently draggable elements.
* **Packages:** `jotai`, `nanostores`. Recoil, an experimental atom-based library from Meta ([Recoil: Core concepts](https://recoiljs.org/docs/introduction/core-concepts)), is archived on GitHub ([facebookexperimental/Recoil](https://github.com/facebookexperimental/Recoil)); do not start new projects on it.

### Category 4: Local-First Sync (Yjs, Automerge, TinyBase, Replicache, Electric)
* **Mental model:** the application reads and writes a local replica (an in-memory CRDT document, IndexedDB, or an embedded database), and a sync layer exchanges changes with the server or other clients in the background.
* **What it is for:** offline-capable and collaborative applications where interactions must not wait for the network.
* **Packages, and how they differ:**
  * `yjs` (13.x) and `@automerge/automerge` (3.x) merge concurrent edits. Yjs is "a CRDT implementation", is "network agnostic" and supports offline editing ([Yjs README](https://github.com/yjs/yjs)); when users make overlapping edits, Automerge "performs a consistent merge", and offline "changes queue locally, and everything syncs when you reconnect" ([Automerge](https://automerge.org/)). The older `automerge` package is deprecated on npm in favour of `@automerge/automerge`.
  * `tinybase` (10.x) is "a reactive in-memory data store with persistence and synchronization" with native CRDT support ([TinyBase](https://tinybase.org/)).
  * `replicache` (15.x) stores data persistently in the browser and queues changes while offline, but its maintainers state that it "is now in maintenance mode" and that existing users "should migrate to Zero" ([Replicache](https://replicache.dev/)).
  * Electric is "a read-path sync engine for Postgres": it syncs data out of Postgres to clients over HTTP, and it does not do write-path sync, so the application chooses how writes get back into Postgres ([Electric Sync](https://electric.ax/docs/intro); [Electric: Writes](https://electric.ax/docs/guides/writes)). Its client is `@electric-sql/client`; the older `electric-sql` package is deprecated on npm.

---

## 3. How the Four Approaches Compare

| Dimension | Server Cache (TanStack Query 5) | Client Store (Zustand 5) | Atomic State (Jotai 3) | Local-First Sync (Yjs 13, Replicache 15) |
| :--- | :--- | :--- | :--- | :--- |
| **Data origin** | Remote backend API or database | Browser memory | Browser memory | Local replica synced with a server or peers |
| **Network model** | Asynchronous requests (REST, GraphQL, any promise) | Synchronous, in memory | Synchronous, in memory | Background sync of changes (CRDT updates or queued mutations) |
| **Staleness handling** | Automatic background refetch of stale queries ([defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)) | Manual | Manual | Continuous background sync |
| **Offline writes** | In the default `online` network mode, mutations do not fire without a connection ([Network mode](https://tanstack.com/query/latest/docs/framework/react/guides/network-mode)) | Memory only, lost on reload | Memory only, lost on reload | Written locally and synced on reconnect ([Replicache](https://replicache.dev/); [Yjs](https://github.com/yjs/yjs)) |
| **Bundle size** (min + gzip) | 13.4 kB ([5.108.2](https://bundlephobia.com/package/@tanstack/react-query@5.108.2)) | 0.5 kB ([5.1.0](https://bundlephobia.com/package/zustand@5.1.0)) | 3.3 kB ([3.0.2](https://bundlephobia.com/package/jotai@3.0.2)) | Yjs 28.2 kB ([13.6.33](https://bundlephobia.com/package/yjs@13.6.33)); Replicache 35.2 kB ([15.3.0](https://bundlephobia.com/package/replicache@15.3.0)) |
| **Primary risk** (the book's judgment) | Over-fetching or cache misses from badly designed query keys | Used as an ad-hoc server cache | Scattered atoms that are hard to trace | High architectural and operational overhead |

Bundle sizes are the `gzip` field of the [Bundlephobia API](https://bundlephobia.com/) for the linked version, read on 2026-11-21 and divided by 1,000; they exclude peer dependencies such as React.

---

## 4. Reach for a Server Cache Before a Global Client Store

**Our recommendation:** in a business application whose data lives behind an API, start with a server cache such as TanStack Query or SWR, and add a global client store only for client-only state that several distant components share. The TanStack Query docs argue the same: "for a vast majority of applications, the truly globally accessible client state that is left over after migrating all of your async code to TanStack Query is usually very tiny" ([Does TanStack Query replace Redux, MobX or other global state managers?](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state)). That page is written by the library's maintainers, so read it as advocacy as well as documentation.

When you adopt a server cache:
1. Fetching, caching, loading and error states are declared per query instead of written as reducers and actions.
2. The remaining client state is often small: a modal's visibility, the active tab, a search string. It can live in component state (`useState`) or in URL query parameters.
3. A global client store may no longer be needed.

**When not to:** the same TanStack page names "a visual designer or music production application" as cases with "a massive amount of synchronous client-only state", where a client state manager is still worth having alongside the server cache ([TanStack Query docs](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state)).

---

## 5. Decision Playbook

Start from where the data canonically lives. Server-owned data goes to a server cache. Client-only data stays in component state or the URL unless detached component trees share it; then use an atomic library when components need fine-grained subscriptions, and a store otherwise. Data that must be written locally, work offline and sync across clients needs a local-first sync engine.

```text
                  [Where does the data canonically live?]
                                    │
               ├── On a remote database / API backend
               │      └── Use a server cache: TanStack Query or SWR
               │          (Do not copy raw API data into global stores)
               │
               ├── On the client device only
               │      │
               │      Is it shared across multiple detached component trees?
               │            ├── No  ──> Local component state (useState / useReducer)
               │            │           or URL query parameters
               │            └── Yes
               │                  │
               │                  Does it need fine-grained, per-atom subscriptions?
               │                        ├── Yes ──> Atomic state (Jotai)
               │                        └── No  ──> Lightweight store (Zustand)
               │
               └── On both (instant local writes + offline + multi-client sync)
                      └── Use a local-first sync engine (Yjs or Automerge;
                          Electric for syncing Postgres data to clients)
```

---

## 6. References
* [Further reading: *Designing Data-Intensive Applications* (Martin Kleppmann)](../library/reading_list.md)
* TanStack Query docs: [Does TanStack Query replace Redux, MobX or other global state managers?](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state)
* Redux Toolkit docs: [RTK Query overview](https://redux-toolkit.js.org/rtk-query/overview)
* Martin Kleppmann, Adam Wiggins, Peter van Hardenberg and Mark McGranaghan: [*Local-first software: You own your data, in spite of the cloud*](https://www.inkandswitch.com/essay/local-first/), Onward! 2019
