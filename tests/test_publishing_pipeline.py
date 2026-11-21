# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 blip-cmd and contributors
"""
Automated Test Suite for Publishing & Compilation Pipelines
Verifies Typst e-book compilation, EPUB3 packaging, and zero em-dash validation.
"""

from pathlib import Path
import unittest
from datetime import date
import zipfile

from pipelines.scripts.build_epub_book import build_epub_book
from pipelines.scripts.content_meta import STATUSES, split_front_matter
from pipelines.scripts.audit_repo_standards import audit_content_page
from pipelines.scripts.build_typst_book import (
    CHAPTER_SEQUENCE,
    build_typst_document,
    convert_markdown_to_typst
)

REPO_ROOT = Path(__file__).resolve().parent.parent

class TestPublishingPipeline(unittest.TestCase):
    def test_typst_document_assembly(self):
        out_path = build_typst_document()
        self.assertTrue(out_path.exists(), "Compiled Typst file must exist")

        with open(out_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Verify key chapters are present
        self.assertIn("The Calculus of Choices", content)
        self.assertIn("Where Code Runs", content)
        self.assertIn("The Reactivity Dilemma", content)
        self.assertIn("Content-First Publishing", content)
        self.assertIn("The 15 Deadly Frontend Architectural Anti-Patterns", content)

        # Invariant: Zero em dashes
        self.assertNotIn("—", content, "Compiled Typst must contain zero unicode em dashes")
        self.assertNotIn("--- ", content, "Compiled Typst must contain zero markdown em dashes")

    def test_markdown_to_typst_table_conversion(self):
        sample_md = (
            "| Column A | Column B |\n"
            "| :--- | :--- |\n"
            "| Val 1 | Val 2 |\n"
        )
        converted = convert_markdown_to_typst(sample_md)
        self.assertIn("#table(", converted)
        self.assertIn("table.hline", converted)
        self.assertIn("Val 1", converted)

    def test_epub3_generation(self):
        epub_path = build_epub_book()
        self.assertTrue(epub_path.exists(), "EPUB file must exist")
        self.assertTrue(zipfile.is_zipfile(epub_path), "EPUB must be a valid zip archive")

        with zipfile.ZipFile(epub_path, "r") as zf:
            file_list = zf.namelist()
            self.assertIn("mimetype", file_list)
            self.assertIn("META-INF/container.xml", file_list)
            self.assertIn("OEBPS/content.opf", file_list)
            self.assertIn("OEBPS/nav.xhtml", file_list)
            self.assertIn("OEBPS/style.css", file_list)
            self.assertIn("OEBPS/ch00.xhtml", file_list)

            mimetype_bytes = zf.read("mimetype").decode("utf-8").strip()
            self.assertEqual(mimetype_bytes, "application/epub+zip")

            nav_content = zf.read("OEBPS/nav.xhtml").decode("utf-8")
            self.assertIn("The Calculus of Choices", nav_content)
            self.assertNotIn("—", nav_content)

    def test_github_actions_workflow_exists(self):
        workflow = REPO_ROOT / ".github" / "workflows" / "compile_books.yml"
        self.assertTrue(workflow.exists(), "compile_books.yml workflow must exist")
        with open(workflow, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Compile and Release Book Assets", content)
        self.assertIn("typst-community/setup-typst", content)

class TestContentStandards(unittest.TestCase):
    """Automatable parts of CONTENT_STANDARDS.md."""

    PAGE = (
        "---\nstatus: {status}\nai_involvement: drafted\nlast_verified: {lv}\n"
        "verified_against:\nreview_by: {rb}\nreviewers: {rv}\nledger: {lg}\n---\n\n# Title\n\n{body}\n"
    )

    LEDGER = "CONTENT_STANDARDS.md"  # any existing file stands in for a ledger

    def page(self, status="draft", lv="", rb="", rv="", body="Plain text.", lg=""):
        return self.PAGE.format(status=status, lv=lv, rb=rb, rv=rv, body=body, lg=lg)

    def test_front_matter_parsing(self):
        meta, body = split_front_matter(self.page(status="reviewed", rv="blip-cmd"))
        self.assertEqual(meta["status"], "reviewed")
        self.assertEqual(meta["reviewers"], "blip-cmd")
        self.assertTrue(body.lstrip().startswith("# Title"))
        self.assertEqual(split_front_matter("# No front matter\n"), ({}, "# No front matter\n"))

    def test_every_book_page_has_valid_front_matter(self):
        pages = [p for p in (REPO_ROOT / "book").rglob("*.md") if p.name != "README.md" and "dist" not in p.parts]
        pages += list((REPO_ROOT / "docs" / "essays").glob("*.md"))
        self.assertGreaterEqual(len(pages), 20)
        for p in pages:
            meta, _ = split_front_matter(p.read_text(encoding="utf-8"))
            self.assertIn(meta.get("status"), STATUSES, p.name)

    def test_builders_strip_front_matter(self):
        content = build_typst_document().read_text(encoding="utf-8")
        self.assertNotIn("ai_involvement", content)
        with zipfile.ZipFile(build_epub_book(), "r") as zf:
            self.assertNotIn("ai_involvement", zf.read("OEBPS/ch00.xhtml").decode("utf-8"))

    def test_reviewed_page_requires_human_reviewer_and_dates(self):
        errors, _ = audit_content_page(self.page(status="reviewed"), date(2026, 11, 21))
        self.assertTrue(any("reviewer" in e for e in errors))
        self.assertTrue(any("last_verified" in e for e in errors))
        errors, _ = audit_content_page(self.page(status="reviewed", lv="2026-11", rb="2027-05", rv="blip-cmd", lg=self.LEDGER), date(2026, 11, 21))
        self.assertEqual(errors, [])

    def test_agent_verified_page_needs_ledger_and_no_human_reviewers(self):
        errors, _ = audit_content_page(self.page(status="agent-verified", lv="2026-11", rb="2027-05"), date(2026, 11, 21))
        self.assertTrue(any("ledger" in e for e in errors))
        errors, _ = audit_content_page(self.page(status="agent-verified", lv="2026-11", rb="2027-05", lg="reviews/missing.md"), date(2026, 11, 21))
        self.assertTrue(any("not found" in e for e in errors))
        errors, _ = audit_content_page(self.page(status="agent-verified", lv="2026-11", rb="2027-05", rv="blip-cmd", lg=self.LEDGER), date(2026, 11, 21))
        self.assertTrue(any("humans only" in e for e in errors))
        errors, _ = audit_content_page(self.page(status="agent-verified", lv="2026-11", rb="2027-05", lg=self.LEDGER), date(2026, 11, 21))
        self.assertEqual(errors, [])

    def test_unverified_marker_and_stale_facts_fail(self):
        errors, _ = audit_content_page(self.page(body="<!-- UNVERIFIED: no source -->"), date(2026, 11, 21))
        self.assertTrue(any("UNVERIFIED" in e for e in errors))
        errors, _ = audit_content_page(self.page(body="FID is a Core Web Vital."), date(2026, 11, 21))
        self.assertTrue(any("fid-core-web-vital" in e for e in errors))
        errors, _ = audit_content_page(self.page(body="INP replaced FID in March 2024."), date(2026, 11, 21))
        self.assertEqual(errors, [])

    def test_unsourced_numbers_warn_on_drafts_and_fail_on_reviewed_pages(self):
        body = "Builds are 5x faster."
        errors, warnings = audit_content_page(self.page(body=body), date(2026, 11, 21))
        self.assertEqual(errors, [])
        self.assertTrue(any("G1" in w for w in warnings))
        errors, _ = audit_content_page(self.page(status="reviewed", lv="2026-11", rb="2027-05", rv="blip-cmd", body=body, lg=self.LEDGER), date(2026, 11, 21))
        self.assertTrue(any("G1" in e for e in errors))
        sourced = "Builds are 5x faster ([source](https://example.org/bench))."
        errors, _ = audit_content_page(self.page(status="reviewed", lv="2026-11", rb="2027-05", rv="blip-cmd", body=sourced, lg=self.LEDGER), date(2026, 11, 21))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
