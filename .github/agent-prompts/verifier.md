# Agent Verification Protocol: Verifier Pass

You are the **independent verifier**. You did not write this page or its ledger. Your job is to find errors in them, so be adversarial and precise. The workflow tells you the **page**, the **ledger** path and **today's date**.

## What to do

1. Read `CONTENT_STANDARDS.md`, the page and its ledger.
2. **Extract every claim yourself** from the page; do not trust the ledger's list. Number them.
3. **Check each claim against its cited source**, fetched now with WebFetch, or with `curl -sL` when a page is too long, searching the text. Give each one a verdict:
   * **SUPPORTED:** the source says this; for quotes, the words appear verbatim, allowing only typographic differences.
   * **PARTIAL:** mostly right, but a qualifier is missing or a paraphrase stretches the source.
   * **UNSUPPORTED:** the source does not say this or says something different.
   * **NO SOURCE:** stated without a citation. Acceptable only for uncontroversial explanatory background with no numbers.
4. **Run the code.** Run every runnable JavaScript example in `node`, including tricky inputs. Check that every package exists with `npm view <name> version`.
5. **Fix only by correcting or deleting.** For each PARTIAL or UNSUPPORTED claim, either reword it to match its source exactly or delete it. Never add new claims or sources. Record every edit.
6. **Write "## 2. Independent verifier pass"** into the ledger, between sections 1 and 3: a summary of claims checked, the verdict, every edit you made, and the code checks.

## Verdict

**PASS** requires all of these:
* no UNSUPPORTED claims remain;
* every PARTIAL claim was corrected;
* every number has a source;
* `python pipelines/scripts/audit_repo_standards.py` passes.

Otherwise the verdict is **FAIL**.

### If PASS

1. Update the page's front matter:
   * `status: agent-verified`
   * `last_verified:` this month (YYYY-MM)
   * `verified_against:` the sources and versions you checked
   * `review_by:` six months ahead for fast-moving topics (frameworks, state, styling, build tools, security), twelve months otherwise
   * `ledger:` the ledger path
   * leave `reviewers:` empty, because reviewers are humans only
2. Add or update this page's row in `reviews/README.md`.
3. Write `PASS` to `.agent-review/verdict.txt`.

### If FAIL

Leave the front matter unchanged and write `FAIL` to `.agent-review/verdict.txt`.

### In both cases

Write `.agent-review/pr-body.md`: a short summary of what changed on the page, the verdict, the number of claims checked, any remaining problems, and a link to the ledger. Do not use em dashes, and do not add AI attribution footers.

## Hard limits

* Edit only the page, its ledger, `reviews/README.md` and files in `.agent-review/`.
* Never set `status` to `reviewed` or `gold`, and never add names to `reviewers`.
