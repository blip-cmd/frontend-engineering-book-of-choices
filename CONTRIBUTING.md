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

* **Cite your sources.** Link claims to official documentation, specifications, or primary sources (benchmarks, RFCs, release notes). Unsourced numbers will be questioned in review.
* **Write in your own words.** Do not paste text from other books, courses, or paid articles. Short quotes with attribution are fine.
* **Show the trade-off.** Every recommendation should say what it costs and when it is the wrong choice.
* **No em dashes.** Use a colon, comma, or parentheses instead. The automated audit (`npm run audit`) checks this.
* **AI tools.** You may use them, but you are responsible for verifying every claim and every line of code you submit.

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

## Licensing of Contributions

* Writing (`book/`, `docs/`, `library/`, and site page text) is licensed under [CC BY-NC-ND 4.0](https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/LICENSE-CONTENT.md).
* Code (the calculator, CLI, recipes, scripts, and site code) is licensed under the [MIT License](https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/LICENSE).

By submitting a contribution, you confirm that you have the right to submit it, and you agree that it is licensed under the license that applies to the files you changed. Because the writing license does not allow modified copies, you also grant the maintainer a perpetual, worldwide, non-exclusive, royalty-free right to edit, adapt, and redistribute your contribution as part of this project. You will be credited in the project's contributor history.
