# Data Fetching and API Contracts: REST vs. GraphQL vs. tRPC vs. Server Actions

> **Unverified background notes.** This file is an AI-generated research summary from the book's first draft. It has not been checked against the [content standards](../../CONTENT_STANDARDS.md) and is not part of the book. The verified chapters in `book/` cite primary sources directly; rely on those instead.

* **Category:** `api_contract`
* **Status:** Industry Standard & Emerging Paradigms
* **Core Comparison:** REST (OpenAPI) vs. GraphQL (Apollo/Relay) vs. tRPC vs. Server Actions (RSC)

---

## 1. Mechanics and Contract Models

The interface between the client runtime and backend services governs both data efficiency over cellular networks and developer type safety across repository boundaries:

1. **REST with OpenAPI / Orval:**
   * *Mechanism:* Standard HTTP verbs (GET, POST, PUT, DELETE) hitting resource endpoints. A machine-readable OpenAPI (Swagger) specification generates typed client SDKs and mock servers at build time.
   * *Sweet Spot:* Public APIs, third-party integrations, multi-client ecosystems (Web, iOS, Android, partner SDKs), standard CDN edge caching.
2. **GraphQL (Apollo Client / Relay):**
   * *Mechanism:* A single endpoint where the client submits query documents specifying the exact fields requested. The server resolves fields hierarchically. Relay adds strict component-colocated data fragments.
   * *Sweet Spot:* Massive relational graphs (e.g., Facebook, GitHub), heterogeneous clients with vastly different data needs, eliminating multiple sequential network waterfalls.
3. **tRPC:**
   * *Mechanism:* Leverages TypeScript inference across a unified full-stack monorepo. The client imports router types directly from the backend without intermediate code generation or schema compilation.
   * *Sweet Spot:* Full-stack TypeScript teams working in a single repository where backend and frontend deploy simultaneously.
4. **Server Actions (React 19 / Next.js):**
   * *Mechanism:* Functions defined on the server that can be imported and called directly from client components as if they were local asynchronous functions. The framework serializes parameters, dispatches an HTTP POST request, executes the code on the server, and returns the result with automatic router cache revalidation.
   * *Sweet Spot:* Form submissions, simple database mutations, and co-located server mutations in Server Component architectures.

---

## 2. Comparative Matrix

| Evaluation Vector | REST (OpenAPI) | GraphQL (Relay/Apollo) | tRPC | Server Actions |
| :--- | :--- | :--- | :--- | :--- |
| **Type Safety** | Generated via tooling | Generated via schema introspection | Instant via TS inference (Zero build step) | Native language level |
| **HTTP Caching** | Native, granular (ETag, Cache-Control) | Difficult (POST requests bypass standard CDN caches) | Standard HTTP queries (Batched) | Framework-managed cache invalidation |
| **Over-Fetching Risk** | Moderate to High (Fixed endpoint payloads) | None (Client requests exact fields) | Low (Client controls procedure contracts) | Low (Server procedure returns custom payload) |
| **Client Bundle Cost** | Low (~1-3 KB fetch wrapper) | High (~30-45 KB Apollo runtime parser) | Low (~2 KB lightweight client) | Zero runtime overhead |
| **Repository Coupling**| Loose (Independent deploys) | Loose (Schema acts as formal contract) | Tight (Shared TypeScript codebase required) | Tightly bound to meta-framework |

---

## 3. Decision Playbook

### Choose REST with OpenAPI When:
* The backend services are built in non-TypeScript languages (Go, Java, Python, Rust) or serve diverse third-party external consumers.
* You require battle-tested HTTP CDN caching at the network edge.

### Choose GraphQL When:
* The data graph is deeply nested with complex relationships, and multiple client platforms (iOS, Android, Web, IoT) need customized data shapes from a single backend.
* You operate a large engineering organization where schema governance and formal API contracts prevent breaking changes across dozens of squads.

### Choose tRPC When:
* The team is 100% full-stack TypeScript operating in a single monorepo (Turborepo or pnpm).
* Velocity is the top organizational metric, and maintaining separate schema definition languages (SDL) would be pure overhead.

### Choose Server Actions When:
* Operating in a React Server Components environment (Next.js App Router) for simple form submissions, database inserts, and straightforward mutations tightly coupled to UI views.
