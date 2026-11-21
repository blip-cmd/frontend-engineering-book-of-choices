"""
Automated Test Suite for Publishing & Compilation Pipelines
Verifies Typst e-book compilation, EPUB3 packaging, and zero em-dash validation.
"""

from pathlib import Path
import unittest
import zipfile

from pipelines.scripts.build_epub_book import build_epub_book
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

if __name__ == "__main__":
    unittest.main()
