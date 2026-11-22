# Content Standards

> What makes a page of this book "gold" and what makes it "trash", and how every page, pull request and AI-drafted change is reviewed. These rules apply equally to human and AI-assisted writing.

---

## 1. The Short Version

A page is gold when **every claim can be checked** and **it helps the reader make a decision they could not make by reading the official docs**. In practice:

* every number links to its source;
* every recommendation says what it costs and when it is the wrong choice;
* every version and browser-support claim is pinned and dated;
* every code example runs, or is labelled as a fragment;
* a named human has checked it.

A page is trash when it fails in use: code that does not run, numbers nobody can trace, advice that went stale, or text that paraphrases other sources and adds nothing. Who or what wrote it does not matter; whether it holds up does.

### Why these rules (selected evidence)

* Only 26% of nearly 15,000 tutorial code blocks ran as written ([Mirhosseini & Parnin, FSE 2020](https://par.nsf.gov/servlets/purl/10196169)).
* 58.4% of obsolete Stack Overflow answers were already obsolete when posted, and only 20.5% were ever updated ([Zhang et al., IEEE TSE 2021](https://arxiv.org/pdf/1903.12282)).
* Insecure Stack Overflow snippets were found in 15.4% of 1.3 million Android apps ([Fischer et al., IEEE S&P 2017](https://arxiv.org/pdf/1710.03135)). Readers copy examples verbatim.
* Google rates filler and paraphrased content as lowest quality "no matter how they are created" ([Search Quality Rater Guidelines, Sept 2025](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf); [Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)).
* Language models invent package names (at least 5.2% of suggestions from commercial models, 21.7% from open models) and cite sources that do not exist ([Spracklen et al., USENIX Security 2025](https://arxiv.org/abs/2406.10279v3); [Walters & Wilder, 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980)).
* AI-text detectors are unreliable and flagged 61% of essays by non-native English writers as AI-written ([Liang et al., Patterns 2023](https://arxiv.org/html/2304.02819v3)). **This project never uses detectors as evidence.**
* The references developers trust most explain mechanisms, give "when not to use this" its own space, test their code and date their claims (for example [react.dev: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect), [Crafting Interpreters](https://journal.stuffwithstuff.com/2020/04/05/crafting-crafting-interpreters/), [Diátaxis on explanation](https://diataxis.fr/explanation/)).

---

## 2. Page Status

Every page in `book/` and `docs/essays/` starts with a front matter block:

```yaml
---
status: draft            # draft | agent-verified | reviewed | gold
ai_involvement: drafted  # drafted | assisted | none
last_verified:           # YYYY-MM: change ONLY after re-verifying every claim, never for typo fixes
verified_against:        # versions checked, e.g. react 19.x, tanstack-query 5.x
review_by:               # YYYY-MM: 6 months for fast-moving topics, 12 months otherwise
reviewers:               # comma-separated GitHub usernames of the human reviewers (humans only)
ledger:                  # path to the page's claim ledger in reviews/ (required once verified)
---
```

The website shows each page's status in a box at the top: a warning for drafts; "AI-checked" with a link to the ledger for agent-verified pages; and the reviewers, verification date and next review date for human-reviewed pages. The site's separate "Last updated" date only tracks edits. **`last_verified` is the date that means the facts were checked.**

| Status | Meaning | Requirements |
| :--- | :--- | :--- |
| `draft` | Not yet verified against this standard | Front matter present |
| `agent-verified` | Passed the [Agent Verification Protocol](docs/WORKFLOW.md#2-the-agent-verification-protocol): an author pass and an independent verifier pass, every claim checked against primary sources | `last_verified`, `review_by`, `ledger`; empty `reviewers`; no unsourced numbers. The page tells readers no human expert has reviewed it yet. |
| `reviewed` | A human expert passed every gate; score 13 or more | `last_verified`, `review_by`, `ledger`, at least one human in `reviewers`; no unsourced numbers |
| `gold` | Score 17 or more, no zeros, second reviewer agrees | As `reviewed`, plus two reviewers |

---

## 3. Hard Gates (pass or fail)

Any failed gate blocks merging or a `reviewed` status, regardless of score.

| ID | Gate | Passes when |
| :--- | :--- | :--- |
| G1 | **Every number is sourced** | Every statistic, percentage, threshold, multiplier ("5x faster"), benchmark result and bundle size links to its source, or to a reproducible script in the repo. Otherwise remove it or make the claim qualitative. |
| G2 | **Every citation resolves and supports the claim** | Each link was opened during review, the page says what the text claims, and quotes are verbatim. No invented titles, authors or DOIs. |
| G3 | **Code runs or is labelled** | Each code block has a language tag and is either runnable with complete imports or explicitly marked as a fragment or pseudocode. |
| G4 | **Packages and APIs exist** | Every npm package resolves with `npm view <name>` under the expected owner, and every API exists and is not deprecated in the stated version. |
| G5 | **Examples are safe by default** | No example stores tokens insecurely, disables validation, or injects unsanitised HTML unless it is labelled insecure inline, with a link to OWASP or the spec. |
| G6 | **No synthetic experience** | No "in my experience", "teams I worked with" or case study unless a named human supplied it and agreed to be credited. |
| G7 | **No known-stale facts** | Passes the stale-facts list in [`pipelines/config/stale_facts.json`](pipelines/config/stale_facts.json). Deprecations name the date and link the primary announcement. |
| G8 | **Accountability is honest** | For `reviewed` and `gold`: a named human reviewer approved the page and can explain every recommendation without AI help. For `agent-verified`: both protocol passes are recorded in the ledger and the page discloses that no human expert has reviewed it. AI involvement is always recorded in front matter. |
| G9 | **Same content for agents and humans** | Machine-facing files (llms.txt, Markdown copies, metadata) carry no claims or instructions that the human page does not. |
| G10 | **Original wording, licence-clean** | Nothing pasted or closely paraphrased from books, courses or paid articles. Short quotes are attributed. |

---

## 4. Scored Dimensions (0, 1 or 2 each, 20 in total)

| ID | Dimension | 0 | 1 | 2 |
| :--- | :--- | :--- | :--- | :--- |
| D1 | **Decision framing** | One recommendation, no context | Options listed; context or consequences thin | Constraints stated, at least two real alternatives, good **and** bad consequences, and the conditions that would change the advice |
| D2 | **"When not to"** | Absent, or only "it depends" | Present but abstract | Concrete counter-scenarios |
| D3 | **Mechanism before API** | Recipes or names only | Mechanism mentioned in passing | Explains why it behaves this way, so the reader could predict an edge case |
| D4 | **Fact vs judgment** | Opinion stated as fact | Partly labelled | The book's positions are marked as positions; facts are sourced; advocacy sources are labelled as advocacy |
| D5 | **Evidence quality** | Mostly unsourced | Secondary sources, or missing measurement details | Primary sources (specs, MDN, official docs, changelogs). Field data names dataset, month, 75th percentile and device type. Benchmarks name tool, run and versions. Popularity claims name source, edition and sample. |
| D6 | **Currency** | No versions, no dates | Some versions or dates | Framework claims pin versions ("React 19+"); browser support cites its [Baseline](https://web.dev/baseline) status and date; no "new", "currently", "latest" or "recently" in a time sense; "maintenance mode" and "deprecated" kept distinct |
| D7 | **Specificity** | Filler intros, clusters of AI vocabulary, vague attribution ("many teams") | Some padding | Every paragraph makes a checkable claim; headings say what the section decides |
| D8 | **Retrieval-ready structure** | Sections depend on earlier pages ("as mentioned above") | Mostly self-contained | Each section names its context (framework, version, constraint); headings three levels deep at most; diagrams also described in prose or a table |
| D9 | **Examples** | None, or toy examples | Realistic but unexplained | Real scenario, introduced and explained, errors handled, wrong approaches labelled wrong |
| D10 | **Reader fit** | Undefined jargon; starts abstract | Uneven | Written for a named reader (for example "a tech lead choosing a state approach"); terms defined before use; concrete before abstract |

### Verdicts

| Verdict | Condition | Action |
| :--- | :--- | :--- |
| **Blocked** | Any gate fails | Fix or remove the failing content, then re-review |
| **Revise** | Score below 13, or 0 on D1, D5 or D6 | Rewrite the weak dimensions before merging |
| **Publishable** | Score 13 to 16, no 0 on D1, D5 or D6 | Merge as `reviewed`; open issues for dimensions below 2 |
| **Gold** | Score 17 or more, no 0 anywhere, second reviewer agrees | Merge as `gold` |

If a dimension does not apply (for example D9 on a checklist), mark it N/A and scale: `score = round(points / applicable_max * 20)`. These thresholds are editorial judgment, not research findings; they will be recalibrated after the first five reviewed pages.

---

## 5. Workflow 1: Reviewing a Page

Pages are reviewed in risk order, starting where readers copy examples or act on numbers: the security checklist, the Core Web Vitals guide, the migration playbooks, Chapter 3 and the essays, then the playbooks and remaining chapters.

1. **Brief.** Write one paragraph: the target reader, the decision the page helps make, and its thesis. A human writes or approves it.
2. **Claim ledger.** List every factual claim, number, API, package, version and attribution, one per row (template below).
3. **Verify.** Check each row against a primary source and record the URL and date.
4. **Cut.** Remove what cannot be verified. A deleted claim beats a hedged one.
5. **Gates, then score.** Run G1 to G10, then score D1 to D10.
6. **Rewrite.** Fix low dimensions: add "when not to", replace generic headings, restate context per section.
7. **Second opinion** (for `gold`): a second human scores independently.
8. **Record.** Update front matter (`status`, `last_verified`, `verified_against`, `review_by`, `reviewers`).
9. **Re-review** by the `review_by` date, or sooner after a major release of a framework the page discusses.

Claim ledger template (paste into the pull request):

```markdown
| # | Claim (quote) | Type | Primary source | Checked | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | "INP good is 200 ms or less" | threshold | https://web.dev/articles/inp | 2026-11-21 | verified; added "at the 75th percentile" |
| 2 | "80% to 90% of apps only need a server cache" | statistic | none found | 2026-11-21 | removed; rewritten qualitatively |
```

---

## 6. Workflow 2: Issues and Pull Requests from the Community

| Contribution | Required | Review |
| :--- | :--- | :--- |
| Error or outdated-advice issue | A link to a primary source | Confirm, fix quickly, credit the reporter |
| Experience report ("we chose X; it cost Y") | Named contributor; context (team size, scale, versions, year); consent to attribution | Publish as a labelled experience report; do not generalise it into a universal claim. This is the content no AI can produce: treat it as high-value. |
| Content pull request | Signed [CLA](CLA.md); gates G1 to G10; a claim ledger for new factual claims; score 13 or more on touched pages | Full rubric. A typo or link fix needs only G2 and G10. |
| AI-assisted contribution | Disclosure in the pull request (tool and how much it contributed); the contributor can explain the change without AI | Judged on the rubric, not on suspected AI use |

Rules for reviewers:

* **Never use AI-detector output as evidence**, and never publicly accuse a contributor of using AI.
* A fabricated source, package or experience closes the contribution; a second offence blocks the account.
* Be kind and specific: point to the gate or dimension, and suggest the fix.

---

## 7. Workflow 3: AI Agents

Agents follow the binding rules in [`AGENTS.md`](AGENTS.md). Page verification runs every week as the [Agent Verification Protocol](docs/WORKFLOW.md#2-the-agent-verification-protocol): an author pass and an independent verifier pass, each in a fresh context. Never write a number, citation, package or experience that was not verified in the same session. Mark anything unverifiable with `<!-- UNVERIFIED: reason -->`, and the build fails until it is resolved. Only the verifier pass may set `agent-verified`, and no agent may set `reviewed`, `gold` or `reviewers`.

---

## 8. What CI Checks

| Check | Covers | Status |
| :--- | :--- | :--- |
| No em dashes; no broken relative links | House style; links | Enforced |
| Front matter present and valid; verified pages have dates and a ledger; reviewed pages have a human reviewer | Page status; G8 | Enforced |
| New major versions of libraries the book discusses | G7, D6 | Weekly ([freshness report](docs/WORKFLOW.md#3-keeping-information-current)) |
| Commit message format; no AI attribution trailers | [Commits](docs/WORKFLOW.md#4-commits) | Enforced on pull requests |
| `UNVERIFIED` markers block the build | AGENTS.md rule A7 | Enforced |
| Stale-facts list (`pipelines/config/stale_facts.json`) | G7 | Enforced |
| Numbers with no source link in the same paragraph | G1 | Warning on drafts; **error on verified pages** |
| AI-vocabulary clusters | D7 | Warning only |
| Review overdue (`review_by` passed) | Workflow 1, step 9 | Warning |
| Internal links on the built website | Navigation | Enforced |
| External link checker | G2, link rot | Weekly ([freshness report](docs/WORKFLOW.md#3-keeping-information-current)) |
| Code-block extraction and type-check | G3 | Planned |
| `npm view` check for every package named in code | G4 | Planned |

Run everything locally with `npm run audit` (from the repository root).

---

## 9. House Style

* No em dashes: use a colon, comma or parentheses. This is a style choice; passing it says nothing about quality.
* Prefer short paragraphs that each make one checkable claim. Use bullets only for genuinely parallel items.
* Headings say what the section decides ("Choose a server cache when..."), not generic labels ("The Landscape of Choices").
* Write timelessly: say "since React 19" rather than "the new React".
