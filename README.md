# manamaths-notes

PDF-first teaching notes for Mana Maths.

## Purpose

`manamaths-notes` mirrors Mana Maths learning objectives one-to-one.
Each module is a landscape, slide-looking LaTeX notes deck for first teaching:
- learning goal
- key idea
- steps
- worked examples
- common mistake
- tiny practice

LaTeX is the source of truth. PDF is the primary output. HTML can be generated later from the same source or a parallel conversion pipeline.

## Shape

- `TEMPLATES/` — shared LaTeX templates
- `OBJECTIVES/lo-yr9-.../` — one notes module per LO
- `OPERATIONS/data/notes-tracker.json` — Notes progress tracker
- `OPERATIONS/scripts/generate_notes_tracker.py` — regenerate the Notes tracker from actual repo state
- `build/` — generated outputs when needed

## Conventions

- Keep Notes aligned one-to-one with Mana Maths LO ids and slugs.
- Keep pages landscape and projector-friendly.
- Prefer sparse, slide-looking layouts over dense worksheet layouts.
- Treat `main.tex` as the canonical entry point for each LO.
- Build with `tectonic` for this repo.
- Keep repo-specific workflow notes in `manamaths-notes/AGENTS.md`.
