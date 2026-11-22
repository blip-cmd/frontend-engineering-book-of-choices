---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: solid-js 2.0.3, preact 11.2.0, @preact/signals 2.11.4, react 19.3.1, recharts 3.11.0, uplot 1.6.32, scichart 6.0.18, @bufbuild/protobuf 2.17.0, @msgpack/msgpack 3.1.3, Node 24.18.1, MDN (rAF, WebSocket, WebSocketStream, workers, transferables, SharedArrayBuffer, COEP, WebGPU, WebTransport, canvas), webstatus.dev, web.dev INP and long tasks, react.dev, Chrome DevTools heap snapshots
review_by: 2027-05
reviewers:
ledger: reviews/high-frequency-realtime-dashboard.md
---

# Decision Playbook: High-Frequency Real-Time Telemetry & Financial Dashboards

> For a tech lead building a trading console, IoT telemetry hub, server health monitor or live analytics view, where updates arrive faster than the screen can repaint. Every recommendation below is this book's position unless a source is linked; sources were checked on 2026-11-21.

---

## 1. When this playbook applies

* **Primary success metric (position):** frames keep pace with the display while the stream runs, input stays responsive, and memory stays flat over a full shift. `requestAnimationFrame` callbacks generally fire at the display refresh rate, most commonly 60 Hz, with 75, 120 and 144 Hz also in wide use ([MDN: requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame)). At 60 Hz that leaves about 16.7 ms per frame (1000 / 60) for parsing, state updates and drawing together.
* **Responsiveness target:** web.dev rates Interaction to Next Paint (INP) as good at or below 200 milliseconds, measured at the 75th percentile of page loads in the field ([web.dev: INP](https://web.dev/articles/inp)). Any main-thread task over 50 milliseconds is a long task that delays input handling ([web.dev: Optimize long tasks](https://web.dev/articles/optimize-long-tasks)).
* **Traffic pattern:** a persistent connection pushing numeric time-series records. Server-Sent Events (SSE) are a one-way connection, so the client cannot send events to the server ([MDN: Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)).
* **Target environment:** operations rooms and trading desks where one tab stays open for hours, so a slow memory leak becomes a crash before the session ends.

---

## 2. Recommended stack: keep each tick off the component tree

| Layer | Recommended choice (position) | Rationale and source |
| :--- | :--- | :--- |
| **Reactivity** | **Solid 2.x (`solid-js` 2.0.3) or Preact Signals (`@preact/signals` 2.11.4 with `preact` 11.2.0)** | In Solid 2.0 "a component function runs once" and there is "no virtual DOM and no component re-render" ([Solid docs](https://docs.solidjs.com/)). In Preact, a signal passed into JSX in a text position updates "in-place without Virtual DOM diffing"; reading `.value` inside a component re-renders that component instead ([Preact v11: Signals](https://preactjs.com/guide/v11/signals/)). |
| **Transport** | **WebSocket with `binaryType = "arraybuffer"`, carrying Protocol Buffers (`@bufbuild/protobuf` 2.17.0) or MessagePack (`@msgpack/msgpack` 3.1.3)** | Setting `binaryType` to `"arraybuffer"` delivers binary frames as `ArrayBuffer` objects ([MDN: binaryType](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/binaryType)). Both formats describe themselves as smaller and faster than JSON ([protobuf.dev overview](https://protobuf.dev/overview/); [msgpack.org](https://msgpack.org/)); those are the projects' own claims, and in the browser their decoders run in JavaScript while `JSON.parse` is built in, so benchmark with real messages before switching. |
| **Backpressure** | **Drop or coalesce on the client; do not assume the socket slows the server down** | The WebSocket API "has no way to apply backpressure", so messages that arrive faster than the app can process them fill memory, peg the CPU, or both ([MDN: WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)). MDN points to `WebSocketStream` for backpressure, but marks it non-standard ([MDN: WebSocketStream](https://developer.mozilla.org/en-US/docs/Web/API/WebSocketStream)). |
| **Worker offloading** | **Dedicated Web Worker for ingest, decode, batching and rolling aggregates** | Workers cannot directly manipulate the DOM ([MDN: Using Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers)), and `WebSocket` is available inside workers ([MDN: WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)), so the socket can live in the worker. Send only what the next frame needs with `postMessage`. Transferring an `ArrayBuffer` is a "zero-copy operation" that detaches it from the sender; typed arrays themselves are not transferable, only their `.buffer` ([MDN: Transferable objects](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Transferable_objects)). |
| **Shared memory (optional)** | **`SharedArrayBuffer` only if you can make the page cross-origin isolated** | Shared memory requires a secure context and cross-origin isolation ([MDN: SharedArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer)): `Cross-Origin-Opener-Policy: same-origin` plus `Cross-Origin-Embedder-Policy: require-corp` or `credentialless` ([MDN: crossOriginIsolated](https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated)). Under `require-corp`, cross-origin resources load only if they opt in ([MDN: COEP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy)). Baseline widely available since December 2021. |
| **Time-series charts** | **Canvas 2D (`uplot` 1.6.32) by default; WebGL or WebGPU engines (for example SciChart.js 6, `scichart` 6.0.18, commercial EULA) for very large point counts** | uPlot is "Canvas 2D-based"; its README says it can usually live-stream at 60fps but "may begin to struggle beyond 100k in-view points"; if streaming still struggles after unclogging the rendering pipeline, it suggests reducing the update frequency or switching to a WebGL/WebGPU solution ([uPlot README](https://github.com/leeoniya/uPlot)). SciChart.js 6 combines WebAssembly with WebGPU and WebGL rendering ([SciChart features](https://www.scichart.com/javascript-chart-features/)); its performance figures are vendor claims. WebGPU has limited availability and is not Baseline as of 2026-11 ([webstatus.dev: WebGPU](https://webstatus.dev/features/webgpu); [MDN: WebGPU API](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API)), so keep a WebGL fallback. |
| **Data buffering** | **Fixed-capacity ring buffer in a `Float64Array`** | Allocate once and overwrite the oldest sample, so the visible window never grows the heap. See the example below. |

The ring buffer below runs as written with Node 24 (`node ring.mjs`). The same class works in a worker or on the main thread.

```js
// Fixed-capacity ring buffer: memory is allocated once, the oldest sample is overwritten.
class RingBuffer {
  constructor(capacity) {
    this.values = new Float64Array(capacity);
    this.head = 0; // index of the next write
    this.size = 0;
  }
  push(value) {
    this.values[this.head] = value;
    this.head = (this.head + 1) % this.values.length;
    this.size = Math.min(this.size + 1, this.values.length);
  }
  // Copy samples oldest-first into a caller-owned array, so drawing allocates nothing.
  copyInto(out) {
    const cap = this.values.length;
    const start = (this.head - this.size + cap) % cap;
    for (let i = 0; i < this.size; i++) out[i] = this.values[(start + i) % cap];
    return this.size;
  }
}

const buffer = new RingBuffer(4);
for (const price of [101, 102, 103, 104, 105, 106]) buffer.push(price);
const out = new Float64Array(4);
const n = buffer.copyInto(out);
console.log(Array.from(out.subarray(0, n))); // [ 103, 104, 105, 106 ]
```

---

## 3. Avoid these: per-tick re-renders, SVG streaming charts, main-thread parsing

* **Do not push every tick through React state (position).** In React 19 (`react` 19.3.1), updating a component's state by default re-renders every component nested inside it, which react.dev calls "not optimal for performance if the updated component is very high in the tree" ([react.dev: Render and Commit](https://react.dev/learn/render-and-commit)). If the app is already React, keep fast-changing values in a ref, which does not "trigger new renders" ([react.dev: Referencing values with refs](https://react.dev/learn/referencing-values-with-refs)), and draw them on a canvas; reserve React state for slower UI such as filters and layout.
* **Do not stream line charts into SVG.** SVG provides elements for shapes and curves and has a DOM interface ([MDN: SVG introduction](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Introduction)). Recharts (`recharts` 3.11.0), built with React and D3, lists "Native SVG support" as a feature ([Recharts README](https://github.com/recharts/recharts)); it suits slower dashboards, not a stream that redraws every frame. Use `<canvas>`.
* **Do not decode large message volumes on the main thread.** The main thread runs one task at a time, and a task over 50 milliseconds blocks input ([web.dev: Optimize long tasks](https://web.dev/articles/optimize-long-tasks)). Parse in the worker and hand the UI only the values it draws.

---

## 4. Constraint checklist

* **Does the dashboard run for hours?** Take heap snapshots in Chrome DevTools before and after a period of streaming and use the Comparison view to find objects that keep accumulating; the "Objects retained by detached nodes" filter shows leaks from removed DOM ([Chrome DevTools: heap snapshots](https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots)).
* **Do ticks arrive faster than the display refreshes?** Accumulate data in the ring buffer and draw once per `requestAnimationFrame` callback. Most browsers pause these callbacks in background tabs and hidden iframes ([MDN: requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame)), so a bounded buffer keeps a hidden dashboard from piling up frames to draw.
* **Is the stream unreliable or lossy by nature?** WebTransport is Baseline newly available since March 2026 ([MDN: WebTransport API](https://developer.mozilla.org/en-US/docs/Web/API/WebTransport_API); [webstatus.dev: WebTransport](https://webstatus.dev/features/webtransport)); evaluate it against WebSocket only if the server side supports it.

---

## 5. When this playbook is the wrong choice

* **Updates arrive every few seconds, not every frame.** Ordinary framework state and an SVG chart library such as Recharts are simpler and easier to style; the worker, binary protocol and ring buffer add build and debugging cost for no visible gain (reasoning, not measurement).
* **The page must embed third-party content you cannot change.** Under `require-corp`, cross-origin isolation for `SharedArrayBuffer` blocks cross-origin resources that do not opt in, and under `credentialless` they load without credentials ([MDN: COEP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy)). Use transferable `ArrayBuffer`s with `postMessage` instead.
* **Screen-reader users must read the values.** A `<canvas>` "must be made accessible by providing fallback text", placed inside the element for screen readers ([MDN: Canvas basic usage](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_usage)). Pair the canvas with a slower, throttled HTML table or summary.
* **A large React codebase has one or two hot widgets.** Rewriting in Solid or Preact costs more than keeping those widgets' fast values in React refs and drawing them on a canvas (position).
