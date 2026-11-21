# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 blip-cmd and contributors
"""
Repository Standards Audit

Checks every Markdown file in the repository for house style (no em dashes) and
broken relative links. Book pages (book/ and docs/essays/) are also checked
against the automatable parts of CONTENT_STANDARDS.md:

  errors (fail CI)                       warnings (reported, do not fail)
  - missing or invalid review front matter - unsourced numbers on draft pages
  - verified pages missing dates/ledger     - AI-vocabulary clusters
  - UNVERIFIED markers left in the text    - reviewed pages past their review_by date
  - known-stale facts (stale_facts.json)
  - unsourced numbers on reviewed pages
"""

from datetime import date
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

try:
    from pipelines.scripts.content_meta import AI_INVOLVEMENT, REQUIRED_KEYS, STATUSES, VERIFIED_STATUSES, split_front_matter
except ImportError:  # run directly as a script
    from content_meta import AI_INVOLVEMENT, REQUIRED_KEYS, STATUSES, VERIFIED_STATUSES, split_front_matter

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
STALE_FACTS = json.loads((REPO_ROOT / "pipelines" / "config" / "stale_facts.json").read_text(encoding="utf-8"))

YEAR_MONTH = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
# Numbers that read as factual claims: percentages, multipliers, timings, sizes.
NUMERIC_CLAIM = re.compile(
    r"\d+(?:\.\d+)?\s?%"
    r"|\d+(?:\.\d+)?\s?x\s+(?:faster|slower|smaller|larger|more|less|fewer)"
    r"|\d+(?:\.\d+)?\s?(?:ms|KB|kB|MB|seconds?)\b",
    re.I,
)
INLINE_CODE = re.compile(r"`[^`]*`")
AI_VOCABULARY = re.compile(
    r"\b(delve[sd]?|delving|underscore[sd]?|showcas(?:e|es|ed|ing)|pivotal|crucial|notably|comprehensive|"
    r"testament|tapestry|seamless(?:ly)?|robust|leverag(?:e|es|ed|ing)|landscape|paradigm shift|game[- ]changer)\b",
    re.I,
)


def markdown_files():
    """Tracked and new (non-ignored) Markdown files; local research folders stay out."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", "*.md", "*.mdx"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout
        files = [REPO_ROOT / line for line in out.splitlines() if line.strip()]
    except (OSError, subprocess.CalledProcessError):
        files = [p for p in REPO_ROOT.glob("**/*.md") if ".git" not in p.parts and "node_modules" not in p.parts]
    return sorted(p for p in files if p.exists())


def is_content_page(rel):
    if rel.startswith("book/") and rel != "book/README.md" and not rel.startswith("book/dist/"):
        return rel.endswith(".md")
    return rel.startswith("docs/essays/") and rel.endswith(".md")


def blocks_outside_code(text):
    """Yield (first_line_number, block_text) for blank-line-separated blocks, skipping fenced code."""
    block, start, in_code = [], 0, False
    for idx, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.strip():
            if not block:
                start = idx
            block.append(line)
        elif block:
            yield start, "\n".join(block)
            block = []
    if block:
        yield start, "\n".join(block)


def audit_style_and_links(file_path, text):
    issues = []
    in_code_block = False
    for line_idx, line in enumerate(text.splitlines(), 1):
        if "\u2014" in line:
            issues.append(f"Line {line_idx}: Contains Unicode em-dash (\\u2014)")
        is_table_separator = re.fullmatch(r"\s*\|[\s:\-|]+\|\s*", line) is not None
        if not is_table_separator and re.search(r"[^\s\-]---[^\s\-]", line):
            issues.append(f"Line {line_idx}: Contains triple-dash em-dash in text")

        if line.strip().startswith("```"):
            in_code_block = not in_code_block
        if in_code_block:
            continue
        for target in re.findall(r"\]\(([^)\s]+)\)", line):
            if re.match(r"^(https?:|mailto:|#|/)", target):
                continue
            path_part = unquote(target.split("#")[0])
            if path_part and not (file_path.parent / path_part).exists():
                issues.append(f"Line {line_idx}: Broken relative link -> {target}")
    return issues


def audit_content_page(text, today):
    """Return (errors, warnings) for a book page, per CONTENT_STANDARDS.md."""
    errors, warnings = [], []
    meta, body = split_front_matter(text)
    offset = text[: len(text) - len(body)].count("\n")  # front matter lines, for line numbers

    if not meta:
        return ["Missing review front matter (see CONTENT_STANDARDS.md, 'Page status')"], []
    missing = [k for k in REQUIRED_KEYS if k not in meta]
    if missing:
        errors.append(f"Front matter missing keys: {', '.join(missing)}")
    status = meta.get("status", "")
    if status not in STATUSES:
        errors.append(f"Front matter status must be one of {STATUSES}, got '{status}'")
    if meta.get("ai_involvement", "") not in AI_INVOLVEMENT:
        errors.append(f"Front matter ai_involvement must be one of {AI_INVOLVEMENT}")
    reviewed = status in VERIFIED_STATUSES
    if reviewed:
        for key in ("last_verified", "review_by"):
            if not YEAR_MONTH.match(meta.get(key, "")):
                errors.append(f"Verified page needs {key} as YYYY-MM")
        ledger = meta.get("ledger", "")
        if not ledger:
            errors.append("Verified page needs a ledger: path to its claim ledger in reviews/")
        elif not (REPO_ROOT / ledger).is_file():
            errors.append(f"Claim ledger not found: {ledger}")
    if status in ("reviewed", "gold") and not meta.get("reviewers"):
        errors.append("Reviewed page needs at least one human reviewer (gate G8)")
    if status == "agent-verified" and meta.get("reviewers"):
        errors.append("agent-verified pages must leave reviewers empty: reviewers are humans only (rule A12)")
        if YEAR_MONTH.match(meta.get("review_by", "")) and meta["review_by"] < today.strftime("%Y-%m"):
            warnings.append(f"Review overdue: review_by {meta['review_by']} has passed")

    lines = body.splitlines()
    for idx, line in enumerate(lines, 1 + offset):
        if "UNVERIFIED" in line:
            errors.append(f"Line {idx}: UNVERIFIED marker must be resolved by a human (rule A7)")
        for fact in STALE_FACTS:
            if re.search(fact["pattern"], line) and not re.search(fact["unless"], line):
                errors.append(f"Line {idx}: Stale fact [{fact['id']}]: {fact['message']}")

    unsourced = []
    for start, block in blocks_outside_code(body):
        if NUMERIC_CLAIM.search(INLINE_CODE.sub("", block)) and "](http" not in block:
            unsourced.append(start + offset)
    if unsourced:
        msg = f"{len(unsourced)} block(s) with numbers but no source link (gate G1), starting at lines {', '.join(map(str, unsourced[:8]))}{'...' if len(unsourced) > 8 else ''}"
        (errors if reviewed else warnings).append(msg)

    words = max(len(re.findall(r"\b\w+\b", body)), 1)
    hits = len(AI_VOCABULARY.findall(body))
    if hits * 300 / words >= 3:
        warnings.append(f"AI-vocabulary cluster: {hits} watch-list words in {words} words (dimension D7)")
    return errors, warnings


def main():
    print("=" * 70)
    print(" REPOSITORY STANDARDS AUDIT")
    print("=" * 70)

    today = date.today()
    total_files = total_words = content_pages = 0
    all_errors, all_warnings, statuses = {}, {}, {}

    for md_file in markdown_files():
        rel = md_file.relative_to(REPO_ROOT).as_posix()
        # Generated copies of the book for the website (links there are site URLs)
        if rel.startswith(("site/src/content/docs/", "site/dist/")) and not rel.endswith("index.mdx"):
            continue
        text = md_file.read_text(encoding="utf-8")
        total_files += 1
        total_words += len(re.findall(r"\b\w+\b", text))

        errors = audit_style_and_links(md_file, text)
        warnings = []
        if is_content_page(rel):
            content_pages += 1
            content_errors, warnings = audit_content_page(text, today)
            errors += content_errors
            status = split_front_matter(text)[0].get("status", "missing")
            statuses[status] = statuses.get(status, 0) + 1
        if errors:
            all_errors[rel] = errors
        if warnings:
            all_warnings[rel] = warnings

    print(f"Audited {total_files} markdown files ({total_words:,} words), including {content_pages} book pages.")
    print("Book page status: " + ", ".join(f"{k} {v}" for k, v in sorted(statuses.items())))

    if all_warnings:
        print(f"\n[WARNINGS] {sum(len(w) for w in all_warnings.values())} warning(s) (do not fail the build):")
        for f, warns in all_warnings.items():
            for w in warns:
                print(f"  {f}: {w}")

    if all_errors:
        print("\n[FAILED] Issues that must be fixed:")
        for f, errs in all_errors.items():
            print(f"\n  File: {f}")
            for e in errs:
                print(f"    - {e}")
        sys.exit(1)
    print("\n[PASSED] House style, links and content-standards gates verified.")


if __name__ == "__main__":
    main()
