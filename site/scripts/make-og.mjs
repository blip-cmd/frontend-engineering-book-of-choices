// SPDX-License-Identifier: AGPL-3.0-only
// Copyright (C) 2026 blip-cmd and contributors
// Renders the default social preview image (public/og/default.png, 1200x630).
// Run after editing the text or design: npm run og (from site/), then commit the PNG.
// Social networks cache previews; refresh LinkedIn's with its Post Inspector.
import sharp from 'sharp';
import { fileURLToPath } from 'node:url';

// Edit the text here. Keep each subtitle line under about 65 characters so it fits.
const TITLE = ['Frontend Engineering', 'as a Book of Choices'];
const SUBTITLE = [
  '20 pages checked by AI, none yet reviewed by a human expert.',
  'Know a frontend topic well? Review a page, put your name on it.',
];
const URL_TEXT = 'blip-cmd.github.io/frontend-engineering-book-of-choices';
const SANS = 'Segoe UI, Helvetica, Arial, sans-serif';

const out = fileURLToPath(new URL('../public/og/default.png', import.meta.url));
const svg = `
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1e1b4b"/><stop offset="1" stop-color="#090d16"/>
    </linearGradient>
    <linearGradient id="t" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#38bdf8"/><stop offset="0.5" stop-color="#818cf8"/><stop offset="1" stop-color="#c084fc"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <g transform="translate(80 80) scale(3)" fill="none">
    <path d="M9 8v16M9 16h6l8-8M15 16l8 8" stroke="#38bdf8" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="23" cy="8" r="2.4" fill="#c084fc"/><circle cx="23" cy="24" r="2.4" fill="#c084fc"/>
  </g>
  ${TITLE.map((line, i) => `<text x="80" y="${290 + i * 85}" font-family="${SANS}" font-size="72" font-weight="800" fill="url(#t)">${line}</text>`).join('')}
  ${SUBTITLE.map((line, i) => `<text x="80" y="${455 + i * 45}" font-family="${SANS}" font-size="32" fill="#cbd5e1">${line}</text>`).join('')}
  <text x="80" y="575" font-family="Consolas, Menlo, monospace" font-size="26" fill="#38bdf8">${URL_TEXT}</text>
</svg>`;

await sharp(Buffer.from(svg)).png().toFile(out);
console.log(`Wrote ${out}`);
