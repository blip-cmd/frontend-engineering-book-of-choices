---
status: draft
ai_involvement: drafted
last_verified:
verified_against:
review_by:
reviewers:
---

# Decision Playbook: Collaborative Canvas & Document Workspaces

> Recommended Architecture for: Whiteboards (Miro style), Design Tools (Figma style), Diagramming Studios, and Real-Time Collaborative Document Editors.

---

## 1. The Archetype Profile

* **Primary Success Metric:** Fluid multi-user collaboration (seeing remote user cursors in real time), zero perceived latency on local drawing/editing actions, seamless offline resilience, and mathematically guaranteed document convergence without data loss.
* **Traffic Pattern:** Continuous broadcast of delta operations, cursor spatial coordinates, and scene graph mutations over WebSockets or WebRTC data channels.
* **Interaction Complexity:** Complex viewport panning, zooming, spatial geometric calculations, undo/redo trees, and drag-and-drop node graphs.

---

## 2. The Recommended Architectural Stack

| Layer | Recommended Choice | Rationale |
| :--- | :--- | :--- |
| **Canvas & Rendering** | **HTML5 Canvas / WebGPU (via Pixi.js, Konva, or custom Wasm)** | Bypasses the DOM for the interactive workspace. Millions of vector coordinates and visual primitives render smoothly on the GPU without triggering browser style recalculations or layout reflows. |
| **Multiplayer State Sync**| **Yjs (CRDT) or Automerge** | Operation-based CRDTs ensure mathematical convergence across all peer edits, offline edits, and concurrent mutations. Bundled rich-text and key-value primitives integrate directly with collaborative editors. |
| **Transport Layer** | **WebSocket Room Broker + WebRTC Data Channels** | WebSockets provide reliable message ordering and persistence; WebRTC data channels deliver ultra-low-latency peer-to-peer transmission for ephemeral spatial cursor coordinates. |
| **Local Persistence** | **Origin Private File System (OPFS) / IndexedDB** | Writes all local document operations to disk instantly. Users can close their laptop mid-session and resume work offline without losing a single stroke. |
| **App Shell & Menus** | **Standard DOM (React / Svelte + Tailwind CSS)** | The surrounding UI (toolbars, export menus, properties panels, layer lists) runs on standard DOM elements with rich accessibility and keyboard shortcuts. |

---

## 3. What to Explicitly Avoid

* **Do NOT render canvas elements as individual DOM `<div>` or `<svg>` nodes:**
  Attempting to render 10,000 editable shapes using SVG or absolute-positioned HTML elements causes severe layout thrashing during zoom and pan gestures.
* **Do NOT use naive Last-Write-Wins (LWW) timestamps for collaborative editing:**
  In distributed networks, clock drift guarantees that concurrent user modifications will overwrite and destroy each other's work. Always adopt a proven CRDT engine (Yjs or Automerge).
* **Do NOT store high-frequency cursor coordinates in persistent document history:**
  Cursor positions are ephemeral. Transmit them via separate unpersisted WebSocket channels or WebRTC data channels; do not append mouse coordinates to your durable CRDT document change log.

---

## 4. Constraint Checklist
* Is offline editing required? Ensure document state loads from local IndexedDB or OPFS prior to attempting network connection.
* Are there massive documents (>50 MB)? Implement spatial partitioning (e.g., R-Trees or quadtrees) so the canvas renderer only processes elements currently visible inside the user's viewport bounding box.
