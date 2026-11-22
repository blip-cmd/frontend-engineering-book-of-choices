---
page: book/08_local_first_and_offline_resilience.md
verified: 2026-11-22
---

# Claim Ledger: Chapter 8, Local-First and Offline Resilience

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead deciding whether a web app should keep the primary copy of its data on the device and sync in the background. The page helps them decide between cloud-first and local-first, and within local-first, between a CRDT and a server-ordered merge model and between browser storage engines (IndexedDB, SQLite over OPFS, PGlite). Thesis (kept from the draft): local-first suits apps where users create and own documents and work with intermittent connectivity; it costs engineering complexity, storage-eviction risk and the ability to enforce global invariants, so domains that need a single authority (bookings, balances, auctions) should stay cloud-first.

**History.** Author pass on 2026-11-22 rewrote the AI-generated draft. Among other errors, the draft promised "Exactly 0 ms" writes, "100%" offline support, "100-400 ms" cloud write latency, sub-millisecond local queries and "disk throughput competitive with native desktop software" (no primary source found for any figure; removed or made qualitative); said IndexedDB lacks "complex indexing" (MDN: IndexedDB uses indexes; what it lacks is SQL and relational tables); named Figma as a local-first example (the Ink & Switch essay lists Figma among cloud web apps, and Figma says it does not use true CRDTs); claimed CRDTs make all nodes converge without noting that concurrent writes to one property keep one visible value; classified Yjs, Automerge and Loro as "operation-based" (the Yjs README describes commutative, idempotent updates that can be applied in any order and exchanged as state-vector diffs, closer to delta-state); and cited a Yjs paper title ("Yjs: A CRDT Framework for Shared Editing") that could not be found, plus two links to unverified `library/` research notes. All were corrected or removed.

**Recommendation changes (rule A1).**
1. "Choose local-first for ... Linear, Figma, Obsidian, Notion" became a scope taken from the Ink & Switch essay (documents and personal data repositories) with Obsidian as the one sourced example. Figma was removed because the essay groups it with cloud web apps and Figma's own post says "Figma isn't using true CRDTs". Linear and Notion were removed: no primary source found that describes either as local-first.
2. "Avoid local-first" kept its bookings, balances and auctions examples, now backed by the essay's own exclusion of "banking services, e-commerce ..." and by Preguiça et al.'s auction example ("selecting a single winning bid will require global agreement"). Added three sourced or labelled "wrong choice" cases: mostly-read apps (labelled as the book's position), browser-only copies on rarely visited sites (MDN Safari eviction; essay prefers installed executables), and apps with an always-present ordering server (Figma).
3. Section 4 now gives each storage engine a concrete "when it is the wrong choice" from its own docs (IndexedDB: no SQL; SQLite `opfs-sahpool`: no multiple simultaneous connections; PGlite: OPFS backend fails in Safari).

**Headings.** The page had no "The Landscape of Choices" heading, but its generic headings ("The Core Dilemma", "The Four Pillars of Local-First Architecture", "The Mathematics of Convergence", "The Local Storage Engine", "Comparative Trade-offs", "Decision Playbook", "References & Library Audits") were replaced with headings that state what each section decides. The ASCII box diagram of the "four pillars" became a table mapped to the essay's ideals (dimension D8).

**Length.** The page grew from about 870 to about 1,870 words (including a 20-line code example), because every claim now carries its quote and source. No new sections were added.

---

## 1. Author pass (2026-11-22)

Sources were fetched in the same session with `curl -sL` (HTML stripped to text, PDFs converted with `pdftotext`) and quotes matched against the text. Package versions came from `npm view` on 2026-11-22. The page's code block was extracted and run with Node 24.18.1 and `@automerge/automerge` 3.5.0 in a temp folder outside the repository.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | In cloud apps "the data on the server is treated as the primary, authoritative copy of the data"; a client copy "is merely a cache" | [Ink & Switch, *Local-first software* (Kleppmann, Wiggins, van Hardenberg, McGranaghan; Onward! 2019, doi:10.1145/3359591.3359737)](https://www.inkandswitch.com/essay/local-first/) | verified (quote) |
| 2 | Google Docs offline "blocks editing of the document"; optimistic UI: "until the request is complete, there is always the possibility that it may fail" | Ink & Switch essay | verified (quote) |
| 3 | Servers in local-first "are in a supporting role, not the source of truth" | Ink & Switch essay | verified (quote) |
| 4 | Seven ideals; titles "No spinners: your work at your fingertips", "The network is optional", "You retain ultimate ownership and control"; ideal 4 is collaboration; local storage "does not guarantee that the software will be fast" | Ink & Switch essay | verified (quote); ideal 4 paraphrased to avoid its title |
| 5 | Timestamps under clock skew "do not necessarily respect the happens-before relation" | [Preguiça, Baquero, Shapiro, *Conflict-free Replicated Data Types* (arXiv 1805.06358; Encyclopedia of Big Data Technologies, 2018)](https://arxiv.org/pdf/1805.06358.pdf) | verified (quote); journal reference confirmed on the [arXiv abstract page](https://arxiv.org/abs/1805.06358) |
| 6 | CRDT replicas accept updates without remote synchronisation and "are guaranteed to converge" | [Shapiro et al., SSS 2011 (Springer abstract)](https://link.springer.com/chapter/10.1007/978-3-642-24550-3_29) | verified (quote); the HAL full text was blocked by a bot check, so only the abstract was read |
| 7 | State-based merge computes the join (least upper bound); delta-state CRDTs send only recent changes; op-based needs operations "reliably delivered to all replicas"; "Most operation-based CRDT design require causal delivery" | Preguiça et al. 2018 | verified (quote); draft's "commutative, associative, and idempotent" replaced by the source's join wording; draft's "Bandwidth efficiency matches standard WebSocket streaming" removed (no source) |
| 8 | Yjs updates "are commutative and idempotent" and "can be applied in any order and multiple times"; state vectors allow diff sync | [Yjs README](https://github.com/yjs/yjs) | verified (quote); draft's "operation-based" classification removed |
| 9 | Yjs editor bindings include ProseMirror, Tiptap, CodeMirror | [Yjs docs](https://docs.yjs.dev/) | verified |
| 10 | Automerge is "a local-first sync engine for multiplayer apps that works offline" and "remembers every change" | [Automerge](https://automerge.org/) | verified (quote); draft's "optimized for structured JSON documents" removed |
| 11 | Loro usable "in Rust, JS (via WASM), and Swift" | [Loro README](https://github.com/loro-dev/loro) | verified (quote); draft's "high-performance" removed as a vendor self-description |
| 12 | "The only type of change that a CRDT cannot automatically resolve is when multiple users concurrently update the same property of the same object" | Ink & Switch essay | verified (quote) |
| 13 | Automerge picks one "winner", the same on all nodes; others available via `getConflicts()` | [Automerge conflicts](https://automerge.org/docs/reference/documents/conflicts/) | verified (quote) |
| 14 | Code example: both replicas converge, `done: true` survives, one title visible, `getConflicts()` returns both titles, winner varies | Node 24.18.1 run, `@automerge/automerge` 3.5.0, 11 runs | verified (run); winner was `Final draft` 4 times and `Draft v2` 7 times; both replicas always matched |
| 15 | "Figma isn't using true CRDTs"; CRDTs carry "some unavoidable performance and memory overhead"; Figma lets users "go offline for an arbitrary amount of time and continue editing"; post dated 2019 | [Figma engineering (October 16, 2019)](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/) | verified (quote); consistent with the verified collaborative canvas playbook |
| 16 | "Performance and memory/disk usage quickly became a problem because CRDTs store all history" | Ink & Switch essay | verified (quote) |
| 17 | IndexedDB: transactional, uses indexes; Baseline widely available since July 2015 | [MDN IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API); [MDN Window.indexedDB](https://developer.mozilla.org/en-US/docs/Web/API/Window/indexedDB) | verified (quote); draft's "lacking complex indexing" corrected |
| 18 | "IndexedDB is not a relational database"; "does not use Structured Query Language (SQL)"; no equivalent of `LIKE` | [MDN IndexedDB terminology](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Basic_Terminology) | verified (quote) |
| 19 | OPFS "offers in-place write access"; Baseline widely available since March 2023; `createSyncAccessHandle()` only in dedicated workers | [MDN OPFS](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system); [MDN createSyncAccessHandle()](https://developer.mozilla.org/en-US/docs/Web/API/FileSystemFileHandle/createSyncAccessHandle) | verified (quote) |
| 20 | SQLite `opfs-sahpool`: "Easily the highest OPFS performance", no COOP/COEP needed, "Does not support multiple simultaneous connections to the same database"; `opfs` VFS needs COOP/COEP for concurrency support | [SQLite WASM persistence](https://sqlite.org/wasm/doc/trunk/persistence.md) | verified (quote) |
| 21 | PGlite is "Postgres in WASM", developed by Electric to sync "a subset of their server-side Postgres database" | [PGlite: What is PGlite](https://pglite.dev/docs/about) | verified (quote) |
| 22 | PGlite OPFS backend does not work in Safari (open sync access handle limit below a Postgres install's file count); IndexedDB backend loads all files into memory and flushes whole files after each query | [PGlite filesystems](https://pglite.dev/docs/filesystems) | verified; the exact handle and file counts were left off the page |
| 23 | Removed: "Local query execution times measuring under 1 millisecond", "throughput competitive with native desktop software" | none found | removed (gate G1, rule A14) |
| 24 | Storage is best-effort by default; data that "isn't persisted anywhere else" should use `navigator.storage.persist()` | [MDN storage quotas and eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria) | verified (quote) |
| 25 | `persist()` Baseline widely available since December 2021 | [MDN persist()](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist) | verified |
| 26 | Chromium: up to 60% of total disk per origin; Firefox best-effort: smaller of 10% of disk or 10 GiB | MDN storage quotas and eviction | verified |
| 27 | Safari, with tracking prevention: deletes script-created data after "no user interaction, such as click or tap, in the last seven days of browser use"; eviction deletes "all of its data, not parts of it"; `QuotaExceededError` | MDN storage quotas and eviction | verified (quote) |
| 28 | `navigator.storage.estimate()` exists (Baseline widely available since September 2023) | [MDN estimate()](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/estimate) | verified; the date is not on the page |
| 29 | Each cloud write needs a server round trip | Ink & Switch essay ("all data modifications ... require a round-trip to a server") | verified; draft's "100-400 ms" removed |
| 30 | CRDT writes "only require local durability" | Preguiça et al. 2018 | verified (quote); draft's "Exactly 0 ms" corrected |
| 31 | Background Synchronization API defers tasks to a service worker; Limited availability, not Baseline | [MDN Background Sync](https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API) | verified |
| 32 | `ServiceWorker` Baseline widely available since April 2018 | [MDN ServiceWorker](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorker) | verified; draft's "100% Native full read/write offline support" corrected |
| 33 | "CRDT algorithms provide only for the merging of data" | Ink & Switch essay | verified (quote); draft's "Built directly into data model semantics" corrected |
| 34 | Some operations "require global agreement", such as "closing the auction and selecting a single winning bid" | Preguiça et al. 2018 | verified (quote) |
| 35 | Local-first scope: "text, graphics, spreadsheets, CAD drawings, or music", "notes, calendars, to-do lists, or password managers"; excludes "banking services, e-commerce, social networking, ride-sharing, or similar services, which are well served by centralized systems" | Ink & Switch essay | verified (quote) |
| 36 | Obsidian "stores your notes locally as plain text Markdown files" | [Obsidian](https://obsidian.md/) | verified (quote) |
| 37 | The essay prefers "a locally installed executable" to "a tab in a web browser" for offline support | Ink & Switch essay | verified (quote) |
| 38 | Versions: yjs 13.6.33, @automerge/automerge 3.5.0, loro-crdt 1.18.0, @sqlite.org/sqlite-wasm 3.54.1-build1, @electric-sql/pglite 0.5.17 | `npm view` | verified; repositories match yjs, automerge, loro-dev, sqlite and electric-sql. Also checked but not on the page: @electric-sql/client 1.5.28, tinybase 10.1.0, dexie 4.4.7, rxdb 17.6.0, replicache 15.3.0 |
| 39 | References: Onward! 2019 citation; Shapiro et al. SSS 2011; Preguiça et al. 2018 | Ink & Switch essay (citation block); Springer chapter page; arXiv abstract page | verified; draft's "Kevin Jahns: *Yjs: A CRDT Framework for Shared Editing*" not found and replaced by the Yjs README; two `library/` research-note links removed |
| 40 | Engineering complexity is higher for local-first; read-mostly apps fit a server cache better; field staff and travellers as intermittent-connectivity examples | none | the book's judgment, labelled as such on the page |

## 2. Independent verifier pass (2026-11-22)

A separate agent that did not write the page or section 1 extracted the claims from the page itself (48 claims: every quote, number, Baseline date, version, attribution and reference) and checked each against its source, fetched again on 2026-11-22 with `curl -sL` (HTML stripped to text; the arXiv PDF converted with `pdftotext`) and matched by case-insensitive substring search with whitespace normalised. Also read for context: the WebKit posts [Full Third-Party Cookie Blocking and More (2020)](https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/) and [Updates to Storage Policy (2023)](https://webkit.org/blog/14403/updates-to-storage-policy/), to check MDN's Safari wording (not cited on the page).

**Verdict: PASS** after 7 edits. 41 claims SUPPORTED as written, 7 PARTIAL corrected, 0 UNSUPPORTED left. Every number on the page (60%, 10%, 10 GiB, seven days, Baseline months, versions) has a source in its paragraph.

**Checks that held.**
* Ink & Switch: all 17 quotes appear verbatim, including the seven ideal titles and the citation block (Onward! 2019, pages 154 to 178, doi:10.1145/3359591.3359737). The essay groups Figma with web apps (Google Docs, Trello, Figma, Pinterest) and with "installable desktop clients that are essentially repackaged web browsers"; the page does not call Figma local-first. The "store all history" quote comes from the PushPin prototype, which the page's "in the Ink & Switch prototypes" covers.
* Figma (Evan Wallace, October 16, 2019): "Figma isn't using true CRDTs though", "some unavoidable performance and memory overhead" (because "our server is the central authority"), "go offline for an arbitrary amount of time and continue editing": verbatim.
* Preguiça, Baquero, Shapiro: all six quotes verbatim; title, authors and Encyclopedia of Big Data Technologies (Springer, 2018) confirmed on the PDF and the arXiv abstract page.
* Shapiro et al. 2011: only the Springer abstract was read. The page now uses only two phrases from it ("without remote synchronisation", "are guaranteed to converge") plus the reference entry (four authors, SSS 2011, LNCS 6976), all on the Springer page. Nothing else on the page rests on this paper.
* MDN quota page (last modified Jan 5, 2026): best-effort by default; "isn't persisted anywhere else"; Chromium 60% of total disk in both modes; Firefox best-effort the smaller of 10% of disk or the 10 GiB group limit; Safari proactive eviction "when cross-site tracking prevention is turned on" after "no user interaction, such as click or tap, in the last seven days of browser use"; "all of its data, not parts of it"; `QuotaExceededError` for IndexedDB, Cache and OPFS; `estimate()`. All match. MDN's Safari wording agrees with WebKit's 2020 "7-Day Cap on All Script-Writeable Storage" (WebKit adds that Home Screen web apps have their own day counter; the page's "can delete" stays accurate).
* Baseline: Window.indexedDB July 2015, OPFS March 2023, createSyncAccessHandle() March 2023 (dedicated workers only), persist() December 2021, ServiceWorker April 2018, estimate() September 2023; Background Synchronization API Limited availability, not Baseline. All match MDN.
* SQLite WASM persistence, MDN IndexedDB terminology and OPFS, PGlite about page, Automerge home and conflicts docs, Loro README, Obsidian: quotes verbatim. The Yjs README writes "*commutative* and *idempotent*" (emphasis only).
* Versions (`npm view`, 2026-11-22): yjs 13.6.33, @automerge/automerge 3.5.0, loro-crdt 1.18.0, @sqlite.org/sqlite-wasm 3.54.1-build1, @electric-sql/pglite 0.5.17; repositories yjs/yjs, automerge/automerge, loro-dev/loro, sqlite/sqlite-wasm, electric-sql/pglite.

**Edits (PARTIAL, reworded to match the source).**
1. Section 1, Google Docs: "Google Docs, when it detects it is offline" became "the 2019 essay reports that if Google Docs detects it is offline". The observation is from 2019 and the page stated it as current.
2. Section 3, clock skew: "Last-writer-wins on device timestamps is unreliable for merging offline edits" became "does not follow causality". Preguiça et al. say timestamps "do not necessarily respect the happens-before relation", then use them to define last-writer-wins; they do not call it unreliable.
3. Section 3, Shapiro et al.: "accept a write without coordination" became "accept updates 'without remote synchronisation'", the abstract's wording.
4. Section 3, state-based CRDTs: deleted "so merge order and repetition do not change the result". Preguiça et al. say only that the merge computes the join; the cited text never states the order or idempotence property.
5. Section 3, Yjs: "bindings for rich text editors such as ProseMirror, Tiptap and CodeMirror" became "supports text and rich-text editors such as ...". The Yjs docs say "text and rich-text editors", and CodeMirror is a code editor.
6. Section 4, PGlite: "Safari limits" became "Safari appears to limit" (the docs say "Safari appears to have a limit of 252 open sync access handles"), and "flushes whole files after each query" became "flushes changed files" (the docs: "flushing them to IndexedDB after each query if they have changed").
7. Section 6, global agreement: "Seat reservations, balances and auction results need a server to validate and serialize writes, because offline replicas cannot agree on one winner" became "Some writes cannot be merged after the fact: 'closing the auction and selecting a single winning bid will require global agreement'". Preguiça et al. give only the auction example, and in the next sentences say escrow techniques (the Bounded Counter CRDT) can keep a counter from going negative without global coordination, which goes against citing them for balances. Balances stay covered by the essay's exclusion of "banking services" in the same bullet.

**Code checks.** The page's `merge.mjs` block was extracted unchanged and run with Node 24.18.1 and `@automerge/automerge` 3.5.0 (`npm ls` confirmed) in a scratch folder outside the repository, 16 runs. Both replicas always printed the same task with `done: true`; `getConflicts(a.task, 'title')` returned both titles under two actor IDs; the visible title was `Draft v2` 11 times and `Final draft` 5 times. The page's claim that the winner varies between runs holds.

**Not errors, left as they are.** "A commuter in a tunnel gets a spinner or an error" is an illustration, not a quote, and has no numbers. "Locks need every client online" is uncontroversial background. Recommendation change 2 at the top of this ledger mentions seat reservations and balances; after edit 7 the page names auctions (Preguiça et al.) and banking (the essay) only.

## 3. Known omissions (follow-up content, not errors)

* Sync engines as an alternative to CRDT libraries: Electric (read-path sync, client `@electric-sql/client`), Zero (Replicache's successor; Replicache is in maintenance mode), PowerSync. Chapter 3 covers Electric and Replicache.
* IndexedDB wrappers and reactive stores: Dexie, RxDB, TinyBase.
* Schema migrations across offline clients, and end-to-end encryption of synced data (an Ink & Switch ideal the page leaves out).
* Multi-tab coordination for SQLite over OPFS (Web Locks, `BroadcastChannel`, the `opfs-sahpool` pause API).
* Service worker update strategy for the offline app shell, and the Cache API's place in the same eviction unit.
* Auth and access control when the server is not the source of truth.

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 1 | 2 | **18** |

D8 is 1 because sections 5 and 6 refer back to sections 3 and 4. D9 is 1 because the one code example shows the conflict behaviour but not storage or sync code. All gates pass except G8 (human accountability), which an `agent-verified` status would disclose instead.
