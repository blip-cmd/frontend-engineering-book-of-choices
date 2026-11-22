# Real-time dashboard starter

A minimal starter for a high-frequency telemetry view. A module Web Worker generates simulated ticks locally (no network) and posts them in batches as a `Float64Array` whose `.buffer` is transferred. The main thread writes the ticks into fixed-capacity ring buffers and redraws a uPlot (Canvas 2D) chart at most once per animation frame. A Solid 2 component owns the setup and teardown, and a slower text summary is refreshed once per second for screen readers.

It implements the playbook [High-Frequency Real-Time Telemetry and Financial Dashboards](../../book/09_decision_playbooks/high_frequency_realtime_dashboard.md).

## Files

| File | Role |
| :--- | :--- |
| `src/worker.ts` | Simulated feed. Replace the timer with a WebSocket (`binaryType = "arraybuffer"`) and decode here. |
| `src/ring.ts` | Ring buffer from the playbook, typed. |
| `src/Dashboard.tsx` | Worker wiring, ring buffers, uPlot chart and the `requestAnimationFrame` draw loop. |
| `src/index.tsx` | Renders the component. |

## Run

Requires Node.js 22.12 or later.

```bash
npm install
npm run dev        # development server
npm run typecheck  # tsc --noEmit, strict mode
npm run build      # production build into dist/
npm run preview    # serve the build
```

## Versions

Built and type-checked on 2026-11-22 with Node.js 24.18.1 and:

| Package | Version |
| :--- | :--- |
| `solid-js` | 2.0.3 |
| `@solidjs/web` | 2.0.3 |
| `@solidjs/vite-plugin` | 3.0.1 |
| `uplot` | 1.6.32 |
| `vite` | 8.3.8 |
| `typescript` | 7.0.2 |

`package-lock.json` pins the exact tree.

## License

MIT, like everything under `recipes/`.
