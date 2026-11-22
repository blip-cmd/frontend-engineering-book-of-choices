# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 blip-cmd and contributors
"""
Frontend Engineering Choice Engine CLI
An interactive architectural decision engine mapping project constraints
directly to recommended rendering models, reactivity engines, state managers,
scaffolding recipes, and standardized Architectural Decision Records (ADR).
"""

import argparse
import datetime
import json
import os
from pathlib import Path
import shutil
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RECIPES_DIR = REPO_ROOT / "recipes"

ARCHETYPE_RECIPES = {
    "content_first_astro": {
        "title": "Content Publishing and Documentation",
        "stack": "Astro 7 + Preact 11 islands + Tailwind 4",
        "recipe_dir": "content_first_astro",
        "playbook": "book/09_decision_playbooks/content_first_publishing.md"
    },
    "enterprise_b2b_saas": {
        "title": "B2B SaaS, Admin Portals, Data Grids",
        "stack": "Vite 8 + React 19 + TanStack Query 5 / Table 9 + Zod 4 + Tailwind 4",
        "recipe_dir": "enterprise_b2b_saas",
        "playbook": "book/09_decision_playbooks/enterprise_b2b_saas.md"
    },
    "realtime_dashboard": {
        "title": "Real-Time Telemetry and Financial Consoles",
        "stack": "Vite 8 + Solid 2 signals + uPlot + Web Worker",
        "recipe_dir": "realtime_dashboard",
        "playbook": "book/09_decision_playbooks/high_frequency_realtime_dashboard.md"
    },
    "collaborative_canvas": {
        "title": "Collaborative Canvas and Document Workspaces",
        "stack": "Vite 8 + React 19 + Yjs 13 (CRDT) + IndexedDB, optional y-websocket sync",
        "recipe_dir": "collaborative_canvas",
        "playbook": "book/09_decision_playbooks/collaborative_canvas_workspace.md"
    },
    "low_latency_ecommerce": {
        "title": "Low-Latency Global E-Commerce Storefronts",
        "stack": "Next.js 16 on Node.js + ISR revalidation + useOptimistic cart + Tailwind 4",
        "recipe_dir": "low_latency_ecommerce",
        "playbook": "book/09_decision_playbooks/low_latency_ecommerce.md"
    },
    "shared_configs": {
        "title": "Base Monorepo Configurations",
        "stack": "Shared tsconfig.base.json and Tailwind 4 design tokens (tokens.css)",
        "recipe_dir": "shared_configs",
        "playbook": "book/05_design_engineering_and_ui.md"
    }
}

def prompt_choice(question, options):
    print(f"\n{question}")
    for idx, (label, desc) in enumerate(options, 1):
        print(f"  [{idx}] {label} : {desc}")
    while True:
        try:
            choice = input("\nSelect an option (number): ").strip()
            val = int(choice)
            if 1 <= val <= len(options):
                return val
        except (ValueError, KeyboardInterrupt):
            pass
        print("Invalid selection. Please enter a valid number.")

def evaluate_architecture(profile):
    recommendation = {}
    
    # Execution Boundary
    if profile.get("seo") == "critical":
        if profile.get("traffic") == "mostly_static":
            recommendation["execution"] = "Islands Architecture (Astro) or SSG"
            recommendation["execution_chapter"] = "book/01_where_code_runs.md"
            recommendation["suggested_recipe"] = "content_first_astro"
        else:
            recommendation["execution"] = "Streaming SSR / React Server Components (Next.js or Remix)"
            recommendation["execution_chapter"] = "book/01_where_code_runs.md"
            recommendation["suggested_recipe"] = "low_latency_ecommerce"
    else:
        if profile.get("complexity") == "local_first":
            recommendation["execution"] = "Local-First Desktop PWA (Vite + Wasm / OPFS)"
            recommendation["execution_chapter"] = "book/08_local_first_and_offline_resilience.md"
            recommendation["suggested_recipe"] = "collaborative_canvas"
        else:
            recommendation["execution"] = "Client-Side SPA (Vite + React / Solid)"
            recommendation["execution_chapter"] = "book/01_where_code_runs.md"
            if profile.get("update_frequency") == "high_telemetry":
                recommendation["suggested_recipe"] = "realtime_dashboard"
            else:
                recommendation["suggested_recipe"] = "enterprise_b2b_saas"

    # Reactivity Engine
    if profile.get("update_frequency") == "high_telemetry":
        recommendation["reactivity"] = "Fine-Grained Signals (Solid 2, Svelte 5 runes, or Preact with signals in JSX)"
        recommendation["reactivity_chapter"] = "book/02_the_reactivity_dilemma.md"
    elif profile.get("team_size") == "solo_founder":
        recommendation["reactivity"] = "Compile-Time AST (Svelte 5 Runes) or React"
        recommendation["reactivity_chapter"] = "book/02_the_reactivity_dilemma.md"
    else:
        recommendation["reactivity"] = "Virtual DOM (React 19) or Signals (Angular/Vue 3)"
        recommendation["reactivity_chapter"] = "book/02_the_reactivity_dilemma.md"

    # State & Cache Topology
    if profile.get("complexity") == "local_first" or profile.get("state_origin") == "local_first":
        recommendation["state"] = "Local Embedded DB (PGlite / SQLite Wasm over OPFS) + CRDTs (Yjs)"
        recommendation["state_chapter"] = "book/08_local_first_and_offline_resilience.md"
    elif profile.get("state_origin") == "remote_api":
        recommendation["state"] = "Server Cache (TanStack Query) + URL State (nuqs)"
        recommendation["state_chapter"] = "book/03_state_and_cache_topologies.md"
    else:
        recommendation["state"] = "Lightweight Client Store (Zustand) + Local Component State"
        recommendation["state_chapter"] = "book/03_state_and_cache_topologies.md"

    # API Contract
    if profile.get("monorepo_ts"):
        recommendation["api"] = "tRPC (Zero code-gen, instant TypeScript inference)"
        recommendation["api_chapter"] = "book/04_the_networking_contract.md"
    else:
        recommendation["api"] = "REST with OpenAPI code generation (Orval) or GraphQL"
        recommendation["api_chapter"] = "book/04_the_networking_contract.md"

    # Styling & Design Engineering
    if profile.get("brand_uniqueness") == "custom_brand":
        recommendation["ui"] = "Headless Primitives (shadcn/ui on Base UI or Radix) + Tailwind 4"
        recommendation["ui_chapter"] = "book/05_design_engineering_and_ui.md"
    else:
        recommendation["ui"] = "Complete UI Component Suite (MUI, Ant Design, Mantine)"
        recommendation["ui_chapter"] = "book/05_design_engineering_and_ui.md"

    return recommendation

def generate_adr(profile, recommendation, project_name="Web Application"):
    today = datetime.date.today().isoformat()
    lines = [
        f"# ADR-0001: Frontend Architecture Selection for {project_name}",
        "",
        "## Status",
        "Accepted",
        "",
        "## Date",
        today,
        "",
        "## Context and Problem Statement",
        "Selecting the core frontend architecture requires balancing discoverability, latency budgets, update frequencies, team skillset, and brand requirements. The project constraint profile was evaluated against the decision matrices in Frontend Engineering as a Book of Choices.",
        "",
        "### Project Constraint Profile",
        f"* SEO Requirement: {profile.get('seo', 'standard')}",
        f"* Traffic and Content Nature: {profile.get('traffic', 'standard')}",
        f"* UI Update Frequency: {profile.get('update_frequency', 'standard')}",
        f"* Data Ownership Model: {profile.get('state_origin', 'remote_api')}",
        f"* Monorepo Full-Stack TypeScript: {'Yes' if profile.get('monorepo_ts') else 'No'}",
        f"* Brand Differentiation: {profile.get('brand_uniqueness', 'custom_brand')}",
        "",
        "## Decision",
        "The following architectural foundation was determined based on evaluated constraints:",
        "",
        f"1. **Execution Boundary**: {recommendation.get('execution')}",
        f"   * Reference: `{recommendation.get('execution_chapter')}`",
        f"2. **Reactivity Engine**: {recommendation.get('reactivity')}",
        f"   * Reference: `{recommendation.get('reactivity_chapter')}`",
        f"3. **State and Cache Topology**: {recommendation.get('state')}",
        f"   * Reference: `{recommendation.get('state_chapter')}`",
        f"4. **API Contract Layer**: {recommendation.get('api')}",
        f"   * Reference: `{recommendation.get('api_chapter')}`",
        f"5. **UI Component and Styling Strategy**: {recommendation.get('ui')}",
        f"   * Reference: `{recommendation.get('ui_chapter')}`",
        "",
        "## Consequences",
        "### Positive",
        "* Architecture directly aligns with the primary latency and discoverability requirements.",
        "* Minimizes unnecessary runtime abstraction layers and prevents architectural drift.",
        "* References concrete implementation playbooks and hardening checklists.",
        "",
        "### Negative and Trade-offs",
        "* Requires team adherence to the chosen execution boundaries and state ownership contracts.",
        "* Cross-boundary data passing must adhere strictly to the defined contract validation.",
        "",
        "## References",
        "* Book of Choices Catalog: `library/INDEX.md`",
        f"* Suggested Starter Recipe: `recipes/{recommendation.get('suggested_recipe')}/`",
        "* Playbooks and Hardening Guides: `book/09_decision_playbooks/` and `book/10_appendices/`"
    ]
    return "\n".join(lines)

def list_archetypes():
    return ARCHETYPE_RECIPES

def scaffold_recipe(archetype_key, target_dir):
    if archetype_key not in ARCHETYPE_RECIPES:
        raise ValueError(f"Unknown archetype '{archetype_key}'. Available: {', '.join(ARCHETYPE_RECIPES.keys())}")
    
    src = RECIPES_DIR / ARCHETYPE_RECIPES[archetype_key]["recipe_dir"]
    if not src.exists():
        raise FileNotFoundError(f"Recipe directory does not exist: {src}")
    
    dest = Path(target_dir).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    
    copied_files = []
    for item in src.iterdir():
        if item.is_file():
            shutil.copy2(item, dest / item.name)
            copied_files.append(item.name)
        elif item.is_dir():
            shutil.copytree(item, dest / item.name, dirs_exist_ok=True)
            copied_files.append(f"{item.name}/")
            
    return copied_files

def main():
    parser = argparse.ArgumentParser(description="Frontend Engineering Choice Engine CLI")
    parser.add_argument("--list", action="store_true", help="List all available starter recipes and archetypes")
    parser.add_argument("--init", type=str, metavar="ARCHETYPE", help="Scaffold a recipe into the target directory")
    parser.add_argument("--target", type=str, default=".", help="Target directory for scaffolding (default: current directory)")
    parser.add_argument("--export-adr", action="store_true", help="Export an Architectural Decision Record in Markdown")
    parser.add_argument("--output", type=str, help="Output file path for ADR export")
    parser.add_argument("--project-name", type=str, default="Web Application", help="Project name for ADR header")
    parser.add_argument("--json", action="store_true", help="Output recommendation in JSON format")
    
    # Non-interactive evaluation flags
    parser.add_argument("--seo", choices=["critical", "moderate", "irrelevant"], help="SEO requirement")
    parser.add_argument("--traffic", choices=["mostly_static", "dynamic"], help="Traffic nature")
    parser.add_argument("--update-frequency", choices=["standard", "high_telemetry"], help="Update frequency")
    parser.add_argument("--data", choices=["remote_api", "local_first"], help="Data ownership model")
    parser.add_argument("--monorepo-ts", action="store_true", default=None, help="Full-stack TypeScript monorepo")
    parser.add_argument("--brand", choices=["custom_brand", "standard_admin"], help="Brand differentiation")

    args = parser.parse_args()

    if args.list:
        print("\nAvailable Starter Architecture Recipes:")
        print("=" * 70)
        for key, meta in ARCHETYPE_RECIPES.items():
            print(f"* {key:22} : {meta['title']}")
            print(f"  Stack                  : {meta['stack']}")
            print(f"  Playbook Reference     : {meta['playbook']}")
        print("=" * 70)
        return

    if args.init:
        try:
            files = scaffold_recipe(args.init, args.target)
            print(f"\n[SUCCESS] Scaffolding recipe '{args.init}' into: {Path(args.target).resolve()}")
            for f in files:
                print(f"  + {f}")
            print("\nInitialization complete. Install dependencies and start development.\n")
        except Exception as e:
            print(f"[ERROR] Scaffolding failed: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Check if flags provided for non-interactive evaluation
    has_flags = any([args.seo, args.traffic, args.update_frequency, args.data, args.brand])
    
    if has_flags:
        profile = {
            "seo": args.seo or "moderate",
            "traffic": args.traffic or "dynamic",
            "update_frequency": args.update_frequency or "standard",
            "state_origin": args.data or "remote_api",
            "complexity": "local_first" if args.data == "local_first" else "standard",
            "team_size": "standard",
            "monorepo_ts": True if args.monorepo_ts else False,
            "brand_uniqueness": args.brand or "custom_brand"
        }
    else:
        print("=" * 70)
        print(" FRONTEND ENGINEERING AS A BOOK OF CHOICES : DECISION ENGINE")
        print(" Answer the following 6 questions to generate your optimal architecture.")
        print("=" * 70)

        seo_choice = prompt_choice("1. What is your SEO and Public Discoverability requirement?", [
            ("Critical", "Every page must be indexed by search engines with high Core Web Vitals"),
            ("Moderate", "Some marketing pages matter, but authenticated user dashboard dominates"),
            ("Irrelevant", "Internal enterprise software, authenticated B2B portal, or desktop utility")
        ])
        seo_map = {1: "critical", 2: "moderate", 3: "irrelevant"}

        traffic_choice = prompt_choice("2. What is the nature of your content and traffic?", [
            ("Mostly Static Content", "Articles, documentation, marketing copy, product descriptions"),
            ("Highly Dynamic Personalized", "Personalized social feeds, order status, real-time banking")
        ])
        traffic_map = {1: "mostly_static", 2: "dynamic"}

        freq_choice = prompt_choice("3. What is the update frequency of your user interface?", [
            ("Standard User Interaction", "Form inputs, button clicks, page transitions, modal dialogs"),
            ("High-Frequency Streaming", "50-200 updates/second: financial tickers, telemetry, canvas")
        ])
        freq_map = {1: "standard", 2: "high_telemetry"}

        data_choice = prompt_choice("4. What is the primary data ownership model?", [
            ("Remote Database / API", "Data lives in cloud databases; browser fetches snapshots via HTTP"),
            ("Local-First & Offline", "Data lives locally on user disk with background peer/cloud sync")
        ])
        data_map = {1: "remote_api", 2: "local_first"}

        mono_choice = prompt_choice("5. Is your entire stack TypeScript in a single monorepo?", [
            ("Yes", "Full-stack TypeScript in pnpm or Turborepo monorepo"),
            ("No", "Polyglot backend (Go, Python, Java) or separate frontend repo")
        ])
        mono_map = {1: True, 2: False}

        brand_choice = prompt_choice("6. What is the requirement for visual brand differentiation?", [
            ("Custom Unique Brand", "Distinctive design, custom tokens, bespoke micro-interactions"),
            ("Utility Over Brand", "Standard internal admin tool where delivery speed is priority")
        ])
        brand_map = {1: "custom_brand", 2: "standard_admin"}

        profile = {
            "seo": seo_map[seo_choice],
            "traffic": traffic_map[traffic_choice],
            "update_frequency": freq_map[freq_choice],
            "state_origin": data_map[data_choice],
            "complexity": "local_first" if data_choice == 2 else "standard",
            "team_size": "standard",
            "monorepo_ts": mono_map[mono_choice],
            "brand_uniqueness": brand_map[brand_choice]
        }

    rec = evaluate_architecture(profile)

    if args.json:
        print(json.dumps({"profile": profile, "recommendation": rec}, indent=2))
        return

    if args.export_adr:
        adr_content = generate_adr(profile, rec, args.project_name)
        if args.output:
            out_path = Path(args.output).resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(adr_content)
            print(f"[SUCCESS] Architectural Decision Record written to: {out_path}")
        else:
            print("\n" + adr_content)
        return

    print("\n" + "=" * 70)
    print(" RECOMMENDED ARCHITECTURAL MATRIX PROFILE")
    print("=" * 70)
    print(f"* Execution Boundary  : {rec['execution']}")
    print(f"  Reference Chapter   : {rec['execution_chapter']}")
    print(f"* Reactivity Engine   : {rec['reactivity']}")
    print(f"  Reference Chapter   : {rec['reactivity_chapter']}")
    print(f"* State & Cache       : {rec['state']}")
    print(f"  Reference Chapter   : {rec['state_chapter']}")
    print(f"* API Contract Layer  : {rec['api']}")
    print(f"  Reference Chapter   : {rec['api_chapter']}")
    print(f"* UI & Design Tokens  : {rec['ui']}")
    print(f"  Reference Chapter   : {rec['ui_chapter']}")
    if "suggested_recipe" in rec:
        print(f"* Suggested Recipe    : recipes/{rec['suggested_recipe']}/")
        print(f"  Scaffold with       : python pipelines/cli/choice_engine.py --init {rec['suggested_recipe']} --target <dir>")
    print("=" * 70)
    print("Run complete. Consult the referenced chapters in the book/ directory.\n")

if __name__ == "__main__":
    main()
