---
page: book/09_decision_playbooks/collaborative_canvas_workspace.md
verified: 2026-11-21
---

# Claim Ledger: Decision Playbook, Collaborative Canvas & Document Workspaces

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead starting a multi-user whiteboard, design tool, diagramming tool or collaborative editor. The page helps them choose the rendering, sync, transport and local-storage layers. Thesis (kept from the draft): render the workspace on a canvas, sync it with a CRDT library (Yjs or Automerge), keep ephemeral presence out of the document, persist locally for offline work, and keep menus and panels in the DOM.

**History.** Author pass on 2026-11-21 rewrote the AI-generated draft. Among other errors, the draft recommended WebGPU for rendering (PixiJS 8 marks its WebGPU renderer "Experimental" and recommends WebGL for production; MDN lists WebGPU as Limited availability); promised "mathematically guaranteed document convergence without data loss" (concurrent writes to one property keep a single visible value in both Yjs and Automerge, confirmed by a Node run); said WebSockets "provide persistence" (persistence is a server backend concern per the y-websocket README); and carried unsourced numbers ("10,000 editable shapes", ">50 MB", "millions of vector coordinates"), which were removed.

**Recommendation changes (rule A1).**
1. Rendering: "HTML5 Canvas / WebGPU" became Canvas 2D or WebGL (PixiJS 8.23 WebGL renderer, Konva 10.10), with WebGPU named as not yet production-ready, per the [PixiJS renderers guide](https://pixijs.com/8.x/guides/components/renderers) and [MDN WebGPU](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API).
2. "Do NOT render canvas elements as DOM or SVG nodes" became "do not render a DOM node per shape with no culling": tldraw renders shapes as DOM elements with spatial-index culling ([tldraw performance docs](https://tldraw.dev/sdk-features/performance)).
3. "Do NOT use naive Last-Write-Wins" became "do not use whole-document last-write-wins on client clocks": Figma uses per-property last-writer-wins ordered by its server ([Figma engineering](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)), and Automerge resolves same-property conflicts by operation ID, "not a wall clock time" ([Automerge conflicts](https://automerge.org/docs/reference/documents/conflicts/)). The draft's "clock drift guarantees" data loss was removed.
4. Transport: WebRTC data channels are now optional rather than part of the recommended pair, since y-websocket already distributes awareness (presence) through the server, and y-webrtc's own README says a full mesh does not suit many collaborators.
5. Added "When this playbook is the wrong choice" (requested for all playbooks), built on the Figma, MDN, tldraw and y-webrtc sources plus one labelled position.

---

## 1. Author pass (2026-11-21)

Sources were fetched in the same session (curl, HTML stripped to text) and quotes matched against the text. Package versions came from `npm view` on 2026-11-21. The page's one code block was extracted and run with Node 24.18.1 and `yjs` 13.6.33.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | "All CRDTs satisfy certain mathematical properties which guarantee eventual consistency" | [Figma: How Figma's multiplayer technology works (Evan Wallace, 2019-10-16)](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/) | verified (quote) |
| 2 | Canvas content "is not exposed to accessibility tools as semantic HTML is"; a canvas is a bitmap with no information about drawn objects | [MDN `<canvas>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/canvas) | verified (quote) |
| 3 | PixiJS 8 renderers: WebGL recommended, WebGPU and Canvas "Experimental"; "Use the WebGL renderer for production applications" | [PixiJS renderers guide](https://pixijs.com/8.x/guides/components/renderers) | verified (quote); draft's WebGPU recommendation corrected |
| 4 | WebGPU is Limited availability, not Baseline | [MDN WebGPU API](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API) | verified |
| 5 | WebGL2 Baseline widely available since September 2021 | [MDN WebGL2RenderingContext](https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext) | verified (quote) |
| 6 | Konva is a Canvas 2D framework; "Each Layer is a separate `<canvas>` element" | [Konva docs](https://konvajs.org/docs/index.html) | verified (quote) |
| 7 | Yjs shared types "automatically merge without merge conflicts" | [Yjs docs](https://docs.yjs.dev/) | verified (quote) |
| 8 | Yjs bindings for ProseMirror, Tiptap, Quill, CodeMirror, Monaco, Lexical | [Yjs README](https://github.com/yjs/yjs) | verified |
| 9 | Text CRDTs "only grow in size"; Yjs merges structs and garbage-collects some tombstones | [Yjs README](https://github.com/yjs/yjs) | verified (quote) |
| 10 | Automerge supports rich text with marks and blocks | [Automerge rich text](https://automerge.org/docs/reference/documents/rich-text/) | verified |
| 11 | WebSocket is "layered over TCP" | [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455) | verified (quote); ordering follows from TCP |
| 12 | y-websocket server "distributes awareness information and document updates among clients"; persistence depends on the backend | [y-websocket README](https://github.com/yjs/y-websocket) | verified (quote); draft's "WebSockets provide persistence" corrected |
| 13 | `createDataChannel()` options `ordered` (default true) and `maxRetransmits` for unreliable mode | [MDN createDataChannel()](https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection/createDataChannel) | verified; draft's "ultra-low-latency" removed |
| 14 | WebRTC needs signaling; symmetric NAT requires relaying through TURN | [MDN WebRTC protocols](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols); [y-webrtc README](https://github.com/yjs/y-webrtc) | verified |
| 15 | y-webrtc is a full mesh, "Not suited for a large amount of collaborators on a single document" | [y-webrtc README](https://github.com/yjs/y-webrtc) | verified (quote) |
| 16 | y-indexeddb loads changes "from the local browser database"; makes offline editing possible; `synced` fires once "all available content has been loaded", also when empty | [y-indexeddb docs](https://docs.yjs.dev/ecosystem/database-provider/y-indexeddb) | verified (quote) |
| 17 | `@automerge/automerge-repo-storage-indexeddb` stores Automerge Repo data in IndexedDB | [Automerge storage docs](https://automerge.org/docs/reference/repositories/storage/) | verified |
| 18 | IndexedDB Baseline widely available since July 2015 | [MDN Window.indexedDB](https://developer.mozilla.org/en-US/docs/Web/API/Window/indexedDB) | verified (quote) |
| 19 | OPFS Baseline widely available since March 2023; `createSyncAccessHandle()` only in dedicated workers | [MDN OPFS](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system); [MDN createSyncAccessHandle()](https://developer.mozilla.org/en-US/docs/Web/API/FileSystemFileHandle/createSyncAccessHandle) | verified (quote); draft's "writes to disk instantly ... without losing a single stroke" removed |
| 20 | Storage is best-effort by default; `navigator.storage.persist()` opts in to persistent storage | [MDN storage quotas and eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria) | verified |
| 21 | tldraw renders shapes as DOM elements, keeps a spatial index, and hides off-screen shapes with `display: none`; claims "smooth performance even with thousands of shapes" | [tldraw performance docs](https://tldraw.dev/sdk-features/performance); [tldraw culling](https://tldraw.dev/sdk-features/culling) | verified (quote); labelled as the vendor's claim |
| 22 | Figma resolves same-property conflicts with "the last value that was sent to the server", server-ordered, no timestamp; "Figma isn't using true CRDTs"; CRDTs carry "some unavoidable performance and memory overhead"; client/server over WebSockets | [Figma engineering](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/) | verified (quote) |
| 23 | Automerge picks a deterministic winner for concurrent writes to one property, keeps losers in `getConflicts()`, orders by operation ID "not a wall clock time" | [Automerge conflicts](https://automerge.org/docs/reference/documents/conflicts/) | verified (quote) and reproduced with `@automerge/automerge` 3.5.0 in Node |
| 24 | Yjs keeps one value when two replicas set the same `Y.Map` key; other keys survive; replicas converge | Node 24.18.1 run of the page's example with `yjs` 13.6.33 | verified (run); output `{ color: 'blue', x: 10 }` on both replicas (winner varies by client ID) |
| 25 | "Awareness information isn't stored in the Yjs document, as it doesn't need to be persisted across sessions" | [Yjs awareness guide](https://docs.yjs.dev/getting-started/adding-awareness) | verified (quote) |
| 26 | rbush is an R-tree library for queries like "all items within this bounding box" | [rbush README](https://github.com/mourner/rbush) | verified (quote) |
| 27 | PixiJS `CullerPlugin` skips off-screen containers; culling is off by default; helps when GPU-bound, can hurt when CPU-bound | [PixiJS culler guide](https://pixijs.com/8.x/guides/components/application/culler-plugin); [PixiJS performance tips](https://pixijs.com/8.x/guides/concepts/performance-tips) | verified (quote) |
| 28 | Versions: yjs 13.6.33, y-websocket 3.1.0, y-webrtc 10.3.0, y-indexeddb 9.0.12, @automerge/automerge 3.5.0, pixi.js 8.23.0, konva 10.10.0, rbush 4.0.1 | `npm view` | verified; owners match the yjs, automerge, pixijs, konvajs and mourner repositories. `@automerge/automerge-repo` has an alpha on its `latest` tag (2.6.0-alpha.3), so no version is pinned for it |
| 29 | Removed: "10,000 editable shapes", ">50 MB", "millions of vector coordinates", "clock drift guarantees" overwrites, "zero perceived latency" | none found | removed or made qualitative (gate G1, rule A14) |
| 30 | Whole-document LWW on client clocks drops concurrent edits to unrelated shapes; cursors over unreliable channels suit "newest only" data; single-editor documents do not need a sync layer | none | explanatory reasoning; the last is labelled as the book's position |

## 2. Independent verifier pass (2026-11-22)

A separate agent that did not write the page or section 1 extracted the claims from the page itself (34 factual claims, plus versions and dates), fetched every cited source with `curl -sL` (HTML stripped to text) and searched the text for each quote.

**Verdict: PASS** after three corrections. 31 claims SUPPORTED as written, 3 PARTIAL corrected, 0 UNSUPPORTED left. Every number (versions, Baseline dates, the 2019 Figma date) traces to npm, MDN or the cited post.

**Edits to the page.**

1. Multiplayer state sync row: "Yjs reduces the overhead by merging and garbage-collecting structs" was PARTIAL. The Yjs README says "We can't garbage collect deleted structs (tombstones) while ensuring a unique order of the structs" and lists three mitigations. Reworded to match: merging structs, deleting the content of deleted structs, and garbage-collecting tombstones only once their order no longer matters (for example when the parent was deleted).
2. Transport row: "peers need a signaling server" was cited to MDN WebRTC protocols, whose article body does not discuss signaling (the word appears only in the sidebar). Deleted that clause; the symmetric NAT and TURN relay claim stays, because the MDN article says TURN relays "all information through that server".
3. Section 5, first bullet: the heading "There is always a server and offline editing is not a requirement" used Figma as its example, but the same Figma post says "Figma lets you go offline for an arbitrary amount of time and continue editing" without CRDTs. Deleted "and offline editing is not a requirement" so the condition matches the source.

**Claims confirmed verbatim** (quote found in the fetched source): Figma ("guarantee eventual consistency", "the same property on the same object", "the last value that was sent to the server", "Figma isn't using true CRDTs", "some unavoidable performance and memory overhead", client/server over WebSockets, 2019-10-16 by Evan Wallace); MDN canvas ("not exposed to accessibility tools as semantic HTML is"); PixiJS renderers (WebGPU "Experimental", "Use the WebGL renderer for production applications"); MDN WebGPU (Limited availability, not Baseline); MDN WebGL2 (Baseline widely available since September 2021); Konva ("Each Layer is a separate `<canvas>` element", Canvas 2D framework); Yjs docs ("automatically merge without merge conflicts"); Yjs README (bindings table lists ProseMirror, Tiptap, Quill, CodeMirror, Monaco and Lexical; "only grow in size"); Automerge rich text (marks and block markers); RFC 6455 ("layered over TCP"); y-websocket README ("distributes awareness information and document updates among clients"; backends "can persist to databases"); MDN createDataChannel (`ordered`, `maxRetransmits` in unreliable mode); y-webrtc README ("Not suited for a large amount of collaborators on a single document", each peer connected to each other); Automerge storage (`@automerge/automerge-repo-storage-indexeddb` stores data in IndexedDB); y-indexeddb ("from the local browser database", "Makes offline editing possible", `synced` fires when "all available content has been loaded" and when no content is available); MDN indexedDB (Baseline since July 2015); MDN OPFS and createSyncAccessHandle (Baseline since March 2023, dedicated workers only); MDN storage quotas (best-effort by default, `navigator.storage.persist()`); tldraw performance (spatial index, `display: none` on DOM elements, "smooth performance even with thousands of shapes on the canvas"); Automerge conflicts (deterministic winner, `getConflicts()`, "not a wall clock time"); Yjs awareness (quote verbatim); rbush ("all items within this bounding box", R-tree); PixiJS culler (CullerPlugin skips offscreen objects, not enabled by default) and performance tips (GPU-bound improves, CPU-bound degrades).

**Unsourced statements accepted as background** (no numbers): canvas shapes are pixels with no per-shape style or layout work; a DOM node per shape adds style and layout work; whole-document last-write-wins on client clocks drops unrelated concurrent edits; TCP ordering implies in-order WebSocket messages; the single-editor bullet, labelled as the book's position.

**Versions** (`npm view`, 2026-11-22): yjs 13.6.33, y-websocket 3.1.0, y-webrtc 10.3.0, y-indexeddb 9.0.12, @automerge/automerge 3.5.0, pixi.js 8.23.0, konva 10.10.0, rbush 4.0.1; repositories match the yjs, automerge, pixijs, konvajs and mourner owners. `@automerge/automerge-repo-storage-indexeddb` resolves (latest tag 2.6.0-alpha.3), and the page pins no version for it.

**Code checks.** In a temp folder outside the repo, the page's code block was extracted and run five times with Node 24.18.1 and yjs 13.6.33. Both replicas always converged, `x: 10` always survived, and the color winner varied by run (`red` three times, `blue` twice), as the page says. A three-replica variant also converged on one value. The Automerge claim was reproduced with @automerge/automerge 3.5.0: both merges show the same winner and `getConflicts()` returns both values.

**Remaining note (not an error).** Section 1 lists offline merge as a success criterion, and section 5 shows Figma doing offline editing without a CRDT; a human reviewer may want the page to discuss that tension.

## 3. Known omissions (follow-up content, not errors)

Topics a complete playbook could add, each needing its own sourced entry:

* Undo and redo in a multi-user document (`Y.UndoManager` tracked origins; Figma's undo rules)
* Authorization and access control for rooms (y-websocket auth, Automerge Repo sharing)
* Server-side persistence and scaling (y-redis, @y/hub, y-sweet, Automerge Repo sync servers)
* Snapshots, version history and document compaction
* Operational transformation as an alternative, and hosted services (Liveblocks, tldraw sync)
* Moving rendering or storage to workers (`OffscreenCanvas`, OPFS sync handles)
* Fractional indexing for z-order and list ordering (tldraw documents it)
* Accessibility techniques for canvas editors beyond keeping menus in the DOM

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 1 | 2 | **18** |

D8 is 1 because the rationale table packs several claims per cell. D9 is 1 because the single example shows the conflict mechanism but not a full provider setup. G8 (human accountability) is not met until a human reviews the page.
