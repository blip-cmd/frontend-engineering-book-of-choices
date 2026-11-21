"""
Target Sources Ingestion and Library Scaffold Generator
Reads target_sources.json and ensures structured audit stubs exist in library/
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = REPO_ROOT / "pipelines" / "config" / "target_sources.json"
LIBRARY_DIR = REPO_ROOT / "library"

def generate_methodology_stub(method):
    filename = f"{method['id']}.md"
    target_path = LIBRARY_DIR / "methodologies" / filename
    if target_path.exists():
        print(f"Skipping existing: {target_path.name}")
        return

    content = f"""# Architectural Methodology: {method['name']}

* **Identifier:** `{method['id']}`
* **Pioneers / Organizations:** {', '.join(method.get('pioneers', []))}
* **Core Mechanisms:** {', '.join(method.get('topics', []))}

---

## 1. Mechanics and Mental Model
<!-- Detail how this pattern works from network request to DOM mutation -->

## 2. Comparative Trade-offs
* **What you gain:**
* **What you forfeit:**

## 3. Decision Bounds
* **When to choose this:**
* **When to avoid this:**

## 4. Enabling Ecosystem & Tooling
<!-- List existing libraries, frameworks, and tools implementing this pattern -->
"""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    print(f"Created methodology stub: {target_path.name}")

def main():
    if not CONFIG_FILE.exists():
        print(f"Configuration file not found: {CONFIG_FILE}")
        return

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Published books are not summarised here (copyright). They are listed with
    # short original commentary in library/reading_list.md instead.

    for method in data.get("architectural_methodologies", []):
        generate_methodology_stub(method)

    print("Ingestion scaffolding complete.")

if __name__ == "__main__":
    main()
