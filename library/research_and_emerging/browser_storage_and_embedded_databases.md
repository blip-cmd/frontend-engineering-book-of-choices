# Research & Emerging: Embedded Client Databases and Storage Topologies

* **Category:** `research_and_emerging`
* **Status:** Emerging Standard & Production in Specialized Clients
* **Core Comparison:** LocalStorage vs. IndexedDB vs. OPFS (Origin Private File System) vs. Embedded SQL (SQLite WASM / PGlite)

---

## 1. The Hierarchy of Browser Storage

Modern web applications increasingly need persistent storage that goes far beyond simple 5 MB string key-value caches. Storing local offline models, cached document logs, and synchronized client databases requires understanding the browser storage hierarchy:

1. **LocalStorage / SessionStorage:**
   * *Mechanism:* Synchronous, blocking key-value string storage capped at 5 MB.
   * *The Critical Flaw:* Accessing LocalStorage blocks the browser main thread and event loop. It lacks indexing, querying capabilities, and binary data support. Reserved exclusively for trivial flags (e.g., `theme: "dark"`).
2. **IndexedDB:**
   * *Mechanism:* Asynchronous, transactional, NoSQL object store capable of storing gigabytes of structured data, blobs, and typed arrays.
   * *The Problem:* The native API is notoriously difficult and callback-heavy. Browser performance varies widely; slow index scans can stall UI frames.
3. **Origin Private File System (OPFS):**
   * *Mechanism:* A modern HTML5 storage standard providing a private, optimized filesystem accessible to the origin. In dedicated Web Workers, OPFS offers synchronous, zero-overhead file access handles (`FileSystemSyncAccessHandle`).
   * *The Breakthrough:* Delivers raw read/write throughput competitive with native desktop disk operations, enabling true relational databases to run inside the browser.
4. **Embedded Relational Engines (SQLite in Wasm, PGlite):**
   * *Mechanism:* Compiles enterprise relational engines (SQLite, Postgres) to WebAssembly and backs their storage with OPFS.
   * *The Capability:* Developers can write full ACID SQL queries (`SELECT`, `JOIN`, `GROUP BY`) against a local client database in sub-millisecond execution times.

---

## 2. Comparative Matrix

| Storage Layer | Access Model | Storage Limit | Query Capabilities | Main-Thread Blocking Risk | Best Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LocalStorage** | Synchronous | ~5 MB | Exact key match only (Strings only) | High (Blocks main event loop) | Theme preference, auth token flag |
| **IndexedDB (via Dexie / idb)** | Asynchronous | Up to 80% of available disk space | Index range queries, cursor scans | Low (Async transactions) | Caching REST responses, offline asset blobs |
| **OPFS (Worker Access Handle)** | Synchronous (in Worker) | Up to 80% of available disk space | Direct byte-offset read/write | Zero (Executes in background worker) | File caching, embedded database backing store |
| **PGlite / wa-sqlite** | Asynchronous / Worker | Gigabytes (OPFS backed) | Full Relational SQL, Vector Search (pgvector) | Zero (Worker isolated) | Local-First applications, offline analytics |

---

## 3. Architectural Best Practices

* **Always Offload Heavy Queries to Web Workers:**
  Never run large SQLite or IndexedDB queries on the browser main thread. Wrap the database engine inside a Web Worker and communicate via asynchronous message passing or Comlink.
* **Storage Eviction Resilience:**
  Mobile browsers (especially iOS Safari) automatically evict storage if a device runs low on disk space or if the website has not been visited for a prolonged period. Production local-first apps must invoke `navigator.storage.persist()` to request explicit persistent storage status from the browser.
