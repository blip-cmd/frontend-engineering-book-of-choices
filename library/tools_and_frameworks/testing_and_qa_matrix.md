# Testing & QA Strategy: Unit vs. Integration vs. E2E vs. Visual Regression

* **Category:** `delivery_and_build`
* **Status:** Industry Standard & Best Practice
* **Core Comparison:** Vitest / Jest vs. React Testing Library vs. Playwright / Cypress vs. Storybook / Chromatic vs. MSW (Mock Service Worker)

---

## 1. The Modern Testing Trophy vs. The Legacy Testing Pyramid

The classical testing pyramid (pioneered in the backend era) mandated thousands of isolated unit tests, a modest layer of integration tests, and very few end-to-end (E2E) tests.

In modern frontend engineering, Kent C. Dodds introduced the **Testing Trophy**:
* Pure unit tests on presentation components offer low confidence because they test implementation details rather than user behavior.
* **Integration Tests** form the bulk of the trophy: mounting component trees, mocking network requests at the network layer (via Mock Service Worker), and asserting that user interactions produce expected DOM changes and network dispatches.
* **End-to-End Tests (Playwright)** test critical golden user journeys (e.g., signup, checkout) against real production builds.
* **Visual Regression Tests (Chromatic / Percy)** capture screenshot diffs across viewport widths to catch accidental styling and layout shifts.

---

## 2. Comparative Matrix: Frontend Testing Tools

| Layer | Tooling Choices | Execution Speed | Confidence Level | Maintenance Burden | Primary Hazard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Unit & Integration** | Vitest vs. Jest | Blazing (Vitest native ESM / Vite) | High when focused on user actions | Low | Testing internal state instead of user outcomes |
| **Component DOM Testing**| React Testing Library | Fast (JSDOM or Happy-DOM) | High for user accessibility paths | Low | Over-relying on container queries instead of ARIA roles |
| **Network Mocking** | Mock Service Worker (MSW) | Near-Zero Overhead | Highest (Standard fetch interceptor) | Low (Single source of truth) | Mock drift from real backend responses |
| **End-to-End (E2E)** | Playwright vs. Cypress | Moderate (Headless real browsers) | Highest (Full system verification) | Moderate (Flaky tests if timing is unmanaged) | Over-testing edge cases in E2E instead of integration |
| **Visual Regression** | Storybook + Chromatic | Async in CI | Highest for CSS and layout fidelity | Moderate | Flaky diffs caused by font loading or animations |

---

## 3. The Network Mocking Paradigm: Why MSW Wins

Traditional mocking involved stubbing `global.fetch` or mocking module imports (`jest.mock('./api')`). This hides actual HTTP transport mechanics and couples tests to internal code structures.

**Mock Service Worker (MSW)** intercepts requests at the network level using the browser's native Service Worker API (or Node's `http` interceptors):
* The component code dispatches real `fetch()` calls.
* MSW intercepts the request in the network layer and returns declarative mock responses.
* The exact same mock handlers are shared across Vitest integration tests, Storybook preview states, and local development fallback modes.

---

## 4. Decision Playbook: Allocating Your Testing Budget

1. **Allocate 60% of Effort to Integration Tests (Vitest + RTL + MSW):**
   * Test complex forms, interactive dashboards, and multi-step dialogs.
   * Query elements strictly via accessible roles: `screen.getByRole('button', { name: /submit/i })`.
2. **Allocate 25% of Effort to End-to-End Tests (Playwright):**
   * Restrict E2E tests strictly to revenue-critical paths: Authentication, Billing Checkout, and Core CRUD loops.
3. **Allocate 10% of Effort to Visual Regression (Storybook / Chromatic):**
   * Isolate design system primitives (buttons, inputs, modals) and test across color themes and responsive viewports.
4. **Allocate 5% of Effort to Pure Unit Tests:**
   * Reserve pure unit tests for pure business logic: mathematical calculations, date parsers, and custom data transformation utilities.
