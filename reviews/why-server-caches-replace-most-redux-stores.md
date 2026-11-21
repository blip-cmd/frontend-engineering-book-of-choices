---
page: docs/essays/why_server_caches_replace_most_redux_stores.md
verified: 2026-11-21
---

# Claim Ledger: Essay, Why Server Caches Replace Most Redux Stores

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a React developer or tech lead deciding where server data should live in a front end. The page helps them decide whether to keep fetched data in a client store (Redux, Zustand, Pinia) or in a purpose-built query cache. Thesis (kept from the draft): server data is a cache of remote state, not client state; a query cache such as TanStack Query handles its lifecycle with far less code, and what remains for a global client store is usually small. The author pass added the exception the TanStack docs themselves name (apps with large synchronous client-only state) and noted that RTK Query offers the same model inside Redux; neither reverses the recommendation.

**History.** The AI-generated draft contained five unsourced numbers, all removed: custom data-fetching code "consumes 80% of an engineering team's time"; "over 90% of boilerplate ... disappear"; a state split of "80% to 90%" server cache, "5% to 10%" URL state, "5%" local state and "1% to 2%" global store; optimistic updates "within 16 milliseconds"; and a Zustand store "often under 50 lines". It also recommended keeping "authentication session tokens" in a Zustand store, which the rewrite replaces with the `HttpOnly` cookie guidance from MDN; called reconnect handling "polling"; said convention "dictated placing all application data" in Redux, which the Redux FAQ contradicts; and used "we must", which is gone.

---

## 1. Author pass (2026-11-21)

Sources were fetched in the same session with `curl` (TanStack, Redux and SWR docs from their source Markdown on GitHub, then confirmed on the live tanstack.com, redux.js.org and redux-toolkit.js.org pages); quotes were matched against the fetched text.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | Redux docs teach a request-status pattern; recommend a status enum over an `isLoading` boolean; separate success and failure action types | [Redux Fundamentals, Part 7](https://redux.js.org/tutorials/fundamentals/part-7-standard-patterns) | verified; step 2 corrected from "toggle a boolean" to the documented enum |
| 2 | Redux FAQ lists caching as a reason to store data in Redux; "Using local component state is fine" | [Redux FAQ: Organizing State](https://redux.js.org/faq/organizing-state) | verified (quote); replaced the draft's "conventional wisdom dictated placing all application data" in Redux |
| 3 | Redux evolves Flux "but avoids its complexity by taking cues from Elm" | [Redux: Prior Art](https://redux.js.org/understanding/history-and-design/prior-art) | verified (quote); replaced "implementation of Flux and the Elm Architecture" |
| 4 | Server state is remote, async, shared ("can be changed by other people without your knowledge") and can go out of date | [TanStack Query: Overview](https://tanstack.com/query/latest/docs/framework/react/overview) | verified (quote); draft's "inherently out of date the moment it finishes downloading" relabelled as the book's position |
| 5 | Queries "consider cached data as stale" by default; `staleTime` changes that | [Important Defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults) | verified (quote) |
| 6 | In-flight requests for the same key are deduplicated ("Deduping multiple requests for the same data into a single request"); after completion a new stale mount refetches | Overview; [Caching Examples](https://tanstack.com/query/latest/docs/framework/react/guides/caching); query-core 5.108.2 run | verified (quote and run: two observers, one fetch) |
| 7 | Inactive queries garbage-collected after `gcTime`, default 5 minutes | Important Defaults; [Migrating to v5](https://tanstack.com/query/latest/docs/framework/react/guides/migrating-to-v5) | verified; draft's "prevent browser memory leaks" reworded to "does not grow without limit" |
| 8 | Structural sharing keeps references when data is unchanged and replaces only changed parts | [Render Optimizations](https://tanstack.com/query/latest/docs/framework/react/guides/render-optimizations) | verified (quote and run: identical refetch kept the same reference) |
| 9 | Stale data is refetched in the background on window focus | [Window Focus Refetching](https://tanstack.com/query/latest/docs/framework/react/guides/window-focus-refetching) | verified (quote); draft's "after an hour away" removed |
| 10 | Requests pause offline and continue on reconnect; `refetchOnReconnect` | [Network Mode](https://tanstack.com/query/latest/docs/framework/react/guides/network-mode) | verified; "polling" corrected |
| 11 | Optimistic updates with rollback via `onMutate` context in `onError` | [Optimistic Updates](https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates) | verified; "within 16 milliseconds" removed (no source) |
| 12 | `useInfiniteQuery` keeps pages in `data.pages`; `hasNextPage` | [Infinite Queries](https://tanstack.com/query/latest/docs/framework/react/guides/infinite-queries) | verified; draft's "without race conditions" removed (not claimed by the docs) |
| 13 | Invalidate related queries in a mutation's `onSuccess`; returning the promise keeps `isPending` true until it settles | [Invalidations from Mutations](https://tanstack.com/query/latest/docs/framework/react/guides/invalidations-from-mutations) | verified (quote); snippet changed to return the promise |
| 14 | `invalidateQueries` marks matching queries stale and refetches rendered ones; matches by key prefix | [Query Invalidation](https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation) | verified (quote and run); draft comment "all mounted components update automatically" made precise |
| 15 | Hand-written cost: with `createAsyncThunk` "users still have to write significant amounts of reducer logic to manage the loading state and the cached data" | [RTK Query Overview](https://redux-toolkit.js.org/rtk-query/overview) | verified (quote); replaces the unsourced "80% of an engineering team's time" |
| 16 | v5 single-object signature; `isLoading` renamed `isPending`; `cacheTime` renamed `gcTime` | Migrating to v5 | verified; snippets already used v5 names |
| 17 | Code removed: connectors, action creators, middlewares, reducers, loading/error/result states, contexts | [Does TanStack Query replace Redux, MobX or other global state managers?](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state) | verified; labelled as the library's advocacy; replaces unsourced "over 90%" |
| 18 | RTK Query is included in Redux Toolkit; "'data fetching and caching' is really a different set of concerns than 'state management'" | RTK Query Overview | verified (quote) |
| 19 | Remaining global state in TanStack's example: `themeMode`, `sidebarStatus` | Does TanStack Query replace... | verified; replaces unsourced percentage split and "under 50 lines" |
| 20 | Apps like "a visual designer or music production application" still want a client state manager; TanStack Query "is not a replacement for local/client state management" | Does TanStack Query replace... | verified (quote); added as the counter-scenario |
| 21 | SWR is named after `stale-while-revalidate` (HTTP RFC 5861); dedup; revalidation on focus and network recovery | [SWR README](https://github.com/vercel/swr) | verified |
| 22 | Apollo Client stores results in a normalized, in-memory cache | [Apollo Client: Caching overview](https://www.apollographql.com/docs/react/caching/overview) | verified (quote) |
| 23 | nuqs: "Like useState, but stored in the URL query string" | [nuqs.dev](https://nuqs.dev/); `npm view nuqs description` | verified (quote) |
| 24 | `useState` / `useReducer` for local state | [React: Managing State](https://react.dev/learn/managing-state) | verified (page resolves; standard React API) |
| 25 | `HttpOnly` "Forbids JavaScript from accessing the cookie" and "mitigates attacks against cross-site scripting (XSS)" | [MDN: Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie) | verified (quote); replaces the draft's advice to keep session tokens in a Zustand store (G5) |
| 26 | Packages and versions: `@tanstack/react-query` 5.108.2, `@reduxjs/toolkit` 2.15.0, `swr` 2.5.1, `@apollo/client` 4.3.8, `zustand` 5.1.0, `nuqs` 2.10.3, `redux` 5.0.1, `react` 19.3.1 | `npm view <name> version` | verified |
| 27 | Both snippets are React fragments (need a component and `QueryClientProvider`) | query-core 5.108.2 under Node | labelled as fragments; their options and `invalidateQueries({ queryKey })` behaviour were run against `@tanstack/query-core` |
| 28 | Client state vs server cache taxonomy; "did this data originate from a network endpoint?" heuristic; form drafts as an exception | none | the book's positions, labelled as such on the page |

Note on row 7: under Node (no `window`), query-core reported `gcTime` as `Infinity`, which is TanStack's server-side default; the browser default is the documented 5 minutes.

## 2. Independent verifier pass (2026-11-21)

A separate agent that did not write the page or section 1 extracted the claims from the page itself and fetched every cited source in the same session with `curl`: the TanStack Query v5 guides as source Markdown from `TanStack/query` on GitHub (main), with the overview, Render Optimizations and "Does TanStack Query replace Redux" pages also confirmed live on tanstack.com (`latest` shows v5); the Redux Fundamentals Part 7, Redux FAQ, Prior Art and RTK Query Overview pages live; the SWR README; Apollo Client's caching overview; nuqs.dev (meta description); react.dev Managing State; and MDN Set-Cookie. Quotes were matched against the fetched text.

**Claims checked: 34** (section 1 pattern steps and enum recommendation; FAQ caching rule of thumb and "Using local component state is fine"; Prior Art quote; four server-state properties; stale-by-default; the nine mechanisms and their sources; `gcTime` 5 minutes; `createAsyncThunk` quote; package version claims; snippet behaviour; v5 object signature and `isPending`; prefix invalidation; removed-boilerplate list; RTK Query motivation quote; SWR, Apollo, nuqs, React and MDN claims; `themeMode`/`sidebarStatus` example; visual designer and music production exception; "is not a replacement" quote). The client/server taxonomy, the origin test and the form-draft exception are the book's positions and are labelled as such.

**Results.** 31 SUPPORTED, 3 PARTIAL (all corrected below), 0 UNSUPPORTED. No first-person experience. Every number (5 minutes, version numbers with their date, four kinds of server data, RFC 5861) has a source in the same paragraph.

**Edits made**

| Where | Before | After | Reason |
| :--- | :--- | :--- | :--- |
| Section 3, item 4 (structural sharing) | "so values passed to `useMemo`, `useCallback` and memoized components stay stable" | "so the `data` returned from the hooks stays as stable as possible" | PARTIAL: Render Optimizations says the `data` properties "will be as stable as possible"; it does not mention `useMemo`, `useCallback` or memoized components in this context |
| Section 3, item 9 (invalidation) | "marking affected queries stale when an edit or delete succeeds, so they refetch" | "invalidating related queries when an edit or delete succeeds, so they can be refetched to account for the change" | PARTIAL: the guide says related queries "need to be invalidated and possibly refetched"; only rendered queries refetch (Query Invalidation) |
| Section 5, item 1 (SWR) | "the `stale-while-revalidate` strategy of HTTP RFC 5861" | "`stale-while-revalidate`, a cache invalidation strategy popularized by HTTP RFC 5861" | PARTIAL: the SWR README says "popularized by", not defined by |

**Code and package checks.** `npm view` on 2026-11-21: `@tanstack/react-query` 5.108.2, `@tanstack/query-core` 5.108.2, `@reduxjs/toolkit` 2.15.0, `swr` 2.5.1, `@apollo/client` 4.3.8, `zustand` 5.1.0, `nuqs` 2.10.3, `redux` 5.0.1, `react` 19.3.1; the two versions stated on the page match. `@tanstack/react-query` 5.108.2 exports `useQuery`, `useMutation`, `useQueryClient`, `QueryClientProvider` and `useInfiniteQuery`. Both snippets are labelled fragments and use the v5 object signature and `isPending`. Their options were run under Node against `@tanstack/query-core` 5.108.2 with `QueryObserver` and `MutationObserver`: two observers on `['users', 7]` while in flight made one fetch and shared one data reference; a third mount within `staleTime` made no request; a mount with `staleTime: 0` refetched in the background and structural sharing kept the identical object's reference; the mutation's `onSuccess` returning `invalidateQueries({ queryKey: ['users', userId] })` refetched the active query once and the mutation was still `isPending` while it ran, and unchanged nested data kept its reference; `invalidateQueries({ queryKey: ['users'] })` refetched the active `['users', 7]` and marked the inactive `['users', 'list']` invalidated (prefix match).

**Verdict: PASS.**

## 3. Known omissions (follow-up content, not errors)

* Server Components and framework loaders (Next.js App Router, React Router) as an alternative to a client query cache
* Normalized caches (Apollo, RTK Query tags) versus TanStack Query's key-based invalidation, and when normalization pays off
* Hydrating a query cache from server-rendered data (TanStack `HydrationBoundary`)
* Offline-first and sync-engine approaches, where client and server state merge
* Migration path from an existing Redux store to RTK Query or TanStack Query

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | **19** |

D9 is 1 because the snippets are fragments without error handling or a full scenario. G8 (human accountability) is not met; an `agent-verified` status would disclose that instead.
