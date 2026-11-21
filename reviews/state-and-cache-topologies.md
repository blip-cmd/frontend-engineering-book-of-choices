---
page: book/03_state_and_cache_topologies.md
verified: 2026-11-21
---

# Claim Ledger: Chapter 3, State and Cache Topologies

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead or senior frontend developer choosing how a web application holds data. The page helps them decide which kind of tool owns each kind of state: a server cache, a client store, atomic state, or a local-first sync engine. Thesis (unchanged from the draft): server state and client state are different problems; data the server owns belongs in a server cache, and most of what remains is small enough for component state or the URL, so a global client store is often unnecessary.

**History.** The AI-generated draft was rewritten by the author pass on 2026-11-21. Main corrections: the draft said all three server caches roll back optimistic updates automatically (only SWR does; TanStack Query and RTK Query need manual rollback); it grouped MobX with single-store libraries (MobX documents multiple domain stores); it presented ElectricSQL as a local SQLite write-path sync engine (Electric is a read-path sync engine for Postgres, and the `electric-sql` package is deprecated); it did not say Replicache is in maintenance mode; it cited a non-existent Tanner Linsley talk ("Inside React Query" is a TkDodo blog post from December 2022); its bundle sizes had no source; and its "80% to 90% of business applications" figure had no source. No recommendation was changed.

---

## 1. Author pass (2026-11-21)

Sources were fetched in the same session with `curl` and searched as text; package versions were checked with `npm view` on 2026-11-21.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | Redux: "the global state of your application is stored in an object tree within a single store" | [Redux: Three Principles](https://redux.js.org/understanding/thinking-in-redux/three-principles) | verified (quote) |
| 2 | Vuex "uses a single state tree" | [Vuex: State](https://vuex.vuejs.org/guide/state.html) | verified (quote) |
| 3 | Draft: MobX encouraged a single centralized store | [MobX: Defining data stores](https://mobx.js.org/defining-data-stores.html) ("one or multiple domain stores") | corrected: MobX now described as using one or several domain stores |
| 4 | Vuex docs recommend Pinia for new projects | [What is Vuex?](https://vuex.vuejs.org/) | verified ("we highly recommend using Pinia instead") |
| 5 | RTK Query motivation list (loading state, duplicate requests, optimistic updates, cache lifetimes); "significant amounts of reducer logic" | [RTK Query overview](https://redux-toolkit.js.org/rtk-query/overview) | verified (quote); replaced the unsourced "hundreds of lines of boilerplate" |
| 6 | Server state is "persisted remotely in a location you may not control or own", needs "asynchronous APIs", implies "shared ownership", can go out of date; deduping and background updates are listed challenges | [TanStack Query overview](https://tanstack.com/query/latest/docs/framework/react/overview) | verified (quote) |
| 7 | Race condition: "there is no guarantee about which order the responses will arrive in" | [react.dev: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) | verified (quote) |
| 8 | TanStack Query treats cached data as stale by default; `staleTime`; inactive queries garbage-collected per `gcTime` | [Important defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults) | verified |
| 9 | `cacheTime` renamed to `gcTime` in v5 | [Migrating to v5](https://tanstack.com/query/latest/docs/framework/react/guides/migrating-to-v5) | verified ("Rename cacheTime to gcTime") |
| 10 | SWR named after stale-while-revalidate from HTTP RFC 5861 | [SWR home](https://swr.vercel.app/) | verified (quote) |
| 11 | RTK Query cache lifetime option `keepUnusedDataFor` | [RTK Query createApi](https://redux-toolkit.js.org/rtk-query/api/createApi) | verified |
| 12 | Deduplication: SWR by key; RTK Query by serialized query arguments | [SWR home](https://swr.vercel.app/); [RTK Query: Queries](https://redux-toolkit.js.org/rtk-query/usage/queries) | verified |
| 13 | Focus and reconnect refetching on by default in TanStack Query and SWR | [Important defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults); [SWR: Revalidation](https://swr.vercel.app/docs/revalidation) | verified ("enabled by default") |
| 14 | RTK Query `refetchOnFocus` and `refetchOnReconnect` default to `false` | [RTK Query createApi](https://redux-toolkit.js.org/rtk-query/api/createApi) | verified ("Defaults to false"); added, draft implied all three refetch automatically |
| 15 | Draft: "Optimistic mutations with automatic rollback" for all server caches | [SWR: Mutation](https://swr.vercel.app/docs/mutation) (`rollbackOnError = true`); [TanStack: Optimistic updates](https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates) (`onMutate` snapshot, restore in `onError`); [RTK Query: Manual cache updates](https://redux-toolkit.js.org/rtk-query/usage/manual-cache-updates) (`.undo`) | corrected: automatic only in SWR |
| 16 | Import paths `@reduxjs/toolkit/query` and `@reduxjs/toolkit/query/react` | `npm view @reduxjs/toolkit exports`; [RTK Query overview](https://redux-toolkit.js.org/rtk-query/overview) | verified |
| 17 | Zustand store is a hook, no providers, component re-renders on selected state changes | [Zustand README](https://github.com/pmndrs/zustand) | verified |
| 18 | Jotai atom config "doesn't hold a value"; "the atom value exists in a store" | [Jotai docs: atom](https://github.com/pmndrs/jotai/blob/main/docs/core/atom.mdx) | verified (quote); corrects the draft's "atoms reside outside the React tree" |
| 19 | Nano Stores "uses many atomic stores"; works with React, Vue, Svelte and others | [Nano Stores README](https://github.com/nanostores/nanostores) | verified (quote) |
| 20 | Recoil is an experimental atom-based library from Meta, archived on GitHub | [Recoil: Core concepts](https://recoiljs.org/docs/introduction/core-concepts); GitHub API `repos/facebookexperimental/Recoil` (`archived: true`) | verified; draft's "early 2025" date dropped (the API does not expose the archive date; last push 2025-01-01) and "popularised this model" removed as unsourced |
| 21 | Yjs is a CRDT implementation, "network agnostic", supports offline editing | [Yjs README](https://github.com/yjs/yjs) | verified (quote) |
| 22 | Automerge: offline "changes queue locally, and everything syncs when you reconnect" | [Automerge](https://automerge.org/) | verified (quote) |
| 23 | `automerge` npm package deprecated in favour of `@automerge/automerge` | `npm view automerge deprecated` ("Please see @automerge/automerge instead.") | verified; draft listed `automerge` |
| 24 | TinyBase is "a reactive in-memory data store with persistence and synchronization", native CRDT support | [TinyBase](https://tinybase.org/) | verified (quote) |
| 25 | Replicache stores data in the browser, queues changes offline; "is now in maintenance mode"; users "should migrate to Zero" | [Replicache](https://replicache.dev/) | verified (quote); added, draft omitted the status |
| 26 | Electric is "a read-path sync engine for Postgres", syncs to clients over HTTP; writes go through your API | [Electric Sync](https://electric.ax/docs/intro) (redirect from electric-sql.com); [Electric: Writes](https://electric.ax/docs/guides/writes) | verified (quote); corrected the draft's "SQLite in Wasm, synchronous local reads and writes" description |
| 27 | `electric-sql` npm package deprecated; client is `@electric-sql/client` | `npm view electric-sql deprecated`; `npm view @electric-sql/client version` (1.5.28) | verified |
| 28 | Draft: local-first reads and writes "happen synchronously against local disk" | IndexedDB and network sync are asynchronous | removed; rewritten as "reads and writes a local replica" |
| 29 | Pinned majors: @tanstack/react-query 5.108.2, swr 2.5.1, zustand 5.1.0, jotai 3.0.2, nanostores 1.5.5, @reduxjs/toolkit 2.15.0, pinia 4.1.0, yjs 13.6.33, @automerge/automerge 3.5.0, tinybase 10.1.0, replicache 15.3.0 | `npm view <name> version`, 2026-11-21 | verified |
| 30 | TanStack Query default `online` network mode: queries and mutations do not fire without a connection | [Network mode](https://tanstack.com/query/latest/docs/framework/react/guides/network-mode) | verified (quote); replaced the draft's "Queue or fail on error" |
| 31 | Bundle sizes, min + gzip, `gzip` field of Bundlephobia API: @tanstack/react-query 5.108.2 13,352 B; zustand 5.1.0 491 B; jotai 3.0.2 3,307 B; yjs 13.6.33 28,163 B; replicache 15.3.0 35,247 B | [Bundlephobia](https://bundlephobia.com/) (`/api/size?package=<name>@<version>`) | verified (reproducible); draft's "~12 KB", "~1 KB", "~3 KB", "~25 KB to 80 KB" replaced |
| 32 | Draft: "In 80% to 90% of business applications ... only need a server cache" | none found | removed; rewritten as the book's labelled position ("Our recommendation:") with the TanStack maintainers' qualitative statement, labelled advocacy |
| 33 | TanStack: leftover global client state "is usually very tiny"; visual designer or music production apps keep "a massive amount of synchronous client-only state" | [Does TanStack Query replace Redux, MobX or other global state managers?](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state) | verified (quote); the second quote is used as the section's "when not to" |
| 34 | Kleppmann, Wiggins, van Hardenberg, McGranaghan, *Local-first software: You own your data, in spite of the cloud*, Onward! 2019 | [Ink & Switch essay](https://www.inkandswitch.com/essay/local-first/) | verified; draft's "Kleppmann et al." given full authors and a link |
| 35 | Draft reference: Tanner Linsley, *Inside React Query: The State Separation Revolution* (2020) | [TkDodo: Inside React Query](https://tkdodo.eu/blog/inside-react-query) (Dominik Dorfmeister, 2022-12-03) | removed: misattributed, invented subtitle; replaced with the TanStack docs page |
| 36 | Draft reference to `library/tools_and_frameworks/state_and_cache.md` research notes | unverified AI summary | removed; primary sources cited inline instead |
| 37 | Draft epigraph: "Most bugs in modern frontend applications ... stem from" mismanaging remote data | none | removed as an unsourced quantity; rewritten as the chapter's framing |
| 38 | Typical uses per category, primary-risk row, decision tree | none | the book's judgment; labelled as such on the page |
| 39 | Code examples | none on the page | the only code block is a text decision tree, tagged `text`; nothing to run |

## 2. Independent verifier pass (2026-11-21)

**Verdict: PASS.** A separate agent that did not write the page extracted 50 claims from it independently and checked each against its cited source, fetched on 2026-11-21 with `curl -sL` and searched as stripped text. 46 were SUPPORTED, 4 were PARTIAL and are corrected below, none were UNSUPPORTED, and the remaining unsourced sentences are explanatory background or labelled as the book's judgment, with no numbers.

Sources fetched: all 29 linked pages (Redux, Vuex x2, MobX, RTK Query overview, queries, createApi and manual cache updates, TanStack Query overview, important defaults, migrating to v5, optimistic updates, network mode and "does this replace client state", SWR home, revalidation and mutation, react.dev, Zustand, Jotai `atom.mdx`, Nano Stores, Recoil core concepts and GitHub repo, Yjs, Automerge, TinyBase, Replicache, Electric intro and writes guide, Ink & Switch essay). Every quote was found verbatim. Recoil's archived status was confirmed with the GitHub API (`archived: true`).

Edits (each a rewording to match the source; no claims or sources added):

| Claim | Verdict | Edit |
| :--- | :--- | :--- |
| RTK Query: the four jobs "otherwise need 'significant amounts of reducer logic'" | PARTIAL: the source lists the behaviors, then says users of `createAsyncThunk` "still have to write significant amounts of reducer logic to manage the loading state and the cached data"; it does not tie the phrase to all four jobs | quoted the full source sentence with its `createAsyncThunk` context |
| "RTK Query uses `keepUnusedDataFor`" (under configurable freshness) | PARTIAL: the option is a cache lifetime, "how long RTK Query will keep your data cached for after the last component unsubscribes", not freshness | reworded to that meaning |
| `yjs` and `@automerge/automerge` "are CRDT libraries" | PARTIAL: the Yjs README says "a CRDT implementation"; the cited automerge.org page never says CRDT, only that Automerge "performs a consistent merge" | attributed "a CRDT implementation" to Yjs and "performs a consistent merge" to Automerge |
| Electric: "writes go back through your own API" | PARTIAL: the writes guide says Electric "does not do write-path sync" and describes four write patterns, including through-the-database sync, not only API calls | reworded to "does not do write-path sync, so the application chooses how writes get back into Postgres" |

Numbers and packages:

* `npm view <name> version` on 2026-11-21 confirmed every pinned version in row 29, plus `@electric-sql/client` 1.5.28; `automerge` and `electric-sql` are deprecated on npm; `@reduxjs/toolkit` exports `./query` and `./query/react`.
* Bundlephobia API `gzip` fields re-read on 2026-11-21 match the page exactly: 13,352 B, 491 B, 3,307 B, 28,163 B and 35,247 B for the linked versions (13.4, 0.5, 3.3, 28.2 and 35.2 kB after dividing by 1,000).

Code checks: the page has no JavaScript; its only code block is a `text` decision tree, so nothing was run.

## 3. Known omissions (follow-up content, not errors)

Topics a complete chapter could add, each needing its own sourced entry:

* Zero (Rocicorp), named on the page only as Replicache's successor, and TanStack DB, which Electric's docs list as a sync primitive
* Persisting the TanStack Query cache and paused mutations across reloads (`persistQueryClient`, `offlineFirst` network mode)
* URL state as a first-class store (search params in React Router or Next.js)
* Server Components and framework loaders (React 19, Next.js) reducing the need for a client-side server cache
* Vue- and Svelte-specific options (Pinia setup stores, TanStack Query for Vue, Svelte runes)
* Signals-based state (Preact Signals, Angular signals), covered in Chapter 2 but not cross-referenced here
* Apollo Client and urql normalized caches for GraphQL

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | N/A | 2 | **19** (17 of 18 points, scaled) |

D2 is 1 because only Section 4 has a concrete "when not to"; the categories in Section 2 do not each state when they are the wrong choice. D9 is N/A: the page has no code examples. Gate G8 (human accountability) is met in its agent-verified form: both protocol passes are recorded here, and the page tells readers it has not been reviewed by a human expert.
