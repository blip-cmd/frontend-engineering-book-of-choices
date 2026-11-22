# Monorepos & Workspace Tooling: Turborepo vs. Nx vs. pnpm Workspaces

> **Unverified background notes.** This file is an AI-generated research summary from the book's first draft. It has not been checked against the [content standards](../../CONTENT_STANDARDS.md) and is not part of the book. The verified chapters in `book/` cite primary sources directly; rely on those instead.

* **Category:** `delivery_and_build`
* **Status:** Industry Standard for Multi-Package Teams
* **Core Comparison:** Turborepo vs. Nx vs. Pure pnpm Workspaces vs. Polyrepo Governance

---

## 1. The Monorepo Dilemma: Polyrepo vs. Monorepo

When scaling frontend development across multiple products, libraries, and design systems, engineering teams face a structural choice:

* **The Polyrepo Model (Separate Repositories):**
  * *Advantage:* Isolated repository boundaries, separate Git permissions, smaller repository clones.
  * *Failure Mode:* Version drift across shared packages, multi-step PRs to update a single design token across 5 apps, broken local development loops, and massive overhead maintaining synchronized CI configurations.
* **The Monorepo Model (Single Unified Repository):**
  * *Advantage:* Atomic cross-package commits, zero-publish local development linking, unified TypeScript configurations, and single source of truth for design systems.
  * *Failure Mode:* Unmanaged monorepos suffer from slow CI builds where modifying a utility function triggers complete rebuilds of every application.

---

## 2. The Three Generations of Monorepo Tooling

1. **Generation 1: Package Linking (Lerna, npm/yarn v1 workspaces):**
   * Simply symlinked packages together on disk. Lacked task graph understanding and executed tasks sequentially or with naive parallelism.
2. **Generation 2: Task Orchestration & Computation Caching (Turborepo, Nx):**
   * Models dependencies as a Directed Acyclic Graph (DAG).
   * **Computation Caching:** Computes cryptographic hashes of inputs (source files, environment variables, dependencies). If inputs have not changed, it restores build and test outputs directly from cache in milliseconds rather than re-running the work.
   * **Remote Caching:** Shares cache artifacts across the entire engineering team and CI pipeline. A build executed by developer A in Tokyo is restored instantly on CI in Virginia without recomputing.

---

## 3. Comparative Matrix: Turborepo vs. Nx

| Evaluation Dimension | Turborepo | Nx | Pure pnpm Workspaces |
| :--- | :--- | :--- | :--- |
| **Philosophy** | Lightweight, unobtrusive build orchestrator | Full-featured extensible platform | Raw package manager workspace linking |
| **Configuration Burden** | Very Low (`turbo.json` under 40 lines) | Moderate to High (`nx.json` + plugins) | Zero (Built into `pnpm-workspace.yaml`) |
| **Computation Caching** | Native, ultra-fast (Written in Rust) | Native, highly granular (Written in TypeScript/Rust) | None (Re-runs every command from scratch) |
| **Remote Cache Support** | Yes (Vercel Remote Cache or self-hosted) | Yes (Nx Cloud or self-hosted) | None |
| **Code Generation / Generators**| None (Follows standard file structures) | Extensive (Built-in schematics for apps/libs) | None |
| **Best-Fit Team Size** | 2 to 50 engineers | 50 to 500+ engineers (Massive enterprise) | Solo developers or tiny 2-person teams |

---

## 4. Package Manager Selection: pnpm as the Foundation

Regardless of whether Turborepo or Nx is selected as the task runner, **pnpm** has emerged as the definitive package manager for modern monorepos:
* **Content-Addressable Hard Linking:** Stores all package versions in a single global content-addressable store on disk. Multiple monorepo projects link to the same files, saving gigabytes of disk space.
* **Strict Non-Hoisting:** Unlike npm and Yarn classic, pnpm does not hoist undeclared transitive dependencies to the root `node_modules`. This prevents "phantom dependencies", where code accidentally imports packages not declared in its `package.json`, which subsequently breaks production builds.

---

## 5. Decision Playbook

```
                  [How many engineers and packages exist in the project?]
                                             │
             ├── Small Team (1-10 engineers, 2-5 packages)
             │      └── Choose pnpm Workspaces + Turborepo
             │          (Near-zero setup overhead, instant local & CI caching)
             │
             └── Large Enterprise (50+ engineers, dozens of micro-apps)
                    │
                    Do you need strict architectural boundaries and code generation?
                          ├── Yes ──> Choose Nx (Enforces boundary rules and dependency graphs)
                          └── No  ──> Choose Turborepo (Fast, modular, minimal maintenance)
```
