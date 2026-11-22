---
page: book/09_decision_playbooks/high_frequency_realtime_dashboard.md
verified: 2026-11-21
---

# Claim Ledger: Decision Playbook, High-Frequency Real-Time Telemetry & Financial Dashboards

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a tech lead building a trading console, telemetry hub or monitoring view where updates arrive faster than the display repaints. The page helps them choose a reactivity model, transport, threading model, chart renderer and buffering strategy. Thesis: keep each tick off the component tree. Decode and aggregate in a worker, hold data in a fixed-size typed-array buffer, render with fine-grained signals and canvas, and draw at most once per animation frame.

**History.** The author pass (2026-11-21) rewrote the AI-generated draft. The draft had an invented message rate ("50 to 200 message updates per second"), an INP target of "< 50ms" (web.dev rates good INP as 200 ms or less at p75), a "5x to 10x" binary decoding speedup and an "80% of its budget" React figure with no source, an "8-12 hours" session length, and a claim that uPlot renders "on the GPU" (uPlot is Canvas 2D). It also omitted the cross-origin isolation requirement for `SharedArrayBuffer` and the fact that WebSocket has no backpressure. One recommendation was narrowed: "Do NOT use standard React" became "Do not push every tick through React state", because react.dev documents refs as the way to hold values without re-rendering, so an existing React app can keep React and move only the hot path to refs and canvas. A "When this playbook is the wrong choice" section and a runnable ring-buffer example were added.

---

## 1. Author pass (2026-11-21)

Sources were downloaded in the same session and quotes matched against the page text. Package versions come from `npm view` on 2026-11-21.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | rAF callbacks generally match the display refresh rate; 60 Hz most common; 75, 120, 144 Hz widely used | [MDN requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) | verified (quote); replaced the draft's "Sustained 60 FPS" metric |
| 2 | About 16.7 ms per frame at 60 Hz | arithmetic (1000 / 60) on claim 1 | verified |
| 3 | INP good at or below 200 ms at the 75th percentile, mobile and desktop segmented | [web.dev INP](https://web.dev/articles/inp) | verified (quote); draft's "INP < 50ms" corrected |
| 4 | Tasks over 50 ms are long tasks; main thread runs one task at a time | [web.dev Optimize long tasks](https://web.dev/articles/optimize-long-tasks) | verified (quote) |
| 5 | WebSocket is two-way; SSE is one-way server to client | [MDN Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) | verified (quote "one-way") |
| 6 | "50 to 200 message updates per second" | none found | removed; replaced with "faster than the screen can repaint" |
| 7 | "8-12 hours per session" | none found | removed; made qualitative ("for hours") |
| 8 | Solid 2.0: "a component function runs once"; "no virtual DOM and no component re-render" | [Solid docs](https://docs.solidjs.com/) (docs state they cover Solid 2.0) | verified (quote) |
| 9 | Preact signal in JSX text position updates "in-place without Virtual DOM diffing"; reading `.value` re-renders the component | [Preact v11 Signals](https://preactjs.com/guide/v11/signals/) | verified (quote) |
| 10 | Draft: signals "eliminate garbage collection churn" | none found | removed |
| 11 | Versions: `solid-js` 2.0.3, `preact` 11.2.0, `@preact/signals` 2.11.4, `uplot` 1.6.32, `recharts` 3.11.0, `react` 19.3.1, `@bufbuild/protobuf` 2.17.0, `@msgpack/msgpack` 3.1.3, `scichart` 6.0.18 (license field points to the SciChart EULA) | `npm view <name> version` | verified |
| 12 | `binaryType = "arraybuffer"` delivers binary data as `ArrayBuffer` | [MDN binaryType](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/binaryType) | verified (quote) |
| 13 | Protobuf: "like JSON, except it's smaller and faster"; MessagePack: "like JSON. but fast and small" | [protobuf.dev overview](https://protobuf.dev/overview/); [msgpack.org](https://msgpack.org/) | verified (quote); labelled as the projects' own claims |
| 14 | Draft: binary records "decode at 5x to 10x the speed of standard JSON"; binary "eliminates" parsing overhead | none found | removed; page now says decoders run in JavaScript while `JSON.parse` is built in, and advises benchmarking (reasoning, labelled) |
| 15 | WebSocket API "has no way to apply backpressure"; overload fills memory or pegs CPU | [MDN WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) | verified (quote); added |
| 16 | `WebSocketStream` provides backpressure; marked non-standard | [MDN WebSocketStream](https://developer.mozilla.org/en-US/docs/Web/API/WebSocketStream) | verified |
| 17 | `WebSocket` is available in Web Workers | [MDN WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) | verified (quote) |
| 18 | Workers cannot directly manipulate the DOM | [MDN Using Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) | verified (quote) |
| 19 | Transferring an `ArrayBuffer` is zero-copy and detaches it; typed arrays are not transferable, their buffer is | [MDN Transferable objects](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Transferable_objects) | verified (quote) |
| 20 | `SharedArrayBuffer` needs a secure context and cross-origin isolation; Baseline widely available since December 2021 | [MDN SharedArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer) | verified (quote); added |
| 21 | Cross-origin isolation = COOP `same-origin` + COEP `require-corp` or `credentialless` | [MDN crossOriginIsolated](https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated) | verified (quote) |
| 22 | Under COEP `require-corp`, cross-origin resources must opt in | [MDN COEP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy) | verified (quote) |
| 23 | uPlot is Canvas 2D-based; live-streams at 60fps "in most sane cases"; "may begin to struggle beyond 100k in-view points"; suggests WebGL/WebGPU libraries beyond that | [uPlot README](https://github.com/leeoniya/uPlot) | verified (quote); maintainer's claim. Draft's "render millions of data points smoothly on the GPU" corrected |
| 24 | SciChart.js 6 combines WebAssembly with WebGPU and WebGL rendering | [SciChart features](https://www.scichart.com/javascript-chart-features/) | verified; vendor performance numbers deliberately not repeated |
| 25 | WebGPU: limited availability, not Baseline (webstatus.dev lists Chrome 144, Edge 144, Safari 26; no Firefox entry) | [webstatus.dev WebGPU](https://webstatus.dev/features/webgpu) (API `api.webstatus.dev/v1/features/webgpu`); [MDN WebGPU API](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API) | verified |
| 26 | WebTransport: Baseline newly available since March 2026 (Safari 26.4, 2026-03-24) | [MDN WebTransport API](https://developer.mozilla.org/en-US/docs/Web/API/WebTransport_API); [webstatus.dev WebTransport](https://webstatus.dev/features/webtransport) | verified (quote "Baseline 2026 Newly available") |
| 27 | Updating a component re-renders all nested components, "not optimal for performance if the updated component is very high in the tree" | [react.dev Render and Commit](https://react.dev/learn/render-and-commit) | verified (quote) |
| 28 | Refs hold values that do not "trigger new renders" | [react.dev Referencing values with refs](https://react.dev/learn/referencing-values-with-refs) | verified (quote); basis for narrowing the React recommendation |
| 29 | Draft: "100 WebSocket messages per second ... CPU spends 80% of its budget reconciling" | none found | removed |
| 30 | SVG elements have a DOM interface | [MDN SVG introduction](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Introduction) | verified (quote "having a DOM interface") |
| 31 | Recharts is built with React and D3 and lists "Native SVG support" | [Recharts README](https://github.com/recharts/recharts) | verified (quote) |
| 32 | Draft: "Updating 10,000 SVG coordinates per second will freeze the browser" | none found | removed |
| 33 | Draft: JSON parsing makes clicks "register seconds late" | none found | removed; replaced with the sourced long-task mechanism (claim 4) |
| 34 | Heap snapshot Comparison view finds leaked objects; "Objects retained by detached nodes" filter | [Chrome DevTools heap snapshots](https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots) | verified (quote) |
| 35 | rAF is paused in background tabs and hidden iframes in most browsers | [MDN requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) | verified (quote) |
| 36 | `<canvas>` must be made accessible with fallback text or sub-DOM | [MDN Canvas basic usage](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_usage) | verified (quote) |
| 37 | Ring-buffer example: keeps the newest samples oldest-first and allocates nothing when copying out | Node 24.18.1 run (full buffer prints `[ 103, 104, 105, 106 ]`; partial fill with two values prints `[ 7, 8 ]`) | verified (run) |
| 38 | "When this playbook is the wrong choice": slow updates favour ordinary state and SVG; React rewrite costs more than isolating hot widgets | none | labelled on the page as reasoning or position |

Links to `library/` research notes: none were present on the page.

## 2. Independent verifier pass (2026-11-21)

A separate agent that did not write the page extracted 44 claims from the page text itself (not from the list above), fetched every cited source on 2026-11-21 (`curl -sL`, and WebFetch for the SciChart page, which blocks curl), and searched each one for the claimed wording. The webstatus.dev entries were read from `api.webstatus.dev/v1/features/{webgpu,webtransport}`.

**Verdict: PASS** after the edits below. 36 claims SUPPORTED, 6 PARTIAL (all corrected), 2 UNSUPPORTED (both deleted). The remaining unsourced statements carry no numbers and are labelled positions or reasoning, or are uncontroversial background (for example that the protobuf and MessagePack decoders run in JavaScript while `JSON.parse` is built in).

Edits to the page:

| # | Original | Verdict | Edit |
| :--- | :--- | :--- | :--- |
| V1 | "WebSocket is two-way" (cited to MDN Using server-sent events) | UNSUPPORTED: neither the SSE page nor MDN WebSocket says this | deleted; the SSE half reworded to the source ("a one-way connection, so the client cannot send events to the server") |
| V2 | Each SVG shape is an element with a DOM interface, "so the node count grows with the point count" | UNSUPPORTED: the MDN intro says SVG "provides elements for circles, rectangles, and simple and complex curves" and has "a DOM interface"; it says nothing about node counts, and a line drawn as one `<path>` does not grow per point | node-count clause deleted; reworded to the source |
| V3 | `<canvas>` must be made accessible "by providing fallback text" "or sub-DOM" | PARTIAL: MDN Canvas basic usage never mentions a sub-DOM | "or sub-DOM" replaced with the source's "inside the element ... for screen readers" |
| V4 | "Browsers pause these callbacks in background tabs" | PARTIAL: MDN says "paused in most browsers" | now "Most browsers pause" |
| V5 | updating a component's state "re-renders every component nested inside it" | PARTIAL: react.dev calls this "the default behavior" | added "by default" |
| V6 | uPlot README "suggests WebGL/WebGPU libraries past that" (past 100k points) | PARTIAL: the README first suggests unclogging the rendering pipeline, then "reducing the update frequency or switch to a WebGL/WebGPU solution" | reworded to the README's sequence |
| V7 | "Cross-origin isolation for `SharedArrayBuffer` blocks cross-origin resources that do not opt in" | PARTIAL: true for COEP `require-corp`; MDN COEP says that under `credentialless` no-cors resources load without explicit permission but without credentials | qualified with `require-corp` and the `credentialless` behaviour from the same source |
| V8 | "Workers cannot touch the DOM" | PARTIAL (paraphrase): MDN says "you can't directly manipulate the DOM" | now "cannot directly manipulate the DOM" |

Confirmed verbatim or exact: rAF refresh-rate sentence (60, 75, 120, 144 Hz); INP "below or at 200 milliseconds" at the 75th percentile of page loads in the field; "Any task that takes longer than 50 milliseconds is a long task" and "one task at a time"; WebSocket "has no way to apply backpressure" (memory, 100% CPU, or both) and its Web Workers note; WebSocketStream non-standard and experimental, with stream backpressure; `binaryType` "arraybuffer"; protobuf "smaller and faster"; MessagePack "fast and small"; Solid docs (covering Solid 2.0) "a component function runs once" and "no virtual DOM and no component re-render"; Preact v11 "in-place without Virtual DOM diffing" and `.value` re-rendering; transferable `ArrayBuffer` "zero-copy", and typed arrays "serializable, but not transferable"; `SharedArrayBuffer` secure context plus cross-origin isolation, Baseline widely available since December 2021; COOP `same-origin` plus COEP `require-corp` or `credentialless`; uPlot "Canvas 2D-based", 60fps "in most sane cases", "beyond 100k in-view points"; SciChart "In SciChart.js v6, the Visual Xccelerator engine combines WebAssembly with WebGPU and WebGL rendering"; WebGPU limited availability, not Baseline (MDN, and webstatus.dev `baseline.status: limited`, no Firefox implementation listed); WebTransport "Baseline 2026 Newly available", "Since March 2026" (webstatus.dev `low_date` 2026-03-24, Safari 26.4); react.dev "not optimal for performance if the updated component is very high in the tree" and refs not triggering "new renders"; Recharts "built with React and D3" and "Native SVG support"; DevTools Comparison view and "Objects retained by detached nodes".

Versions (`npm view <name> version`, 2026-11-21): `solid-js` 2.0.3 (dist-tag latest), `preact` 11.2.0, `@preact/signals` 2.11.4 (peer `preact >= 10.25.0 || >=11.0.0-0`, so the pairing is valid), `uplot` 1.6.32, `recharts` 3.11.0, `react` 19.3.1, `@bufbuild/protobuf` 2.17.0, `@msgpack/msgpack` 3.1.3, `scichart` 6.0.18 (license field `https://www.scichart.com/scichart-eula`). All match the page.

Code checks: the ring-buffer block was extracted from the page and run with Node v24.18.1; it prints `[ 103, 104, 105, 106 ]` as stated. Edge cases: empty buffer `[]`; partial fill `[ 7, 8 ]`; exactly full `[ 1, 2, 3, 4 ]`; capacity 3 after ten pushes `[ 8, 9, 10 ]`; capacity 1 `[ 3 ]`; `NaN` values are stored and returned in order. Capacity 0 does not throw but leaves `head` as `NaN` (modulo by zero); the page makes no claim about capacity validation, so this is noted, not an error.

## 3. Known omissions (follow-up content, not errors)

Each needs its own sourced entry before it is added:

* `OffscreenCanvas` (listed as transferable on MDN) for drawing charts entirely inside the worker
* Reconnection, resubscription and gap-filling after a dropped socket; sequence numbers for ordering
* Server-side throttling or conflation of ticks, which removes load before it reaches the browser
* Long Animation Frames API and the DevTools Performance panel for measuring frame cost
* Number formatting and locale cost in tables that update every frame
* Behaviour on high-refresh displays: whether to cap drawing at 60 Hz to save CPU
* SSE's per-domain connection limit over HTTP/1.1 (MDN: 6), relevant when many dashboard tabs open

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | **19** |

D9 is 1 because the only runnable example is the ring buffer; the worker, socket and `requestAnimationFrame` wiring is described in prose, not shown. G8 (human accountability) is not met until a human reviews the page.
