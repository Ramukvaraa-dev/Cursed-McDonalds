import os
import re
import sys
from pathlib import Path
import runpy

import pygame


def _base_dir() -> Path:
    # PyInstaller sets sys._MEIPASS to the extracted/bundle resource dir.
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass).resolve()
    return Path(__file__).resolve().parent


def _extract_level_title(script_path: Path) -> str:
    try:
        text = script_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return script_path.stem

    # Prefer an explicit window caption if present.
    m = re.search(r'pygame\.display\.set_caption\(\s*([\'"])(.+?)\1\s*\)', text)
    if m:
        return m.group(2).strip()

    # Or a "Season X - Level Y" string.
    m = re.search(r'([Ss]eason\s*\d+\s*-\s*[Ll]evel\s*\d+)', text)
    if m:
        return m.group(1).strip()

    return script_path.stem


def _discover_levels() -> list[dict]:
    here = _base_dir()
    search_roots = [here, here / "Cursed McDonalds 1"]
    levels: list[dict] = []

    for root in search_roots:
        if not root.exists() or not root.is_dir():
            continue
        for script in sorted(root.glob("*.py")):
            if script.name == "opener.py":
                continue
            title = _extract_level_title(script)
            levels.append({"path": script, "title": title})

    # De-dupe by absolute path
    seen: set[Path] = set()
    unique: list[dict] = []
    for lvl in levels:
        p = lvl["path"].resolve()
        if p in seen:
            continue
        seen.add(p)
        unique.append(lvl)

    unique.sort(key=lambda x: (x["title"].lower(), str(x["path"]).lower()))
    return unique


def _pick_level1_script(discovered: list[dict]) -> Path | None:
    if not discovered:
        return None
    for lvl in discovered:
        title = str(lvl.get("title", "")).lower()
        if "level 1" in title or "lvl 1" in title or "level1" in title:
            return lvl["path"]
    # Fallback: first discovered script.
    return discovered[0]["path"]


def _run_game(game_script: Path) -> None:
    os.chdir(str(game_script.parent))
    # Run in-process so this works inside a PyInstaller-bundled app.
    runpy.run_path(str(game_script), run_name="__main__")
    sys.exit(0)


def main() -> None:
    pygame.init()

    WIDTH, HEIGHT = 900, 620
    FLAGS = 0
    if hasattr(pygame, "SCALED"):
        FLAGS |= pygame.SCALED
    if hasattr(pygame, "RESIZABLE"):
        FLAGS |= pygame.RESIZABLE
    screen = pygame.display.set_mode((WIDTH, HEIGHT), FLAGS)
    pygame.display.set_caption("Cursed McDonald's")

    # Colors
    INK = (27, 24, 20)
    PAPER = (255, 250, 242)
    PAPER_2 = (255, 238, 214)
    TOMATO = (222, 29, 29)
    SHADOW = (0, 0, 0, 70)

    def get_font(names, size, bold=False):
        for name in names:
            font = pygame.font.SysFont(name, size, bold=bold)
            if font:
                return font
        return pygame.font.Font(None, size)

    font_title = get_font(["Palatino", "Palatino Linotype", "Georgia"], 56, bold=True)
    font_body = get_font(["Palatino", "Palatino Linotype", "Georgia"], 24, bold=False)
    font_ui = get_font(["Avenir Next", "Avenir", "Verdana", "Arial"], 24, bold=True)
    font_hint = get_font(["Avenir Next", "Avenir", "Verdana", "Arial"], 16, bold=False)

    here = _base_dir()

    # Window icon (best-effort; keep app runnable if missing)
    fallback_icon = pygame.Surface((32, 32), pygame.SRCALPHA)
    fallback_icon.fill(PAPER)
    pygame.display.set_icon(fallback_icon)
    for candidate in (
        here / "Cursed McDonalds Logo.ico",
        here / "Cursed McDonalds Logo.png",
        here / "Cursed McDonalds 1" / "Cursed McDonalds Logo.ico",
        here / "Cursed McDonalds 1" / "Cursed McDonalds Logo.png",
    ):
        try:
            icon = pygame.image.load(str(candidate))
            pygame.display.set_icon(icon)
            break
        except Exception:
            pass

    logo = None
    for candidate in (
        here / "Cursed McDonalds 1" / "Cursed McDonalds Logo.png",
        here / "Cursed McDonalds Logo.png",
    ):
        try:
            raw_logo = pygame.image.load(str(candidate)).convert_alpha()
            max_h = 92
            scale = max_h / raw_logo.get_height()
            logo = pygame.transform.smoothscale(
                raw_logo,
                (int(raw_logo.get_width() * scale), int(raw_logo.get_height() * scale)),
            )
            break
        except Exception:
            logo = None

    def draw_vertical_gradient(surface, top_color, bottom_color):
        w, h = surface.get_size()
        if h <= 1:
            return
        for y in range(h):
            t = y / (h - 1)
            r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
            g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
            b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
            pygame.draw.line(surface, (r, g, b), (0, y), (w, y))

    def draw_shadowed_roundrect(surface, rect, fill, radius=22, shadow_offset=(0, 10)):
        shadow = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(shadow, SHADOW, shadow.get_rect(), border_radius=radius)
        surface.blit(shadow, (rect.x + shadow_offset[0], rect.y + shadow_offset[1]))
        pygame.draw.rect(surface, fill, rect, border_radius=radius)

    def draw_button(surface, text, rect, hovered, pressed, enabled=True):
        if not enabled:
            fill = (232, 224, 214)
            text_rgb = (120, 110, 100)
            border = (200, 190, 178)
        else:
            fill = PAPER if hovered else TOMATO
            text_rgb = TOMATO if hovered else (255, 255, 255)
            border = TOMATO if hovered else None

        bsurf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(bsurf, (*fill, 255), bsurf.get_rect(), border_radius=16)
        if border is not None:
            pygame.draw.rect(bsurf, (*border, 255), bsurf.get_rect(), width=2, border_radius=16)

        label = font_ui.render(text, True, text_rgb)
        bsurf.blit(label, label.get_rect(center=(rect.w // 2, rect.h // 2)))

        shadow = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(shadow, SHADOW, shadow.get_rect(), border_radius=16)
        surface.blit(shadow, (rect.x, rect.y + 6))
        surface.blit(bsurf, (rect.x, rect.y + ((2 if pressed else 0) if enabled else 0)))

    levels = _discover_levels()
    level1_script = _pick_level1_script(levels)
    error_text = None if level1_script else "Level 1 file not found."

    clock = pygame.time.Clock()
    screen_name = "home"  # "home" | "levels"

    running = True
    while running:
        w, h = screen.get_size()
        draw_vertical_gradient(screen, PAPER, PAPER_2)

        # Panel
        panel_w = min(760, int(w * 0.88))
        panel_h = min(520, int(h * 0.86))
        panel = pygame.Rect((w - panel_w) // 2, (h - panel_h) // 2, panel_w, panel_h)
        draw_shadowed_roundrect(screen, panel, PAPER, radius=26, shadow_offset=(0, 10))

        # Title
        title = font_title.render("Cursed McDonald's", True, INK)
        screen.blit(title, (panel.x + 26, panel.y + 24))

        if logo:
            screen.blit(logo, (panel.right - 26 - logo.get_width(), panel.y + 26))

        subtitle_text = "Home" if screen_name == "home" else "Select Level"
        subtitle = font_body.render(subtitle_text, True, (70, 62, 54))
        screen.blit(subtitle, (panel.x + 28, panel.y + 92))

        pygame.draw.line(
            screen,
            (235, 220, 201),
            (panel.x + 22, panel.y + 130),
            (panel.right - 22, panel.y + 130),
            2,
        )

        if screen_name == "home":
            body_lines = [
                "Press Start to choose a level.",
                "Keys: Enter start, Esc quit",
            ]
            if error_text:
                body_lines = [error_text, "Put level .py files next to this folder."] + body_lines
        else:
            # Level select screen draws its own header/helper to avoid overlap.
            body_lines = []
            if not level1_script:
                body_lines = ["Level 1 not found.", "Add your level file and restart."]

        y = panel.y + 156
        for line in body_lines:
            surf = font_body.render(line, True, (90, 80, 70))
            screen.blit(surf, (panel.x + 28, y))
            y += surf.get_height() + 10

        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]

        # Buttons
        btn_w = min(520, panel.w - 56)
        btn_h = 58
        gap = 14
        home_start_btn = None
        back_btn = None
        level_buttons: list[tuple[pygame.Rect, int]] = []
        hover_message = None

        if screen_name == "home":
            btn = pygame.Rect(panel.x + (panel.w - btn_w) // 2, panel.bottom - 120, btn_w, btn_h)
            home_start_btn = btn
            hovered = btn.collidepoint(mouse)
            draw_button(screen, "Start", btn, hovered=hovered, pressed=pressed and hovered, enabled=True)
        else:
            # Header + helper text
            header = font_body.render("Season 1", True, (70, 62, 54))
            helper = font_hint.render("Level 1 is playable. Hover others for Coming soon.", True, (110, 100, 88))
            header_x = panel.x + 28
            header_y = panel.y + 140
            helper_y = header_y + header.get_height() + 6
            screen.blit(header, (header_x, header_y))
            screen.blit(helper, (header_x, helper_y))

            back = pygame.Rect(panel.x + 28, panel.bottom - 120, 170, btn_h)
            back_btn = back
            hovered = back.collidepoint(mouse)
            draw_button(screen, "Back", back, hovered=hovered, pressed=pressed and hovered, enabled=True)

            # Grid of 10 levels (only Level 1 available)
            grid_top = helper_y + helper.get_height() + 16
            grid_left = panel.x + 28
            grid_right = panel.right - 28
            grid_bottom = back.top - 18
            grid_w = max(0, grid_right - grid_left)
            grid_h = max(0, grid_bottom - grid_top)

            # Prefer a wide grid if there is room.
            if panel.w >= 720:
                cols, rows = 5, 2
            else:
                cols, rows = 2, 5

            cell_gap_x = 12
            cell_gap_y = 14
            cell_h = 56
            cell_w = (grid_w - cell_gap_x * (cols - 1)) // cols if cols else grid_w

            total_h = rows * cell_h + (rows - 1) * cell_gap_y
            start_y = grid_top + max(0, (grid_h - total_h) // 2)

            for i in range(10):
                level_num = i + 1
                r = i // cols
                c = i % cols
                x = grid_left + c * (cell_w + cell_gap_x)
                y = start_y + r * (cell_h + cell_gap_y)
                rect = pygame.Rect(x, y, cell_w, cell_h)

                enabled = level_num == 1 and level1_script is not None
                hovered = rect.collidepoint(mouse)
                draw_button(
                    screen,
                    f"Level {level_num}",
                    rect,
                    hovered=hovered,
                    pressed=pressed and hovered,
                    enabled=enabled,
                )
                level_buttons.append((rect, level_num))

                if hovered and level_num > 1:
                    hover_message = "Coming soon"
                elif hovered and level_num == 1:
                    hover_message = "Click to play"

            if hover_message:
                # Tooltip-like message near bottom center.
                msg = font_hint.render(hover_message, True, (110, 100, 88))
                msg_x = panel.x + (panel.w - msg.get_width()) // 2
                msg_y = back.top - msg.get_height() - 10
                screen.blit(msg, (msg_x, msg_y))

        hint = font_hint.render("If the window is blank, click it to focus.", True, (110, 100, 88))
        screen.blit(hint, (panel.x + 28, panel.bottom - 28))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if screen_name == "levels":
                        screen_name = "home"
                    else:
                        running = False
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if screen_name == "home":
                        screen_name = "levels"
                    elif screen_name == "levels" and level1_script is not None:
                        pygame.quit()
                        _run_game(level1_script)
                elif screen_name == "levels" and level1_script is not None:
                    if event.key == pygame.K_1:
                        pygame.quit()
                        _run_game(level1_script)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if screen_name == "home":
                    if home_start_btn and home_start_btn.collidepoint(event.pos):
                        screen_name = "levels"
                else:
                    if back_btn and back_btn.collidepoint(event.pos):
                        screen_name = "home"
                    else:
                        for rect, level_num in level_buttons:
                            if rect.collidepoint(event.pos) and level_num == 1 and level1_script is not None:
                                pygame.quit()
                                _run_game(level1_script)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
