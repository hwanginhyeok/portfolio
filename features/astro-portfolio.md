# Feature: astro-portfolio

## What

Interactive personal engineering portfolio static website built with Astro and Tailwind CSS. Showcases career narrative, case studies (SS500 MBD, EOP 400W motor pump, Autonomy Stack, Production Validation, Patent analysis), architecture diagrams, and interactive Observable Plot charts.

## Entry points

- `npm run dev` — Local development server
- `npm run build` — Compiles static assets into `dist/` (10 static pages + sitemap)
- `npm run preview` — Previews static build locally

## Contract

- Inputs: Markdown case studies (`src/pages/cases/`), Astro layouts/components (`src/components/`, `src/layouts/`), static assets (`public/`)
- Outputs: Static HTML, CSS, JS bundles and XML sitemap in `dist/`
- Gate: Type checking and clean Astro build with zero route errors

## Data and state

- Repository data: `src/`, `public/`, `astro.config.mjs`, `tailwind.config.mjs`
- External state: None (fully self-contained static site)
- Secrets: None

## Tests

- `npm run build` (verifies 10 static pages and sitemap compile successfully)

## Status

live; actively maintained on macOS and buildable hermetically.
