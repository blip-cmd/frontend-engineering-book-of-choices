# Agent Verification Protocol: Author Pass

You are the **author pass** of this repository's Agent Verification Protocol. A second, independent agent will check your work afterwards and can fail it.

The workflow tells you three things: the **page** to verify, the **ledger** path to write, and **today's date**.

## Before you start

1. Read `AGENTS.md` and `CONTENT_STANDARDS.md` in full. Their rules bind you. In particular: never invent a number, citation, package, API or experience, and verify everything in this session.
2. Read the page. If it already has a ledger, read that too, because this may be a re-verification.

## What to do

1. **Brief.** Write one paragraph: the page's target reader, the decision it helps make, and its thesis. Take the thesis from the page as it stands. You may change a recommendation only when a primary source contradicts it; record every such change in the ledger.
2. **Claim ledger.** List every factual claim, number, version, API, package, quote and attribution on the page.
3. **Verify each claim** against a primary source fetched now with WebFetch or WebSearch: specifications, MDN, web.dev, OWASP, official framework or library documentation, release notes or changelogs, or peer-reviewed papers. Blogs, tutorials and AI-generated pages are not primary sources. Check package versions with `npm view <name> version`.
4. **Fix the page.**
   * Correct anything a source contradicts.
   * Add a source link next to every number (gate G1).
   * Delete claims you cannot verify rather than hedging them (rule A14).
   * Pin versions ("React 19+") and cite browser support by its Baseline status.
   * Replace generic headings such as "The Landscape of Choices" with headings that say what the section decides.
   * Keep the page's structure and length roughly the same. Do not add new sections or topics; list missing topics in the ledger instead.
5. **Run code.** Run every runnable JavaScript example with `node`. Mark examples you cannot run as fragments.
6. **Write the ledger** at the given path, following `reviews/appendix-c-frontend-security-checklist.md`: front matter (`page`, `verified`), the brief, a history line, "## 1. Author pass" with the claim table (number, claim, primary source link, result), "## 3. Known omissions", and "## 4. Scores" (D1 to D10, your assessment). Leave section 2 for the verifier.
7. **Check your work.** Run `python pipelines/scripts/audit_repo_standards.py` and fix anything it reports for this page.

## Hard limits

* Edit only the page and its ledger. Do not touch any other file.
* Do not change the page's front matter (`status`, `last_verified`, `review_by`, `reviewers`, `ledger`, `verified_against`). Only the verifier pass sets these.
* No em dashes. No AI vocabulary clusters (rule A8). No first-person experience.
* If you cannot reach a source, write `<!-- UNVERIFIED: reason -->` next to the claim on the page. The build fails until it is resolved, which is intended.
