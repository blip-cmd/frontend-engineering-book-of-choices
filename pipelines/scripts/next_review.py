# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 blip-cmd and contributors
"""
Pick the next book page for agent verification (see docs/WORKFLOW.md).

Priority:
  1. a verified page whose review_by month has passed (re-verification);
  2. otherwise the first draft page in pipelines/config/review_queue.json;
  3. otherwise any other draft page not listed in the queue.

Prints the page path, or nothing if every page is verified and current.
With --github-output, also writes `page=` and `slug=` to $GITHUB_OUTPUT.
"""

from datetime import date
import json
import os
from pathlib import Path
import sys

try:
    from pipelines.scripts.content_meta import VERIFIED_STATUSES, split_front_matter
except ImportError:  # run directly as a script
    from content_meta import VERIFIED_STATUSES, split_front_matter

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
QUEUE = REPO_ROOT / "pipelines" / "config" / "review_queue.json"


def content_pages():
    pages = [p for p in (REPO_ROOT / "book").rglob("*.md") if p.name != "README.md" and "dist" not in p.parts]
    pages += list((REPO_ROOT / "docs" / "essays").glob("*.md"))
    return sorted(p.relative_to(REPO_ROOT).as_posix() for p in pages)


def status_of(rel):
    meta, _ = split_front_matter((REPO_ROOT / rel).read_text(encoding="utf-8"))
    return meta


def pick(today=None):
    this_month = (today or date.today()).strftime("%Y-%m")
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))["queue"]
    pages = content_pages()
    ordered = [p for p in queue if p in pages] + [p for p in pages if p not in queue]

    for rel in ordered:
        meta = status_of(rel)
        if meta.get("status") in VERIFIED_STATUSES and meta.get("review_by", "9999-99") < this_month:
            return rel, "re-verification (review_by passed)"
    for rel in ordered:
        if status_of(rel).get("status", "draft") == "draft":
            return rel, "first draft in the review queue"
    return None, "every page is verified and current"


def slug_for(rel):
    return Path(rel).stem.lstrip("0123456789_").replace("_", "-")


def ledger_for(rel):
    """Existing ledger path from front matter, or reviews/<slug>.md for a first verification."""
    return status_of(rel).get("ledger") or f"reviews/{slug_for(rel)}.md"


def main():
    forced = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--page=") and a.split("=", 1)[1]), None)
    page, reason = (forced, "requested manually") if forced else pick()
    if page:
        print(page)
        print(f"reason: {reason}", file=sys.stderr)
    else:
        print(reason, file=sys.stderr)
    if "--github-output" in sys.argv and os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as out:
            out.write(f"page={page or ''}\nslug={slug_for(page) if page else ''}\n"
                      f"ledger={ledger_for(page) if page else ''}\nreason={reason}\n")


if __name__ == "__main__":
    main()
