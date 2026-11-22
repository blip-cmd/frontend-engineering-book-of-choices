# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 blip-cmd and contributors
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
try:
    from pipelines.scripts.content_meta import strip_front_matter
except ImportError:  # run directly as a script
    from content_meta import strip_front_matter

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

def find_pandoc():
    """Pandoc 3.x converts the book's GitHub-flavoured Markdown to Typst with correct escaping."""
    return shutil.which("pandoc")


REPO_URL = "https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/"
RELATIVE_LINK = re.compile(r"\]\((?!https?:|mailto:|#)([^)\s]+)\)")


def absolutize_links(md_content, source_path):
    """Relative links mean nothing inside a PDF: point them at the file on GitHub."""
    def repl(match):
        target, _, anchor = match.group(1).partition("#")
        resolved = (source_path.parent / target).resolve().relative_to(REPO_ROOT).as_posix()
        return f"]({REPO_URL}{resolved}{'#' + anchor if anchor else ''})"
    return RELATIVE_LINK.sub(repl, md_content)


def convert_markdown_to_typst(md_content):
    pandoc = find_pandoc()
    if not pandoc:
        raise RuntimeError("pandoc 3.x is required to build the PDF source (https://pandoc.org/installing.html).")
    result = subprocess.run(
        [pandoc, "--from", "gfm", "--to", "typst", "--wrap=none"],
        input=md_content, capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return result.stdout


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

// Styling for pandoc-generated content
#let horizontalrule = align(center, line(length: 100%, stroke: 0.4pt + rgb("#cbd5e1")))
#show heading.where(level: 1): it => { pagebreak(weak: true); it }
#show link: set text(fill: rgb("#0369a1"))
#set table(
  inset: 5pt,
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#0f172a"), bottom: 0.6pt + rgb("#475569")) } else { (bottom: 0.3pt + rgb("#e2e8f0")) },
)
#show table: set text(size: 8.5pt)
#show table: set par(justify: false)
#show raw.where(block: true): block.with(width: 100%, fill: rgb("#f8fafc"), stroke: 0.5pt + rgb("#cbd5e1"), inset: (x: 10pt, y: 8pt), radius: 4pt)
#show raw: set text(size: 8.5pt)
#show quote.where(block: true): it => block(width: 100%, fill: rgb("#f0f9ff"), stroke: (left: 3pt + rgb("#0284c7")), inset: (x: 12pt, y: 8pt), radius: 2pt, emph(it.body))

// Title Page
#v(3cm)
#align(center)[
  #text(size: 26pt, weight: "bold", fill: rgb("#0f172a"))[
    Frontend Engineering as a Book of Choices
  ]
  #v(0.8cm)
  #text(size: 14pt, fill: rgb("#475569"), hyphenate: false)[
    A Practical Decision Matrix and Architectural Reference for Modern Web Applications
  ]
  #v(1.5cm)
  #text(size: 11pt, weight: "medium", fill: rgb("#1e293b"))[
    blip-cmd
  ]
  #v(0.4cm)
  #text(size: 9.5pt, fill: rgb("#64748b"))[
    Agent-Verified Edition : November 2026
  ]
]

#v(6cm)
#align(center)[
  #text(size: 8pt, fill: rgb("#94a3b8"))[
    Copyright (c) 2026 blip-cmd and contributors. Licensed under CC BY-NC-ND 4.0. \\
    Every page was verified against primary sources by AI agents; see the claim ledgers at \\
    github.com/blip-cmd/frontend-engineering-book-of-choices
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
            content = strip_front_matter(f.read())
        converted = convert_markdown_to_typst(absolutize_links(content, chap_path))
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
