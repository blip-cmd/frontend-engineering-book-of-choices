# Instructions for AI Agents

> Binding rules for any AI agent (Claude Code, Codex, Cursor, Copilot, Gemini and others) working in this repository. Humans: see [CONTRIBUTING.md](CONTRIBUTING.md).

## What This Project Is

*Frontend Engineering as a Book of Choices* is a free, open reference that maps frontend project constraints to architecture choices and their trade-offs. The book's first draft was AI-generated; it is being reviewed page by page against [CONTENT_STANDARDS.md](CONTENT_STANDARDS.md). **Accuracy matters more than volume.** A short, verified page is worth more than a long, unverified one.

## Repository Map

| Path | What it is | License |
| :--- | :--- | :--- |
| `book/`, `docs/essays/`, `library/` | The writing: single source of truth | CC BY-NC-ND 4.0 |
| `site/` | Astro Starlight website, generated from `book/` by `site/scripts/sync-content.mjs` | AGPL-3.0 |
| `site/src/content/docs/` (except `index.mdx`) | **Generated. Never edit.** Edit the source in `book/` instead | |
| `bin/`, `pipelines/`, `tests/` | CLI, PDF/EPUB builders, standards audit, tests | AGPL-3.0 |
| `recipes/` | Starter configurations | MIT |

## Commands

```bash
npm run audit                                        # standards audit: must pass
npm test                                             # Node CLI tests
python -m unittest discover -s tests -p "test_*.py"  # Python tests
cd site && npm run build                             # website build + internal link check
```

Run all four before proposing any change.

---

## Rules for Drafting or Revising Book Pages

These rules bind any agent that edits `book/`, `docs/` or `library/`. They implement [CONTENT_STANDARDS.md](CONTENT_STANDARDS.md); read it before editing a page.

| ID | Rule |
| :--- | :--- |
| A1 | **MUST** work from a brief: the target reader, the decision the page supports, and its thesis. In the Agent Verification Protocol the thesis is the page's existing one. **MUST NOT** change a recommendation unless a primary source contradicts it, and **MUST** record every such change in the ledger. |
| A2 | **MUST** produce a claim ledger with every content change: every factual claim, number, API, package, version and attribution, each marked verified (with URL and date) or `UNVERIFIED`. |
| A3 | **MUST NOT** write any number, threshold, benchmark or percentage without a source fetched in the same session. If there is no source, make the claim qualitative or remove it. |
| A4 | **MUST** check package names and versions against the registry (`npm view <name>`) and APIs against current official docs. **MUST NOT** rely on versions remembered from training data. |
| A5 | **MUST** open every URL you cite and confirm the page supports the claim. **MUST NOT** cite from memory. |
| A6 | **MUST NOT** write first-person experience, invented case studies, or attributions like "many teams find". |
| A7 | **MUST** mark any claim you could not verify with `<!-- UNVERIFIED: reason -->`. The audit fails on this marker, so a human resolves each one. |
| A8 | **MUST** avoid filler openings, clusters of AI vocabulary (delve, underscore, showcase, pivotal, crucial, notably, comprehensive, testament, tapestry, seamless, robust, leverage, landscape), "not just X but Y" constructions, rule-of-three padding and closing lines about significance. Fix these by making the claim specific, not by swapping synonyms. |
| A9 | **MUST** keep each section self-contained (name its framework, version and constraint) and pin versions in place. **MUST NOT** use "currently", "new", "latest" or "recently" in a time sense. |
| A10 | **MUST NOT** change `status`, `last_verified`, `review_by`, `verified_against` or `ledger` in front matter, **except** as the verifier pass of the [Agent Verification Protocol](docs/WORKFLOW.md#2-the-agent-verification-protocol) after a PASS verdict, and then only to set `agent-verified`. |
| A11 | **MUST NOT** add agent-only instructions or content (llms.txt, hidden markup, metadata) that differs from what the human-readable page says. |
| A12 | **MUST NOT** approve pull requests, set `reviewed` or `gold`, or add names to `reviewers`. Only humans certify human review. |
| A13 | **MUST** default to the safe pattern in examples, and label any insecure code inline with a link to OWASP or the relevant spec. |
| A14 | **MUST** prefer deleting a dubious claim over hedging it ("may", "often", "in some cases") to keep it. |
| A15 | **MUST** follow the house style (no em dashes; `npm run audit` checks this). Treat it as style, not as evidence of quality. |

## Rules for Code Changes

* Keep the SPDX header (`SPDX-License-Identifier: AGPL-3.0-only`) at the top of code files outside `recipes/`.
* Add or update tests for any behaviour you change.
* Do not add dependencies without a stated reason in the pull request.

## Commits and Pull Requests

Follow [docs/WORKFLOW.md](docs/WORKFLOW.md): `type(scope): summary` commit messages, **no AI attribution trailers** (no `Co-authored-by: Claude`, no "Generated with" footers), one concern per pull request, and the pull request template with its AI-assistance disclosure and claim ledger.
