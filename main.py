from __future__ import annotations

import os
import json
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

# Web port of `Cursed McDonalds 1/Cursed Mcdonalds.py` story graph.
LEVEL1_STORY: dict[str, tuple[str, list[str]]] = {
    "start": ("You go to McDonalds. It has a weird logo", ["Go in it", "Walk away"]),
    "Go in it": (
        "A Ronald comes and says hi. He wants to tell you something",
        ["Listen", "Ignore"],
    ),
    "Walk away": ("A Ronald tells you to go in", ["Listen to him", "Ignore him"]),
    "Listen": ("He becomes your friend", ["Buy a burger", "Go home"]),
    "Ignore": ("Ronald gets angry and gets a knife", ["Run for your life", "Ask for him to listen"]),
    "Listen to him": (
        "You go into McDonalds. You have to buy a burger. Choose a combo",
        ["Super special ultra combo", "Normal combo", "Death combo"],
    ),
    "Ignore him": ('Ronald kills you. "Death by a bloodthirsty evil devilish Ronald"', []),
    "Buy a burger": ("The burgers are way too expensive", ["Cheap Burger", "Fancy Burger"]),
    "Go home": (
        'You trip on a rock. You are unconscious. Ronald takes you to McDonalds and makes you into a burger. "Extra special burger ending"',
        [],
    ),
    "Super special ultra combo": (
        'There is a human. You get hanged for cannibalism. "Hanged ending"',
        [],
    ),
    "Normal combo": ("You pay your whole wallet", ["Loan", "Quit life", "Sue McDonalds"]),
    "Death combo": ("It was actually good. You are surprised", ["Run", "Go back home", "Pay", "Stare", "Eat Ronald", "Go to hospital"]),
    "Cheap Burger": ("You die of every disease. \"Every death with disease ending\"", []),
    "Fancy Burger": ("It has fancy poisons. You die. \"Fancy poisoning ending\"", []),
    "Loan": ("Banker denies and you go out and trip. You die. \"Broke Ending\"", []),
    "Quit life": ("Guess what happens", []),
    "Sue McDonalds": ("McDonalds shut down, But it will return.\nWIN ENDING", ["Play again"]),
    "Run": ("Ronald kills you. \"No payment ending\"", []),
    "Go back home": ("Ronald kills you. \"No payment ending\"", []),
    "Pay": ("You are $1 short. \"No payment ending\"", []),
    "Stare": ('You stare at Ronald in disbelief. He stares back. You die. "Awkward ending"', []),
    "Run for your life": ("You trip and get killed", []),
    "Ask for him to listen": ("He kills you", []),
    "Eat Ronald": ("\"Why did you choose this ending?\"", []),
    "Go to hospital": ("There is an evil doctor, \"OOF ending\"", []),
    "Play again": (
        "You go to McDonalds. It has a weird logo",
        ["Go in it", "Walk away", "Question reality"],
    ),
    "Question reality": (
        "You question reality so hard that you break the fourth wall and escape the game "
        '(Secret ending, can only be achieved by winning the game). "Fourth wall escape ending"',
        ["Play again"],
    ),
}


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
    <meta name="theme-color" content="#de1d1d" />
    <link rel="icon" type="image/png" href="/static/Cursed%20McDonalds%20Logo.png" />
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

      html {{
        background: transparent;
      }}

      body {{
        margin: 0;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        color: var(--ink);
        min-height: 100vh;
        background: transparent;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
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
        border-radius: 26px;
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
        font-size: 48px;
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
        width: 320px;
        max-width: 42vw;
        height: auto;
        border-radius: 14px;
      }}

      .body {{
        color: var(--muted);
        font-family: ui-serif, "Palatino", "Palatino Linotype", Georgia, serif;
        font-size: 22px;
      }}

      .hint {{
        margin-top: 18px;
        color: rgba(110, 100, 88, .98);
        font-size: 14px;
      }}

      .btn {{
        appearance: none;
        border: 2px solid transparent;
        border-radius: 16px;
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
        box-shadow: 0 12px 0 rgba(0,0,0,.12);
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
        box-shadow: 0 12px 0 rgba(0,0,0,.08);
      }}

      .btn-secondary:hover {{
        background: rgba(255, 255, 255, .4);
      }}

      .btn:active {{
        transform: translateY(2px);
        box-shadow: 0 10px 0 rgba(0,0,0,.10);
      }}

      .grid {{
        display: grid;
        gap: 12px;
        margin-top: 18px;
        grid-template-columns: repeat(5, minmax(0, 1fr));
      }}

      @media (max-width: 720px) {{
        .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        h1 {{ font-size: 42px; }}
        .logo {{ width: 240px; }}
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

      .blob-bg {{
        position: relative;
        overflow: hidden;
      }}

      .blob-bg::before {{
        content: "";
        position: absolute;
        inset: -220px -120px -220px -120px;
        background:
          radial-gradient(circle at 12% 18%, rgba(255, 197, 46, .95) 0 120px, transparent 121px),
          radial-gradient(circle at 88% 10%, rgba(255, 216, 94, .95) 0 92px, transparent 93px),
          radial-gradient(circle at 86% 74%, rgba(255, 190, 70, .95) 0 145px, transparent 146px);
        pointer-events: none;
        z-index: 0;
        filter: saturate(1.05);
      }}

      .blob-bg > * {{
        position: relative;
        z-index: 1;
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

      .story {{
        max-height: 280px;
        overflow: auto;
        padding-right: 6px;
      }}

      .story p {{
        margin: 0 0 10px;
      }}
    </style>
  </head>
  <body>
    <div class="wrap">
      <div class="panel blob-bg">
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
  <p><strong>Playable in your browser.</strong></p>
  <p>This is a web version of Season 1 – Level 1.</p>
</div>
<div style="display:flex; justify-content: space-between; margin-top: 22px; gap: 12px; flex-wrap: wrap;">
  <a class="btn btn-secondary" href="/levels">Back</a>
  <a class="btn btn-primary" href="/play">Play Level 1</a>
</div>
"""
    return _page(shell, title="Level 1 · Cursed McDonald's")


@app.get("/play", response_class=HTMLResponse)
def play_level1() -> str:
    has_logo = STATIC_DIR.is_dir() and (STATIC_DIR / "Cursed McDonalds Logo.png").is_file()
    logo_html = (
        '<img class="logo" src="/static/Cursed%20McDonalds%20Logo.png" alt="Cursed McDonalds logo" />'
        if has_logo
        else ""
    )

    story_json = json.dumps(LEVEL1_STORY, ensure_ascii=False)

    shell = f"""\
<div class="top">
  <div>
    <h1>Cursed McDonald's</h1>
    <div class="subtitle">Season 1 - Level 1</div>
  </div>
  <div>{logo_html}</div>
</div>
<hr />

<div class="body story" id="sceneText" style="min-height: 180px;"></div>

<div id="choices" class="grid" style="grid-template-columns: 1fr; margin-top: 16px;"></div>

<div class="hint">
  Keys: <span class="kbd">1-9</span> choose, <span class="kbd">Esc</span> back to levels
</div>

<script>
  const STORY = {story_json};
  let current = "start";

  const sceneTextEl = document.getElementById("sceneText");
  const choicesEl = document.getElementById("choices");

  function setScene(key) {{
    current = key;
    render();
  }}

  function getChoices() {{
    const scene = STORY[current];
    if (!scene) return ["Restart"];
    const choices = Array.isArray(scene[1]) ? [...scene[1]] : [];
    return choices.length ? choices : ["Restart"];
  }}

  function getText() {{
    const scene = STORY[current];
    return scene ? String(scene[0] ?? "") : "Unknown scene.";
  }}

  function render() {{
    // Fade-in effect similar to the pygame version.
    sceneTextEl.style.opacity = "0";
    choicesEl.style.opacity = "0";

    const text = getText();
    const html = text
      .split("\\n")
      .map((line) => `<p>${{escapeHtml(line)}}</p>`)
      .join("");
    sceneTextEl.innerHTML = html;

    const choices = getChoices();
    // Use a 1–3 column grid depending on count, like the pygame layout.
    let cols = 1;
    if (choices.length >= 6) cols = 3;
    else if (choices.length >= 3) cols = 2;
    choicesEl.style.gridTemplateColumns = `repeat(${{cols}}, minmax(0, 1fr))`;

    choicesEl.innerHTML = "";
    choices.forEach((choice, idx) => {{
      const btn = document.createElement("button");
      btn.className = "btn btn-primary";
      btn.type = "button";
      btn.textContent = `${{idx + 1}}. ${{choice}}`;
      btn.onclick = () => onChoose(choice);
      choicesEl.appendChild(btn);
    }});

    requestAnimationFrame(() => {{
      sceneTextEl.style.transition = "opacity 180ms ease";
      choicesEl.style.transition = "opacity 180ms ease";
      sceneTextEl.style.opacity = "1";
      choicesEl.style.opacity = "1";
    }});
  }}

  function onChoose(choice) {{
    if (choice === "Restart") {{
      setScene("start");
      return;
    }}
    if (STORY[choice]) {{
      setScene(choice);
      return;
    }}
    // If the story graph is missing a node, treat it as an ending.
    setScene("start");
  }}

  function escapeHtml(str) {{
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }}

  document.addEventListener("keydown", (e) => {{
    if (e.key === "Escape") {{
      window.location.href = "/levels";
      return;
    }}
    if (e.key >= "1" && e.key <= "9") {{
      const idx = Number(e.key) - 1;
      const choices = getChoices();
      if (idx >= 0 && idx < choices.length) onChoose(choices[idx]);
    }}
    if (e.key === "Enter") {{
      const choices = getChoices();
      if (choices.length === 1) onChoose(choices[0]);
    }}
  }});

  render();
</script>
"""

    return _page(shell, title="Season 1 - Level 1 · Cursed McDonald's")
