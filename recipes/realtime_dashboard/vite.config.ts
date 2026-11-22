import { defineConfig } from 'vite';
import solid from '@solidjs/vite-plugin';

export default defineConfig({
  plugins: [solid()],
  // Emit the worker as an ES module, matching `new Worker(..., { type: 'module' })`.
  worker: { format: 'es' },
});
