"""
Schema Validation Script
Validates structured decision item files against pipelines/schemas/decision_item_schema.json
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_FILE = REPO_ROOT / "pipelines" / "schemas" / "decision_item_schema.json"

def validate_schema_structure(data, schema):
    required_fields = schema.get("required", [])
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, "Valid"

def main():
    if not SCHEMA_FILE.exists():
        print(f"Schema not found: {SCHEMA_FILE}")
        return

    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema = json.load(f)

    print(f"Loaded schema: {schema.get('title', 'Schema')}")
    print("Schema is ready for item validation across pipelines.")

if __name__ == "__main__":
    main()
