# Recipe: Low-Latency E-Commerce Storefront

A minimal Next.js 16 App Router starter for a storefront whose catalog pages are cached and regenerated in the background, with an optimistic "Add to cart" button. It implements the [Low-Latency Global E-Commerce Storefronts playbook](../../book/09_decision_playbooks/low_latency_ecommerce.md).

## What it shows

* `app/page.tsx`: product list with `export const revalidate = 3600` (Incremental Static Regeneration).
* `app/product/[id]/page.tsx`: product pages prerendered with `generateStaticParams`, also revalidated hourly.
* `app/product/[id]/add-to-cart.tsx`: client component using React 19 `useOptimistic`, confirmed by the `addToCart` Server Function in `app/actions.ts`, which re-checks stock on the server.
* `app/api/cart/route.ts`: the personalised cart response, sent with `Cache-Control: private, no-store` so shared caches do not store it.
* Tailwind CSS 4 through `@tailwindcss/postcss`.
* No route sets `export const runtime = 'edge'`: ISR needs the default Node.js runtime. Put a CDN in front of `next start` for the catalog HTML.

The catalog is local mock data in `lib/products.ts`; replace it with your commerce API.

## Run it

```bash
npm install
npm run dev        # http://localhost:3000
npm run typecheck
npm run build && npm start
```

## Versions

Built and type-checked on 2026-11-22 with Node.js 24.18.1, `next` 16.4.6, `react` and `react-dom` 19.3.1, `tailwindcss` and `@tailwindcss/postcss` 4.3.5, `postcss` 8.5.33 and `typescript` 7.0.2.

## License

MIT, like everything in `recipes/`.
