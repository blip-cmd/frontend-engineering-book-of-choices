---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: Ink & Switch local-first essay (2019), Preguiça et al. 2018, Shapiro et al. SSS 2011 (abstract), Figma multiplayer post (2019), MDN storage quotas and Baseline pages, SQLite WASM persistence docs, PGlite docs, yjs 13.6.33, @automerge/automerge 3.5.0 (Node 24.18.1), loro-crdt 1.18.0, @sqlite.org/sqlite-wasm 3.54.1-build1, @electric-sql/pglite 0.5.17
review_by: 2027-05
reviewers:
ledger: reviews/local-first-and-offline-resilience.md
---

# Chapter 8: Local-First and Offline Resilience: CRDTs and Client Databases

> What if the network is a background worker, and the device holds the primary copy of the data? This chapter is for a tech lead deciding whether a web app should work that way, and if so, which merge model and browser storage engine to build on. Package versions were checked on npm on 2026-11-22.

---

## 1. Why a Cloud-First App Stops When the Network Does

In a cloud app, "the data on the server is treated as the primary, authoritative copy of the data", and a client copy "is merely a cache" ([Kleppmann et al., *Local-first software*, Ink & Switch, 2019](https://www.inkandswitch.com/essay/local-first/)). Every write waits for a server round trip. A commuter in a tunnel gets a spinner or an error; the 2019 essay reports that if Google Docs detects it is offline, it "blocks editing of the document"; and optimistic UI only hides the wait, because "until the request is complete, there is always the possibility that it may fail" (all from the same essay).

**Local-first architecture** moves the primary copy to the device. The app reads and writes local storage, and a sync layer exchanges changes with servers and other devices when a connection is available. Servers remain, but "they are in a supporting role, not the source of truth" ([Ink & Switch](https://www.inkandswitch.com/essay/local-first/)).

---

## 2. Four Properties to Check Before Calling an App Local-First

The [Ink & Switch essay](https://www.inkandswitch.com/essay/local-first/) lists seven ideals. Four of them define the architecture in this chapter:

| Property | Ink & Switch ideal | What it requires in a web app |
| :--- | :--- | :--- |
| **No network wait on user actions** | "No spinners: your work at your fingertips" | Reads and writes go to local storage and sync runs in the background; the essay adds that this "does not guarantee that the software will be fast" |
| **Works offline** | "The network is optional" | Local data, plus an app shell a service worker can load without a network (section 5) |
| **Concurrent edits converge** | Collaboration with colleagues | A merge model such as a CRDT (section 3) |
| **The user controls the data** | "You retain ultimate ownership and control" | Data the user can keep, export and back up, not data that exists only on the vendor's servers |

---

## 3. How CRDTs Converge, and What They Do Not Merge

Last-writer-wins on device timestamps does not follow causality: "Due to the clock skew among multiple nodes", timestamps "do not necessarily respect the happens-before relation" ([Preguiça, Baquero and Shapiro, 2018](https://arxiv.org/pdf/1805.06358.pdf)). Locks need every client online, which defeats offline work.

A **Conflict-free Replicated Data Type (CRDT)** lets any replica accept updates "without remote synchronisation", and its replicas "are guaranteed to converge" ([Shapiro et al., SSS 2011](https://link.springer.com/chapter/10.1007/978-3-642-24550-3_29)). Replicas exchange updates in one of two ways ([Preguiça et al.](https://arxiv.org/pdf/1805.06358.pdf)):

1. **State-based:** a replica sends its state, and the receiver merges it by computing the join (least upper bound) of the two states. *Cost:* resending full state is wasteful when the peer knows most of it; delta-state CRDTs send only recent changes.
2. **Operation-based:** a replica sends each operation. *Cost:* every operation must be "reliably delivered to all replicas", and "Most operation-based CRDT design require causal delivery".

The JavaScript libraries hide this choice behind their own update formats. **Yjs** (`yjs` 13.6) document updates "are commutative and idempotent" and "can be applied in any order and multiple times" ([Yjs README](https://github.com/yjs/yjs)); it supports text and rich-text editors such as ProseMirror, Tiptap and CodeMirror ([Yjs docs](https://docs.yjs.dev/)). **Automerge** (`@automerge/automerge` 3.5) calls itself "a local-first sync engine for multiplayer apps that works offline" and "remembers every change" ([Automerge](https://automerge.org/)). **Loro** (`loro-crdt` 1.18) runs "in Rust, JS (via WASM), and Swift" ([Loro README](https://github.com/loro-dev/loro)).

**Convergence does not mean every edit survives.** "The only type of change that a CRDT cannot automatically resolve is when multiple users concurrently update the same property of the same object" ([Ink & Switch](https://www.inkandswitch.com/essay/local-first/)). Automerge picks one "winner", the same on all nodes, and keeps the others in `getConflicts()` ([Automerge conflicts](https://automerge.org/docs/reference/documents/conflicts/)). This runs with Node 24 and `@automerge/automerge` 3.5 (save it as `merge.mjs`):

```js
import * as A from '@automerge/automerge'

// One shared starting document, copied to two devices.
const base = A.from({ task: { title: 'Draft', done: false } })
let phone = A.clone(base)
let laptop = A.clone(base)

// Both devices edit offline. Two writes hit the same property.
phone = A.change(phone, d => { d.task.title = 'Draft v2' })
laptop = A.change(laptop, d => { d.task.title = 'Final draft'; d.task.done = true })

// Reconnect: each side merges the other's changes.
const a = A.merge(A.clone(phone), laptop)
const b = A.merge(A.clone(laptop), phone)

console.log(a.task, b.task)                 // identical on both devices
console.log(A.getConflicts(a.task, 'title')) // both titles are still recorded
```

Both devices print the same task with `done: true`, but only one title is visible, and which one wins varies between runs. If a lost value matters, show the conflict to the user or model the data so concurrent edits land on different properties.

**When a CRDT is the wrong choice:** when a server is always present to order writes. Figma orders changes on its server and says "Figma isn't using true CRDTs", because CRDTs carry "some unavoidable performance and memory overhead" ([Figma engineering, 2019](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)). Long-lived documents also pay for history: in the Ink & Switch prototypes, "Performance and memory/disk usage quickly became a problem because CRDTs store all history" ([Ink & Switch](https://www.inkandswitch.com/essay/local-first/)).

---

## 4. Choose the Browser Storage Engine: IndexedDB, SQLite over OPFS, or PGlite

| Engine | What it gives you | When it is the wrong choice |
| :--- | :--- | :--- |
| **IndexedDB**, directly or through a CRDT library's adapter | A transactional object store with indexes; Baseline widely available since July 2015 ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/indexedDB)) | When you need joins or ad hoc queries: "IndexedDB is not a relational database", "does not use Structured Query Language (SQL)", and has no equivalent of `LIKE` ([MDN IndexedDB terminology](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Basic_Terminology)) |
| **SQLite in WebAssembly over OPFS** (`@sqlite.org/sqlite-wasm` 3.54) | Full SQL. OPFS "offers in-place write access" ([MDN OPFS](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system), Baseline widely available since March 2023), and its synchronous access handles work only in dedicated workers ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/FileSystemFileHandle/createSyncAccessHandle)). The `opfs-sahpool` VFS gives "Easily the highest OPFS performance" of SQLite's options and needs no COOP/COEP headers ([SQLite WASM persistence](https://sqlite.org/wasm/doc/trunk/persistence.md)) | When several tabs write one database and you cannot coordinate them: `opfs-sahpool` "Does not support multiple simultaneous connections to the same database", and the multi-tab `opfs` VFS needs COOP/COEP headers for its concurrency support ([SQLite WASM persistence](https://sqlite.org/wasm/doc/trunk/persistence.md)) |
| **PGlite** (`@electric-sql/pglite` 0.5) | "Postgres in WASM", built by Electric to sync "a subset of their server-side Postgres database" ([PGlite](https://pglite.dev/docs/about)); persists to IndexedDB or OPFS | When Safari needs the OPFS backend: it does not work there, because Safari appears to limit open sync access handles below a Postgres install's file count. The IndexedDB backend loads all files into memory on start and flushes changed files after each query ([PGlite filesystems](https://pglite.dev/docs/filesystems)) |

**Every engine sits on best-effort storage by default.** An app whose data "isn't persisted anywhere else" should call `navigator.storage.persist()` ([MDN storage quotas and eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria); [MDN `persist()`](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist), Baseline widely available since December 2021). From the same MDN quota page: Chromium browsers let an origin use up to 60% of total disk, and Firefox the smaller of 10% of disk or 10 GiB in best-effort mode; with tracking prevention on, Safari deletes script-created data after "no user interaction, such as click or tap, in the last seven days of browser use"; and eviction removes "all of its data, not parts of it". Read the real limit with `navigator.storage.estimate()` and handle `QuotaExceededError`.

---

## 5. Cloud-First or Local-First: What Each Costs

| Dimension | Cloud-first (server is the source of truth) | Local-first (device holds the primary copy) |
| :--- | :--- | :--- |
| **Write latency** | Each write waits for a server round trip ([Ink & Switch](https://www.inkandswitch.com/essay/local-first/)) | Writes "only require local durability" ([Preguiça et al.](https://arxiv.org/pdf/1805.06358.pdf)): a local storage write, not zero |
| **Offline writes** | A queue; the Background Synchronization API can defer sends to a service worker, but it has Limited availability and is not Baseline ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API)) | Reads and writes work offline once a service worker caches the app shell; `ServiceWorker` is Baseline widely available since April 2018 ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorker)) |
| **Real-time collaboration** | Server logic orders and broadcasts changes | The CRDT merges, but "CRDT algorithms provide only for the merging of data"; transport is still yours to build or buy ([Ink & Switch](https://www.inkandswitch.com/essay/local-first/)) |
| **Engineering complexity** | Standard request and response patterns | Higher (this book's judgment): sync, schema changes on every client, history growth, conflict UI |
| **Storage risk** | Little user data on the client | Quotas and eviction (section 4) |
| **Global invariants** | The server rejects invalid writes | Some operations "require global agreement", such as "closing the auction and selecting a single winning bid" ([Preguiça et al.](https://arxiv.org/pdf/1805.06358.pdf)) |

---

## 6. When to Choose Local-First, and When It Is the Wrong Choice

### Choose local-first when:

* Users create documents or personal data: the essay scopes local-first to apps for "text, graphics, spreadsheets, CAD drawings, or music" and to "notes, calendars, to-do lists, or password managers" ([Ink & Switch](https://www.inkandswitch.com/essay/local-first/)). Obsidian, for example, "stores your notes locally as plain text Markdown files" ([Obsidian](https://obsidian.md/)).
* Users expect instant feedback without spinners or save buttons, and edits from several devices must merge.
* Users work with intermittent connectivity, such as field staff or travellers (this book's examples).

### Local-first is the wrong choice when:

* **The domain needs one authority.** The essay excludes "banking services, e-commerce, social networking, ride-sharing, or similar services, which are well served by centralized systems" ([Ink & Switch](https://www.inkandswitch.com/essay/local-first/)). Some writes cannot be merged after the fact: "closing the auction and selecting a single winning bid will require global agreement" ([Preguiça et al.](https://arxiv.org/pdf/1805.06358.pdf)).
* **The app mostly reads server data.** This book's position: a server cache (Chapter 3) is simpler, and a service worker cache covers offline reading.
* **The browser is the only copy and users visit rarely.** Safari's seven-day rule and best-effort storage (section 4) can delete unsynced work, and the essay itself prefers "a locally installed executable" to "a tab in a web browser" for offline use ([Ink & Switch](https://www.inkandswitch.com/essay/local-first/)).
* **A server is always there to order writes.** Figma's server-ordered model avoids CRDT overhead and still lets users "go offline for an arbitrary amount of time and continue editing" ([Figma engineering](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)).

---

## 7. References

* Martin Kleppmann, Adam Wiggins, Peter van Hardenberg and Mark McGranaghan: [*Local-first software: You own your data, in spite of the cloud*](https://www.inkandswitch.com/essay/local-first/), Onward! 2019
* Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski: [*Conflict-Free Replicated Data Types*](https://link.springer.com/chapter/10.1007/978-3-642-24550-3_29), SSS 2011
* Nuno Preguiça, Carlos Baquero and Marc Shapiro: [*Conflict-free Replicated Data Types*](https://arxiv.org/abs/1805.06358), Encyclopedia of Big Data Technologies, 2018
* [Yjs README](https://github.com/yjs/yjs); [Automerge](https://automerge.org/)
* [MDN: Storage quotas and eviction criteria](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria); [SQLite WASM persistence](https://sqlite.org/wasm/doc/trunk/persistence.md)
* [Further reading: *Designing Data-Intensive Applications* (Martin Kleppmann)](../library/reading_list.md)
