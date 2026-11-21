# Why Server Caches Replace Most Redux Stores

> An architectural analysis on why conflating remote asynchronous server state with local synchronous UI state created a decade of unnecessary frontend complexity.

---

## 1. The Redux Era and the Monolithic State Delusion

For nearly a decade, the conventional wisdom in React development dictated placing all application data into a centralized, single-source-of-truth Redux or MobX store. Whenever an application needed data from a backend server, the pattern was invariant:

1. Dispatch an action (`FETCH_USERS_REQUEST`).
2. Toggle a boolean flag in a reducer (`state.isLoading = true`).
3. Make an asynchronous HTTP request using `axios` or `fetch`.
4. Dispatch a success action (`FETCH_USERS_SUCCESS`) with payload.
5. Store the raw server response inside the global client state tree.
6. Write selectors to slice, memoize, and project that data into React components.

This workflow was repeated for every entity in the system: users, billing items, comments, permissions, and notifications. 

The fundamental architectural flaw was not Redux itself; Redux is a clean, deterministic implementation of Flux and the Elm Architecture. The fatal mistake was treating **server-origin data** as if it were **client state**.

---

## 2. The Great Taxonomy: Client State vs. Server Cache

To understand why this architecture collapsed under its own weight, we must separate data into two orthogonal categories:

### True Client State
Data that is created, owned, and manipulated entirely within the user's browser session:
* Open modal toggles and dialog visibility.
* Active tab selection and navigation drawers.
* Controlled form inputs prior to submission.
* Theme preferences (light/dark mode) and layout column widths.

True client state is synchronous, client-owned, instantly mutable, and represents the ephemeral posture of the user interface.

### Server Cache
Data that is persisted remotely on backend databases:
* User profile records.
* Shopping cart contents.
* Inventory availability and account balances.
* Team member permissions and activity feeds.

Server data is asynchronous, remote-owned, shared across multiple users concurrently, and inherently out of date the moment it finishes downloading over the network. It is not state; it is a **temporary, potentially stale snapshot cache of remote state**.

---

## 3. The 9 Hidden Complexities of Server Cache Management

When engineering teams attempt to manage server data manually inside a client store (Redux, Zustand, Pinia), they must invent bespoke solutions for nine distinct operational problems:

1. **Deduplication:** Preventing three components mounted on the same page from firing three identical HTTP requests.
2. **Staleness Tracking:** Knowing when cached data is fresh enough to render versus when background refetching is required.
3. **Garbage Collection:** Evicting unmounted query cache entries to prevent browser memory leaks.
4. **Structural Sharing:** Preserving immutable object references between identical background fetches to avoid unnecessary React re-renders.
5. **Window Refocus Invalidation:** Silently updating stale data when a user navigates back to the browser tab after an hour away.
6. **Network Reconnect Polling:** Automatically resuming fetches when an unstable mobile device regains cellular connectivity.
7. **Optimistic Mutations:** Updating the UI within 16 milliseconds of a button click, with deterministic rollback if the network request fails.
8. **Pagination and Infinite Scroll State:** Merging subsequent pages of data without race conditions.
9. **Mutation Invalidation Cascades:** Purging affected read caches whenever an edit or delete mutation succeeds.

In a traditional Redux codebase, writing custom code to address these nine concerns consumes 80% of an engineering team's time.

---

## 4. How TanStack Query Inverted the Model

TanStack Query (React Query) fundamentally re-centered the frontend architecture by treating remote data strictly as a managed asynchronous cache keyed by deterministic arrays:

```typescript
// Reading cached server data with automatic deduplication, caching, and background refetch
const { data: user, isPending, error } = useQuery({
  queryKey: ['users', userId],
  queryFn: () => fetchUserById(userId),
  staleTime: 1000 * 60 * 5, // Data remains fresh for 5 minutes
});
```

When a user mutates data, declarative cache invalidation replaces manual reducer updates:

```typescript
const queryClient = useQueryClient();

const mutation = useMutation({
  mutationFn: updateUserName,
  onSuccess: () => {
    // Invalidate the cache key globally; all mounted components update automatically
    queryClient.invalidateQueries({ queryKey: ['users', userId] });
  },
});
```

By delegating staleness, deduplication, and cache invalidation to the runtime engine, over 90% of boilerplate actions, reducers, and selectors disappear from the codebase.

---

## 5. The Modern Frontend Architecture Topology

With server cache offloaded to specialized cache runtimes (TanStack Query, SWR, or Apollo Client), what remains in the global client store?

Very little. The resulting stack is compact, fast, and durable:

1. **Server Cache (80% to 90% of application data):** Managed by TanStack Query. Handles all remote network synchronization and optimistic rollbacks.
2. **URL State (5% to 10% of state):** Search parameters, active page numbers, and filtering facets stored in the browser URL (via `nuqs` or router hooks). This makes application states shareable and bookmarkable by default.
3. **Local Component State (5%):** Managed by `useState` or `useReducer` for ephemeral toggles and input fields.
4. **Global Client Store (Remaining 1% to 2%):** A tiny Zustand store (often under 50 lines of code) managing authentication session tokens and global user preferences.

---

## 6. Conclusion and Actionable Heuristic

Before creating a new slice in your global client store, ask a simple question:

> Did this data originate from a network endpoint?

If the answer is yes, do not write a reducer for it. Treat it as a remote cache entry with an explicit staleness policy, and let a dedicated query engine own the lifecycle.
