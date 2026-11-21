---
status: draft
ai_involvement: drafted
last_verified:
verified_against:
review_by:
reviewers:
---

# Decision Playbook: High-Frequency Real-Time Telemetry & Financial Dashboards

> Recommended Architecture for: Financial Trading Consoles, IoT Telemetry Hubs, Server Health Monitoring, and Live Analytics Streaming.

---

## 1. The Archetype Profile

* **Primary Success Metric:** Sustained 60 frames-per-second (FPS) rendering under continuous WebSocket data streams (50 to 200 message updates per second), zero main-thread event loop blocking, low Interaction to Next Paint (INP < 50ms), and stable memory footprints.
* **Traffic Pattern:** Persistent bidirectional WebSocket or Server-Sent Events (SSE) connections pushing continuous numeric time-series records.
* **Target Environment:** Multi-monitor trading desks or operations control centers running continuously for 8-12 hours per session. Memory leaks are fatal.

---

## 2. The Recommended Architectural Stack

| Layer | Recommended Choice | Rationale |
| :--- | :--- | :--- |
| **Reactivity Engine** | **Solid.js (Fine-Grained Signals) or Preact Signals** | Component functions execute only once. High-frequency incoming data updates ping exact DOM text nodes and table cells directly, completely bypassing Virtual DOM tree diffing and eliminating garbage collection churn. |
| **Transport Protocol** | **Binary WebSockets (Protocol Buffers / MessagePack)** | Eliminates JSON serialization and parsing overhead on the browser main thread. Packed binary records decode at 5x to 10x the speed of standard JSON. |
| **Worker Offloading** | **Web Worker Data Pipeline** | Ingest, parse, batch, and calculate rolling window averages inside a dedicated Web Worker. Send only visual delta updates to the UI thread via `postMessage` or SharedArrayBuffer. |
| **Time-Series Charts** | **WebGPU / Canvas-Based Engine (uPlot / SciChart)** | Standard SVG charting libraries (e.g., Recharts) create thousands of DOM nodes that choke the browser at 60fps. uPlot or Canvas render millions of data points smoothly on the GPU. |
| **Data Buffering** | **Circular Ring Buffer in In-Memory TypedArray** | Pre-allocate fixed-size `Float64Array` buffers. Overwrite oldest records in place to prevent JavaScript heap growth and garbage collection pauses. |

---

## 3. What to Explicitly Avoid

* **Do NOT use standard React with Virtual DOM reconciliation:**
  Receiving 100 WebSocket messages per second in React triggers continuous re-renders across the component tree. Even with memoization, the CPU spends 80% of its budget reconciling trees instead of processing data.
* **Do NOT use SVG for streaming real-time line charts:**
  Every SVG point, line, and rectangle is an explicit DOM node. Updating 10,000 SVG coordinates per second will freeze the browser. Use HTML5 `<canvas>` or WebGPU.
* **Do NOT parse raw JSON on the main thread for massive message volumes:**
  Ingesting megabytes of streaming JSON on the main thread locks the browser event loop, causing mouse clicks and keystrokes to register seconds late.

---

## 4. Constraint Checklist
* Does the dashboard run for multiple hours continuously? Run Chrome DevTools Heap Snapshots to verify that memory allocation hits a flat plateau rather than climbing continuously (preventing memory leaks).
* Are tick updates arriving faster than the monitor refresh rate (60Hz / 144Hz)? Throttle DOM updates to `requestAnimationFrame` cycles while continuing to accumulate raw data in memory.
