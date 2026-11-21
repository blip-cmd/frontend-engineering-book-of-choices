---
status: draft
ai_involvement: drafted
last_verified:
verified_against:
review_by:
reviewers:
---

# Chapter 4: The Networking Contract: REST vs. GraphQL vs. tRPC vs. Server Actions

> The boundary between client and server is the most volatile interface in software. How you structure that contract dictates your type safety, network latency, and deployment coupling.

---

## 1. The Core Dilemma

Frontend and backend systems must communicate across high-latency, unreliable networks. When structuring this communication, engineers confront two opposing pressures:

1. **The Transport Efficiency Dilemma:** 
   Over cellular connections, every round trip carries a steep latency penalty (100-300ms). Sending too much data wastes user bandwidth; sending too little triggers cascading request waterfalls where component A fetches data, and its child component B must wait before dispatching its own request.
2. **The Schema Contract Dilemma:**
   If the backend changes a field name from `userId` to `id` and the client expects `userId`, the frontend will silently crash in production with `TypeError: Cannot read properties of undefined`. 

The architecture must choose how to enforce this contract: through formal schemas (GraphQL, OpenAPI), compile-time language inference (tRPC), or server-side execution primitives (Server Actions).

---

## 2. The Landscape of Choices

### Choice A: REST with OpenAPI Code Generation
* **Mechanism:** Traditional HTTP endpoints using standard verbs (`GET /api/users/123`). The backend exposes a machine-readable OpenAPI specification (Swagger). The frontend uses tools like Orval or OpenAPI TypeScript to automatically generate fully typed fetch SDKs and TanStack Query hooks at build time.
* **The Sweet Spot:** Public APIs, multi-platform consumers (iOS, Android, Web), third-party developer ecosystems, and HTTP edge caching via standard CDNs.
* **The Friction:** Prone to over-fetching fixed payloads, and requires a separate build step to regenerate client SDKs whenever the backend API updates.

### Choice B: GraphQL (Relay / Apollo Client)
* **Mechanism:** The client submits a query document describing the precise shape of the data needed (`query { user(id: 123) { name avatarUrl } }`). The server parses the document and resolves fields hierarchically in a single HTTP response. Relay adds component-colocated data fragments.
* **The Sweet Spot:** Massive, deeply interconnected relational data graphs (e.g., social graphs, large e-commerce catalogs) and heterogeneous clients with wildly divergent screen requirements.
* **The Friction:** HTTP POST queries bypass standard browser and CDN caching; server-side N+1 query complexity requires dataloader layers; client runtime parser bundles (Apollo) add 30-45 KB of JavaScript weight.

### Choice C: tRPC (End-to-End TypeScript Inference)
* **Mechanism:** The client imports the backend router's TypeScript type definition directly in a monorepo. No schemas are declared, no code is generated, and no compilation step is required. When a backend procedure signature changes, TypeScript immediately flags errors in the frontend component code during editing.
* **The Sweet Spot:** Full-stack TypeScript teams working in a single unified repository (Turborepo, pnpm workspaces).
* **The Friction:** Strictly couples the frontend and backend to TypeScript and a shared repository; impossible to share directly with non-TypeScript mobile teams without extra adapters.

### Choice D: React Server Actions & RPC
* **Mechanism:** Functions declared with `"use server"` execute exclusively on the server but are imported and called like ordinary asynchronous functions in client components. The framework abstracts the HTTP POST transport, parameter serialization, and subsequent router cache invalidation.
* **The Sweet Spot:** Simple mutations, form submissions, and database writes tightly coupled to React Server Components.
* **The Friction:** Vendor and framework lock-in (tightly coupled to Next.js or React 19 meta-frameworks); difficult to audit or mock independently of the framework runtime.

---

## 3. Comparative Matrix

| Evaluation Dimension | REST with OpenAPI | GraphQL (Apollo/Relay) | tRPC | Server Actions (React 19) |
| :--- | :--- | :--- | :--- | :--- |
| **Type Safety Mechanism** | Build-time code generation | Build-time schema generation | Instant TypeScript inference | Native language level |
| **HTTP CDN Caching** | Native, granular (ETags, max-age) | Complex (POST requests bypass CDN) | Native (GET procedures batched) | Framework router cache only |
| **Over-Fetching Risk** | Moderate to High | Completely Eliminated | Low | Low |
| **Client Bundle Impact** | ~1 KB (Standard fetch wrapper) | ~30 KB to 45 KB (Apollo Client) | ~2 KB (Lightweight client wrapper) | Exactly 0 KB |
| **Multi-Platform Support**| Universal (Web, iOS, Android, CLI) | Universal (All languages supported) | TypeScript Only | React Only |
| **Mental Model Friction**| Low | High (Requires SDL, resolvers, fragments)| Low | Low |

---

## 4. The Defensive Validation Rule: Runtime Zod vs. Compile-Time Trust

A common failure mode in TypeScript frontend engineering is the **Unchecked Assertion Trap**:
```typescript
// DANGEROUS: Compile-time TypeScript types vanish at runtime!
const response = await fetch('/api/user');
const user = (await response.json()) as User; // If API schema drifts, app crashes!
```

To achieve true runtime resilience, external data crossing the network boundary must be validated at runtime:
* **The Solution:** Use lightweight runtime parsing libraries like `zod` or `valibot`:
```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});

const raw = await response.json();
const user = UserSchema.parse(raw); // Throws clean error if schema is violated
```
* **Performance Rule:** On high-frequency or multi-megabyte payloads, full recursive schema parsing incurs CPU overhead. In performance-critical streams, validate payload envelopes or sample validation rather than blocking the main thread on massive arrays.

---

## 5. Decision Playbook

```
                   [Is the stack 100% TypeScript in a Monorepo?]
                                        │
                         ├── Yes ───────> Choose tRPC
                         │                (Maximum developer velocity and zero code-gen)
                         │
                         └── No (Polyglot backend or external client platforms)
                                 │
                 Is the data graph deeply nested with multiple client types?
                         ├── Yes ───────> Choose GraphQL
                         │                (Unified schema, exact query shapes)
                         │
                         └── No  ───────> Choose REST with OpenAPI Code Generation
                                          (Battle-tested, universal CDN caching)
```

---

## 6. References & Library Audits
* [Data Fetching and API Contracts (research notes)](../library/tools_and_frameworks/data_fetching_and_api_contracts.md)
* [Further reading: *High Performance Browser Networking* (Ilya Grigorik)](../library/reading_list.md)
* Colin McDonnell: *Zod: TypeScript-First Schema Validation with Static Type Inference*
* Alex Johansson: *tRPC: Move Fast and Break Nothing with End-to-End Type Safety*
