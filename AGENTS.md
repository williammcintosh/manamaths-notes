# AGENTS.md

Repo-specific notes for `manamaths-notes`.

## Purpose

This repo is for PDF-first Mana Maths teaching notes.
LaTeX is the source of truth.
Layouts should stay landscape and slide-looking.

## Build toolchain

Use `tectonic` for LaTeX builds in this repo.
Current confirmed binary in this environment:
- `/home/debid/bin/tectonic`

Do not assume `pdflatex` is installed.
Do not add global workspace rules for this repo here; keep notes repo-specific.

## Build command

From the workspace root:

```bash
tectonic --outdir manamaths-notes/OBJECTIVES/<slug>/build manamaths-notes/OBJECTIVES/<slug>/main.tex
```

Confirmed working example:

```bash
tectonic --outdir manamaths-notes/OBJECTIVES/lo-yr9-place-values-and-decimals/build manamaths-notes/OBJECTIVES/lo-yr9-place-values-and-decimals/main.tex
```

This produced:
- `manamaths-notes/OBJECTIVES/lo-yr9-place-values-and-decimals/build/main.pdf`

## Notes

- Tectonic may download LaTeX bundle files on first run.
- Fira Sans is currently referenced in the LaTeX source and builds under Tectonic in this environment.
- If layout warnings appear, treat them as a cue to tighten spacing or shorten text before adding more content.
- Keep generated files inside each LO `build/` folder.
- Track repo progress in `OPERATIONS/data/notes-tracker.json`.
- Refresh progress with `python3 manamaths-notes/OPERATIONS/scripts/generate_notes_tracker.py` after adding or finishing a module.

## Website pipeline

Use `python3 manamaths-notes/OPERATIONS/scripts/generate_site.py` to build the static site into `manamaths-notes/SITE/`.

The site currently:
- builds an index page from `OPERATIONS/data/notes-tracker.json`
- builds one HTML page per complete LO from the LaTeX source
- builds one embeddable HTML fragment per complete LO in `SITE/fragments/`
- deploys via `.github/workflows/deploy-pages.yml`
- can be embedded or linked from the main `manamaths` site
- should prefer a denser, narrower notes column with tighter module padding and a strong green divider between the upper and lower notes sections

After changing Notes content, refresh in this order:
1. build the target PDF with `tectonic` if you want a printable/export copy
2. refresh `notes-tracker.json`
3. regenerate the site and fragments
4. commit and push

## Future thread guidance

When working on this repo:
1. Edit `main.tex` in the target LO folder.
2. Build with `tectonic`.
3. Visually inspect the PDF.
4. Refresh `notes-tracker.json`.
5. Regenerate `SITE/`.
6. Adjust spacing/content until it feels like a sparse teaching deck, not a worksheet.
