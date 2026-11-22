import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Vite 8 configuration for the collaborative canvas starter.
export default defineConfig({
  plugins: [react()],
  server: { port: 3000 },
  build: { target: 'es2022' },
});
