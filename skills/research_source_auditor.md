# Skill: Research Source Auditor

> **Binding rules first.** This prompt predates the project's content standards. Where it conflicts with [`AGENTS.md`](../AGENTS.md) or [`CONTENT_STANDARDS.md`](../CONTENT_STANDARDS.md), those files win. In particular: verify every claim against a primary source in the same session, never invent numbers, citations, packages or experience, and never mark your own work as reviewed.

## Mission
Audit incoming literature, engineering whitepapers, framework documentation, and production post-mortems into standardized decision intelligence.

## Trigger Scenarios
* Ingesting a technical book (e.g., High Performance Browser Networking, Web Performance in Action).
* Evaluating a new framework or major version release (e.g., Next.js App Router, Svelte 5 Runes, React 19 Actions).
* Auditing an engineering tech blog post (e.g., Figma's canvas architecture, Netflix's client data fetching).

## Standardized Audit Procedure

1. **Thesis Extraction:**
   Identify the primary architectural friction the author or tool aimed to eliminate. Avoid summarizing tutorials; focus strictly on structural mechanics.

2. **Constraint Identification:**
   Determine the underlying conditions under which the solution was tested:
   * Team topology and skill distribution.
   * Traffic volume and latency budgets.
   * Client device profiles (high-end desktop vs. low-powered mobile).
   * Infrastructure budget and deployment model (edge, serverless, origin server, static CDN).

3. **Trade-off Quantification:**
   Every choice trades one property for another. Record:
   * **Acquired Benefits:** What became faster, simpler, or more resilient?
   * **Incurred Costs:** What became heavier, harder to debug, more expensive, or more complex?

4. **Schema Compliance:**
   Format the audited output to match [decision_item_schema.json](../pipelines/schemas/decision_item_schema.json).

5. **Storage Location:**
   Save audited markdown reports in the appropriate subfolder under `library/`:
   * Books: `library/books/<slug>.md`
   * Methodologies: `library/methodologies/<slug>.md`
   * Frameworks & Tools: `library/tools_and_frameworks/<slug>.md`
   * Research & Standards: `library/research_and_emerging/<slug>.md`
   * External Resources: `library/free_resources/<slug>.md`
