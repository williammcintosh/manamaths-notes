# manamaths-notes

PDF-first teaching notes for Mana Maths.

Live site target:
- https://williammcintosh.github.io/manamaths-notes/

## Purpose

`manamaths-notes` mirrors Mana Maths learning objectives one-to-one.
Each module is a landscape, slide-looking LaTeX notes deck for first teaching:
- learning goal
- key idea
- steps
- worked examples
- common mistake
- tiny practice

LaTeX is the source of truth. HTML notes pages are generated from that LaTeX source for the website. PDF can still be built separately for print/export.

## Shape

- `TEMPLATES/` — shared LaTeX templates
- `OBJECTIVES/lo-yr9-.../` — one notes module per LO
- `OPERATIONS/data/notes-tracker.json` — Notes progress tracker
- `OPERATIONS/scripts/generate_notes_tracker.py` — regenerate the Notes tracker from actual repo state
- `OPERATIONS/scripts/generate_site.py` — build the static website into `SITE/`
- `SITE/` — generated website output for GitHub Pages
- `build/` — generated outputs when needed

## Conventions

- Keep Notes aligned one-to-one with Mana Maths LO ids and slugs.
- Keep pages landscape and projector-friendly.
- Prefer sparse, slide-looking layouts over dense worksheet layouts.
- Treat `main.tex` as the canonical entry point for each LO.
- Build with `tectonic` for this repo.
- Keep repo-specific workflow notes in `manamaths-notes/AGENTS.md`.
