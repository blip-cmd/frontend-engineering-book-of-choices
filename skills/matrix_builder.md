# Skill: Decision Matrix Builder

## Mission
Synthesize individual audited research records into high-density, side-by-side comparison matrices that guide engineering selection under specific constraints.

## Trigger Scenarios
* Creating a comparative breakdown between competing architectural paradigms (e.g., VDOM vs. Signals vs. Direct AST Compilation).
* Generating a library selection guide for a specific engineering tier (e.g., State Management: Zustand vs. TanStack Query vs. Jotai vs. Redux Toolkit).
* Producing visual cheat sheets for the final book chapters.

## Standardized Synthesis Rules

1. **Orthogonal Comparison Criteria:**
   Always evaluate options along identical, objective vectors:
   * **Compute Location & Overhead:** CPU cycles, memory allocation, and bundle footprint.
   * **Initial Load Performance:** Impact on Time to First Byte (TTFB), First Contentful Paint (FCP), and Largest Contentful Paint (LCP).
   * **Runtime Responsiveness:** Interaction to Next Paint (INP) implications and event-loop blocking risks.
   * **Type Safety & Contract Strength:** Compile-time validation vs. runtime assertions.
   * **Operational & Infrastructure Cost:** Compute bills, build times, CDN caching efficiency.
   * **Ecosystem Maturity:** Production longevity, enterprise adoption, and backward compatibility stability.

2. **Zero False Equivalence:**
   Explicitly articulate where each tool fails. Avoid presenting options as universally interchangeable. 

3. **Format Requirement:**
   * Generate an executive markdown comparison table.
   * Provide a definitive "When to Choose Option A" rule.
   * Provide a definitive "When to Choose Option B" rule.
   * List the primary enabling packages and reference links.
