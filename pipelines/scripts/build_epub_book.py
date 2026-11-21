"""
Mobile-Optimized EPUB3 Generation Pipeline
Compiles all markdown chapters, playbooks, and appendices into a compliant
EPUB3 digital book package compatible with Apple Books, Kindle, and Calibre.
"""

import html
from pathlib import Path
import re
import sys
import uuid
import zipfile

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BOOK_DIR = REPO_ROOT / "book"
DIST_DIR = BOOK_DIR / "dist"

CHAPTER_SEQUENCE = [
    ("ch00", "Chapter 0: The Calculus of Choices", BOOK_DIR / "00_the_calculus_of_choices.md"),
    ("ch01", "Chapter 1: Where Code Runs", BOOK_DIR / "01_where_code_runs.md"),
    ("ch02", "Chapter 2: The Reactivity Dilemma", BOOK_DIR / "02_the_reactivity_dilemma.md"),
    ("ch03", "Chapter 3: State and Cache Topologies", BOOK_DIR / "03_state_and_cache_topologies.md"),
    ("ch04", "Chapter 4: The Networking Contract", BOOK_DIR / "04_the_networking_contract.md"),
    ("ch05", "Chapter 5: Design Engineering and UI Architecture", BOOK_DIR / "05_design_engineering_and_ui.md"),
    ("ch06", "Chapter 6: Styling and Presentation", BOOK_DIR / "06_styling_and_presentation.md"),
    ("ch07", "Chapter 7: Delivery and Build Pipeline", BOOK_DIR / "07_delivery_and_build_pipeline.md"),
    ("ch08", "Chapter 8: Local-First and Offline Resilience", BOOK_DIR / "08_local_first_and_offline_resilience.md"),
    ("play01", "Playbook 1: Content-First Publishing", BOOK_DIR / "09_decision_playbooks" / "content_first_publishing.md"),
    ("play02", "Playbook 2: Enterprise B2B SaaS", BOOK_DIR / "09_decision_playbooks" / "enterprise_b2b_saas.md"),
    ("play03", "Playbook 3: Real-Time Telemetry Dashboards", BOOK_DIR / "09_decision_playbooks" / "high_frequency_realtime_dashboard.md"),
    ("play04", "Playbook 4: Collaborative Canvas Workspaces", BOOK_DIR / "09_decision_playbooks" / "collaborative_canvas_workspace.md"),
    ("play05", "Playbook 5: Low-Latency E-Commerce", BOOK_DIR / "09_decision_playbooks" / "low_latency_ecommerce.md"),
    ("appA", "Appendix A: Architectural Anti-Patterns", BOOK_DIR / "10_appendices" / "architecture_anti_patterns.md"),
    ("appB", "Appendix B: Core Web Vitals Triage", BOOK_DIR / "10_appendices" / "core_web_vitals_triage_guide.md"),
    ("appC", "Appendix C: Frontend Security Checklist", BOOK_DIR / "10_appendices" / "frontend_security_checklist.md"),
    ("appD", "Appendix D: Zero-Downtime Migration Playbooks", BOOK_DIR / "10_appendices" / "migration_playbooks.md")
]

CSS_STYLES = """
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, serif;
  line-height: 1.6;
  color: #1e293b;
  margin: 0;
  padding: 1.5rem;
}
h1 {
  font-size: 1.8rem;
  color: #0f172a;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0.5rem;
  margin-top: 1.5rem;
}
h2 {
  font-size: 1.4rem;
  color: #1e293b;
  margin-top: 1.5rem;
}
h3 {
  font-size: 1.15rem;
  color: #334155;
  margin-top: 1.25rem;
}
p {
  margin: 0.8rem 0;
  text-align: justify;
}
blockquote {
  border-left: 4px solid #0284c7;
  background-color: #f0f9ff;
  margin: 1rem 0;
  padding: 0.75rem 1rem;
  font-style: italic;
  color: #0369a1;
}
pre {
  background-color: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  padding: 0.75rem 1rem;
  overflow-x: auto;
  font-size: 0.85rem;
  font-family: ui-monospace, Menlo, Monaco, Consolas, monospace;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.25rem 0;
  font-size: 0.9rem;
}
th {
  background-color: #f8fafc;
  border-top: 2px solid #0f172a;
  border-bottom: 1px solid #475569;
  padding: 0.5rem 0.75rem;
  text-align: left;
  font-weight: 600;
}
td {
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}
tr:last-child td {
  border-bottom: 2px solid #0f172a;
}
code {
  font-family: ui-monospace, Menlo, Monaco, Consolas, monospace;
  font-size: 0.88em;
  background-color: #f1f5f9;
  padding: 0.15rem 0.3rem;
  border-radius: 3px;
}
hr {
  border: none;
  border-top: 1px solid #cbd5e1;
  margin: 1.5rem 0;
}
"""

def md_table_to_html(table_lines):
    if len(table_lines) < 2:
        return ""
    headers = [c.strip() for c in table_lines[0].strip().strip('|').split('|')]
    rows = []
    for line in table_lines[2:]:
        if not line.strip() or not line.strip().startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        while len(cells) < len(headers):
            cells.append("")
        rows.append(cells[:len(headers)])

    out = ["<table>", "<thead>", "<tr>"]
    for h in headers:
        out.append(f"<th>{html.escape(h)}</th>")
    out.append("</tr>")
    out.append("</thead>")
    out.append("<tbody>")
    for r in rows:
        out.append("<tr>")
        for cell in r:
            out.append(f"<td>{html.escape(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody>")
    out.append("</table>")
    return "\n".join(out)

def md_to_xhtml(md_text, title):
    lines = md_text.splitlines()
    body_parts = []
    in_code = False
    code_lang = ""
    code_lines = []
    in_table = False
    table_lines = []
    in_list = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                code_lang = stripped[3:].strip()
                code_lines = []
            else:
                in_code = False
                escaped_code = html.escape("\n".join(code_lines))
                body_parts.append(f'<pre><code class="language-{html.escape(code_lang)}">{escaped_code}</code></pre>')
            continue

        if in_code:
            code_lines.append(line)
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            in_table = False
            body_parts.append(md_table_to_html(table_lines))
            table_lines = []

        if in_list and not (stripped.startswith("* ") or stripped.startswith("- ") or re.match(r'^\d+\.\s', stripped)):
            in_list = False
            body_parts.append("</ul>")

        if stripped.startswith("# "):
            body_parts.append(f"<h1>{html.escape(stripped[2:])}</h1>")
            continue
        elif stripped.startswith("## "):
            body_parts.append(f"<h2>{html.escape(stripped[3:])}</h2>")
            continue
        elif stripped.startswith("### "):
            body_parts.append(f"<h3>{html.escape(stripped[4:])}</h3>")
            continue
        elif stripped.startswith("> "):
            body_parts.append(f"<blockquote><p>{html.escape(stripped[2:])}</p></blockquote>")
            continue
        elif stripped == "---":
            body_parts.append("<hr />")
            continue
        elif stripped.startswith("* ") or stripped.startswith("- "):
            if not in_list:
                in_list = True
                body_parts.append("<ul>")
            body_parts.append(f"<li>{html.escape(stripped[2:])}</li>")
            continue
        elif re.match(r'^\d+\.\s', stripped):
            item_text = re.sub(r'^\d+\.\s', '', stripped)
            if not in_list:
                in_list = True
                body_parts.append("<ol>")
            body_parts.append(f"<li>{html.escape(item_text)}</li>")
            continue

        if stripped:
            # Inline replacements
            p_text = html.escape(stripped)
            # Bold
            p_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p_text)
            # Inline code
            p_text = re.sub(r'`(.+?)`', r'<code>\1</code>', p_text)
            body_parts.append(f"<p>{p_text}</p>")

    if in_table and table_lines:
        body_parts.append(md_table_to_html(table_lines))
    if in_list:
        body_parts.append("</ul>")

    body_html = "\n".join(body_parts)

    xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
{body_html}
</body>
</html>
"""
    return xhtml

def build_epub_book():
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out_epub_path = DIST_DIR / "Frontend_Engineering_as_a_Book_of_Choices.epub"
    book_uuid = str(uuid.uuid4())

    with zipfile.ZipFile(out_epub_path, "w") as zf:
        # 1. Mimetype must be first and uncompressed
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)

        # 2. META-INF/container.xml
        container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""
        zf.writestr("META-INF/container.xml", container_xml, compress_type=zipfile.ZIP_DEFLATED)

        # 3. Stylesheet
        zf.writestr("OEBPS/style.css", CSS_STYLES.strip(), compress_type=zipfile.ZIP_DEFLATED)

        # 4. Chapters
        manifest_items = [
            '<item id="style" href="style.css" media-type="text/css"/>',
            '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
        ]
        spine_items = []
        nav_points = []

        for cid, ctitle, cpath in CHAPTER_SEQUENCE:
            if not cpath.exists():
                print(f"[WARNING] Chapter file not found: {cpath}", file=sys.stderr)
                continue
            with open(cpath, "r", encoding="utf-8") as f:
                md_content = f.read()

            xhtml_content = md_to_xhtml(md_content, ctitle)
            # Verify zero em dashes
            if "—" in xhtml_content:
                raise ValueError(f"Unicode em dash detected in EPUB chapter {cid}")

            filename = f"{cid}.xhtml"
            zf.writestr(f"OEBPS/{filename}", xhtml_content, compress_type=zipfile.ZIP_DEFLATED)

            manifest_items.append(f'<item id="{cid}" href="{filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{cid}"/>')
            nav_points.append(f'<li><a href="{filename}">{html.escape(ctitle)}</a></li>')

        # 5. OEBPS/nav.xhtml
        nav_xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Table of Contents</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Table of Contents</h1>
    <ol>
      {"".join(nav_points)}
    </ol>
  </nav>
</body>
</html>
"""
        zf.writestr("OEBPS/nav.xhtml", nav_xhtml, compress_type=zipfile.ZIP_DEFLATED)

        # 6. OEBPS/content.opf
        content_opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">urn:uuid:{book_uuid}</dc:identifier>
    <dc:title>Frontend Engineering as a Book of Choices</dc:title>
    <dc:creator>blip-cmd</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>The Book of Choices Series</dc:publisher>
    <meta property="dcterms:modified">2026-11-21T18:00:00Z</meta>
  </metadata>
  <manifest>
    {"".join(manifest_items)}
  </manifest>
  <spine>
    {"".join(spine_items)}
  </spine>
</package>
"""
        zf.writestr("OEBPS/content.opf", content_opf, compress_type=zipfile.ZIP_DEFLATED)

    print(f"[SUCCESS] Compliant EPUB3 digital book assembled: {out_epub_path}")
    print(f"  Total chapters packaged : {len(CHAPTER_SEQUENCE)}")
    print(f"  Distribution package size: {out_epub_path.stat().st_size} bytes")
    return out_epub_path

if __name__ == "__main__":
    build_epub_book()
