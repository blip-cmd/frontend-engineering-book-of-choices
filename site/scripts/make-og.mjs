// Renders the default social preview image (public/og/default.png, 1200x630).
// Run manually after changing the design: node scripts/make-og.mjs
import sharp from 'sharp';
import { fileURLToPath } from 'node:url';

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
  <text x="80" y="290" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="72" font-weight="800" fill="url(#t)">Frontend Engineering</text>
  <text x="80" y="375" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="72" font-weight="800" fill="url(#t)">as a Book of Choices</text>
  <text x="80" y="455" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="32" fill="#cbd5e1">A free, open reference: map your constraints to the frontend</text>
  <text x="80" y="500" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="32" fill="#cbd5e1">architecture that fits, and see what each choice costs.</text>
  <text x="80" y="575" font-family="Consolas, Menlo, monospace" font-size="26" fill="#38bdf8">blip-cmd.github.io/frontend-engineering-book-of-choices</text>
</svg>`;

await sharp(Buffer.from(svg)).png().toFile(out);
console.log(`Wrote ${out}`);
