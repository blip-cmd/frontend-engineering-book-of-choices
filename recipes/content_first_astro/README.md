# Recipe: Content-First Astro

A minimal static site starter for documentation hubs, blogs and marketing sites. It implements the [Content-First Publishing and Documentation playbook](../../book/09_decision_playbooks/content_first_publishing.md).

## What is inside

* `src/pages/index.astro`: a static page. It ships no JavaScript except the island below.
* `src/components/Counter.tsx`: one Preact island, hydrated with `client:visible` when it scrolls into view.
* `src/content.config.ts` and `src/content/notes/`: a content collection with a schema and one Markdown entry, rendered by `src/pages/notes/[id].astro`.
* `src/styles/global.css`: Tailwind CSS 4, loaded through the `@tailwindcss/vite` plugin in `astro.config.mjs`.
* `src/assets/hero.png`: a local image rendered with Astro's `<Image />`, which converts it to WebP and sets its width and height at build time.
* `tsconfig.json`: extends `astro/tsconfigs/strict`.

Set `site` in `astro.config.mjs` to your production URL. For a documentation site, the playbook recommends adding [Starlight](https://starlight.astro.build/), which this starter does not include.

## Run it

Requires Node.js 22.23.4 or later (the `engines` field of Astro 7.4.13).

```bash
npm install
npm run dev      # local dev server
npm run check    # type and template diagnostics
npm run build    # static output in dist/
npm run preview  # serve dist/ locally
```

## Versions

Built and checked on 2026-11-22 with astro 7.4.13, @astrojs/preact 6.1.6, preact 11.2.0, tailwindcss 4.3.5, @tailwindcss/vite 4.3.5, @astrojs/check 0.9.12 and typescript 6.0.3 on Node.js 24.18.1. TypeScript stays on 6 because @astrojs/check 0.9.12 declares a peer range of `^5.0.0 || ^6.0.0`.

## License

MIT, see [../LICENSE](../LICENSE).
