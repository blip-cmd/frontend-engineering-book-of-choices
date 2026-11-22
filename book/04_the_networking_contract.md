---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: next 16.4 docs, react.dev (react 19.3), @trpc/server 11.29, @trpc/openapi 11.29.7-alpha, graphql 17.1, graphql-over-http draft, @apollo/client 4.3, relay-runtime 21.0, urql 5.0, OpenAPI 3.2.1, openapi-typescript 7.13, orval 8.48, zod 4.6.7, valibot 1.5, typescript 7.0.2, node 24.18
review_by: 2027-05
reviewers:
ledger: reviews/the-networking-contract.md
---

# Chapter 4: The Networking Contract: REST vs. GraphQL vs. tRPC vs. Server Functions

> For a tech lead choosing how a web frontend talks to its backend. The choice of contract decides where types come from, which responses HTTP caches can store, and which clients besides your own web app can call the API. Versions on this page were checked on 2026-11-22.

---

## 1. What the Contract Must Solve: Round Trips and Schema Drift

Frontend and backend code communicate across a network that is slow and unreliable compared with a function call. Two pressures shape the contract:

1. **Round trips.** Each request waits at least one network round trip, and mobile connections make each one expensive. Sending too much data wastes bandwidth; sending too little causes request waterfalls, where component A fetches its data and only then renders child component B, which starts its own request.
2. **Schema drift.** If the backend renames a field from `userId` to `id` and the client still reads `userId`, nothing fails at the moment of the fetch. The client reads `undefined`, and the error surfaces later, wherever code first touches a property of that value: `TypeError: Cannot read properties of undefined` (the example in section 4 reproduces this in Node.js 24).

Each option below enforces the contract differently: a formal schema (OpenAPI, GraphQL), TypeScript inference across a shared codebase (tRPC), or a framework-generated endpoint behind an imported function (React Server Functions).

---

## 2. Which Contract Fits Your Consumers: REST, GraphQL, tRPC or Server Functions

### Choice A: REST with OpenAPI Code Generation
* **Mechanism:** HTTP endpoints addressed by URL and method (`GET /api/users/123`). The backend publishes a machine-readable OpenAPI document; the [OpenAPI Initiative](https://spec.openapis.org/oas/) lists versions up to 3.2.1. Generators turn that document into client code at build time: [Orval](https://orval.dev/) (8.x) generates typed clients and hooks for React Query, SWR, Vue, Svelte, Solid and Angular, while [openapi-typescript](https://openapi-ts.dev/) (7.x) generates types only, with "zero runtime cost", and pairs with `openapi-fetch` for requests. The [openapi-typescript README](https://github.com/openapi-ts/openapi-typescript/tree/main/packages/openapi-typescript) documents support for OpenAPI 3.0 and 3.1, so check your generator before relying on 3.2 features.
* **Where it fits:** public APIs, several client platforms (iOS, Android, web, partners), and responses you want stored by browsers and CDNs. Each resource has its own URL, which is the cache key HTTP caching works with; `Cache-Control: max-age` sets freshness and `ETag` lets a client revalidate and receive `304 Not Modified` ([MDN: HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)).
* **The cost:** fixed response shapes over-fetch for some screens, and screens that combine many resources either chain requests or need a purpose-built endpoint. The generated client goes stale until the generator runs again after a backend change.
* **When it is the wrong choice (the book's reasoning):** a single TypeScript team ships the only client, in one repository, and has no plans for outside consumers. The codegen step and the OpenAPI document then add work that tRPC removes.

### Choice B: GraphQL (Relay, Apollo Client, urql)
* **Mechanism:** the client sends a document describing the exact fields it needs (`query { user(id: 123) { name avatarUrl } }`) and the server resolves those fields into one response. Relay builds this from fragments: "the data requirements for a component are specified with fragments", which nest into a query that Relay sends as "a single network request" ([Relay: Thinking in Relay](https://relay.dev/docs/principles-and-architecture/thinking-in-relay/)). The Relay compiler emits TypeScript or Flow types for each operation and fragment ([Relay: Type Emission](https://relay.dev/docs/guides/type-emission/)). Versions checked: `graphql` 17.1, `@apollo/client` 4.3, `relay-runtime` 21.0, `urql` 5.0.
* **Where it fits:** interconnected data (social graphs, product catalogs) read by several clients whose screens need different fields from the same objects.
* **The cost:** servers must support POST and may support GET for queries ([GraphQL over HTTP draft](https://graphql.github.io/graphql-over-http/draft/)). graphql.org notes that GET requests "are typically considered cacheable by default", which can help HTTP caching or a CDN when the server sends caching headers, and that URL size limits may make it impossible to send a large document in the query string; persisted queries send a hash instead ([graphql.org: Performance](https://graphql.org/learn/performance/)). Nested resolvers cause the N+1 problem, which graphql.org says is "commonly solved by a batching technique" such as DataLoader (same source). A normalized client cache (Apollo, Relay) is extra JavaScript to ship and extra concepts to learn; measure its size in your own bundle rather than trusting published figures.
* **When it is the wrong choice (the book's reasoning):** one web client reads a handful of screens' worth of data, or the product depends on CDN caching of public pages and the team cannot run persisted queries. The schema, resolvers and batching layer then cost more than the over-fetching they remove.

### Choice C: tRPC (End-to-End TypeScript Inference)
* **Mechanism:** the client imports only the TypeScript *type* of the server's router. tRPC lets you "consume fully typesafe APIs without schemas or code generation" ([tRPC docs](https://trpc.io/docs)); when a procedure's input or output changes, the TypeScript compiler reports the mismatch in client code. On the wire, queries are HTTP GET requests with JSON input in a query parameter and mutations are POST ([tRPC HTTP RPC specification](https://trpc.io/docs/rpc)). Version checked: `@trpc/server` 11.29.
* **Where it fits:** a full-stack TypeScript team whose client and server live in one repository; tRPC describes itself as "designed for TypeScript monorepos" ([tRPC concepts](https://trpc.io/docs/concepts)).
* **The cost:** the type safety exists only for TypeScript clients that can import the router type. A Swift, Kotlin or partner client can call the HTTP endpoints but gets no types; the `@trpc/openapi` package that generates an OpenAPI document "is in alpha" ([tRPC: OpenAPI](https://trpc.io/docs/openapi)). Because queries are GET, standard cache headers work, but batching is on by default and one `responseMeta` decision applies to every procedure in a batch, so the docs say to cache only when all of them are public ([tRPC: Response Caching](https://trpc.io/docs/server/caching)).
* **When it is the wrong choice (the book's reasoning):** native mobile apps, other languages or outside developers must consume the same API, or the frontend and backend are released from separate repositories by separate teams.

### Choice D: React Server Functions (Server Actions)
* **Mechanism:** a function marked with `"use server"` runs on the server, and client components import and call it like an async function. React sends "a network request to the server that includes a serialized copy of any arguments passed" ([react.dev: 'use server'](https://react.dev/reference/rsc/use-server)). React called all of these "Server Actions" until September 2024; a Server Action is now the subset of Server Functions passed to an `action` prop or called inside an action ([react.dev: Server Functions](https://react.dev/reference/rsc/server-functions)). In Next.js 16, actions use POST only, and after a mutation the developer can call `refresh` to refresh the client router, or `revalidatePath` or `revalidateTag` to revalidate the Next.js cache ([Next.js: Mutating Data](https://nextjs.org/docs/app/getting-started/mutating-data)).
* **Where it fits:** form submissions and other mutations in a React 19 app built on a framework that supports React Server Components.
* **The cost:** you need such a framework or bundler; react.dev notes that the APIs bundlers use to implement Server Functions "do not follow semver" within React 19. Each exported function is a reachable endpoint, so each one must check authentication and authorization and treat its arguments as untrusted input (react.dev: 'use server'; Next.js: Mutating Data).
* **When it is the wrong choice:** reading data, since Server Functions "are not recommended for data fetching" (react.dev: 'use server'); parallel calls from the client, since Next.js "dispatches Server Actions one at a time per client" ([Next.js: Server Actions and Mutations](https://nextjs.org/docs/app/guides/server-actions)); and any API that a non-React client must also call.

---

## 3. How the Four Options Compare on Caching, Types and Reach

Sources for each cell are linked in section 2; the "learning cost" row is the book's judgment.

| Dimension | REST with OpenAPI | GraphQL (Relay, Apollo) | tRPC 11 | Server Functions (React 19) |
| :--- | :--- | :--- | :--- | :--- |
| **Where client types come from** | Build-time generation from the OpenAPI document | Build-time generation from the schema and operations (Relay compiler, codegen tools) | TypeScript inference from the imported router type | TypeScript types of the imported function |
| **Runtime checks** | None on the client unless added (section 4) | Server validates each request against the schema ([graphql.org: Validation](https://graphql.org/learn/validation/)); client trusts the response | Optional input and output validators on the server ([tRPC: Validators](https://trpc.io/docs/server/validators)); client trusts the response | None for arguments unless added; treat them as untrusted |
| **HTTP and CDN caching** | Standard: URL as cache key, `max-age`, `ETag` | Needs GET, plus persisted queries for large documents | Queries are GET; cache headers apply per batch | POST only (Next.js 16); framework cache updated by explicit revalidation calls |
| **Over-fetching** | Fixed shapes; likely on some screens | Client selects fields | Procedure returns what the server chose | Function returns what the server chose |
| **Clients that get types** | Any language with an OpenAPI generator | Any language with a GraphQL client and codegen | TypeScript only | React components in the same app |
| **Learning cost (judgment)** | Low | High: schema, resolvers, fragments, batching | Low for TypeScript teams | Low, plus framework caching rules |

---

## 4. Validate Responses at Runtime, Whatever the Contract

Every option in section 2 gives you compile-time types, and none of them checks at runtime that the JSON a client receives matches those types. A TypeScript `as` assertion is erased when the code is compiled. The example below is unsafe on purpose; it shows the drift from section 1. It runs as-is in Node.js 24, which strips TypeScript types:

```typescript
// UNSAFE: `as User` is erased at compile time and checks nothing at runtime.
type User = { userId: string; name: string };

// Simulates a backend that renamed `userId` to `id`.
const response = new Response(JSON.stringify({ id: 'u_123', name: 'Ada' }));
const user = (await response.json()) as User;

console.log(user.userId); // undefined, and no error is thrown here
console.log(user.userId.toUpperCase()); // TypeError, thrown later and far from the fetch
```

The safer pattern parses data at the network boundary with a schema library such as [Zod](https://zod.dev/api) (4.x) or [Valibot](https://valibot.dev/guides/introduction/) (1.x), and fails there with the name of the field that drifted. This version runs in Node.js 24 with `zod` 4.6 installed and passes `tsc --strict` with TypeScript 7.0:

```typescript
import { z } from 'zod'; // zod 4.x

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.email(), // zod 4 form; z.string().email() is deprecated
});
type User = z.infer<typeof UserSchema>;

async function readUser(response: Response): Promise<User> {
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const result = UserSchema.safeParse(await response.json());
  if (!result.success) {
    // Fail at the boundary, with the field that drifted, instead of deep in the UI.
    throw new Error(`User payload failed validation:\n${z.prettifyError(result.error)}`);
  }
  return result.data;
}

// A response that matches the contract...
const ok = new Response(JSON.stringify({ id: 'u_123', name: 'Ada', email: 'ada@example.com' }));
console.log(await readUser(ok));

// ...and one where the backend renamed `id` to `userId`.
const drifted = new Response(JSON.stringify({ userId: 'u_123', name: 'Ada', email: 'ada@example.com' }));
await readUser(drifted).catch((error) => console.error(error.message));
```

The second call prints `Invalid input: expected string, received undefined` for the path `id`. Zod 4 deprecates the method forms such as `z.string().email()` in favour of top-level `z.email()` ([Zod 4 changelog](https://zod.dev/v4/changelog)).

**When full parsing is the wrong choice (the book's reasoning):** parsing walks every field, so for very large arrays or high-frequency streams, measure the cost first. If it blocks the main thread, validate the envelope and a sample of items, or move parsing to a Web Worker.

---

## 5. Picking One: A Decision Tree

The tree below is the book's reasoning, built from the "when it is the wrong choice" lines in section 2.

```text
        [Is every client TypeScript, in the same repository as the server?]
                                   │
                    ├── Yes ───────> Choose tRPC
                    │                (types flow from server to client, no codegen)
                    │
                    └── No (other languages, mobile apps or outside developers)
                            │
            Do several clients need different fields from interconnected data?
                    ├── Yes ───────> Choose GraphQL
                    │                (one schema; each client selects its fields)
                    │
                    └── No  ───────> Choose REST with OpenAPI code generation
                                     (standard HTTP caching; generators for many languages)

  In a React 19 framework app, use Server Functions for form submissions and
  other mutations alongside any of the above, not for reading data.
```

---

## 6. Sources and Further Reading
* [OpenAPI Specification versions](https://spec.openapis.org/oas/) (OpenAPI Initiative)
* [GraphQL over HTTP (draft specification)](https://graphql.github.io/graphql-over-http/draft/) and [graphql.org: Performance](https://graphql.org/learn/performance/)
* [tRPC documentation](https://trpc.io/docs) (tRPC's tagline is "Move Fast and Break Nothing")
* [react.dev: Server Functions](https://react.dev/reference/rsc/server-functions) and [`'use server'`](https://react.dev/reference/rsc/use-server)
* [MDN: HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)
* [Zod API documentation](https://zod.dev/api)
* [Further reading: *High Performance Browser Networking* (Ilya Grigorik)](../library/reading_list.md)
