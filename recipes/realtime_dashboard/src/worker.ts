// Simulated feed: generates ticks locally (no network) and posts them in batches.
// In a real app, open the WebSocket here (binaryType = "arraybuffer") and decode in this worker.
const TICKS_PER_BATCH = 20;
const BATCH_INTERVAL_MS = 10; // about 2000 ticks per second

let price = 100;

setInterval(() => {
  // Interleaved pairs: [time in seconds, value, time, value, ...]
  const batch = new Float64Array(TICKS_PER_BATCH * 2);
  const now = Date.now() / 1000;
  for (let i = 0; i < TICKS_PER_BATCH; i++) {
    price += (Math.random() - 0.5) * 0.2;
    batch[i * 2] = now + i / (TICKS_PER_BATCH * 100);
    batch[i * 2 + 1] = price;
  }
  // Typed arrays are not transferable; their .buffer is. Transferring detaches it here.
  self.postMessage(batch.buffer, { transfer: [batch.buffer] });
}, BATCH_INTERVAL_MS);
