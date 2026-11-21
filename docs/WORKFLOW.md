# How We Work

> How changes are made, checked and shipped: quality through gates, timeliness through a fixed weekly rhythm, and current information through automated freshness checks. Content rules live in [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md); rules for AI agents in [AGENTS.md](../AGENTS.md).

---

## 1. The Weekly Rhythm

Everything below runs on its own. Times are UTC.

| When | What | Result |
| :--- | :--- | :--- |
| Monday 05:43 | **Freshness report** ([workflow](../.github/workflows/freshness.yml)): new major versions of libraries the book discusses, pages overdue for re-verification, broken links | One issue labelled `freshness`, updated every week |
| Monday 06:17 | **Agent review** ([workflow](../.github/workflows/agent-review.yml)): verifies the next page with the Agent Verification Protocol | A pull request. It **auto-merges** if the independent verifier passes it and every check is green; otherwise it is labelled `needs-attention` |
| Daily 07:11 | **Site rebuild** | Publishes anything merged by automation |
| Every pull request | **CI**: commit messages, standards audit, tests, site build, CLA | A green or red check |

**Pace.** One page per week. After Appendix C, 19 draft pages remain, so if every run passes, the whole book is agent-verified by the end of March 2027. Re-verification takes priority: a page whose `review_by` month has passed goes before any new draft.

**The maintainer's 15 minutes a week:**

1. Read the freshness issue.
2. Look at any pull request labelled `needs-attention`.
3. If you have time, pick and post one draft from [`outreach/`](../outreach/), then tell the agent so it updates the log.

---

## 2. The Agent Verification Protocol

Pages move from `draft` to `agent-verified` without a human reviewer, and honestly say so. Each page gets two passes by separate agent runs that do not share context:

1. **Author pass** ([prompt](../.github/agent-prompts/author.md)) checks every claim against primary sources fetched in the same run. It corrects or deletes what does not hold, runs the code, and writes the claim ledger in [`reviews/`](../reviews/).
2. **Verifier pass** ([prompt](../.github/agent-prompts/verifier.md)) independently re-extracts the claims, re-fetches every source and gives each claim a verdict. It may only correct or delete, never add. It sets `status: agent-verified` only if nothing unsupported remains.

Then the workflow checks that only the page, its ledger and `reviews/README.md` changed, and runs every repository check before opening the pull request.

The website shows such pages as **"Verified by AI agents"**, with a link to the ledger and the line "It has not yet been reviewed by a human expert." The `reviewed` and `gold` statuses remain reserved for human experts: community contributors, or the maintainer for future volumes in their own field.

### One-time setup (maintainer)

1. In a terminal with Claude Code, run `claude setup-token` and copy the token it prints. Runs use your Claude subscription, not API billing.
2. In GitHub, go to **Settings**, **Secrets and variables**, **Actions**, then **New repository secret**. Name it `CLAUDE_CODE_OAUTH_TOKEN` and paste the token.
3. At [cla-assistant.io](https://cla-assistant.io), open the repository's settings and add `github-actions[bot]` to the allowlist, so automated pull requests pass the CLA check.
4. In the **Actions** tab, open **Weekly Agent Review** and choose **Run workflow** for a first supervised run.

Until the secret exists, the review workflow skips itself without failing.

---

## 3. Keeping Information Current

* **Library versions.** [`pipelines/config/version_watch.json`](../pipelines/config/version_watch.json) records the major version of about forty libraries the book discusses, with a baseline date of 2026-11-21. When npm shows a new major version, the freshness report lists every page that mentions the library. After those pages are re-verified, raise the recorded `major`.
* **Review dates.** Every verified page carries `review_by`: six months for fast-moving topics, twelve otherwise. Overdue pages are re-verified first.
* **Stale facts.** [`pipelines/config/stale_facts.json`](../pipelines/config/stale_facts.json) blocks known-outdated claims in CI, for example FID presented as a Core Web Vital. Add an entry whenever a deprecation lands.
* **Links.** The freshness report checks every external link weekly.

---

## 4. Commits

Every commit message follows this format, and CI checks it on pull requests:

```text
type(scope): imperative summary in lowercase, 72 characters or fewer

Optional body: why the change was made. Link the issue or the claim ledger.
```

| Type | Use for |
| :--- | :--- |
| `content` | New or expanded book content |
| `review` | A verification pass on a page (claim ledger, status change) |
| `fix` | A correction to content or code |
| `feat` | A new feature in the calculator, CLI or website |
| `docs` | Repository documentation |
| `outreach` | Promotion drafts and the posting log |
| `ci` | Workflows and automation |
| `test`, `refactor`, `chore` | Tests, restructuring, maintenance |

Rules:

* **Scope** is optional: a page or area in kebab-case, for example `review(core-web-vitals-triage-guide): ...` or `feat(calculator): ...`.
* **One concern per commit.** Do not mix a content review with a code change.
* **No AI attribution trailers** (`Co-authored-by: Claude ...`, "Generated with ..."). Disclose AI involvement in the pull request description and in page front matter instead.
* **Check locally (optional):** `git config core.hooksPath .githooks` runs the same checker on every commit.

Examples:

```text
review(frontend-security-checklist): verify against OWASP and MDN
fix(calculator): keep answers in the URL after reset
content(testing-strategy): add chapter outline
outreach: log LinkedIn post for Appendix C
```

---

## 5. Branches and Pull Requests

* **Branch names:** `review/<page-slug>[-date]`, `content/<topic>`, `fix/<topic>`, `feat/<topic>`, `docs/<topic>`, `outreach/<topic>`, `chore/<topic>`.
* **Everything reaches `main` through a pull request**, using the [template](../.github/pull_request_template.md): AI disclosure plus a claim ledger for content changes.
* **Merging:** squash merge, with the pull request title as the commit message, so the title follows the commit format too.
* **Required:** green CI and a signed CLA. Agent review pull requests also need a PASS verdict to auto-merge.
* **Maintainer override:** the repository admin can bypass the branch rules, including force-push, until the book is declared ready. This is reserved for history cleanup and emergencies.

---

## 6. Definition of Done for a Page

A page is done for now when:

1. its front matter says `agent-verified` (or `reviewed` / `gold`), with `last_verified`, `review_by` and `ledger` set;
2. its ledger in `reviews/` records both passes;
3. CI passes with no warnings for that page;
4. it is listed in [`reviews/README.md`](../reviews/README.md);
5. an outreach draft exists for it in [`outreach/`](../outreach/).
