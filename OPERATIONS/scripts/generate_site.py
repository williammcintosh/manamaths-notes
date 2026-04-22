#!/usr/bin/env python3
import html
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TRACKER = REPO / 'OPERATIONS/data/notes-tracker.json'
SITE = REPO / 'SITE'
OBJECTIVES_SITE = SITE / 'objectives'
BASE_URL = 'https://williammcintosh.github.io/manamaths-notes'

STYLE = '''
:root {
  --bg: #f6f8fb;
  --card: #ffffff;
  --text: #163047;
  --muted: #5d7183;
  --line: #d8e1e8;
  --blue: #1f4e79;
  --green: #2f6b3b;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--text);
}
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 32px 20px 64px; }
.hero { margin-bottom: 28px; }
.hero h1 { margin: 0 0 8px; font-size: 2.2rem; }
.hero p { margin: 0; color: var(--muted); }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin: 22px 0 30px; }
.stat, .card { background: var(--card); border: 1px solid var(--line); border-radius: 16px; box-shadow: 0 6px 18px rgba(12,30,44,0.05); }
.stat { padding: 18px; }
.stat .label { color: var(--muted); font-size: 0.95rem; margin-bottom: 6px; }
.stat .value { font-size: 2rem; font-weight: 700; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
.card { padding: 18px; }
.card h3 { margin: 0 0 8px; font-size: 1.1rem; }
.meta { color: var(--muted); font-size: 0.95rem; margin-bottom: 14px; }
.badge { display: inline-block; padding: 5px 10px; border-radius: 999px; font-size: 0.82rem; font-weight: 700; margin-bottom: 12px; }
.badge.complete { background: #e8f5ec; color: var(--green); }
.badge.started { background: #fff4df; color: #9a6200; }
.badge.not_started { background: #edf2f7; color: #607286; }
.actions { display: flex; gap: 14px; flex-wrap: wrap; }
.viewer { width: 100%; height: 82vh; border: 1px solid var(--line); border-radius: 14px; background: #fff; }
.topnav { display: flex; gap: 18px; flex-wrap: wrap; margin: 0 0 16px; font-size: 0.95rem; }
.small { color: var(--muted); font-size: 0.92rem; }
'''


def page(title: str, body: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{STYLE}</style>
</head>
<body>
  <div class="wrap">
    {body}
  </div>
</body>
</html>
'''


def rel_pdf_path(slug: str) -> str:
    return f'../../OBJECTIVES/{slug}/build/main.pdf'


def objective_body(lo: dict) -> str:
    title = html.escape(lo['canonicalDisplayTitle'])
    code = html.escape(lo['canonicalInternalCode'])
    slug = lo['slug']
    pdf_path = rel_pdf_path(slug)
    status = lo['notesStatus']
    return f'''
<div class="topnav">
  <a href="../index.html">← Notes index</a>
  <a href="{pdf_path}">Open PDF</a>
</div>
<div class="hero">
  <h1>{title}</h1>
  <p>{code} · {html.escape(slug)}</p>
</div>
<div class="card" style="margin-bottom: 18px;">
  <div class="badge {status}">{status.replace('_', ' ').title()}</div>
  <div class="actions">
    <a href="{pdf_path}">Download PDF</a>
  </div>
</div>
<iframe class="viewer" src="{pdf_path}#view=FitH"></iframe>
<p class="small" style="margin-top: 10px;">If the embedded viewer fails on your browser, use the PDF link above.</p>
'''


def index_body(data: dict) -> str:
    summary = data['summary']
    cards = []
    for lo in data['learningObjectives']:
        status = lo['notesStatus']
        title = html.escape(lo['canonicalDisplayTitle'])
        code = html.escape(lo['canonicalInternalCode'])
        slug = lo['slug']
        if status == 'complete':
            actions = f'<div class="actions"><a href="objectives/{slug}.html">Open notes page</a><a href="OBJECTIVES/{slug}/build/main.pdf">PDF</a></div>'
        elif status == 'started':
            actions = '<div class="small">In progress</div>'
        else:
            actions = '<div class="small">Not started yet</div>'
        cards.append(f'''<div class="card">
  <div class="badge {status}">{status.replace('_', ' ').title()}</div>
  <h3>{title}</h3>
  <div class="meta">{code} · {html.escape(slug)}</div>
  {actions}
</div>''')
    return f'''
<div class="hero">
  <h1>Mana Maths Notes</h1>
  <p>PDF-first teaching notes for Mana Maths learning objectives.</p>
</div>
<div class="stats">
  <div class="stat"><div class="label">Total LOs</div><div class="value">{summary['totalObjectives']}</div></div>
  <div class="stat"><div class="label">Notes complete</div><div class="value">{summary['notesComplete']}</div></div>
  <div class="stat"><div class="label">Started</div><div class="value">{summary['notesStarted']}</div></div>
  <div class="stat"><div class="label">Not started</div><div class="value">{summary['notesNotStarted']}</div></div>
</div>
<div class="card" style="margin-bottom: 18px;">
  <strong>Latest live site base:</strong> <a href="{BASE_URL}">{BASE_URL}</a>
</div>
<div class="grid">
  {''.join(cards)}
</div>
'''


def main():
    data = json.loads(TRACKER.read_text())
    OBJECTIVES_SITE.mkdir(parents=True, exist_ok=True)
    (SITE / 'index.html').write_text(page('Mana Maths Notes', index_body(data)))
    for lo in data['learningObjectives']:
        if lo['notesStatus'] != 'complete':
            continue
        out = OBJECTIVES_SITE / f"{lo['slug']}.html"
        out.write_text(page(lo['canonicalDisplayTitle'], objective_body(lo)))


if __name__ == '__main__':
    main()
