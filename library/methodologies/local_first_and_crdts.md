# Architectural Methodology: Local-First Software and CRDTs

* **Identifier:** `local-first-and-crdts`
* **Pioneers & Key Researchers:** Ink & Switch (Kleppmann, Litt, van Hardenberg), Yjs (Kevin Jahns), Automerge (Martin Kleppmann, Peter van Hardenberg)
* **Core Mechanisms:** Client-side persistent databases (IndexedDB, OPFS), Conflict-Free Replicated Data Types, Peer-to-Peer / Sync-Server synchronization, Zero-latency optimistic mutation

---

## 1. Mechanics and Mental Model

Traditional cloud web applications treat the server database as the definitive source of truth; the client is an ephemeral display that asks for data over HTTP and requests permission to change it. If the network disconnects or latency spikes, the interface stalls or fails.

**Local-First Architecture** turns this model upside down:
1. **Local Primary Database:** All reads and writes hit an embedded client database (SQLite in WASM, PGlite, RxDB, or IndexedDB) instantly with zero network delay.
2. **Asynchronous Background Synchronization:** Mutations are appended to an immutable local change log or represented as CRDT operations. These operations sync with peers or a synchronization server whenever connectivity is available.
3. **Deterministic Conflict Resolution:** State mathematically converges without requiring synchronous lock managers or human conflict resolution dialogues.

---

## 2. Comparative Trade-offs

### What You Gain:
* **Perceived Zero Latency:** Instantaneous UI response on every keystroke, click, or toggle; no spinners or loading bars for write operations.
* **Seamless Offline Resilience:** The application is fully functional without an internet connection indefinitely.
* **Effortless Real-Time Collaboration:** Multi-device synchronization and multiplayer collaboration are built into the data structure itself.
* **User Data Ownership:** Users retain local copies of their files and data, operating independently of centralized cloud uptime.

### What You Forfeit:
* **Storage Limits & Memory Overhead:** Mobile browsers enforce quota limits on IndexedDB and OPFS; holding large datasets in client memory strains lower-end devices.
* **Architectural Complexity:** Debugging eventual consistency bugs and CRDT tombstones requires specialized engineering expertise.
* **Server-Side Authorization & Invariant Enforcement:** Traditional relational constraints (e.g., unique username guarantees, complex balance checks) are difficult to enforce when multiple offline clients mutate concurrently.

---

## 3. Decision Bounds: When to Choose and Avoid

### Choose Local-First When:
* Building document editors, note-taking applications, project planning boards, creative design tools, or personal productivity software (e.g., Linear, Figma, Notion, Obsidian).
* Users frequently operate in degraded connectivity environments (airplanes, subways, field work).
* The user experience demands instantaneous interaction feedback without network round-trip delays.

### Avoid Local-First When:
* The core domain involves scarce resource allocation or strict linear financial transactions (e.g., airline seat reservations, ticket sales, banking ledgers, stock trading) where an authoritative central database must reject invalid concurrent transactions synchronously.
* The dataset is tens of gigabytes in size and cannot reasonably reside on a mobile client.

---

## 4. Enabling Ecosystem & Tooling
* **CRDT Engines:** Yjs, Automerge, Loro.
* **Sync Engines & Databases:** ElectricSQL, Replicache / Reflect, RxDB, PowerSync, Zero (Rocicorp), TinyBase.
* **Client Storage:** OPFS (Origin Private File System), PGlite, wa-sqlite, Dexie.js.
