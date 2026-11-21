"""
Social Comparison Card Generator
Generates high-contrast 1200x630 vector SVG cards summarizing key architectural
trade-off matrices for social distribution and developer documentation.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = REPO_ROOT / "docs" / "cards"

CARDS = [
    {
        "filename": "card_01_reactivity_engines.svg",
        "title": "Reactivity Dilemma: Virtual DOM vs Signals vs Compilers",
        "subtitle": "Choosing the right UI reactivity model based on update frequency and team scale",
        "columns": [
            {
                "name": "Virtual DOM",
                "tag": "React 19",
                "color": "#38bdf8",
                "advantage": "Unbounded flexibility; pure JavaScript semantics; massive component ecosystem.",
                "bottleneck": "Re-renders entire component subtrees; requires manual memoization at scale.",
                "best_for": "Large teams, enterprise design systems, complex state orchestration."
            },
            {
                "name": "Fine-Grained Signals",
                "tag": "Solid.js / Preact",
                "color": "#a855f7",
                "advantage": "Surgical DOM updates without re-running components; maximum runtime speed.",
                "bottleneck": "Subtle reactivity loss when destructuring props; mental model shift.",
                "best_for": "High-frequency telemetry, financial tickers, real-time dashboards."
            },
            {
                "name": "Compile-Time AST",
                "tag": "Svelte 5 Runes",
                "color": "#f97316",
                "advantage": "Minimal runtime overhead; concise syntax; zero virtual DOM reconciliation.",
                "bottleneck": "Tighter coupling to compiler; smaller third-party ecosystem.",
                "best_for": "Solo founders, rapid prototyping, memory-constrained mobile devices."
            }
        ]
    },
    {
        "filename": "card_02_css_architectures.svg",
        "title": "CSS Architecture: Tailwind vs Runtime CSS-in-JS vs Zero-Runtime",
        "subtitle": "Balancing runtime bundle cost, design token ergonomics, and server streaming",
        "columns": [
            {
                "name": "Utility-First CSS",
                "tag": "Tailwind CSS",
                "color": "#06b6d4",
                "advantage": "Sub-15 KB fixed CSS bundle; zero runtime JS parsing overhead; dead-code purged.",
                "bottleneck": "Verbose HTML markup; requires discipline with component abstraction.",
                "best_for": "Public marketing, e-commerce storefronts, high-traffic consumer web."
            },
            {
                "name": "Runtime CSS-in-JS",
                "tag": "Styled-Components / Emotion",
                "color": "#ec4899",
                "advantage": "Co-located styling with props; dynamic runtime theme computation.",
                "bottleneck": "Incompatible with React Server Components; degrades Interaction to Next Paint (INP).",
                "best_for": "Legacy internal enterprise applications without SSR requirements."
            },
            {
                "name": "Zero-Runtime Type-Safe",
                "tag": "StyleX / Panda CSS",
                "color": "#10b981",
                "advantage": "Compile-time extraction; deterministic class ordering; strict design token contracts.",
                "bottleneck": "More complex build step; requires strict AST compiler tooling.",
                "best_for": "Massive multi-brand design systems, large-scale cross-team repos."
            }
        ]
    },
    {
        "filename": "card_03_api_contracts.svg",
        "title": "API Contract Layer: REST vs GraphQL vs tRPC",
        "subtitle": "Selecting the optimal data boundary across polyglot and full-stack topologies",
        "columns": [
            {
                "name": "REST + OpenAPI",
                "tag": "OpenAPI / Orval",
                "color": "#3b82f6",
                "advantage": "Universal standard; trivial HTTP edge caching; polyglot backend compatibility.",
                "bottleneck": "Over-fetching and under-fetching without careful endpoint design.",
                "best_for": "Public APIs, polyglot backends (Go/Python/Java), microservice architectures."
            },
            {
                "name": "GraphQL",
                "tag": "Apollo / Urql",
                "color": "#e11d48",
                "advantage": "Client-specified queries; unified schema gateway; zero over-fetching.",
                "bottleneck": "Complex client caching (normalized store); difficult HTTP edge caching.",
                "best_for": "Complex graph data, mobile apps with multiple downstream services."
            },
            {
                "name": "End-to-End tRPC",
                "tag": "tRPC v11",
                "color": "#8b5cf6",
                "advantage": "Zero code generation; instant TypeScript type inference; highest dev velocity.",
                "bottleneck": "Strictly requires TypeScript on both client and server; single monorepo.",
                "best_for": "Full-stack TypeScript monorepos, B2B SaaS startups, agile product teams."
            }
        ]
    }
]

def generate_svg_card(card_data):
    title = card_data["title"]
    subtitle = card_data["subtitle"]
    cols = card_data["columns"]

    col_width = 340
    col_gap = 30
    start_x = 60
    card_y = 190
    card_h = 360

    col_elements = []
    for i, col in enumerate(cols):
        x = start_x + i * (col_width + col_gap)
        col_elements.append(f"""
    <!-- Column {i+1}: {col['name']} -->
    <g transform="translate({x}, {card_y})">
      <rect width="{col_width}" height="{card_h}" rx="12" fill="#111827" stroke="{col['color']}" stroke-width="1.5" stroke-opacity="0.6"/>
      <rect width="{col_width}" height="60" rx="12" fill="#1e293b" fill-opacity="0.8"/>
      <rect x="0" y="48" width="{col_width}" height="12" fill="#1e293b" fill-opacity="0.8"/>
      
      <!-- Column Header -->
      <text x="20" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="19" font-weight="bold" fill="#f8fafc">{col['name']}</text>
      <rect x="{col_width - 120}" y="16" width="105" height="24" rx="12" fill="{col['color']}" fill-opacity="0.15"/>
      <text x="{col_width - 68}" y="32" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="{col['color']}">{col['tag']}</text>
      
      <!-- Primary Advantage -->
      <text x="20" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#38bdf8">PRIMARY ADVANTAGE</text>
      <foreignObject x="20" y="100" width="{col_width - 40}" height="70">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; color: #cbd5e1; line-height: 1.4;">
          {col['advantage']}
        </div>
      </foreignObject>
      
      <!-- Critical Bottleneck -->
      <text x="20" y="185" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#f87171">PRIMARY TRADE-OFF</text>
      <foreignObject x="20" y="195" width="{col_width - 40}" height="70">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; color: #cbd5e1; line-height: 1.4;">
          {col['bottleneck']}
        </div>
      </foreignObject>

      <!-- Best For -->
      <text x="20" y="280" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#34d399">BEST FIT</text>
      <foreignObject x="20" y="290" width="{col_width - 40}" height="60">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; font-weight: 500; color: #e2e8f0; line-height: 1.35;">
          {col['best_for']}
        </div>
      </foreignObject>
    </g>
""")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#090d16"/>
    </linearGradient>
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#818cf8"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1200" height="630" fill="url(#bg)"/>

  <!-- Top Badge Bar -->
  <g transform="translate(60, 48)">
    <rect width="365" height="28" rx="14" fill="#1e293b" stroke="#334155" stroke-width="1"/>
    <circle cx="16" cy="14" r="5" fill="#38bdf8"/>
    <text x="28" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#94a3b8" letter-spacing="1">FRONTEND ENGINEERING AS A BOOK OF CHOICES</text>
  </g>

  <!-- Title & Subtitle -->
  <text x="60" y="118" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="30" font-weight="800" fill="#f8fafc" letter-spacing="-0.5">{title}</text>
  <text x="60" y="152" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" fill="#94a3b8">{subtitle}</text>

  <!-- Matrix Columns -->
  {"".join(col_elements)}

  <!-- Footer -->
  <text x="60" y="592" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="500" fill="#64748b">The Architectural Decision Matrix for Senior Web Engineers</text>
  <text x="1140" y="592" text-anchor="end" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#38bdf8">blip-cmd / bookofchoices.dev</text>
</svg>
"""
    return svg_content

def build_all_cards():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    for card_data in CARDS:
        svg_text = generate_svg_card(card_data)
        out_file = OUTPUT_DIR / card_data["filename"]
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(svg_text)
        generated.append(out_file)
        print(f"[SUCCESS] Social card generated: {out_file}")
    return generated

if __name__ == "__main__":
    build_all_cards()
