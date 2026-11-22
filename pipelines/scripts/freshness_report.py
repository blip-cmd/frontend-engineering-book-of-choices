# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 blip-cmd and contributors
"""
Weekly freshness report (see docs/WORKFLOW.md). Checks, without changing anything:

  1. Library releases: packages in pipelines/config/version_watch.json whose latest
     npm major version differs from the recorded baseline, and the pages that mention them.
  2. Overdue pages: verified pages whose review_by month has passed.
  3. Broken links: external links in the book, essays and project docs.
  4. Recipes: dependencies in recipes/*/package.json a major version behind npm.

Writes a Markdown report to stdout (or --output FILE). Exit code is always 0;
the report is meant to be read by people and by the agent review job.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import json
from pathlib import Path
import re
import urllib.error
import urllib.request

try:
    from pipelines.scripts.content_meta import VERIFIED_STATUSES, split_front_matter
    from pipelines.scripts.next_review import content_pages
except ImportError:  # run directly as a script
    from content_meta import VERIFIED_STATUSES, split_front_matter
    from next_review import content_pages

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WATCH = REPO_ROOT / "pipelines" / "config" / "version_watch.json"
LINK = re.compile(r"\]\((https?://[^)\s]+)\)|<(https?://[^>\s]+)>")
DOC_FILES = ["README.md", "CONTRIBUTING.md", "CONTENT_STANDARDS.md", "ROADMAP.md", "library/reading_list.md"]
# Sites that refuse or drop automated requests: failures there are "unverifiable", not "broken".
BOT_HOSTILE = ("npmjs.com", "www.npmjs.com", "oreilly.com", "www.oreilly.com", "medium.com", "x.com", "twitter.com", "linkedin.com")
UA = "Mozilla/5.0 (compatible; book-of-choices-freshness/1.0; +https://github.com/blip-cmd/frontend-engineering-book-of-choices)"


def npm_latest(package):
    url = f"https://registry.npmjs.org/{package.replace('/', '%2F')}/latest"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)["version"]


def major_of(version):
    parts = version.split(".")
    return f"0.{parts[1]}" if parts[0] == "0" else parts[0]


def page_texts():
    return {rel: (REPO_ROOT / rel).read_text(encoding="utf-8") for rel in content_pages()}


def check_versions(texts):
    watch = json.loads(WATCH.read_text(encoding="utf-8"))["packages"]
    rows, errors = [], []

    def one(item):
        name, cfg = item
        try:
            return name, cfg, npm_latest(name), None
        except Exception as exc:  # network or registry problem
            return name, cfg, None, str(exc)

    with ThreadPoolExecutor(max_workers=8) as pool:
        for name, cfg, latest, err in pool.map(one, watch.items()):
            if err:
                errors.append(f"`{name}`: {err}")
                continue
            if major_of(latest) != cfg["major"]:
                terms = [re.compile(rf"(?<![\w-]){re.escape(t)}(?![\w-])") for t in cfg["terms"]]
                pages = [rel for rel, text in texts.items() if any(t.search(text) for t in terms)]
                rows.append((name, cfg["major"], latest, pages))
    return rows, errors


def check_recipes():
    """(recipe, package, declared range, latest) for recipe dependencies a major behind npm."""
    wanted = []
    for pkg_json in sorted((REPO_ROOT / "recipes").glob("*/package.json")):
        data = json.loads(pkg_json.read_text(encoding="utf-8"))
        for section in ("dependencies", "devDependencies"):
            for name, spec in data.get(section, {}).items():
                m = re.search(r"\d+(?:\.\d+)?", spec)
                if m:
                    wanted.append((pkg_json.parent.name, name, spec, m.group(0)))

    def one(item):
        recipe, name, spec, declared = item
        try:
            latest = npm_latest(name)
        except Exception:
            return None
        declared_major = declared if declared.startswith("0.") else declared.split(".")[0]
        return (recipe, name, spec, latest) if major_of(latest) != declared_major else None

    with ThreadPoolExecutor(max_workers=8) as pool:
        return [row for row in pool.map(one, wanted) if row]


def check_overdue(texts, today):
    month = today.strftime("%Y-%m")
    overdue = []
    for rel, text in texts.items():
        meta, _ = split_front_matter(text)
        if meta.get("status") in VERIFIED_STATUSES and meta.get("review_by", "9999-99") < month:
            overdue.append((rel, meta.get("review_by")))
    return overdue


def collect_links(texts):
    files = dict(texts)
    for rel in DOC_FILES:
        path = REPO_ROOT / rel
        if path.exists():
            files[rel] = path.read_text(encoding="utf-8")
    links = {}
    for rel, text in files.items():
        for m in LINK.finditer(text):
            url = (m.group(1) or m.group(2)).rstrip(".,;")
            if "example.com" in url or "{" in url:
                continue
            links.setdefault(url, set()).add(rel)
    return links


def probe(url):
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                return resp.status
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in (403, 404, 405, 429, 501):
                continue  # some servers reject HEAD; retry with GET
            return exc.code
        except Exception as exc:
            if method == "HEAD":
                continue
            return f"error: {type(exc).__name__}"
    return "error"


def check_links(texts):
    links = collect_links(texts)
    broken, unverifiable = [], []
    with ThreadPoolExecutor(max_workers=12) as pool:
        for url, result in zip(links, pool.map(probe, links)):
            ok = isinstance(result, int) and result < 400
            if ok:
                continue
            host = re.sub(r"^https?://([^/]+).*$", r"\1", url)
            target = unverifiable if host in BOT_HOSTILE else broken
            target.append((url, result, sorted(links[url])))
    return len(links), broken, unverifiable


def render(today, versions, version_errors, overdue, link_total, broken, unverifiable, texts, recipes_behind=()):
    statuses = {}
    for text in texts.values():
        s = split_front_matter(text)[0].get("status", "missing")
        statuses[s] = statuses.get(s, 0) + 1
    out = [f"# Freshness report, {today.isoformat()}", "",
           "Page status: " + ", ".join(f"**{k}** {v}" for k, v in sorted(statuses.items())), ""]

    out += ["## Library releases since the baseline", ""]
    if versions:
        out += ["| Package | Baseline major | Latest | Pages that mention it |", "| :--- | :--- | :--- | :--- |"]
        for name, base, latest, pages in versions:
            out.append(f"| `{name}` | {base} | {latest} | {', '.join(f'`{p}`' for p in pages) or 'none'} |")
        out += ["", "Re-verify the listed pages, then update `major` in `pipelines/config/version_watch.json`."]
    else:
        out.append("No new major versions.")
    if version_errors:
        out += ["", "Could not check: " + "; ".join(version_errors)]

    out += ["", "## Pages overdue for re-verification", ""]
    out += [f"- `{rel}` (review_by {rb})" for rel, rb in overdue] or ["None."]

    out += ["", "## Recipe dependencies behind the latest major", ""]
    if recipes_behind:
        out += ["| Recipe | Package | Declared | Latest |", "| :--- | :--- | :--- | :--- |"]
        out += [f"| `{r}` | `{n}` | {spec} | {latest} |" for r, n, spec, latest in recipes_behind]
        out += ["", "Upgrade the recipe, run `npm install`, its type check and `npm run build`, and commit the lockfile."]
    else:
        out.append("All recipe dependencies are on the latest major.")

    out += ["", f"## Links ({link_total} checked)", ""]
    if broken:
        out += ["| Link | Result | Used in |", "| :--- | :--- | :--- |"]
        out += [f"| {url} | {res} | {', '.join(f'`{f}`' for f in files)} |" for url, res, files in broken]
    else:
        out.append("No broken links.")
    if unverifiable:
        out += ["", f"{len(unverifiable)} link(s) on sites that block automated checks were skipped: "
                + ", ".join(url for url, _, _ in unverifiable)]
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Weekly freshness report")
    parser.add_argument("--output", help="write the report to this file instead of stdout")
    parser.add_argument("--skip-links", action="store_true", help="skip the external link check")
    args = parser.parse_args()

    today = date.today()
    texts = page_texts()
    versions, version_errors = check_versions(texts)
    overdue = check_overdue(texts, today)
    link_total, broken, unverifiable = (0, [], []) if args.skip_links else check_links(texts)
    recipes_behind = check_recipes()
    report = render(today, versions, version_errors, overdue, link_total, broken, unverifiable, texts, recipes_behind)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
