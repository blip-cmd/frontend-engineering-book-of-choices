// SPDX-License-Identifier: AGPL-3.0-only
// Copyright (C) 2026 blip-cmd and contributors
// Fails the build if any page links to a path on this site that was not built.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DIST = fileURLToPath(new URL('../dist/', import.meta.url));
const BASE = '/frontend-engineering-book-of-choices';

const htmlFiles = fs.readdirSync(DIST, { recursive: true }).filter((f) => f.endsWith('.html'));
const broken = [];
for (const file of htmlFiles) {
  const html = fs.readFileSync(path.join(DIST, file), 'utf8');
  for (const [, href] of html.matchAll(/href="([^"]+)"/g)) {
    if (!href.startsWith(`${BASE}/`)) continue;
    const rel = decodeURIComponent(href.slice(BASE.length).split(/[?#]/)[0]);
    const target = path.join(DIST, rel);
    const ok = (fs.existsSync(target) && fs.statSync(target).isFile()) || fs.existsSync(path.join(target, 'index.html'));
    if (!ok) broken.push(`${file} -> ${href}`);
  }
}
if (broken.length) {
  console.error(`[check-links] ${broken.length} broken internal link(s):\n  ${broken.join('\n  ')}`);
  process.exit(1);
}
console.log(`[check-links] ${htmlFiles.length} pages checked, no broken internal links.`);
