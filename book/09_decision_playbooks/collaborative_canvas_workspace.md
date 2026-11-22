---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: yjs 13.6.33, y-websocket 3.1.0, y-webrtc 10.3.0, y-indexeddb 9.0.12, @automerge/automerge 3.5.0, pixi.js 8.23.0, konva 10.10.0, rbush 4.0.1, Node 24.18.1; MDN (canvas, WebGPU, WebGL2, indexedDB, OPFS, createSyncAccessHandle, createDataChannel, WebRTC protocols, storage quotas); RFC 6455; Figma multiplayer post (2019); PixiJS, Konva, tldraw, Automerge and Yjs docs
review_by: 2027-05
reviewers:
ledger: reviews/collaborative-canvas-workspace.md
---

# Decision Playbook: Collaborative Canvas & Document Workspaces

> Recommended architecture for whiteboards (Miro style), design tools (Figma style), diagramming studios and real-time collaborative document editors. Package versions on this page were checked on npm on 2026-11-21.

---

## 1. Who This Playbook Is For

This playbook is for a tech lead starting a multi-user editor where people draw, move shapes or type on the same document at the same time. It recommends a stack for that case; the recommendations are this book's positions, and the facts behind them are linked.

* **What success looks like:** remote cursors and edits appear while you watch, local drawing responds without waiting for the network, edits made offline merge on reconnect, and every replica ends up with the same document. That last property, convergence, is what CRDTs guarantee: "All CRDTs satisfy certain mathematical properties which guarantee eventual consistency" ([Figma engineering, 2019](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)). Convergence does not mean no edit is lost; see section 3.
* **Traffic pattern:** a steady stream of small document updates plus cursor and selection positions, sent over WebSockets, WebRTC data channels, or both.
* **Interaction complexity:** panning and zooming a large scene, hit testing shapes under the pointer, undo and redo, and dragging connected nodes.

---

## 2. The Recommended Stack, Layer by Layer

| Layer | Recommended choice (this book's position) | Why, and what it costs |
| :--- | :--- | :--- |
| **Canvas and rendering** | A `<canvas>` scene drawn with PixiJS 8.23 (WebGL renderer) or Konva 10.10 (Canvas 2D), or a custom renderer | Shapes drawn into a canvas are pixels, not DOM elements, so the browser does no per-shape style or layout work. The cost is accessibility: "Canvas content is not exposed to accessibility tools as semantic HTML is" ([MDN `<canvas>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/canvas)). PixiJS 8 also ships a WebGPU renderer but marks it "Experimental" and says "Use the WebGL renderer for production applications" ([PixiJS renderers guide](https://pixijs.com/8.x/guides/components/renderers)); MDN lists WebGPU as Limited availability, not Baseline ([MDN WebGPU API](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API)). WebGL2 is Baseline widely available since September 2021 ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext)). In Konva, "Each Layer is a separate `<canvas>` element" ([Konva docs](https://konvajs.org/docs/index.html)). |
| **Multiplayer state sync** | Yjs 13.6 or Automerge 3.5 (both CRDT libraries) | Shared types "automatically merge without merge conflicts" ([Yjs docs](https://docs.yjs.dev/)). Yjs has bindings for ProseMirror, Tiptap, Quill, CodeMirror, Monaco and Lexical ([Yjs README](https://github.com/yjs/yjs)); Automerge supports rich text through marks and blocks ([Automerge rich text](https://automerge.org/docs/reference/documents/rich-text/)). The cost: text CRDTs "only grow in size", although Yjs reduces the overhead by merging structs, deleting the content of deleted structs, and garbage-collecting tombstones only once their order no longer matters, for example when the parent was deleted ([Yjs README](https://github.com/yjs/yjs)). |
| **Transport** | A WebSocket room server (y-websocket 3.1) for document updates and presence; WebRTC data channels (y-webrtc 10.3) only if you want peer-to-peer | WebSocket is "layered over TCP" ([RFC 6455](https://www.rfc-editor.org/rfc/rfc6455)), so messages arrive in order. The WebSocket itself stores nothing: in y-websocket the server "distributes awareness information and document updates among clients", and persistence is a backend choice ([y-websocket README](https://github.com/yjs/y-websocket)). WebRTC data channels can be created with `ordered: false` and `maxRetransmits` for unreliable delivery ([MDN `createDataChannel()`](https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection/createDataChannel)), which suits cursor positions where only the newest one matters. The costs: behind symmetric NAT, traffic is relayed through a TURN server ([MDN WebRTC protocols](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols)); y-webrtc connects every peer to every other, and its README lists it as "Not suited for a large amount of collaborators on a single document" ([y-webrtc README](https://github.com/yjs/y-webrtc)). |
| **Local persistence** | IndexedDB through y-indexeddb 9.0 (Yjs) or `@automerge/automerge-repo-storage-indexeddb` ([Automerge storage docs](https://automerge.org/docs/reference/repositories/storage/)); OPFS for custom storage engines | y-indexeddb loads stored changes "from the local browser database" on the next session, which makes offline editing possible ([y-indexeddb docs](https://docs.yjs.dev/ecosystem/database-provider/y-indexeddb)). IndexedDB is Baseline widely available since July 2015 ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/indexedDB)). OPFS is Baseline widely available since March 2023, and its fast synchronous access handles work only in dedicated workers ([MDN OPFS](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system); [MDN `createSyncAccessHandle()`](https://developer.mozilla.org/en-US/docs/Web/API/FileSystemFileHandle/createSyncAccessHandle)). Both are best-effort storage by default; call `navigator.storage.persist()` if the local copy is the only copy ([MDN storage quotas and eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)). |
| **App shell and menus** | Ordinary DOM components in your UI framework | Toolbars, export menus, property panels and layer lists stay in HTML, where they get keyboard focus and screen-reader semantics that canvas content lacks ([MDN `<canvas>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/canvas)). |

---

## 3. Three Mistakes That Lose Edits or Frames

**Rendering every shape as a DOM or SVG node with no culling.** Each node joins the browser's style and layout work, so a large board slows down during zoom and pan. DOM rendering is workable when off-screen shapes are hidden: tldraw renders shapes as DOM elements and keeps a spatial index so that off-screen shapes get `display: none` ([tldraw performance docs](https://tldraw.dev/sdk-features/performance)). What to avoid is a DOM node per shape with nothing culled.

**Resolving conflicts with whole-document last-write-wins on client clocks.** If each save replaces the whole document and the newest wall-clock timestamp wins, one user's concurrent edits to unrelated shapes disappear, and a client with a fast clock wins every time. Per-property last-write-wins is a different, sound design: Figma resolves a conflict on "the same property on the same object" by keeping "the last value that was sent to the server", with the server defining the order ([Figma engineering](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)), and Automerge orders concurrent writes by operation ID, "not a wall clock time" ([Automerge conflicts](https://automerge.org/docs/reference/documents/conflicts/)). Even with a CRDT, two concurrent writes to the same property keep only one visible value. Automerge keeps the losing value available through `getConflicts()`; Yjs keeps one value for the key. This runs with Node 24 and `yjs` 13.6:

```js
import * as Y from 'yjs'

const alice = new Y.Doc()
const bob = new Y.Doc()
alice.getMap('shape').set('color', 'red')   // concurrent edits to the same key
bob.getMap('shape').set('color', 'blue')
bob.getMap('shape').set('x', 10)            // an edit to a different key

const fromAlice = Y.encodeStateAsUpdate(alice)
const fromBob = Y.encodeStateAsUpdate(bob)
Y.applyUpdate(alice, fromBob)
Y.applyUpdate(bob, fromAlice)

// Both replicas converge; x survives, and only one color survives.
console.log(alice.getMap('shape').toJSON(), bob.getMap('shape').toJSON())
```

If a lost concurrent value matters (for example two people renaming the same layer), model it so the edits land on different keys, or surface the conflict in the UI.

**Storing cursor positions in the document history.** Cursor positions are ephemeral. In Yjs, send them through the awareness protocol: "Awareness information isn't stored in the Yjs document, as it doesn't need to be persisted across sessions" ([Yjs awareness guide](https://docs.yjs.dev/getting-started/adding-awareness)). Writing pointer coordinates into the CRDT document instead turns every mouse move into a document update that each client and the persistence layer must sync and store.

---

## 4. Checks Before You Build

* **Is offline editing required?** Load the document from IndexedDB or OPFS before connecting to the network. With y-indexeddb, wait for the `synced` event, which fires once "all available content has been loaded", including when there is none yet ([y-indexeddb docs](https://docs.yjs.dev/ecosystem/database-provider/y-indexeddb)).
* **Will boards hold many shapes?** Keep shape bounding boxes in a spatial index such as an R-tree, so that rendering and hit testing only touch shapes inside the viewport. rbush 4.0 is an R-tree library for queries like "all items within this bounding box" ([rbush README](https://github.com/mourner/rbush)). PixiJS 8's `CullerPlugin` skips off-screen containers, is off by default, and helps when GPU-bound but can hurt when CPU-bound ([PixiJS culler guide](https://pixijs.com/8.x/guides/components/application/culler-plugin); [PixiJS performance tips](https://pixijs.com/8.x/guides/concepts/performance-tips)).

---

## 5. When This Playbook Is the Wrong Choice

* **There is always a server.** Figma uses a client/server design over WebSockets and says "Figma isn't using true CRDTs", because CRDTs carry "some unavoidable performance and memory overhead" to support systems with no central authority ([Figma engineering](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)). A server that orders per-property updates may be simpler than a CRDT library.
* **Boards hold a moderate number of shapes and need accessible text.** Since canvas content "is not exposed to accessibility tools as semantic HTML is" ([MDN `<canvas>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/canvas)), DOM rendering with culling is the easier path to an accessible editor. tldraw takes that route and says it keeps "smooth performance even with thousands of shapes on the canvas" ([tldraw performance docs](https://tldraw.dev/sdk-features/performance)); that is the vendor's claim, not an independent benchmark.
* **Many people edit one document at once.** A full WebRTC mesh does not scale to many collaborators ([y-webrtc README](https://github.com/yjs/y-webrtc)); route everything through a server instead.
* **Only one person edits a document.** This book's position: skip the sync layer and store the document as plain data in IndexedDB or on your server. CRDT merge machinery only pays off when there are concurrent writers.
