# Shared Configs

Starter configuration shared across the recipes. MIT licensed, like everything in `recipes/`.

## Files

| File | What it is |
| :--- | :--- |
| `tokens.css` | Design tokens for Tailwind CSS 4.x, which is configured in CSS instead of `tailwind.config.js`. Semantic colours and `--radius` are CSS custom properties on `:root`, with a dark theme on the `.dark` class. An `@theme inline` block maps them to the `--color-*` and `--radius-*` theme variables, so utilities such as `bg-primary`, `text-foreground`, `border-border` and `rounded-lg` exist. It also defines the `dark:` variant for the `.dark` class and a centred `container` (2rem padding, 1400px max width). |
| `tokens.json` | The same values in the W3C Design Tokens Community Group format ([Format Module 2025.10](https://www.designtokens.org/TR/2025.10/format/), a Final Community Group Report, not a W3C Standard). Light and dark colours are separate groups. Use it as the input for token tooling; Tailwind reads only `tokens.css`. |
| `tsconfig.base.json` | TypeScript settings for an app built by a bundler such as Vite: `module: "preserve"`, `moduleResolution: "bundler"`, `verbatimModuleSyntax`, `strict`, `noUncheckedIndexedAccess` and `erasableSyntaxOnly`, with `noEmit` because the bundler writes the output. It sets no options that TypeScript 7 removed (such as `baseUrl` or `target: "es5"`). |

## Use

Tailwind (with `@tailwindcss/vite` in `vite.config.ts`), in your main stylesheet:

```css
@import "tailwindcss";
@import "./tokens.css";
```

Add the `dark` class to `<html>` (or any element) to switch its subtree to the dark theme. Tailwind 4 detects source files automatically, so no `content` list is needed.

TypeScript, in your project's `tsconfig.json`:

```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": { "types": ["vite/client"] },
  "include": ["src"]
}
```

TypeScript 6.0 and later default `types` to `[]`, so list the global types your app needs. `vite/client` also declares CSS imports, which `noUncheckedSideEffectImports` (on by default) would otherwise reject.

## Verified

On 2026-11-22, with Node 24.18.1 on Windows, a fresh Vite project outside this repository imported `tokens.css` and extended `tsconfig.base.json`. `vite build` and `tsc --noEmit` both passed, and the built CSS contained the token utilities and the `.dark` variant. Versions: vite 8.3.8, tailwindcss 4.3.5, @tailwindcss/vite 4.3.5, typescript 7.0.2.
