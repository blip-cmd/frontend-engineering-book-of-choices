"""
Repository Standards and Quality Linter
Audits all markdown files to guarantee zero em-dash usage, validates internal file links,
and computes repository content metrics.
"""

from pathlib import Path
import re
import sys
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def audit_file(file_path):
    text = file_path.read_text(encoding="utf-8")
    issues = []
    
    # Check for em dash characters: unicode \u2014 or triple hyphen in prose
    # (Note: standalone thematic breaks --- on their own line are valid markdown syntax)
    for line_idx, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if "\u2014" in line:
            issues.append(f"Line {line_idx}: Contains Unicode em-dash (\\u2014)")
        is_table_separator = re.fullmatch(r"\s*\|[\s:\-|]+\|\s*", line) is not None
        if not is_table_separator and re.search(r"[^\s\-]---[^\s\-]", line):
            issues.append(f"Line {line_idx}: Contains triple-dash em-dash in text")

    # Relative links must point at files that exist in the repository
    in_code_block = False
    for line_idx, line in enumerate(text.splitlines(), 1):
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

    # Word count
    words = len(re.findall(r"\b\w+\b", text))
    
    return issues, words

def main():
    print("=" * 70)
    print(" REPOSITORY STANDARDS AUDIT: ZERO EM-DASH & LINK VERIFICATION")
    print("=" * 70)
    
    total_files = 0
    total_words = 0
    all_issues = {}

    for md_file in REPO_ROOT.glob("**/*.md"):
        rel = md_file.relative_to(REPO_ROOT).as_posix()
        if ".git" in md_file.parts or "node_modules" in md_file.parts:
            continue
        # Generated copies of the book for the website (links there are site URLs)
        if rel.startswith(("site/src/content/docs/", "site/dist/")) and not rel.endswith("index.mdx"):
            continue
            
        total_files += 1
        issues, words = audit_file(md_file)
        total_words += words
        
        if issues:
            all_issues[str(md_file.relative_to(REPO_ROOT))] = issues

    print(f"Audited {total_files} markdown files ({total_words:,} total words).")

    if all_issues:
        print("\n[FAILED] Found formatting issues in the following files:")
        for f, errs in all_issues.items():
            print(f"\n  File: {f}")
            for e in errs:
                print(f"    - {e}")
        sys.exit(1)
    else:
        print("[PASSED] Zero em-dash violations detected. All markdown standards verified.")

if __name__ == "__main__":
    main()
