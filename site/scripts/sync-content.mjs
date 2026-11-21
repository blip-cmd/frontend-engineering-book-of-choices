// SPDX-License-Identifier: AGPL-3.0-only
// Copyright (C) 2026 blip-cmd and contributors
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

/** Review-status front matter (flat `key: value` lines), as defined in CONTENT_STANDARDS.md. */
function splitFrontMatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n/);
  if (!m) return { meta: {}, body: text };
  const meta = {};
  for (const line of m[1].split('\n')) {
    const i = line.indexOf(':');
    if (i > 0 && !line.trimStart().startsWith('#')) meta[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return { meta, body: text.slice(m[0].length) };
}

const STANDARDS_URL = `${REPO_URL}/blob/${BRANCH}/CONTENT_STANDARDS.md`;

/** A visible notice telling readers how far this page has been checked. */
function reviewBanner(meta, src) {
  if (!meta.status) return null;
  const issue = `${REPO_URL}/issues/new?template=correction.yml`;
  if (meta.status === 'draft') {
    return [
      ':::caution[Draft: not yet reviewed]',
      `This page is an AI-assisted first draft. It has not yet passed the [content standards review](${STANDARDS_URL}), so treat its numbers and recommendations as unverified. Spotted a problem? [Report it](${issue}) or [help review this page](${REPO_URL}/blob/${BRANCH}/${src}).`,
      ':::',
    ].join('\n');
  }
  const ledgerLink = meta.ledger ? `[claim ledger](${REPO_URL}/blob/${BRANCH}/${meta.ledger})` : 'claim ledger';
  if (meta.status === 'agent-verified') {
    return [
      ':::tip[Verified by AI agents]',
      `Every claim on this page was checked against official documentation and primary sources by AI agents, following the [content standards](${STANDARDS_URL}). The ${ledgerLink} lists each claim and its source, plus an independent second check.` +
        (meta.last_verified ? ` Last verified ${meta.last_verified}` : '') +
        (meta.verified_against ? ` against ${meta.verified_against}.` : meta.last_verified ? '.' : '') +
        (meta.review_by ? ` Next check due ${meta.review_by}.` : '') +
        ` It has not yet been reviewed by a human expert. [Report an error](${issue}).`,
      ':::',
    ].join('\n');
  }
  const who = (meta.reviewers || '').split(',').map((r) => r.trim()).filter(Boolean)
    .map((r) => `[${r}](https://github.com/${r})`).join(', ');
  const ai = meta.ai_involvement === 'drafted' ? 'Drafted with AI assistance, then reviewed'
    : meta.ai_involvement === 'assisted' ? 'Written with AI assistance and reviewed' : 'Reviewed';
  const label = meta.status === 'gold' ? 'Reviewed (gold standard)' : 'Reviewed';
  return [
    `:::note[${label}]`,
    `${ai}, source-checked and edited by ${who || 'the maintainers'} against the [content standards](${STANDARDS_URL}).` +
      (meta.last_verified ? ` Last verified ${meta.last_verified}` : '') +
      (meta.verified_against ? ` against ${meta.verified_against}.` : meta.last_verified ? '.' : '') +
      (meta.review_by ? ` Next review due ${meta.review_by}.` : '') +
      ` Sources are linked in the text. [Report an error](${issue}).`,
    ':::',
  ].join('\n');
}

export function sync() {
  const sources = collectSources();
  const slugBySource = new Map(sources.map((s) => [s.src, s.slug]));

  for (const dir of ['chapters', 'playbooks', 'appendices', 'essays']) {
    fs.rmSync(path.join(DOCS_DIR, dir), { recursive: true, force: true });
  }

  for (const entry of sources) {
    const file = fs.readFileSync(path.join(REPO_ROOT, entry.src), 'utf8').replace(/\r\n/g, '\n');
    const { meta, body: raw } = splitFrontMatter(file);
    const h1 = raw.match(/^#\s+(.+)$/m);
    const title = h1 ? h1[1].trim() : entry.slug;
    let body = h1 ? raw.replace(h1[0], '').replace(/^\s+/, '') : raw;
    body = rewriteLinks(body, entry.src, slugBySource);
    const description = describe(body);
    const banner = reviewBanner(meta, entry.src);
    if (banner) body = `${banner}\n\n${body}`;

    const updated = lastCommitDate(entry.src);
    const fm = [
      '---',
      `title: ${yaml(title)}`,
      `description: ${yaml(description)}`,
      `editUrl: ${yaml(`${REPO_URL}/edit/${BRANCH}/${entry.src}`)}`,
      updated ? `lastUpdated: ${updated}` : null,
      meta.status ? `reviewStatus: ${yaml(meta.status)}` : null,
      meta.last_verified ? `lastVerified: ${yaml(meta.last_verified)}` : null,
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
