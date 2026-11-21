# Architectural Methodology: Micro-Frontends and Module Federation

* **Identifier:** `micro-frontends-and-module-federation`
* **Pioneers & Key Implementers:** Zack Jackson (Module Federation), Martin Fowler, Luca Mezzalira, Spotify, DAZN, IKEA, Amazon
* **Core Mechanisms:** Independent deployments, runtime script orchestration, Webpack / Rspack Module Federation, single-spa orchestrator, iframe / Web Component encapsulation

---

## 1. Mechanics and Mental Model

As organizations scale to hundreds of frontend engineers across dozens of squads, a single monolithic frontend repository becomes an organizational bottleneck: merge queues clog, CI pipelines extend to hours, deployment coordination becomes bureaucratic, and a single broken commit can take down an entire platform.

**Micro-Frontends** decompose the frontend user interface into independent sub-applications owned by cross-functional feature teams:
1. **Vertical Ownership:** Each team owns a complete vertical slice (e.g., Team Checkout, Team Catalog, Team User Profile) from frontend UI to database.
2. **Runtime Integration:** Rather than compiling all components into a single bundle at build time, a lightweight host shell dynamically imports remote micro-apps over the network at runtime.
3. **Module Federation:** Enables an application to dynamically load code from another independent build, with intelligent dependency sharing (e.g., ensuring only one copy of React is loaded in memory).

---

## 2. Comparative Trade-offs

### What You Gain:
* **Autonomous Release Cycles:** Teams deploy changes to their micro-app independently multiple times a day without coordinating or triggering a redeploy of the main shell.
* **Localized Failure Boundaries:** A crash in a non-critical micro-frontend (such as a recommendations widget) can be trapped with an error boundary, leaving the primary application intact.
* **Independent Technology Evolution:** Teams can theoretically experiment with newer framework versions or distinct stacks without forcing an immediate organization-wide rewrite.

### What You Forfeit:
* **Severe Performance & Bundle Penalties:** If dependency sharing is misconfigured, users download multiple versions of shared runtimes (e.g., two versions of React, multiple design system styles, duplicated utility libraries).
* **CSS & Style Collisions:** Without strict CSS Modules, Shadow DOM, or scoping conventions, global styles leak across micro-frontend boundaries.
* **Complex Local Development & E2E Testing:** Running the complete application locally requires running multiple service ports or stubbing remote federated modules.
* **Inconsistent User Experience:** Different micro-apps risk developing subtle differences in UI behavior, navigation delays, and accessibility compliance.

---

## 3. Decision Bounds: When to Choose and Avoid

### Choose Micro-Frontends When:
* **The Organization is Massive:** You have more than 50 to 100 frontend engineers divided across distinct, autonomous business domains.
* **Independent Deployment is a Hard Business Requirement:** A release bottleneck in the marketing domain must never block the checkout domain from deploying urgent hotfixes.
* **Legacy Migration:** You are progressively strangler-patterning a massive legacy frontend (e.g., AngularJS, Backbone) to modern stacks without a high-risk big-bang rewrite.

### Avoid Micro-Frontends When:
* **Small to Mid-Sized Teams:** If your team has fewer than 30 frontend engineers, micro-frontends will introduce massive organizational and technical tax with virtually zero benefits.
* **Performance-Critical Consumer Web:** On mobile devices where sub-second LCP and tight bundle limits are critical, micro-frontends introduce network waterfalls and runtime bloat.
* **A Well-Structured Modular Monolith Suffices:** Tools like Turborepo, Nx, and pnpm workspaces provide excellent code isolation, boundary enforcement, and fast cached CI builds without runtime orchestration risk.

---

## 4. Enabling Ecosystem & Tooling
* **Federation Tools:** Webpack Module Federation, Rspack Module Federation, `@originjs/vite-plugin-federation`.
* **Framework Orchestrators:** single-spa, Qiankun, OpenComponents.
* **Monorepo Alternatives:** Nx, Turborepo, pnpm workspaces.
