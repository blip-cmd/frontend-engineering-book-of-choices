---
page: book/04_the_networking_contract.md
verified: 2026-11-22
---

# Claim Ledger: Chapter 4, The Networking Contract

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead choosing how a web frontend talks to its backend. The page helps them choose between REST with OpenAPI code generation, GraphQL, tRPC and React Server Functions. Thesis (unchanged from the draft): pick the contract by who consumes the API; tRPC when every client is TypeScript in the same repository, GraphQL when several clients need different fields from interconnected data, REST with OpenAPI otherwise, Server Functions for mutations inside a React framework app; and whatever the contract, validate responses at runtime because compile-time types are erased.

**History.** The AI-generated draft was rewritten by the author pass on 2026-11-22. Main corrections: the draft said Server Actions invalidate the router cache automatically (Next.js docs show the developer calls `revalidatePath`, `revalidateTag` or `refresh`); it gave Server Actions a client bundle cost of "Exactly 0 KB" and Apollo Client "30 KB to 45 KB" and tRPC "~2 KB" with no source (all removed); it gave cellular round trips as "100-300ms" with no source (made qualitative); it said GraphQL "completely eliminated" over-fetching; it said a renamed field makes the frontend crash, when the read returns `undefined` and the `TypeError` appears only at the next property access (reproduced in Node.js 24); its Zod example used `z.string().email()`, deprecated in Zod 4; it used the name "Server Actions" for what react.dev has called Server Functions since September 2024; it attributed two titles to Colin McDonnell and Alex Johansson that are product taglines, not publications; and it linked an unverified `library/` research note. The heading "The Landscape of Choices" was replaced. No recommendation was changed; the decision tree gained a line placing Server Functions, taken from the draft's own "sweet spot" text.

---

## 1. Author pass (2026-11-22)

Sources were fetched in the same session with `curl` and searched as text. Package versions were checked with `npm view` on 2026-11-22. Code was run with Node.js 24.18.1 and type-checked with TypeScript 7.0.2 (`tsc --noEmit --strict`).

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | OpenAPI Initiative lists specification versions up to 3.2.1 | [spec.openapis.org/oas](https://spec.openapis.org/oas/) | verified (v3.2.1, v3.2.0, v3.1.2 ... listed) |
| 2 | openapi-typescript supports OpenAPI 3.0 and 3.1; types have "zero runtime cost" | [openapi-typescript README](https://github.com/openapi-ts/openapi-typescript/tree/main/packages/openapi-typescript); [openapi-ts.dev](https://openapi-ts.dev/) | verified (quote); draft's "fully typed fetch SDKs" corrected: it generates types only, `openapi-fetch` does requests |
| 3 | Orval generates hooks for React Query, SWR, Angular, Vue, Svelte and Solid | [orval.dev](https://orval.dev/) | verified (quote) |
| 4 | HTTP caching: URL as cache key, `max-age`, `ETag` revalidation returning `304 Not Modified` | [MDN: HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) | verified (quote) |
| 5 | Relay: "the data requirements for a component are specified with fragments"; nested fragments fetched in "a single network request" | [Relay: Thinking in Relay](https://relay.dev/docs/principles-and-architecture/thinking-in-relay/) | verified (quote) |
| 6 | Relay compiler emits TypeScript or Flow types | [Relay: Type Emission](https://relay.dev/docs/guides/type-emission/) | verified (quote) |
| 7 | GraphQL servers MUST support POST and MAY support GET; GET MUST NOT be used for mutations | [GraphQL over HTTP draft](https://graphql.github.io/graphql-over-http/draft/) | verified (quote); page labels it a draft |
| 8 | GET "typically considered cacheable by default"; URL size limits; persisted queries send a hash | [graphql.org: Performance](https://graphql.org/learn/performance/) | verified (quote); replaces the draft's flat "POST queries bypass caching" |
| 9 | N+1 problem "commonly solved by a batching technique" such as DataLoader | graphql.org: Performance | verified (quote) |
| 10 | GraphQL implementations validate incoming requests against the schema | [graphql.org: Validation](https://graphql.org/learn/validation/) | verified (quote) |
| 11 | Draft: Apollo Client adds "30-45 KB" | none found | removed; made qualitative ("measure in your own bundle") |
| 12 | Draft: GraphQL over-fetching "Completely Eliminated" | mechanism only | corrected to "client selects fields" |
| 13 | tRPC: "consume fully typesafe APIs without schemas or code generation" | [tRPC docs](https://trpc.io/docs) | verified (quote); draft's "no compilation step" narrowed to no codegen |
| 14 | tRPC is "designed for TypeScript monorepos" | [tRPC concepts](https://trpc.io/docs/concepts) | verified (quote) |
| 15 | tRPC queries are GET with JSON input in a query parameter; mutations are POST | [tRPC HTTP RPC specification](https://trpc.io/docs/rpc) | verified |
| 16 | `@trpc/openapi` "is in alpha" | [tRPC: OpenAPI](https://trpc.io/docs/openapi); `npm view @trpc/openapi` (latest tag 11.29.7-alpha) | verified (quote) |
| 17 | tRPC queries cacheable with standard headers; batching on by default; `responseMeta` decides for the whole batch, cache only if all are public | [tRPC: Response Caching](https://trpc.io/docs/server/caching) | verified (quote) |
| 18 | tRPC procedures may define input and output validators | [tRPC: Validators](https://trpc.io/docs/server/validators) | verified (quote) |
| 19 | Draft: tRPC client "~2 KB" | none found | removed |
| 20 | Server Function call sends "a serialized copy of any arguments passed" | [react.dev: 'use server'](https://react.dev/reference/rsc/use-server) | verified (quote) |
| 21 | "Until September 2024, we referred to all Server Functions as 'Server Actions'"; Server Action is the subset passed to an action prop or called in an action | [react.dev: Server Functions](https://react.dev/reference/rsc/server-functions) | verified (quote); page renamed accordingly |
| 22 | Bundler APIs for Server Functions "do not follow semver" within React 19 | react.dev: Server Functions | verified (quote) |
| 23 | Next.js: actions use POST only; after a mutation call `revalidatePath`, `revalidateTag` or `refresh` | [Next.js: Mutating Data](https://nextjs.org/docs/app/getting-started/mutating-data) (lastUpdated 2026-10-15) | verified (quote); draft's automatic "router cache invalidation" corrected |
| 24 | Server Functions are exposed endpoints; treat arguments as untrusted; check auth in every function | react.dev: 'use server'; Next.js: Mutating Data | verified (quote) |
| 25 | Server Functions "are not recommended for data fetching" | react.dev: 'use server' | verified (quote) |
| 26 | Next.js "dispatches Server Actions one at a time per client" | [Next.js: Server Actions and Mutations](https://nextjs.org/docs/app/guides/server-actions) | verified (quote) |
| 27 | Draft: Server Actions client bundle "Exactly 0 KB" | none found | removed |
| 28 | Draft: cellular round trip "100-300ms" | none fetched | removed; made qualitative |
| 29 | Renamed field reads `undefined`; `TypeError: Cannot read properties of undefined` only at the next property access | Node.js 24.18.1 run | corrected (run); draft implied the crash happens at the read |
| 30 | `z.string().email()` deprecated in Zod 4 in favour of `z.email()` | [Zod 4 changelog](https://zod.dev/v4/changelog) | verified (quote); code updated |
| 31 | Unsafe `as User` example prints `undefined` then throws `TypeError` | Node.js 24.18.1 run; `tsc --strict` | verified (run) |
| 32 | Zod example: valid payload parses; drifted payload fails with "Invalid input: expected string, received undefined" at `id` | Node.js 24.18.1 run with `zod` 4.6.7; `tsc --strict` | verified (run); `safeParse`, `z.prettifyError` exist in Zod 4 |
| 33 | Versions: `@trpc/server` 11.29.7, `graphql` 17.1.0, `@apollo/client` 4.3.8, `relay-runtime` 21.0.1, `urql` 5.0.4, `zod` 4.6.7, `valibot` 1.5.0, `orval` 8.48.0, `openapi-typescript` 7.13.0, `openapi-fetch` 0.17.0, `next` 16.4.6, `react` 19.3.1 | `npm view` | verified |
| 34 | tRPC tagline "Move Fast and Break Nothing" | [trpc.io](https://trpc.io/) | verified; draft's attribution of it, and of Zod's tagline, as titled works by Alex Johansson and Colin McDonnell removed (no such publications located) |
| 35 | Draft link to `library/tools_and_frameworks/data_fetching_and_api_contracts.md` | unverified research note | removed; primary sources cited instead |
| 36 | "When it is the wrong choice" lines for REST, GraphQL and tRPC; learning-cost row; decision tree; partial validation for large payloads | none | labelled on the page as the book's reasoning |

## 2. Independent verifier pass (2026-11-22)

**Verdict: PASS.** A separate agent that did not write the page extracted 41 claims from the page itself (not from the list above), fetched every cited source with `curl -sL` on 2026-11-22 and searched the text, checked every package with `npm view`, and re-ran both code examples. 39 claims were SUPPORTED, 2 were PARTIAL and were corrected, none were UNSUPPORTED. The remaining unsourced statements (round trips are costly on mobile, `as` is erased at compile time, the "when it is the wrong choice" lines, the learning-cost row and the decision tree) are background or labelled as the book's reasoning and contain no numbers.

| # | Claim on the page | Source checked | Verdict |
| :--- | :--- | :--- | :--- |
| V1 | OpenAPI Initiative lists versions up to 3.2.1 | spec.openapis.org/oas (lists v3.2.1, v3.2.0, v3.1.2 ... v2.0) | SUPPORTED |
| V2 | Orval generates hooks for React Query, SWR, Vue, Svelte, Solid and Angular | orval.dev ("Generate hooks for React Query, SWR, Angular, Vue, Svelte, and Solid") | SUPPORTED |
| V3 | openapi-typescript: types only, "zero runtime cost", pairs with `openapi-fetch`; supports OpenAPI 3.0 and 3.1 | openapi-ts.dev; README ("Supports OpenAPI 3.0 and 3.1", links openapi-fetch) | SUPPORTED |
| V4 | URL as cache key, `max-age`, `ETag` revalidation with `304 Not Modified` | MDN: HTTP caching ("essentially based on their URLs"; `If-None-Match` example) | SUPPORTED |
| V5 | Relay fragments quote; "a single network request" | Relay: Thinking in Relay | SUPPORTED (verbatim) |
| V6 | Relay compiler emits TypeScript or Flow types for operations and fragments | Relay: Type Emission (v21.0.1) | SUPPORTED |
| V7 | Servers must support POST, may support GET | GraphQL over HTTP draft ("MUST support ... POST, and MAY support ... GET") | SUPPORTED |
| V8 | GET "typically considered cacheable by default" and what that enables; URL size limits | graphql.org: Performance | PARTIAL: page said "which is what lets a CDN store them" and that URL limits "rule out" large documents; source says GET "can help facilitate HTTP caching or the use of a CDN when caching-related headers are provided" and that "it may not be possible to send a large document". Reworded to match. |
| V9 | Persisted queries send a hash | graphql.org: Performance | SUPPORTED |
| V10 | N+1 "commonly solved by a batching technique" such as DataLoader | graphql.org: Performance | SUPPORTED (verbatim) |
| V11 | Server validates requests against the schema | graphql.org: Validation | SUPPORTED |
| V12 | tRPC "consume fully typesafe APIs without schemas or code generation"; mismatches caught by the compiler | trpc.io/docs ("catches problems at build time") | SUPPORTED |
| V13 | Queries GET with JSON input in a query parameter; mutations POST | tRPC HTTP RPC specification | SUPPORTED |
| V14 | "designed for TypeScript monorepos" | tRPC concepts | SUPPORTED (verbatim) |
| V15 | `@trpc/openapi` "is in alpha" | tRPC: OpenAPI ("This package is in alpha"); `npm view` latest 11.29.7-alpha | SUPPORTED |
| V16 | Batching on by default; one `responseMeta` decision per batch; cache only if all public | tRPC: Response Caching | SUPPORTED |
| V17 | Optional input and output validators | tRPC: Validators ("procedures may define validation logic for their input and/or output") | SUPPORTED |
| V18 | "a serialized copy of any arguments passed" | react.dev: 'use server' | SUPPORTED (verbatim) |
| V19 | "Server Actions" until September 2024; Server Action subset definition | react.dev: Server Functions | SUPPORTED |
| V20 | Bundler APIs "do not follow semver" within React 19 | react.dev: Server Functions | SUPPORTED (verbatim) |
| V21 | Next.js 16: actions use POST only | Next.js: Mutating Data (docs v16.4, last updated 2026-10-15) | SUPPORTED |
| V22 | After a mutation the developer calls `revalidatePath`, `revalidateTag` or `refresh` "to update cached data; the framework does not infer what to invalidate" | Next.js: Mutating Data | PARTIAL: the page does not say the framework "does not infer" anything, and it says `refresh` refreshes the client router and "does not revalidate tagged data". Reworded to the source: `refresh` refreshes the client router; `revalidatePath` or `revalidateTag` revalidate the Next.js cache. |
| V23 | Each function is a reachable endpoint; check auth; arguments untrusted | react.dev: 'use server'; Next.js: Mutating Data ("reachable via direct POST requests") | SUPPORTED |
| V24 | "are not recommended for data fetching" | react.dev: 'use server' | SUPPORTED (verbatim) |
| V25 | "dispatches Server Actions one at a time per client" | Next.js: Server Actions and Mutations (last updated 2026-11-18) | SUPPORTED (verbatim) |
| V26 | `z.string().email()` deprecated in favour of `z.email()` | Zod 4 changelog ("still exist and work as before, but are now deprecated") | SUPPORTED |
| V27 | Zod API, Valibot introduction links resolve and describe schema libraries | zod.dev/api; valibot.dev | SUPPORTED |
| V28 | tRPC tagline "Move Fast and Break Nothing" | trpc.io | SUPPORTED |
| V29 to V31 | Unsafe example prints `undefined` then `TypeError`; Node.js 24 strips types | Node.js 24.18.1 run | SUPPORTED (run) |
| V32 to V34 | Zod example passes the valid payload, fails the drifted one with "Invalid input: expected string, received undefined" at `id`; passes `tsc --strict` with TypeScript 7.0 | Node.js 24.18.1 run with `zod` 4.6.7; `tsc` 7.0.2 | SUPPORTED (run) |
| V35 to V41 | Pinned versions: Orval 8.x, openapi-typescript 7.x, `graphql` 17.1, `@apollo/client` 4.3, `relay-runtime` 21.0, `urql` 5.0, `@trpc/server` 11.29, Zod 4.x / 4.6, Valibot 1.x | `npm view` | SUPPORTED |

**Edits made.** (1) Section 2, Choice B: "which is what lets a CDN store them, and that URL length limits rule out sending large documents" became "which can help HTTP caching or a CDN when the server sends caching headers, and that URL size limits may make it impossible to send a large document". (2) Section 2, Choice D: "the developer calls `revalidatePath`, `revalidateTag` or `refresh` to update cached data; the framework does not infer what to invalidate" became "the developer can call `refresh` to refresh the client router, or `revalidatePath` or `revalidateTag` to revalidate the Next.js cache". No claims or sources were added.

**Code checks.** Both examples were copied verbatim into a scratch folder outside the repository with `zod@4.6.7` and `typescript@7.0.2`. The unsafe example printed `undefined` and then threw `TypeError: Cannot read properties of undefined (reading 'toUpperCase')`. The safe example printed the parsed user, then `✖ Invalid input: expected string, received undefined → at id`. Extra failing inputs: `{ id: 1, email: 'x' }` reported both `id` and `email`; `null` and a string reported "expected object"; a payload with an extra key passed; a `500` response has `ok` false, so the `HTTP 500` branch is taken. `tsc --strict --noEmit` passed on both files. `npm view` on 2026-11-22: `@trpc/server` 11.29.7, `@trpc/openapi` 11.29.7-alpha, `graphql` 17.1.0, `@apollo/client` 4.3.8, `relay-runtime` 21.0.1, `urql` 5.0.4, `zod` 4.6.7, `valibot` 1.5.0, `orval` 8.48.0, `openapi-typescript` 7.13.0, `openapi-fetch` 0.17.0, `next` 16.4.6, `react` 19.3.1, `typescript` 7.0.2.

## 3. Known omissions (follow-up content, not errors)

Topics a complete chapter could add, each needing its own sourced entry:

* gRPC-Web and Connect as a schema-first RPC alternative
* GraphQL subscriptions, `@defer` and `@stream`, and federation
* tRPC subscriptions over Server-Sent Events or WebSockets; `httpBatchStreamLink`
* OpenAPI 3.2 features (for example streaming media types) and which generators support them
* Request waterfalls in practice: route loaders, React Server Components data fetching, and `Promise.all` patterns
* Error contracts: RFC 9457 problem details for REST, GraphQL `errors` array semantics
* API versioning and deprecation (`@deprecated` in GraphQL, `deprecated` in OpenAPI)
* Standard Schema as the shared interface between Zod, Valibot and tRPC validators

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | **19** |

D8 is 1 because the comparison table relies on section 2 for its sources. All gates pass except G8 (human accountability), which an `agent-verified` status would disclose instead.
