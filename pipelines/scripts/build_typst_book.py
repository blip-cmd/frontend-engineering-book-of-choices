"""
Typst E-Book Assembler and Compilation Pipeline
Compiles all chapters, archetype playbooks, and production appendices
into a single cohesive, publication-grade Typst document (.typ) and PDF.
"""

from pathlib import Path
import re
import shutil
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BOOK_DIR = REPO_ROOT / "book"
DIST_DIR = BOOK_DIR / "dist"

CHAPTER_SEQUENCE = [
    BOOK_DIR / "00_the_calculus_of_choices.md",
    BOOK_DIR / "01_where_code_runs.md",
    BOOK_DIR / "02_the_reactivity_dilemma.md",
    BOOK_DIR / "03_state_and_cache_topologies.md",
    BOOK_DIR / "04_the_networking_contract.md",
    BOOK_DIR / "05_design_engineering_and_ui.md",
    BOOK_DIR / "06_styling_and_presentation.md",
    BOOK_DIR / "07_delivery_and_build_pipeline.md",
    BOOK_DIR / "08_local_first_and_offline_resilience.md",
    BOOK_DIR / "09_decision_playbooks" / "content_first_publishing.md",
    BOOK_DIR / "09_decision_playbooks" / "enterprise_b2b_saas.md",
    BOOK_DIR / "09_decision_playbooks" / "high_frequency_realtime_dashboard.md",
    BOOK_DIR / "09_decision_playbooks" / "collaborative_canvas_workspace.md",
    BOOK_DIR / "09_decision_playbooks" / "low_latency_ecommerce.md",
    BOOK_DIR / "10_appendices" / "architecture_anti_patterns.md",
    BOOK_DIR / "10_appendices" / "core_web_vitals_triage_guide.md",
    BOOK_DIR / "10_appendices" / "frontend_security_checklist.md",
    BOOK_DIR / "10_appendices" / "migration_playbooks.md"
]

def format_table_to_typst(table_lines):
    if len(table_lines) < 2:
        return ""
    
    # Parse header
    headers = [c.strip() for c in table_lines[0].strip().strip('|').split('|')]
    num_cols = len(headers)
    
    # Skip separator row (table_lines[1])
    data_rows = []
    for line in table_lines[2:]:
        if not line.strip() or not line.strip().startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        # Pad or slice to num_cols
        while len(cells) < num_cols:
            cells.append("")
        data_rows.append(cells[:num_cols])
        
    out = []
    out.append(f"#align(center)[")
    out.append(f"#table(")
    out.append(f"  columns: {num_cols},")
    out.append(f"  stroke: none,")
    out.append(f"  fill: (col, row) => if row == 0 {{ rgb(\"#f8fafc\") }} else {{ none }},")
    out.append(f"  table.hline(stroke: 1.2pt + rgb(\"#0f172a\")),")
    
    header_cells = ", ".join(f"[* {h} *]" for h in headers)
    out.append(f"  {header_cells},")
    out.append(f"  table.hline(stroke: 0.6pt + rgb(\"#475569\")),")
    
    for row in data_rows:
        row_cells = ", ".join(f"[{c}]" for c in row)
        out.append(f"  {row_cells},")
        
    out.append(f"  table.hline(stroke: 1.2pt + rgb(\"#0f172a\"))")
    out.append(f")")
    out.append(f"]\n")
    return "\n".join(out)

def convert_markdown_to_typst(md_content):
    lines = md_content.splitlines()
    output_lines = []
    in_code_block = False
    code_lang = ""
    code_buffer = []
    in_table = False
    table_buffer = []

    for line in lines:
        stripped = line.strip()

        # Handle code blocks
        if stripped.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lang = stripped[3:].strip()
                code_buffer = []
            else:
                in_code_block = False
                code_str = "\n".join(code_buffer)
                output_lines.append(f"#block(width: 100%, fill: rgb(\"#f8fafc\"), stroke: 0.5pt + rgb(\"#cbd5e1\"), inset: (x: 10pt, y: 8pt), radius: 4pt)[")
                output_lines.append(f"```{code_lang}\n{code_str}\n```")
                output_lines.append(f"]\n")
            continue

        if in_code_block:
            code_buffer.append(line)
            continue

        # Handle tables
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            table_buffer.append(stripped)
            continue
        elif in_table:
            in_table = False
            output_lines.append(format_table_to_typst(table_buffer))
            table_buffer = []

        # Headings
        if stripped.startswith("# "):
            heading_text = stripped[2:].strip()
            output_lines.append(f"\n#pagebreak()\n= {heading_text}\n")
            continue
        elif stripped.startswith("## "):
            heading_text = stripped[3:].strip()
            output_lines.append(f"\n== {heading_text}\n")
            continue
        elif stripped.startswith("### "):
            heading_text = stripped[4:].strip()
            output_lines.append(f"\n=== {heading_text}\n")
            continue

        # Blockquotes
        if stripped.startswith("> "):
            quote_text = stripped[2:].strip()
            output_lines.append(f"#block(width: 100%, fill: rgb(\"#f0f9ff\"), stroke: (left: 3pt + rgb(\"#0284c7\")), inset: (x: 12pt, y: 8pt), radius: 2pt)[#text(style: \"italic\")[{quote_text}]]\n")
            continue

        # Horizontal rules
        if stripped == "---":
            output_lines.append(f"\n#v(0.6em)#line(length: 100%, stroke: 0.4pt + rgb(\"#cbd5e1\"))#v(0.6em)\n")
            continue

        # Convert basic markdown lists and text formatting
        processed_line = line
        
        # Bold: **text** -> *text*
        processed_line = re.sub(r'\*\*(.+?)\*\*', r'*\1*', processed_line)
        
        # Links: [text](url) -> #link("url")[text]
        processed_line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'#link("\2")[\1]', processed_line)

        output_lines.append(processed_line)

    if in_table and table_buffer:
        output_lines.append(format_table_to_typst(table_buffer))

    return "\n".join(output_lines)

def build_typst_document():
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out_typ_path = DIST_DIR / "frontend_engineering_book_of_choices.typ"

    header = """// Frontend Engineering as a Book of Choices : Publication Master Typst Source
// Generated automatically by pipelines/scripts/build_typst_book.py

#set document(
  title: "Frontend Engineering as a Book of Choices",
  author: "blip-cmd"
)

#set page(
  paper: "a4",
  margin: (x: 2.2cm, top: 2.8cm, bottom: 2.5cm),
  header: context {
    if counter(page).get().first() > 2 [
      #text(size: 8.5pt, fill: rgb("#64748b"), font: "Liberation Sans")[
        #smallcaps[Frontend Engineering as a Book of Choices]
        #h(1fr)
        #counter(page).display("1")
      ]
      #v(-2pt)
      #line(length: 100%, stroke: 0.4pt + rgb("#cbd5e1"))
    ]
  },
  footer: context {
    if counter(page).get().first() > 2 [
      #align(center)[
        #text(size: 7.5pt, fill: rgb("#94a3b8"))[
          Practical Architectural Decision Matrices for Modern Web Engineering
        ]
      ]
    ]
  }
)

#set text(
  font: ("Liberation Serif", "Times New Roman"),
  size: 10pt,
  lang: "en"
)

#set par(justify: true, leading: 0.72em)
#show heading: set text(font: ("Liberation Sans", "Arial"), fill: rgb("#0f172a"))

// Title Page
#v(3cm)
#align(center)[
  #text(size: 26pt, weight: "bold", fill: rgb("#0f172a"))[
    Frontend Engineering as a Book of Choices
  ]
  #v(0.8cm)
  #text(size: 14pt, fill: rgb("#475569"))[
    A Practical Decision Matrix and Architectural Reference for Modern Web Applications
  ]
  #v(1.5cm)
  #text(size: 11pt, weight: "medium", fill: rgb("#1e293b"))[
    blip-cmd
  ]
  #v(0.4cm)
  #text(size: 9.5pt, fill: rgb("#64748b"))[
    Production Edition : Version 1.0.0
  ]
]

#v(6cm)
#align(center)[
  #text(size: 8pt, fill: rgb("#94a3b8"))[
    Copyright (c) 2026 blip-cmd. All rights reserved.
    Published by The Book of Choices Series.
  ]
]

#pagebreak()

// Table of Contents
#outline(
  title: "Table of Contents",
  indent: auto,
  depth: 2
)

#pagebreak()
"""

    typst_body = [header]

    for chap_path in CHAPTER_SEQUENCE:
        if not chap_path.exists():
            print(f"[WARNING] Chapter path not found: {chap_path}", file=sys.stderr)
            continue
        with open(chap_path, "r", encoding="utf-8") as f:
            content = f.read()
        converted = convert_markdown_to_typst(content)
        typst_body.append(converted)

    full_typst = "\n".join(typst_body)

    # Verification of zero em dashes
    if "—" in full_typst:
        raise ValueError("Unicode em dash detected in compiled Typst document.")
    if "--- " in full_typst:
        raise ValueError("Markdown em dash detected in compiled Typst document.")

    with open(out_typ_path, "w", encoding="utf-8") as f:
        f.write(full_typst)

    print(f"[SUCCESS] Typst master document assembled: {out_typ_path}")
    print(f"  Total chapters included: {len(CHAPTER_SEQUENCE)}")
    print(f"  Total source size      : {len(full_typst)} bytes")

    # Attempt compilation if Typst is available
    typst_bin = shutil.which("typst")
    if typst_bin:
        pdf_out = DIST_DIR / "Frontend_Engineering_as_a_Book_of_Choices.pdf"
        print(f"[INFO] Compiling Typst to PDF using {typst_bin}...")
        res = subprocess.run([typst_bin, "compile", str(out_typ_path), str(pdf_out)], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[SUCCESS] PDF compiled successfully: {pdf_out}")
        else:
            print(f"[WARNING] Typst compilation failed:\n{res.stderr}", file=sys.stderr)
    else:
        print("[INFO] Typst executable not found on local PATH. The .typ file is ready for CI compilation via GitHub Actions.")

    return out_typ_path

if __name__ == "__main__":
    build_typst_document()
