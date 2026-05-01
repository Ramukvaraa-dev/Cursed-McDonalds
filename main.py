from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

APP_ROOT = Path(__file__).resolve().parent
STATIC_DIR = APP_ROOT / "Cursed McDonalds 1"

app = FastAPI(title="Cursed McDonalds", version="0.1.0")

if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

GITHUB_REPO_URL = os.environ.get("GITHUB_REPO_URL", "https://github.com/Ramukvaraa-dev/Cursed-McDonalds")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}

def _page(shell: str, *, title: str = "Cursed McDonald's") -> str:
    return f"""\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <style>
      :root {{
        color-scheme: light dark;
        --ink: rgb(27, 24, 20);
        --paper: rgb(255, 250, 242);
        --paper2: rgb(255, 238, 214);
        --tomato: rgb(222, 29, 29);
        --muted: rgba(90, 80, 70, .92);
        --shadow: rgba(0, 0, 0, .18);
        --border: rgba(127, 127, 127, .30);
      }}

      body {{
        margin: 0;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        color: var(--ink);
        min-height: 100vh;
        background: linear-gradient(180deg, var(--paper), var(--paper2));
      }}

      .wrap {{
        max-width: 940px;
        margin: 0 auto;
        padding: 28px 16px 48px;
      }}

      .panel {{
        max-width: 760px;
        margin: 0 auto;
        background: var(--paper);
        border: 1px solid var(--border);
        border-radius: 22px;
        box-shadow: 0 18px 40px var(--shadow);
        padding: 26px;
      }}

      .top {{
        display: flex;
        gap: 18px;
        align-items: flex-start;
        justify-content: space-between;
      }}

      h1 {{
        margin: 0;
        font-family: ui-serif, "Palatino", "Palatino Linotype", Georgia, serif;
        font-size: 44px;
        line-height: 1.06;
        letter-spacing: .2px;
      }}

      .subtitle {{
        margin-top: 10px;
        color: rgba(70, 62, 54, .95);
        font-family: ui-serif, "Palatino", "Palatino Linotype", Georgia, serif;
        font-size: 20px;
      }}

      hr {{
        border: 0;
        height: 2px;
        background: rgba(235, 220, 201, 1);
        margin: 16px 0 18px;
      }}

      .logo {{
        width: 280px;
        max-width: 40vw;
        height: auto;
        border-radius: 12px;
      }}

      .body {{
        color: var(--muted);
        font-family: ui-serif, "Palatino", "Palatino Linotype", Georgia, serif;
        font-size: 20px;
      }}

      .hint {{
        margin-top: 18px;
        color: rgba(110, 100, 88, .98);
        font-size: 14px;
      }}

      .btn {{
        appearance: none;
        border: 2px solid transparent;
        border-radius: 14px;
        padding: 14px 18px;
        font-weight: 800;
        font-size: 18px;
        cursor: pointer;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        transition: transform .06s ease, background-color .15s ease, color .15s ease, border-color .15s ease;
        user-select: none;
      }}

      .btn-primary {{
        background: var(--tomato);
        color: white;
        box-shadow: 0 10px 18px var(--shadow);
      }}

      .btn-primary:hover {{
        background: var(--paper);
        color: var(--tomato);
        border-color: var(--tomato);
      }}

      .btn-secondary {{
        background: var(--paper);
        color: var(--tomato);
        border-color: var(--tomato);
      }}

      .btn-secondary:hover {{
        background: rgba(255, 255, 255, .4);
      }}

      .btn:active {{
        transform: translateY(1px);
      }}

      .grid {{
        display: grid;
        gap: 12px;
        margin-top: 18px;
        grid-template-columns: repeat(5, minmax(0, 1fr));
      }}

      @media (max-width: 720px) {{
        .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        h1 {{ font-size: 40px; }}
      }}

      .cell {{
        width: 100%;
      }}

      .disabled {{
        background: rgb(232, 224, 214);
        color: rgb(120, 110, 100);
        border-color: rgba(200, 190, 178, .95);
        cursor: not-allowed;
        box-shadow: none;
      }}

      .kbd {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        background: rgba(127,127,127,.14);
        border: 1px solid rgba(127,127,127,.22);
        padding: 1px 6px;
        border-radius: 7px;
        font-size: 14px;
      }}

      a {{
        color: var(--tomato);
      }}
    </style>
  </head>
  <body>
    <div class="wrap">
      <div class="panel">
        {shell}
      </div>
    </div>
  </body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    has_logo = STATIC_DIR.is_dir() and (STATIC_DIR / "Cursed McDonalds Logo.png").is_file()
    logo_html = (
        '<img class="logo" src="/static/Cursed%20McDonalds%20Logo.png" alt="Cursed McDonalds logo" />'
        if has_logo
        else ""
    )

    shell = f"""\
<div class="top">
  <div>
    <h1>Cursed McDonald's</h1>
    <div class="subtitle">Home</div>
  </div>
  <div>{logo_html}</div>
</div>
<hr />
<div class="body">
  <p>Press <strong>Start</strong> to choose a level.</p>
  <p>Keys: <span class="kbd">Enter</span> start, <span class="kbd">Esc</span> quit</p>
</div>
<div style="display:flex; justify-content:center; margin-top: 24px;">
  <a class="btn btn-primary" href="/levels">Start</a>
</div>
<div class="hint">To actually play, run <span class="kbd">python3 opener.py</span> on your computer.</div>
"""

    return _page(shell, title="Cursed McDonald's")


@app.get("/levels", response_class=HTMLResponse)
def levels() -> str:
    has_logo = STATIC_DIR.is_dir() and (STATIC_DIR / "Cursed McDonalds Logo.png").is_file()
    logo_html = (
        '<img class="logo" src="/static/Cursed%20McDonalds%20Logo.png" alt="Cursed McDonalds logo" />'
        if has_logo
        else ""
    )

    cells: list[str] = []
    for n in range(1, 11):
        if n == 1:
            cells.append(
                f'<a class="btn btn-primary cell" href="/levels/{n}">Level {n}</a>'
            )
        else:
            cells.append(f'<span class="btn disabled cell" title="Coming soon">Level {n}</span>')
    grid_html = "\n".join(f"<div>{c}</div>" for c in cells)

    shell = f"""\
<div class="top">
  <div>
    <h1>Cursed McDonald's</h1>
    <div class="subtitle">Select Level</div>
  </div>
  <div>{logo_html}</div>
</div>
<hr />
<div class="body">
  <p><strong>Season 1</strong></p>
  <p style="font-size: 15px; margin-top: -6px; color: rgba(110,100,88,.98);">
    Level 1 is playable locally. Others are coming soon.
  </p>
</div>
<div class="grid">
  {grid_html}
</div>
<div style="display:flex; justify-content: space-between; margin-top: 22px; gap: 12px; flex-wrap: wrap;">
  <a class="btn btn-secondary" href="/">Back</a>
  <a class="btn btn-secondary" href="{GITHUB_REPO_URL}" rel="noreferrer">Project</a>
</div>
<div class="hint">Tip: if you want to play now, download the project and run <span class="kbd">python3 opener.py</span>.</div>
"""

    return _page(shell, title="Select Level · Cursed McDonald's")


@app.get("/levels/{level_num}", response_class=HTMLResponse)
def level_detail(level_num: int) -> str:
    if level_num != 1:
        shell = f"""\
<div class="top">
  <div>
    <h1>Cursed McDonald's</h1>
    <div class="subtitle">Level {level_num}</div>
  </div>
</div>
<hr />
<div class="body">
  <p><strong>Coming soon.</strong></p>
  <p>Only Level 1 is available right now.</p>
</div>
<div style="display:flex; justify-content: space-between; margin-top: 22px; gap: 12px; flex-wrap: wrap;">
  <a class="btn btn-secondary" href="/levels">Back</a>
  <a class="btn btn-secondary" href="{GITHUB_REPO_URL}" rel="noreferrer">Project</a>
</div>
"""
        return _page(shell, title=f"Level {level_num} · Cursed McDonald's")

    shell = f"""\
<div class="top">
  <div>
    <h1>Cursed McDonald's</h1>
    <div class="subtitle">Level 1</div>
  </div>
</div>
<hr />
<div class="body">
  <p><strong>Playable locally.</strong></p>
  <p>This website can’t launch the Pygame window. To play Level 1:</p>
  <ol>
    <li>Download/clone the project from <a href="{GITHUB_REPO_URL}" rel="noreferrer">GitHub</a>.</li>
    <li>Install dependencies and run <span class="kbd">python3 opener.py</span>.</li>
  </ol>
</div>
<div style="display:flex; justify-content: space-between; margin-top: 22px; gap: 12px; flex-wrap: wrap;">
  <a class="btn btn-secondary" href="/levels">Back</a>
  <a class="btn btn-primary" href="{GITHUB_REPO_URL}/releases" rel="noreferrer">Downloads</a>
</div>
"""
    return _page(shell, title="Level 1 · Cursed McDonald's")
