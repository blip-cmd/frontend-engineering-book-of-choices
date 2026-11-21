# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 blip-cmd and contributors
"""
Automated Test Suite for Frontend Engineering Choice Engine and Pipelines
Verifies recommendation matrix logic, schema validation, catalog compilation,
recipe scaffolding, and Architectural Decision Record (ADR) generation.
"""

import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

from pipelines.cli.choice_engine import (
    ARCHETYPE_RECIPES,
    evaluate_architecture,
    generate_adr,
    list_archetypes,
    scaffold_recipe
)
from pipelines.scripts.build_matrix_index import parse_markdown_header

REPO_ROOT = Path(__file__).resolve().parent.parent

class TestChoiceEngine(unittest.TestCase):
    def test_content_first_profile(self):
        profile = {
            "seo": "critical",
            "traffic": "mostly_static",
            "update_frequency": "standard",
            "state_origin": "remote_api",
            "complexity": "standard",
            "team_size": "standard",
            "monorepo_ts": False,
            "brand_uniqueness": "custom_brand"
        }
        rec = evaluate_architecture(profile)
        self.assertIn("Islands Architecture", rec["execution"])
        self.assertIn("book/01_where_code_runs.md", rec["execution_chapter"])
        self.assertIn("Tailwind CSS", rec["ui"])
        self.assertEqual(rec["suggested_recipe"], "content_first_astro")

    def test_b2b_saas_profile(self):
        profile = {
            "seo": "irrelevant",
            "traffic": "dynamic",
            "update_frequency": "standard",
            "state_origin": "remote_api",
            "complexity": "standard",
            "team_size": "standard",
            "monorepo_ts": True,
            "brand_uniqueness": "custom_brand"
        }
        rec = evaluate_architecture(profile)
        self.assertIn("Client-Side SPA", rec["execution"])
        self.assertIn("TanStack Query", rec["state"])
        self.assertIn("tRPC", rec["api"])
        self.assertEqual(rec["suggested_recipe"], "enterprise_b2b_saas")

    def test_realtime_telemetry_profile(self):
        profile = {
            "seo": "irrelevant",
            "traffic": "dynamic",
            "update_frequency": "high_telemetry",
            "state_origin": "remote_api",
            "complexity": "standard",
            "team_size": "standard",
            "monorepo_ts": False,
            "brand_uniqueness": "standard_admin"
        }
        rec = evaluate_architecture(profile)
        self.assertIn("Fine-Grained Signals", rec["reactivity"])
        self.assertIn("book/02_the_reactivity_dilemma.md", rec["reactivity_chapter"])
        self.assertEqual(rec["suggested_recipe"], "realtime_dashboard")

    def test_local_first_profile(self):
        profile = {
            "seo": "irrelevant",
            "traffic": "dynamic",
            "update_frequency": "standard",
            "state_origin": "local_first",
            "complexity": "local_first",
            "team_size": "standard",
            "monorepo_ts": True,
            "brand_uniqueness": "custom_brand"
        }
        rec = evaluate_architecture(profile)
        self.assertIn("Local-First", rec["execution"])
        self.assertIn("book/08_local_first_and_offline_resilience.md", rec["execution_chapter"])
        self.assertIn("CRDTs", rec["state"])
        self.assertEqual(rec["suggested_recipe"], "collaborative_canvas")

    def test_ecommerce_profile(self):
        profile = {
            "seo": "critical",
            "traffic": "dynamic",
            "update_frequency": "standard",
            "state_origin": "remote_api",
            "complexity": "standard",
            "team_size": "standard",
            "monorepo_ts": False,
            "brand_uniqueness": "custom_brand"
        }
        rec = evaluate_architecture(profile)
        self.assertIn("Streaming SSR", rec["execution"])
        self.assertEqual(rec["suggested_recipe"], "low_latency_ecommerce")

    def test_adr_generation(self):
        profile = {
            "seo": "critical",
            "traffic": "mostly_static",
            "update_frequency": "standard",
            "state_origin": "remote_api",
            "complexity": "standard",
            "team_size": "standard",
            "monorepo_ts": False,
            "brand_uniqueness": "custom_brand"
        }
        rec = evaluate_architecture(profile)
        adr = generate_adr(profile, rec, "Storefront Portal")
        self.assertIn("# ADR-0001: Frontend Architecture Selection for Storefront Portal", adr)
        self.assertIn("## Status\nAccepted", adr)
        self.assertIn("## Decision", adr)
        self.assertIn("## Consequences", adr)
        self.assertNotIn("—", adr, "ADR must not contain unicode em dash")
        self.assertNotIn("--- ", adr, "ADR must not contain markdown em dash")

    def test_recipe_scaffolding(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            copied = scaffold_recipe("content_first_astro", tmp_dir)
            self.assertIn("package.json", copied)
            self.assertIn("astro.config.mjs", copied)
            self.assertTrue((Path(tmp_dir) / "package.json").exists())
            self.assertTrue((Path(tmp_dir) / "astro.config.mjs").exists())

    def test_list_archetypes(self):
        archetypes = list_archetypes()
        self.assertIn("content_first_astro", archetypes)
        self.assertIn("enterprise_b2b_saas", archetypes)
        self.assertIn("realtime_dashboard", archetypes)
        self.assertIn("collaborative_canvas", archetypes)
        self.assertIn("low_latency_ecommerce", archetypes)
        self.assertIn("shared_configs", archetypes)

class TestLibraryIntegrity(unittest.TestCase):
    def test_catalog_files_exist(self):
        catalog_file = REPO_ROOT / "library" / "catalog.json"
        self.assertTrue(catalog_file.exists(), "catalog.json must exist")
        with open(catalog_file, "r", encoding="utf-8") as f:
            items = json.load(f)
        self.assertGreaterEqual(len(items), 1, "Catalog should list the research notes")
        self.assertTrue((REPO_ROOT / "library" / "reading_list.md").exists(), "Further-reading list must exist")
        for it in items:
            full_path = REPO_ROOT / it["relative_path"]
            self.assertTrue(full_path.exists(), f"Record path {full_path} must exist on disk")

    def test_all_chapters_exist(self):
        expected_chapters = [
            "book/00_the_calculus_of_choices.md",
            "book/01_where_code_runs.md",
            "book/02_the_reactivity_dilemma.md",
            "book/03_state_and_cache_topologies.md",
            "book/04_the_networking_contract.md",
            "book/05_design_engineering_and_ui.md",
            "book/06_styling_and_presentation.md",
            "book/07_delivery_and_build_pipeline.md",
            "book/08_local_first_and_offline_resilience.md",
            "book/09_decision_playbooks/content_first_publishing.md",
            "book/09_decision_playbooks/enterprise_b2b_saas.md",
            "book/09_decision_playbooks/high_frequency_realtime_dashboard.md",
            "book/09_decision_playbooks/collaborative_canvas_workspace.md",
            "book/09_decision_playbooks/low_latency_ecommerce.md",
            "book/10_appendices/architecture_anti_patterns.md",
            "book/10_appendices/core_web_vitals_triage_guide.md",
            "book/10_appendices/frontend_security_checklist.md",
            "book/10_appendices/migration_playbooks.md"
        ]
        for ch in expected_chapters:
            target = REPO_ROOT / ch
            self.assertTrue(target.exists(), f"Expected chapter {ch} must exist")

if __name__ == "__main__":
    unittest.main()
