from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

APP_ROOT = Path(__file__).resolve().parent
STATIC_DIR = APP_ROOT / "Cursed McDonalds 1"

app = FastAPI(title="Cursed McDonalds", version="0.1.0")

if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    logo_html = ""
    if STATIC_DIR.is_dir() and (STATIC_DIR / "Cursed McDonalds Logo.png").is_file():
        logo_html = (
            '<p><img src="/static/Cursed%20McDonalds%20Logo.png" '
            'alt="Cursed McDonalds logo" style="max-width: 420px; width: 100%;"/></p>'
        )

    return f"""\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Cursed McDonalds</title>
    <style>
      :root {{ color-scheme: light dark; }}
      body {{ font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 40px auto; max-width: 780px; padding: 0 16px; }}
      code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
      .card {{ border: 1px solid rgba(127,127,127,.35); border-radius: 12px; padding: 16px; }}
    </style>
  </head>
  <body>
    <h1>Cursed McDonalds</h1>
    {logo_html}
    <div class="card">
      <p>This is a small web wrapper so the repo can deploy on <strong>Render</strong>.</p>
      <p><strong>Note:</strong> Render can't run the interactive Pygame window. To play locally, run <code>python3 opener.py</code>.</p>
      <ul>
        <li>Health check: <code>/healthz</code></li>
        <li>Static assets (if present): <code>/static/...</code></li>
      </ul>
    </div>
  </body>
</html>
"""

