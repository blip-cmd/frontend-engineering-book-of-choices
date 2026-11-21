---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: tanstack-query 5.108.2 docs, redux docs, redux-toolkit 2.15.0 (RTK Query overview), swr 2.5.1 README, apollo-client 4.x caching overview, nuqs 2.10.3, react.dev, MDN Set-Cookie
review_by: 2027-05
reviewers:
ledger: reviews/why-server-caches-replace-most-redux-stores.md
---

# Why Server Caches Replace Most Redux Stores

> An essay for a React developer or tech lead deciding where server data should live. Its position: data fetched from a server is a cache of someone else's state, and a purpose-built query cache handles it with far less code than a hand-written client store. The essay also names the applications where a client store still earns its place.

---

## 1. How server data ended up in Redux stores

The Redux docs teach a standard pattern for tracking a request in the store ([Redux Fundamentals, Part 7: Standard Redux Patterns](https://redux.js.org/tutorials/fundamentals/part-7-standard-patterns)). For each request it looks like this:

1. Dispatch an action when the request starts (`FETCH_USERS_REQUEST`).
2. Set a status field in a reducer (the docs recommend an enum such as `status: 'loading'` over an `isLoading` boolean).
3. Make the HTTP request with `fetch` or `axios`.
4. Dispatch a success or failure action (`FETCH_USERS_SUCCESS`) with the payload.
5. Store the server response in the global state tree.
6. Write selectors that slice, memoize and project that data into components.

An app that uses this pattern for every entity repeats these steps for users, billing items, comments, permissions and notifications. The Redux FAQ lists caching as a reason to put data in Redux ("use what's in state if it's already there instead of re-requesting it"), while also saying "Using local component state is fine" ([Redux FAQ: Organizing State](https://redux.js.org/faq/organizing-state)).

Redux's docs describe it as evolving the ideas of Flux "but avoids its complexity by taking cues from Elm" ([Redux: Prior Art](https://redux.js.org/understanding/history-and-design/prior-art)). The book's position is that Redux is a sound design, and that the costly mistake was treating **server-origin data** as if it were **client state**.

---

## 2. Two kinds of data: client state and server cache

Deciding where a piece of data lives starts with sorting it into one of two categories.

### Client state: owned by the browser session

Data that is created, owned and changed entirely within the user's browser session:

* Whether a modal or dialog is open.
* The active tab and whether a navigation drawer is open.
* Controlled form inputs before submission.
* Theme (light or dark) and layout column widths, until they are saved to an account.

Client state is synchronous: the app changes it directly, and nobody else can change it.

### Server cache: a copy of state the server owns

Data persisted on backend databases:

* User profile records.
* Shopping cart contents saved to an account.
* Inventory availability and account balances.
* Team member permissions and activity feeds.

TanStack Query's docs list what makes server state different: it is persisted remotely, in a location you may not control; it needs asynchronous APIs to fetch and update; it has shared ownership and "can be changed by other people without your knowledge"; and it can become out of date ([TanStack Query: Overview](https://tanstack.com/query/latest/docs/framework/react/overview)). TanStack Query v5 builds that last point into its defaults: queries "consider cached data as stale" unless you set a `staleTime` ([Important Defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)). The book's position follows from this: what the client holds is a **snapshot of remote state that may already be stale**, and code should treat it that way.

---

## 3. Nine problems a hand-written server cache must solve

An application that keeps server data in a client store (Redux, Zustand, Pinia) has to write its own answer to each of these problems. Most of them appear in the challenges list of [TanStack Query's overview](https://tanstack.com/query/latest/docs/framework/react/overview), and the mechanisms named below are TanStack Query v5's:

1. **Deduplication:** two components that mount with the same query key while a request is in flight share that request and one cache entry, instead of firing two ([the overview](https://tanstack.com/query/latest/docs/framework/react/overview) lists "Deduping multiple requests for the same data into a single request"). Once that request has finished and the data is stale, a newly mounted component triggers a background refetch ([Caching Examples](https://tanstack.com/query/latest/docs/framework/react/guides/caching)).
2. **Staleness tracking:** deciding whether cached data is fresh enough to render or needs a background refetch (`staleTime`).
3. **Garbage collection:** deleting cache entries nobody uses so the cache does not grow without limit. TanStack Query removes inactive queries after a `gcTime` that defaults to 5 minutes ([Important Defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)).
4. **Structural sharing:** keeping the same object references when a refetch returns identical data, and replacing only the parts that changed, so the `data` returned from the hooks stays as stable as possible ([Render Optimizations](https://tanstack.com/query/latest/docs/framework/react/guides/render-optimizations)).
5. **Refetch on window focus:** requesting fresh data in the background when a user returns to the tab and the data is stale ([Window Focus Refetching](https://tanstack.com/query/latest/docs/framework/react/guides/window-focus-refetching)).
6. **Offline and reconnect handling:** pausing requests while the device is offline and resuming them, or refetching stale data, when the connection returns ([Network Mode](https://tanstack.com/query/latest/docs/framework/react/guides/network-mode)).
7. **Optimistic updates:** showing the result of a mutation before the server confirms it, and rolling it back if the request fails ([Optimistic Updates](https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates)).
8. **Pagination and infinite scroll:** keeping fetched pages together and knowing whether another page exists (`useInfiniteQuery`, `hasNextPage`) ([Infinite Queries](https://tanstack.com/query/latest/docs/framework/react/guides/infinite-queries)).
9. **Invalidation after mutations:** invalidating related queries when an edit or delete succeeds, so they can be refetched to account for the change ([Invalidations from Mutations](https://tanstack.com/query/latest/docs/framework/react/guides/invalidations-from-mutations)).

The Redux team describes the cost of solving these by hand. Even with Redux Toolkit's `createAsyncThunk`, "users still have to write significant amounts of reducer logic to manage the loading state and the cached data" ([RTK Query Overview](https://redux-toolkit.js.org/rtk-query/overview)).

---

## 4. What a query cache changes: keys, staleness and invalidation

TanStack Query v5 (`@tanstack/react-query`, version 5.108.2 on npm on 2026-11-21) stores each result under a query key, an array that identifies the data. Components ask for a key, and the cache decides whether to fetch. The following fragment runs inside a React component rendered under a `QueryClientProvider`; `fetchUserById` and `userId` come from your application:

```typescript
// Fragment: inside a React component under <QueryClientProvider>.
// Components that use the same key share one cache entry, and requests
// already in flight for that key are deduplicated.
const { data: user, isPending, error } = useQuery({
  queryKey: ['users', userId],
  queryFn: () => fetchUserById(userId),
  staleTime: 1000 * 60 * 5, // treat the data as fresh for 5 minutes
});
```

After a mutation succeeds, you invalidate the affected keys instead of writing a reducer that patches the stored copy:

```typescript
// Fragment: inside the same component; updateUserName is your API call.
const queryClient = useQueryClient();

const mutation = useMutation({
  mutationFn: updateUserName,
  onSuccess: () =>
    // Marks matching queries stale; queries that are rendered refetch in the
    // background. Returning the promise keeps the mutation pending until then.
    queryClient.invalidateQueries({ queryKey: ['users', userId] }),
});
```

Both calls use the v5 single-object signature, and `isPending` is the v5 name for what v4 called `isLoading` ([Migrating to TanStack Query v5](https://tanstack.com/query/latest/docs/framework/react/guides/migrating-to-v5)). Invalidation matches by prefix, so `['users']` also invalidates `['users', 7]` ([Query Invalidation](https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation)).

TanStack's own docs say which code this removes: connectors, action creators, middlewares, reducers, loading, error and result states, and contexts used for server data ([Does TanStack Query replace Redux, MobX or other global state managers?](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state)). That page is the library's own advocacy, and the amount removed depends on how much server data the store held.

The same model is available without leaving Redux. RTK Query ships inside Redux Toolkit (version 2.15.0 on npm on 2026-11-21) and exists because "'data fetching and caching' is really a different set of concerns than 'state management'" ([RTK Query Overview](https://redux-toolkit.js.org/rtk-query/overview)). The decision this essay supports is whether server data sits in a purpose-built cache; that cache can be TanStack Query, SWR, Apollo Client or RTK Query.

---

## 5. Where each kind of state goes once the server cache moves out

With server data in a query cache, the remaining state splits into four places:

1. **Server cache:** TanStack Query, [SWR](https://github.com/vercel/swr) (named after `stale-while-revalidate`, a cache invalidation strategy popularized by HTTP RFC 5861, with request deduplication and revalidation on focus and on network recovery), Apollo Client for GraphQL (a [normalized, in-memory cache](https://www.apollographql.com/docs/react/caching/overview)) or RTK Query. This layer owns fetching, background refetching and optimistic rollback.
2. **URL state:** search parameters, page numbers and filters kept in the URL, through router hooks or [nuqs](https://nuqs.dev/) ("Like useState, but stored in the URL query string"). A URL with its state in it can be shared and bookmarked.
3. **Local component state:** `useState` or `useReducer` for toggles and input fields that one component, or one subtree, uses ([React: Managing State](https://react.dev/learn/managing-state)).
4. **Global client store:** whatever is left. In TanStack's own example, moving four kinds of server data out leaves only `themeMode` and `sidebarStatus` ([TanStack Query docs](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state)). A small [Zustand](https://github.com/pmndrs/zustand) store, React context or a Redux slice can hold that. Session tokens do not need to be in this store: MDN says the `HttpOnly` cookie attribute "Forbids JavaScript from accessing the cookie" and that this "mitigates attacks against cross-site scripting (XSS)" ([MDN: Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)).

The exception is an application whose main state is synchronous and client-only. TanStack's docs name "a visual designer or music production application" as cases where "you will probably still want a client state manager", and say TanStack Query "is not a replacement for local/client state management" ([TanStack Query docs](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state)). In those apps the client store stays large, and a query cache sits next to it for the server data.

---

## 6. A test to run before adding a slice of global state

The book's position, offered as a rule of thumb rather than a law: before adding a slice to a global client store, ask one question.

> Did this data originate from a network endpoint?

If yes, do not write a reducer for it. Give it a query key and an explicit `staleTime`, and let a query cache (TanStack Query, SWR, Apollo Client or RTK Query) own fetching, refetching and invalidation.

The answer changes in two cases. A copy of server data that the user is editing, such as a form draft, becomes client state until it is submitted. And an application whose core is a large client-only document, such as a visual design tool or a music production app, keeps a client state manager for that document and uses a query cache only for what it loads from and saves to the server.
