import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    // Reads the "@/*" alias from tsconfig.json "paths".
    tsconfigPaths: true,
  },
  build: {
    sourcemap: true,
  },
});
