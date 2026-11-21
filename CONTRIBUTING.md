# How to Contribute

> This book gets better when engineers who have shipped real systems correct it, challenge it, and add what is missing. Every issue and pull request helps.

---

## Ways to Help

1. **Report an error or outdated advice.** Frontend tools change fast. If a recommendation is wrong, a library is deprecated, or a number looks off, [open an issue](https://github.com/blip-cmd/frontend-engineering-book-of-choices/issues/new/choose) and link a source.
2. **Share real experience.** The most valuable contributions are trade-offs you have lived through: "we chose X, and this is what it cost us." Open an issue or a pull request against the relevant chapter.
3. **Suggest a missing topic.** See the [roadmap](https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/ROADMAP.md) for chapters already planned, then open an issue for anything else.
4. **Improve the calculator or CLI.** Better questions, better recommendations, accessibility fixes, and tests are all welcome.

---

## Editing a Chapter

The book's text lives in `book/`, `docs/essays/` and `library/`. The website is generated from those files, so **edit the original Markdown, never the copies under `site/src/content/docs/`**. The "Edit page" link at the bottom of every web page opens the right file on GitHub.

### Writing Standards

Every page is reviewed against [CONTENT_STANDARDS.md](https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/CONTENT_STANDARDS.md): ten pass/fail gates and ten scored dimensions. The essentials:

* **Cite your sources.** Every number links to its source; every link must actually support the claim. Prefer official docs, specifications, changelogs and primary data.
* **Write in your own words.** Do not paste text from other books, courses, or paid articles. Short quotes with attribution are fine.
* **Show the trade-off.** Every recommendation says what it costs and when it is the wrong choice.
* **Pin and date.** Name versions ("React 19+") and cite browser support by its Baseline status.
* **Real experience only.** Experience reports are welcome and credited to you; never present invented experience.
* **AI tools** are allowed if you disclose them in the pull request and have checked every claim and line of code yourself. AI agents must follow [AGENTS.md](https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/AGENTS.md).
* **No em dashes.** Use a colon, comma, or parentheses instead. `npm run audit` checks this and the automatable gates.

---

## Running the Project Locally

```bash
# Website (Astro Starlight): http://localhost:4321/frontend-engineering-book-of-choices/
cd site
npm install
npm run dev

# Tests and standards audit (from the repository root)
npm test
python -m unittest discover -s tests -p "test_*.py"
npm run audit
```

---

## Licensing and the Contributor License Agreement

The project uses three licenses:

| Part | License | Why |
| :--- | :--- | :--- |
| Writing: `book/`, `docs/`, `library/`, and the website's page text | [CC BY-NC-ND 4.0](https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/LICENSE-CONTENT.md) | Free to read and share; improvements come back here instead of into competing copies |
| Code: the calculator, CLI, website, pipelines and tests | [GNU AGPL-3.0](https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/LICENSE) | Anyone who runs a modified version, including as a website, must publish their source |
| Starter recipes: `recipes/` | [MIT](https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/recipes/LICENSE) | Copy them freely into your own projects |

**Before your first pull request can be merged, you sign the [Contributor License Agreement](https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/CLA.md) (CLA).** A bot comments on your pull request with a link; signing takes one click with your GitHub account and covers all your future contributions.

In short, the CLA says that:

* you keep the copyright in your work;
* the work is yours to give;
* you have checked anything you made with AI help;
* the maintainer may edit and relicense it as part of the project, and promises to keep it publicly available under the license it was contributed under.

Please read the full text before signing. It is short. You are credited in the project's history for every accepted contribution.
