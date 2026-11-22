# Recipe: Enterprise B2B SaaS starter

A minimal Vite + React single-page app that implements the stack from the [Enterprise B2B SaaS and Data Grids playbook](../../book/09_decision_playbooks/enterprise_b2b_saas.md). It renders one sortable accounts table: TanStack Query loads mock data from a local promise (no network calls), a Zod schema validates the response and supplies the row type, TanStack Table sorts it, and Tailwind CSS styles it.

## Run it

```bash
npm install
npm run dev        # start the dev server
npm run typecheck  # tsc --noEmit, strict mode
npm run build      # type-check, then build to dist/
npm run preview    # serve the production build
```

## What is in it

| File | Purpose |
| :--- | :--- |
| `vite.config.ts` | React and Tailwind plugins; `resolve.tsconfigPaths` reads the `@/*` alias from `tsconfig.json` |
| `src/main.tsx` | Mounts the app inside `QueryClientProvider` |
| `src/App.tsx` | Zod schema, mock fetch, `useQuery`, and a TanStack Table 9 `useTable` with row sorting |
| `src/index.css` | `@import "tailwindcss";` (Tailwind 4 needs no config file or PostCSS setup) |

## Adding the rest of the playbook

The starter installs only what it uses. The playbook also recommends these; add them when you need them:

* Long client-side tables: `@tanstack/react-virtual`
* Forms: `react-hook-form` with `@hookform/resolvers` (`zodResolver`)
* Filters in the URL: `nuqs`
* Component primitives: `npx shadcn init` (Base UI by default, Radix also supported)

## Versions

Built and checked on 2026-11-22 with Node.js 24.18.1 and npm 11.16.0 (`npm run typecheck` and `npm run build` pass):

| Package | Version |
| :--- | :--- |
| vite | 8.3.8 |
| @vitejs/plugin-react | 6.3.0 |
| react, react-dom | 19.3.1 |
| @tanstack/react-query | 5.108.2 |
| @tanstack/react-table | 9.3.1 |
| zod | 4.6.7 |
| tailwindcss, @tailwindcss/vite | 4.3.5 |
| typescript | 7.0.2 |
| @types/react, @types/react-dom | 19.3.0 |

`package-lock.json` pins the exact tree.

## License

MIT, see [../LICENSE](../LICENSE).
