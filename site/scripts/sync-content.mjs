// Copies the book's Markdown (the single source of truth in ../book and friends)
// into Starlight's content folder, adding SEO frontmatter and rewriting links.
// Generated files are git-ignored; edit the originals, never the copies.

import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SITE_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REPO_ROOT = path.resolve(SITE_DIR, '..');
const DOCS_DIR = path.join(SITE_DIR, 'src', 'content', 'docs');

export const REPO_URL = 'https://github.com/blip-cmd/frontend-engineering-book-of-choices';
export const BASE = '/frontend-engineering-book-of-choices';
const BRANCH = 'main';

/** Each source file, where it goes on the site, and its sidebar order. */
function collectSources() {
  const entries = [];
  const add = (src, section, order) => {
    const stem = path.basename(src, '.md').replace(/^\d+_/, '').replace(/_/g, '-');
    entries.push({ src, slug: section ? `${section}/${stem}` : stem, section, order });
  };

  for (const f of fs.readdirSync(path.join(REPO_ROOT, 'book')).sort()) {
    const m = f.match(/^(\d+)_.*\.md$/);
    if (m) add(`book/${f}`, 'chapters', Number(m[1]));
  }
  fs.readdirSync(path.join(REPO_ROOT, 'book', '09_decision_playbooks')).sort()
    .forEach((f, i) => add(`book/09_decision_playbooks/${f}`, 'playbooks', i));
  fs.readdirSync(path.join(REPO_ROOT, 'book', '10_appendices')).sort()
    .forEach((f, i) => add(`book/10_appendices/${f}`, 'appendices', i));
  fs.readdirSync(path.join(REPO_ROOT, 'docs', 'essays')).sort()
    .forEach((f, i) => add(`docs/essays/${f}`, 'essays', i));
  entries.push({ src: 'library/reading_list.md', slug: 'further-reading', section: null, order: 0 });
  entries.push({ src: 'CONTRIBUTING.md', slug: 'contribute', section: null, order: 0 });
  return entries;
}

function lastCommitDate(relPath) {
  try {
    const out = execFileSync('git', ['log', '-1', '--format=%cI', '--', relPath], { cwd: REPO_ROOT, encoding: 'utf8' }).trim();
    return out ? out.slice(0, 10) : null;
  } catch {
    return null;
  }
}

function shortLabel(title, section) {
  const chapter = title.match(/^Chapter (\d+):\s*([^:]+)/);
  if (chapter) return `${chapter[1]}. ${chapter[2].trim()}`;
  const appendix = title.match(/^Appendix ([A-Z]):\s*(.+)/);
  if (appendix) return `${appendix[1]}. ${appendix[2].trim()}`;
  if (section === 'playbooks') return title.replace(/^(Decision Playbook|Playbook|Archetype Playbook):\s*/i, '');
  if (section === 'essays') return title.split(':')[0].trim();
  return title;
}

function describe(body) {
  const quote = body.match(/^>\s*(.+)$/m);
  let text = quote ? quote[1] : (body.split('\n').find((l) => /^[A-Za-z]/.test(l)) ?? '');
  text = text.replace(/\*\*|\*|`|\[|\]\([^)]*\)/g, '').trim();
  if (text.length > 158) text = `${text.slice(0, 155).replace(/\s+\S*$/, '')}...`;
  return text;
}

const yaml = (s) => JSON.stringify(s); // JSON strings are valid YAML scalars

function rewriteLinks(body, srcRel, slugBySource) {
  const srcDir = path.posix.dirname(srcRel);
  return body.replace(/\]\((?!https?:|mailto:|#)([^)\s]+)\)/g, (whole, target) => {
    const [rawPath, anchor] = target.split('#');
    const resolved = path.posix.normalize(path.posix.join(srcDir, decodeURIComponent(rawPath)));
    const hash = anchor ? `#${anchor}` : '';
    const slug = slugBySource.get(resolved);
    if (slug) return `](${BASE}/${slug}/${hash})`;
    const kind = resolved.endsWith('/') || !path.posix.extname(resolved) ? 'tree' : 'blob';
    return `](${REPO_URL}/${kind}/${BRANCH}/${encodeURI(resolved.replace(/\/$/, ''))}${hash})`;
  });
}

export function sync() {
  const sources = collectSources();
  const slugBySource = new Map(sources.map((s) => [s.src, s.slug]));

  for (const dir of ['chapters', 'playbooks', 'appendices', 'essays']) {
    fs.rmSync(path.join(DOCS_DIR, dir), { recursive: true, force: true });
  }

  for (const entry of sources) {
    const raw = fs.readFileSync(path.join(REPO_ROOT, entry.src), 'utf8').replace(/\r\n/g, '\n');
    const h1 = raw.match(/^#\s+(.+)$/m);
    const title = h1 ? h1[1].trim() : entry.slug;
    let body = h1 ? raw.replace(h1[0], '').replace(/^\s+/, '') : raw;
    body = rewriteLinks(body, entry.src, slugBySource);

    const updated = lastCommitDate(entry.src);
    const fm = [
      '---',
      `title: ${yaml(title)}`,
      `description: ${yaml(describe(body))}`,
      `editUrl: ${yaml(`${REPO_URL}/edit/${BRANCH}/${entry.src}`)}`,
      updated ? `lastUpdated: ${updated}` : null,
      `sidebar:`,
      `  label: ${yaml(shortLabel(title, entry.section))}`,
      `  order: ${entry.order}`,
      '---',
      '',
      `{/* Generated from ${entry.src} by site/scripts/sync-content.mjs. Edit the original file. */}`,
      '',
    ].filter((l) => l !== null);

    const out = path.join(DOCS_DIR, `${entry.slug}.md`);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    // Markdown (not MDX) does not support JSX comments; use an HTML comment.
    const header = fm.join('\n').replace(/\{\/\*(.*)\*\/\}/, '<!--$1-->');
    fs.writeFileSync(out, `${header}${body}`);
  }
  console.log(`[sync-content] ${sources.length} pages written to src/content/docs`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) sync();
