// @ts-check
import { defineConfig } from 'astro/config';
import preact from '@astrojs/preact';
import tailwindcss from '@tailwindcss/vite';

// https://docs.astro.build/en/reference/configuration-reference/
export default defineConfig({
  // Replace with your production URL (used for canonical URLs and sitemaps).
  site: 'https://example.com',
  integrations: [preact()],
  vite: {
    plugins: [tailwindcss()],
  },
});
