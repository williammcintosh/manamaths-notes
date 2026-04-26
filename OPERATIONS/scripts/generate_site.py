#!/usr/bin/env python3
import html
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TRACKER = REPO / 'OPERATIONS/data/notes-tracker.json'
SITE = REPO / 'SITE'
OBJECTIVES_SITE = SITE / 'objectives'
FRAGMENTS_SITE = SITE / 'fragments'
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
  --soft: #eef4f8;
  --warn: #a63d40;
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
.wrap { max-width: 760px; margin: 0 auto; padding: 20px 16px 40px; }
.hero { margin-bottom: 18px; }
.hero h1 { margin: 0 0 6px; font-size: 1.9rem; }
.hero p { margin: 0; color: var(--muted); }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin: 22px 0 30px; }
.stat, .card, .notes-page, .notes-fragment { background: var(--card); border: 1px solid var(--line); border-radius: 16px; box-shadow: 0 6px 18px rgba(12,30,44,0.05); }
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
.topnav { display: flex; gap: 18px; flex-wrap: wrap; margin: 0 0 16px; font-size: 0.95rem; }
.small { color: var(--muted); font-size: 0.92rem; }
.notes-page, .notes-fragment { padding: 12px; }
.notes-columns { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 10px; align-items: start; }
.notes-columns > div { border: 5px solid #000; border-radius: 18px; padding: 12px; background: #fff; }
.notes-section-title { font-size: 0.92rem; font-weight: 800; color: var(--blue); margin: 0 0 4px; }
.notes-key-idea { border: 1px solid var(--line); border-radius: 10px; padding: 8px 9px; margin: 0 0 8px; background: var(--soft); }
.notes-example-block, .notes-common-block, .notes-try-block { margin: 0; }
.notes-example-block + .notes-example-block, .notes-common-block + .notes-try-block, .notes-try-block + .notes-common-block { margin-top: 8px; }
.notes-example-title { margin: 0 0 4px; font-size: 0.9rem; color: var(--blue); }
.notes-common-block strong, .notes-try-block strong, .notes-key-idea strong { display: block; margin: 0 0 4px; }
.notes-common-block strong { color: var(--warn); }
.notes-page > .notes-common-block, .notes-page > .notes-try-block { border: 1px solid var(--line); border-radius: 10px; padding: 8px 9px; background: #fff; }
.notes-page > .notes-common-block { border-color: #e6c8cb; }
.notes-steps { margin: 0 0 8px; padding-left: 1rem; }
.notes-steps li, .notes-list li, .notes-try li { margin-bottom: 4px; }
.notes-list, .notes-try { margin: 0 0 8px; padding-left: 1rem; }
.notes-page-split { height: 6px; background: var(--green); border-radius: 999px; margin: 10px 0; }
.notes-page p { margin: 0 0 4px; line-height: 1.18; }
@media (max-width: 900px) { .notes-columns { grid-template-columns: 1fr; } }
'''

MATH_BLOCK_RE = re.compile(r'\\\[(.*?)\\\]', re.S)
MATH_INLINE_RE = re.compile(r'\\\((.*?)\\\)', re.S)
NOTES_TITLE_RE = re.compile(r'\\NotesTitle\{(.*?)\}', re.S)
SECTION_RE = re.compile(r'\\SectionTitle\{(.*?)\}', re.S)
KEY_IDEA_RE = re.compile(r'\\KeyIdea\{(.*?)\}', re.S)
STEP_RE = re.compile(r'\\StepLine\{(.*?)\}\{(.*?)\}', re.S)
ITEMIZE_RE = re.compile(r'\\begin\{itemize\}(.*?)\\end\{itemize\}', re.S)
ENUM_RE = re.compile(r'\\begin\{enumerate\}(.*?)\\end\{enumerate\}', re.S)
ITEM_RE = re.compile(r'\\item\s+(.*?)(?=(?:\\item|$))', re.S)
EXAMPLE_RE = re.compile(r'\\WorkedExample\{(.*?)\}\{(.*?)\}', re.S)
COMMON_RE = re.compile(r'\\CommonMistake\{(.*?)\}', re.S)
TRY_RE = re.compile(r'\\TryThese\{\%?\s*\\begin\{enumerate\}(.*?)\\end\{enumerate\}\s*\}', re.S)
MULTICOLS_RE = re.compile(r'\\begin\{multicols\}\{2\}(.*?)\\columnbreak(.*?)\\end\{multicols\}', re.S)
FRAME_RE = re.compile(r'\\begin\{frame\}(?:\[[^\]]*\])?(.*?)\\end\{frame\}', re.S)
COLUMNS_BLOCK_RE = re.compile(r'\\begin\{columns\}(?:\[[^\]]*\])?(.*?)\\end\{columns\}', re.S)
COLUMN_RE = re.compile(r'\\begin\{column\}\{[^}]+\}(.*?)\\end\{column\}', re.S)
TEXT_REPL = {
    r'\\textbf{': '<strong>',
}


def page(title: str, body: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{STYLE}</style>
  <script>
    window.MathJax = {{ tex: {{ inlineMath: [['\\(','\\)']], displayMath: [['\\[','\\]']] }} }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="wrap">
    {body}
  </div>
</body>
</html>
'''


def norm(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()


def render_tex_inline(text: str) -> str:
    text = text.strip()
    text = html.escape(text)
    text = text.replace('\\textbf{', '<strong>')
    text = text.replace('}', '</strong>', text.count('</strong>') if '</strong>' in text else 0)
    text = text.replace('&lt;strong&gt;', '<strong>').replace('&lt;/strong&gt;', '</strong>')
    text = text.replace('\\text{', '\\text{')
    text = text.replace('\\,', ' ')
    text = text.replace('\\ ', ' ')
    text = text.replace('\\%', '%')
    text = re.sub(r'\\text\{(.*?)\}', lambda m: m.group(1), text)
    text = text.replace('—', '&mdash;')
    return text


def wrap_paragraphs(text: str) -> str:
    chunks = [c.strip() for c in re.split(r'\n\s*\n', text) if c.strip()]
    out = []
    for chunk in chunks:
        chunk = re.sub(r'\n+', '<br />', chunk)
        out.append(f'<p>{chunk}</p>')
    return ''.join(out)


def render_list(body: str, klass: str) -> str:
    items = [render_tex_body(norm(m.group(1))) for m in ITEM_RE.finditer(body)]
    return f'<ul class="{klass}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def render_enum(body: str, klass: str) -> str:
    items = [render_tex_body(norm(m.group(1))) for m in ITEM_RE.finditer(body)]
    return f'<ol class="{klass}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'


def render_tex_body(text: str) -> str:
    text = text.strip()
    text = text.replace('\\f\\frac', '\\frac')
    text = re.sub(r'\\\((.*?)\\\)', lambda m: f'${m.group(1).strip()}$', text, flags=re.S)
    text = re.sub(r'\\\[(.*?)\\\]', lambda m: f'$$ {m.group(1).strip()} $$', text, flags=re.S)
    text = html.escape(text)
    text = re.sub(r'\\text\{(.*?)\}', lambda m: m.group(1), text)
    text = text.replace('\\,', ' ')
    text = text.replace('\\ ', ' ')
    text = text.replace('\\%', '%')
    text = re.sub(r'\\begin\{itemize\}(.*?)\\end\{itemize\}', lambda m: render_list(m.group(1), 'notes-list'), text, flags=re.S)
    text = re.sub(r'\\begin\{enumerate\}(.*?)\\end\{enumerate\}', lambda m: render_enum(m.group(1), 'notes-try'), text, flags=re.S)
    parts = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    rendered = []
    for p in parts:
        if p.startswith('<ul ') or p.startswith('<ol '):
            rendered.append(p)
        else:
            rendered.append(f'<p>{p.replace(chr(10), "<br />")}</p>')
    return ''.join(rendered)


def parse_notes_tex(tex: str) -> list[dict]:
    tex = re.sub(r'\\text\{(.*?)\}', lambda m: m.group(1), tex, flags=re.S)
    document = tex.split('\\begin{document}', 1)[-1].split('\\end{document}', 1)[0]
    pages = [p.strip() for p in FRAME_RE.findall(document) if p.strip()]
    parsed = []
    for page in pages:
        title = norm(NOTES_TITLE_RE.search(page).group(1)) if NOTES_TITLE_RE.search(page) else ''
        left = right = ''
        bottom_left = bottom_right = ''

        multicol_match = MULTICOLS_RE.search(page)
        if multicol_match:
            left, right = multicol_match.group(1), multicol_match.group(2)
            rest = MULTICOLS_RE.sub('', page)
        else:
            column_blocks = COLUMNS_BLOCK_RE.findall(page)
            rest = COLUMNS_BLOCK_RE.sub('', page)
            extracted_blocks = []
            for block in column_blocks:
                cols = [c.strip() for c in COLUMN_RE.findall(block)]
                if len(cols) >= 2:
                    extracted_blocks.append((cols[0], cols[1]))
            if extracted_blocks:
                left, right = extracted_blocks[0]
            if len(extracted_blocks) > 1:
                bottom_left, bottom_right = extracted_blocks[1]

        common = COMMON_RE.search(rest)
        tries = TRY_RE.search(rest)
        parsed.append({
            'title': title,
            'left': left,
            'right': right,
            'bottom_left': bottom_left,
            'bottom_right': bottom_right,
            'common': common.group(1).strip() if common else '',
            'tries': tries.group(1).strip() if tries else '',
        })
    return parsed


def render_column(col: str) -> str:
    out = []
    pos = 0
    patterns = [
        ('section', SECTION_RE),
        ('key', KEY_IDEA_RE),
        ('step', STEP_RE),
        ('example', EXAMPLE_RE),
        ('common', COMMON_RE),
        ('try', TRY_RE),
        ('itemize', ITEMIZE_RE),
    ]
    matches = []
    for kind, rx in patterns:
        for m in rx.finditer(col):
            matches.append((m.start(), m.end(), kind, m))
    matches.sort(key=lambda x: x[0])
    for start, end, kind, m in matches:
        if start > pos:
            plain = norm(col[pos:start])
            if plain:
                out.append(render_tex_body(plain))
        if kind == 'section':
            section_title = norm(m.group(1))
            if section_title.lower() != 'what you are learning':
                out.append(f'<div class="notes-section-title">{render_tex_body(section_title)}</div>')
        elif kind == 'key':
            out.append(f'<div class="notes-key-idea"><strong>Key idea:</strong> {render_tex_body(m.group(1))}</div>')
        elif kind == 'step':
            num = render_tex_body(m.group(1))
            body = render_tex_body(m.group(2))
            out.append(f'<ol class="notes-steps" start="{html.escape(re.sub(r"<.*?>","",num))}"><li>{body}</li></ol>')
        elif kind == 'example':
            out.append(f'<div class="notes-example-block"><h4 class="notes-example-title">{render_tex_body(m.group(1))}</h4>{render_tex_body(m.group(2))}</div>')
        elif kind == 'common':
            out.append(f'<div class="notes-common-block"><strong>Common mistake</strong>{render_tex_body(m.group(1))}</div>')
        elif kind == 'try':
            out.append(f'<div class="notes-try-block"><strong>Try these</strong>{render_enum(m.group(1), "notes-try")}</div>')
        elif kind == 'itemize':
            out.append(render_list(m.group(1), 'notes-list'))
        pos = end
    tail = norm(col[pos:])
    if tail:
        out.append(render_tex_body(tail))
    return ''.join(out)


def render_notes_content(tex_path: Path) -> tuple[str, str]:
    tex = tex_path.read_text()
    pages = parse_notes_tex(tex)
    page_html = []
    frag_html = []
    for i, page_data in enumerate(pages):
        section = f'<section class="notes-page">'
        if page_data['left'] or page_data['right']:
            left_html = render_column(page_data["left"])
            right_html = render_column(page_data["right"])
            stack_class = " notes-columns--stack-when-wide" if 'notes-example-block' in left_html or 'notes-example-block' in right_html else ""
            section += f'<div class="notes-columns{stack_class}"><div>{left_html}</div><div>{right_html}</div></div>'
        if page_data['common']:
            section += f'<div class="notes-common-block"><strong>Common mistake</strong>{render_tex_body(page_data["common"])}</div>'
        if page_data['tries']:
            section += f'<div class="notes-try-block"><strong>Try these</strong>{render_enum(page_data["tries"], "notes-try")}</div>'
        if page_data['bottom_left'] or page_data['bottom_right']:
            section += f'<div class="notes-columns notes-columns-bottom"><div>{render_column(page_data["bottom_left"])}</div><div>{render_column(page_data["bottom_right"])}</div></div>'
        section += '</section>'
        page_html.append(section)
        frag_html.append(section)
        if i != len(pages) - 1:
            page_html.append('<div class="notes-page-split"></div>')
            frag_html.append('<div class="notes-page-split"></div>')
    return ''.join(page_html), ''.join(frag_html)


def objective_body(lo: dict) -> str:
    title = html.escape(lo['canonicalDisplayTitle'])
    code = html.escape(lo['canonicalInternalCode'])
    slug = lo['slug']
    tex_path = REPO / 'OBJECTIVES' / slug / 'main.tex'
    rendered, _fragment = render_notes_content(tex_path)
    status = lo['notesStatus']
    return f'''
<div class="topnav">
  <a href="../index.html">← Notes index</a>
</div>
<div class="hero">
  <h1>{title}</h1>
  <p>{code} · {html.escape(slug)}</p>
</div>
<div class="card" style="margin-bottom: 18px;">
  <div class="badge {status}">{status.replace('_', ' ').title()}</div>
</div>
{rendered}
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
            actions = f'<div class="actions"><a href="objectives/{slug}.html">Open notes page</a></div>'
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
  <p>HTML teaching notes generated from LaTeX source for Mana Maths learning objectives.</p>
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
    FRAGMENTS_SITE.mkdir(parents=True, exist_ok=True)
    (SITE / 'index.html').write_text(page('Mana Maths Notes', index_body(data)))
    for lo in data['learningObjectives']:
        if lo['notesStatus'] != 'complete':
            continue
        slug = lo['slug']
        tex_path = REPO / 'OBJECTIVES' / slug / 'main.tex'
        rendered, fragment = render_notes_content(tex_path)
        out = OBJECTIVES_SITE / f"{slug}.html"
        out.write_text(page(lo['canonicalDisplayTitle'], objective_body(lo)))
        (FRAGMENTS_SITE / f'{slug}.html').write_text(fragment)


if __name__ == '__main__':
    main()
