# Research & Emerging: Modern Browser Primitives & Progressive Web Applications

> **Unverified background notes.** This file is an AI-generated research summary from the book's first draft. It has not been checked against the [content standards](../../CONTENT_STANDARDS.md) and is not part of the book. The verified chapters in `book/` cite primary sources directly; rely on those instead.

* **Category:** `research_and_emerging`
* **Status:** Web Standards & Production in Desktop-Class Web Apps
* **Core Comparison:** Service Workers vs. Web Workers vs. Shared Workers vs. Web Locks vs. BroadcastChannel

---

## 1. Beyond the Tab: Multi-Threaded and Background Web Architecture

Traditional web development assumes a single thread running within an isolated browser tab that terminates when the user closes the tab. Modern HTML5 and browser specifications turn the browser into a full-featured operating system client:

1. **Service Workers:**
   * *Mechanism:* An event-driven background worker registered by the origin that acts as a programmable network proxy between the browser, the web application, and the network.
   * *Capabilities:* Caching static shells for instant offline booting, intercepting HTTP requests, receiving Web Push notifications while the application is closed, and queuing background sync tasks.
2. **Web Workers (Dedicated Workers):**
   * *Mechanism:* Runs intensive computational tasks on a separate operating system thread without blocking the browser UI event loop.
   * *Capabilities:* Parsing large JSON payloads, running physics simulations, decoding image buffers, or executing local embedded databases (SQLite Wasm).
3. **Shared Workers:**
   * *Mechanism:* A single background script accessible by multiple tabs, windows, or iframes open to the same origin.
   * *Capabilities:* Managing a single persistent WebSocket connection across 10 open browser tabs, deduplicating telemetry pings, and coordinating global audio playback.
4. **BroadcastChannel API:**
   * *Mechanism:* Ultra-lightweight publish/subscribe messaging channel between browsing contexts (windows, tabs, workers) on the same origin.
   * *Capabilities:* Synchronizing user logout events across tabs, broadcasting shopping cart mutations, or updating active theme preferences in real time.
5. **Web Locks API (`navigator.locks`):**
   * *Mechanism:* Asynchronous mutex lock manager coordinating operations across multiple open browser tabs.
   * *Capabilities:* Prevents race conditions where two tabs attempt to perform database schema migrations or refresh an expired OAuth refresh token simultaneously.

---

## 2. Comparative Matrix: Browser Background Primitives

| Primitive | Execution Scope | Survives Tab Closure | Can Access DOM | Primary Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Main Thread JS** | Single Browser Tab | No | Direct Access | UI rendering, user interaction, event listeners |
| **Dedicated Web Worker** | Single Tab Lifespan | No | No (Message passing only) | Heavy computations, data parsing, cryptography |
| **Shared Worker** | All Origin Tabs | No (Dies when all tabs close) | No (Message ports) | Shared WebSocket connections, multi-tab coordination |
| **Service Worker** | Global Origin | Yes (Woken by events) | No (Fetch / Cache API) | Offline caching, network proxy, push notifications |

---

## 3. Decision Playbook: When to Move Work Off the Main Thread

* **Rule of Thumb:** If any operation takes longer than **16 milliseconds** (one frame at 60fps), it will cause visual stutter and drop Interaction to Next Paint (INP) scores if run on the main thread.
* **Move to Web Workers:**
  * Ingesting and decoding CSV/JSON payloads larger than 2 MB.
  * Image manipulation, canvas filters, and PDF generation.
  * Executing client-side search index lookups across tens of thousands of records.
* **Adopt Web Locks:**
  * Whenever persisting state to IndexedDB or refreshing authentication tokens to ensure only one tab executes the write at a time.
