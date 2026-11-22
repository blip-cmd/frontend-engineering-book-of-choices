import { createSignal, onSettled } from 'solid-js';
import uPlot from 'uplot';
import 'uplot/dist/uPlot.min.css';
import { RingBuffer } from './ring';

const CAPACITY = 10_000; // visible window: the most recent samples

export function Dashboard() {
  let host!: HTMLDivElement;
  // Slow summary for screen readers, refreshed once per second, not per tick.
  const [summary, setSummary] = createSignal('Waiting for data');

  onSettled(() => {
    const times = new RingBuffer(CAPACITY);
    const values = new RingBuffer(CAPACITY);
    const xs = new Float64Array(CAPACITY);
    const ys = new Float64Array(CAPACITY);
    let dirty = false;
    let lastSummary = 0;

    const chart = new uPlot(
      {
        width: 800,
        height: 300,
        series: [{}, { label: 'Price', stroke: '#2563eb', width: 1 }],
        axes: [{}, {}],
      },
      [new Float64Array(0), new Float64Array(0)],
      host,
    );

    const worker = new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' });
    worker.onmessage = (event: MessageEvent<ArrayBuffer>) => {
      const batch = new Float64Array(event.data);
      for (let i = 0; i < batch.length; i += 2) {
        times.push(batch[i]!);
        values.push(batch[i + 1]!);
      }
      dirty = true; // draw later, once per frame
    };

    let frame = requestAnimationFrame(function draw(now) {
      if (dirty) {
        const n = times.copyInto(xs);
        values.copyInto(ys);
        chart.setData([xs.subarray(0, n), ys.subarray(0, n)]);
        dirty = false;
        if (now - lastSummary > 1000) {
          lastSummary = now;
          setSummary(`${n} samples, latest ${ys[n - 1]!.toFixed(2)}`);
        }
      }
      frame = requestAnimationFrame(draw);
    });

    return () => {
      cancelAnimationFrame(frame);
      worker.terminate();
      chart.destroy();
    };
  });

  return (
    <main>
      <h1>Real-time dashboard</h1>
      <div ref={host} />
      <p role="status">{summary()}</p>
    </main>
  );
}
