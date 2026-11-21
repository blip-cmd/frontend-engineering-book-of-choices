---
status: draft
ai_involvement: drafted
last_verified:
verified_against:
review_by:
reviewers:
---

# Appendix D: Zero-Downtime Migration Playbooks

> How to modernize legacy frontend architectures incrementally without risking catastrophic multi-month total rewrites.

---

## 1. Playbook 1: Migrating from Legacy Webpack to Vite / Rspack

### The Problem:
A large legacy codebase takes 3-5 minutes for local dev server starts and 15+ minutes in CI build pipelines using Webpack 4 or 5.

### Step-by-Step Incremental Migration:
1. **Option A: Rspack Drop-in Replacement:**
   * If the codebase heavily relies on complex custom Webpack loaders and plugins, swap Webpack for **Rspack** (`@rspack/cli`).
   * Rspack replicates 90% of Webpack's API surface in native Rust, delivering 5x to 10x faster builds with minimal configuration changes.
2. **Option B: Transition to Vite:**
   * *Phase 1:* Move environment variables from `process.env` to `import.meta.env` or use `@vitejs/plugin-react`.
   * *Phase 2:* Replace `entry.js` with standard `index.html` root file as expected by Vite.
   * *Phase 3:* Configure path aliases in `vite.config.ts` matching existing `tsconfig.json` paths.
   * *Result:* Instant Hot Module Replacement (HMR) under 50ms and clean modern ESM builds.

---

## 2. Playbook 2: Migrating from Runtime CSS-in-JS to Tailwind CSS / Panda CSS

### The Problem:
An existing React application uses `styled-components` or `@emotion/styled`. The engineering team wants to adopt React Server Components and improve mobile INP, but rewriting 500 components at once is impossible.

### Step-by-Step Incremental Migration:
1. **Phase 1: Co-existence Setup:**
   * Install Tailwind CSS alongside existing Styled Components. Ensure base reset styles do not clobber existing component layouts (set Tailwind `preflight: false` if needed initially).
2. **Phase 2: The "New Components Only" Boundary:**
   * Mandate that all newly created UI components must use headless primitives with Tailwind classes or compile-time Panda CSS.
3. **Phase 3: Leaf-to-Root Conversion:**
   * Begin migrating leaf components first: buttons, badges, avatars, inputs.
   * Replace props-based styled components with Tailwind utility classes and `cva` (Class Variance Authority) for variant mapping.
4. **Phase 4: Remove Runtime Dependency:**
   * Once top-level layout containers are migrated, uninstall `styled-components` or `@emotion/react` to eliminate the runtime JS styling parser from the production bundle.

---

## 3. Playbook 3: Strangler Migration from Monolithic Legacy SPA to Islands Architecture

### The Problem:
A monolithic Single Page Application has poor mobile SEO and failing Core Web Vitals, but business operations prevent taking the site offline for a rewrite.

### Step-by-Step Incremental Migration:
1. **The Edge Reverse Proxy Gateway:**
   * Place an Edge routing layer (Cloudflare Workers, Fastly, or NGINX) in front of the application.
2. **Carve Out High-Value Content Routes:**
   * Stand up a new **Astro** project serving `/blog`, `/docs`, and marketing landing pages.
   * Configure the edge router to route traffic for these specific paths to the Astro application, while routing all other paths (e.g., `/app`, `/dashboard`) to the legacy SPA.
3. **Port Content-Heavy Pages First:**
   * Progressively migrate product catalog and public pages into Astro, exporting existing React widgets as isolated interactive islands (`client:visible`).
4. **Unified Navigation via View Transitions:**
   * Use the native browser View Transitions API to provide seamless visual transitions across the independent applications.
