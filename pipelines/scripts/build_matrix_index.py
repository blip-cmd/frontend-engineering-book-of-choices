"""
Automated Matrix and Library Index Compiler
Scans all markdown files in library/ and compiles a master index table and category summary.
"""

from pathlib import Path
import re
import json

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LIBRARY_DIR = REPO_ROOT / "library"
OUTPUT_INDEX_MD = LIBRARY_DIR / "INDEX.md"
OUTPUT_CATALOG_JSON = LIBRARY_DIR / "catalog.json"

def parse_markdown_header(file_path):
    text = file_path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else file_path.stem
    
    category = file_path.parent.name
    
    # Extract identifier
    id_match = re.search(r"\*?\*?Identifier:\*?\*?\s*`?([a-zA-Z0-9_\-]+)`?", text)
    identifier = id_match.group(1).strip() if id_match else file_path.stem
    
    # Extract topics/status/author
    author_match = re.search(r"\*?\*?Author:\*?\*?\s*([^\n\r]+)", text)
    author = author_match.group(1).strip() if author_match else "N/A"
    
    return {
        "title": title,
        "identifier": identifier,
        "category": category,
        "author": author,
        "relative_path": str(file_path.relative_to(REPO_ROOT)).replace("\\", "/")
    }

def main():
    items = []
    for md_file in LIBRARY_DIR.glob("**/*.md"):
        if md_file.name in ["INDEX.md", "README.md", "reading_list.md"]:
            continue
        item = parse_markdown_header(md_file)
        items.append(item)
        
    items.sort(key=lambda x: (x["category"], x["title"]))
    
    # Generate INDEX.md
    lines = [
        "# Research Notes: Index",
        "",
        "> Automatically generated index of the research notes behind the book. Published books are listed separately in [reading_list.md](reading_list.md).",
        "",
        "| Category | Title | Identifier | Author / Source | File Path |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for it in items:
        rel_from_library = it['relative_path'].removeprefix("library/")
        link_str = f"[{it['title']}]({rel_from_library})"
        lines.append(f"| `{it['category']}` | {link_str} | `{it['identifier']}` | {it['author']} | `{it['relative_path']}` |")
        
    lines.append("")
    lines.append(f"*Total entries: {len(items)}*")
    
    OUTPUT_INDEX_MD.write_text("\n".join(lines), encoding="utf-8")
    OUTPUT_CATALOG_JSON.write_text(json.dumps(items, indent=2), encoding="utf-8")
    print(f"Compiled {len(items)} library records into INDEX.md and catalog.json")

if __name__ == "__main__":
    main()
