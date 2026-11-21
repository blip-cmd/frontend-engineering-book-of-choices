# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 blip-cmd and contributors
"""
Commit message standard (see docs/WORKFLOW.md).

    <type>(<optional scope>): <imperative summary, at most 72 characters>

    <optional body: why the change was made; link the claim ledger or issue>

Usage:
    python pipelines/scripts/check_commits.py --range origin/main..HEAD   # CI: every commit in a PR
    python pipelines/scripts/check_commits.py --file .git/COMMIT_EDITMSG  # local commit-msg hook
"""

import argparse
import re
import subprocess
import sys

TYPES = {
    "content": "new or expanded book content",
    "review": "a verification pass on a page (claim ledger, status change)",
    "fix": "a correction to content or code",
    "feat": "a new feature in the calculator, CLI or website",
    "docs": "repository documentation (README, standards, guides)",
    "outreach": "promotion drafts and the posting log",
    "ci": "workflows and automation",
    "test": "tests only",
    "refactor": "code restructuring without behaviour change",
    "chore": "maintenance, dependencies, housekeeping",
}
HEADER = re.compile(r"^(?P<type>[a-z]+)(?:\((?P<scope>[a-z0-9][a-z0-9-]*)\))?(?P<breaking>!)?: (?P<summary>\S.*)$")
# AI attribution is disclosed in PR descriptions and page front matter, never in commit trailers.
AI_TRAILER = re.compile(
    r"(?im)^(co-authored-by:.*(claude|anthropic|openai|chatgpt|copilot|gemini|\bgpt\b|noreply@anthropic\.com)"
    r"|.*generated with \[?claude code)"
)
EXEMPT = re.compile(r"^(Merge (pull request|branch|remote-tracking branch) |Revert \")")


def check_message(message):
    """Return a list of problems with one commit message."""
    lines = message.strip("\n").splitlines()
    if not lines:
        return ["empty commit message"]
    header = lines[0]
    if EXEMPT.match(header):
        return []
    problems = []
    m = HEADER.match(header)
    if not m:
        problems.append(f'header must look like "type(scope): summary", got: "{header}"')
    else:
        if m["type"] not in TYPES:
            problems.append(f'unknown type "{m["type"]}"; use one of: {", ".join(TYPES)}')
        summary = m["summary"]
        if summary.endswith("."):
            problems.append("summary must not end with a period")
        if summary[0].isupper() and not summary.split()[0].isupper():
            problems.append("summary should start with a lowercase imperative verb (e.g. 'add', 'fix', 'verify')")
    if len(header) > 72:
        problems.append(f"header is {len(header)} characters; keep it to 72 or fewer")
    if len(lines) > 1 and lines[1].strip():
        problems.append("leave a blank line between the header and the body")
    if AI_TRAILER.search(message):
        problems.append("remove AI attribution trailers (Co-authored-by: Claude/AI, 'Generated with ...'); "
                        "disclose AI use in the pull request instead")
    return problems


def commits_in_range(rev_range):
    out = subprocess.run(["git", "log", "--format=%H%x00%B%x1e", rev_range],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    for record in out.split("\x1e"):
        if record.strip():
            sha, _, body = record.strip("\n").partition("\x00")
            yield sha[:7], body


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--range", help="git revision range, e.g. origin/main..HEAD")
    group.add_argument("--file", help="path to a commit message file (commit-msg hook)")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = "\n".join(l for l in f.read().splitlines() if not l.startswith("#"))
        items = [("message", text)]
    else:
        items = list(commits_in_range(args.range))

    failed = False
    for ref, message in items:
        problems = check_message(message)
        if problems:
            failed = True
            print(f"[{ref}] {message.strip().splitlines()[0] if message.strip() else '(empty)'}")
            for p in problems:
                print(f"    - {p}")
    if failed:
        print("\nCommit message standard: docs/WORKFLOW.md#commits")
        sys.exit(1)
    print(f"[PASSED] {len(items)} commit message(s) follow the standard.")


if __name__ == "__main__":
    main()
