import os
import re
import sys
from pathlib import Path

import pygame


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
    here = Path(__file__).resolve().parent
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


def _exec_game(game_script: Path) -> None:
    os.chdir(str(game_script.parent))
    os.execv(sys.executable, [sys.executable, str(game_script)])


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

    here = Path(__file__).resolve().parent
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

    def draw_button(surface, text, rect, hovered, pressed):
        fill = PAPER if hovered else TOMATO
        text_rgb = TOMATO if hovered else (255, 255, 255)

        bsurf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(bsurf, (*fill, 255), bsurf.get_rect(), border_radius=16)
        if hovered:
            pygame.draw.rect(bsurf, (*TOMATO, 255), bsurf.get_rect(), width=2, border_radius=16)

        label = font_ui.render(text, True, text_rgb)
        bsurf.blit(label, label.get_rect(center=(rect.w // 2, rect.h // 2)))

        shadow = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(shadow, SHADOW, shadow.get_rect(), border_radius=16)
        surface.blit(shadow, (rect.x, rect.y + 6))
        surface.blit(bsurf, (rect.x, rect.y + (2 if pressed else 0)))

    levels = _discover_levels()
    error_text = None if levels else "No level files found."

    clock = pygame.time.Clock()
    screen_name = "home"  # "home" | "levels"
    scroll_index = 0

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
            body_lines = ["Pick a level to play.", "Keys: 1-9 choose, Esc back"]
            if not levels:
                body_lines = ["No levels found.", "Add a level .py file and restart."]

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
        level_buttons: list[tuple[pygame.Rect, dict]] = []
        visible_levels: list[dict] = []
        max_btns_for_scroll = 0

        if screen_name == "home":
            btn = pygame.Rect(panel.x + (panel.w - btn_w) // 2, panel.bottom - 120, btn_w, btn_h)
            home_start_btn = btn
            hovered = btn.collidepoint(mouse)
            draw_button(screen, "Start", btn, hovered=hovered, pressed=pressed and hovered)
        else:
            list_top = panel.y + 210
            list_bottom = panel.bottom - 88
            area_h = max(0, list_bottom - list_top)
            max_btns = max(1, area_h // (btn_h + gap))
            max_btns_for_scroll = max_btns
            max_scroll = max(0, len(levels) - max_btns)
            scroll_index = max(0, min(scroll_index, max_scroll))
            visible = levels[scroll_index : scroll_index + max_btns]
            visible_levels = visible

            start_y = list_top
            for idx, lvl in enumerate(visible):
                rect = pygame.Rect(panel.x + (panel.w - btn_w) // 2, start_y + idx * (btn_h + gap), btn_w, btn_h)
                hovered = rect.collidepoint(mouse)
                draw_button(
                    screen,
                    f"{idx+1}. {lvl['title']}",
                    rect,
                    hovered=hovered,
                    pressed=pressed and hovered,
                )
                level_buttons.append((rect, lvl))

            back = pygame.Rect(panel.x + 28, panel.bottom - 120, 170, btn_h)
            back_btn = back
            hovered = back.collidepoint(mouse)
            draw_button(screen, "Back", back, hovered=hovered, pressed=pressed and hovered)

            prev_btn = pygame.Rect(panel.right - 28 - 170 - 12 - 170, panel.bottom - 120, 170, btn_h)
            next_btn = pygame.Rect(panel.right - 28 - 170, panel.bottom - 120, 170, btn_h)
            hovered = prev_btn.collidepoint(mouse)
            draw_button(screen, "Prev \u2190", prev_btn, hovered=hovered, pressed=pressed and hovered)
            hovered = next_btn.collidepoint(mouse)
            draw_button(screen, "Next \u2192", next_btn, hovered=hovered, pressed=pressed and hovered)

            # Small scroll status text
            if levels:
                start_n = scroll_index + 1
                end_n = min(len(levels), scroll_index + len(visible_levels))
                status = font_hint.render(
                    f"Showing {start_n}-{end_n} of {len(levels)} (scroll / \u2191\u2193 / \u2190\u2192)",
                    True,
                    (110, 100, 88),
                )
                screen.blit(status, (panel.x + 28, panel.y + 156))

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
                        scroll_index = 0
                elif screen_name == "levels":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        scroll_index -= 1
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        scroll_index += 1
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        scroll_index -= max(1, max_btns_for_scroll)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        scroll_index += max(1, max_btns_for_scroll)
                    elif event.key == pygame.K_PAGEUP:
                        scroll_index -= max(1, max_btns_for_scroll - 1)
                    elif event.key == pygame.K_PAGEDOWN:
                        scroll_index += max(1, max_btns_for_scroll - 1)
                    elif event.key == pygame.K_HOME:
                        scroll_index = 0
                    elif event.key == pygame.K_END:
                        scroll_index = max(0, len(levels) - max(1, max_btns_for_scroll))
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        if 0 <= idx < len(visible_levels):
                            pygame.quit()
                            _exec_game(visible_levels[idx]["path"])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if screen_name == "home":
                    if home_start_btn and home_start_btn.collidepoint(event.pos):
                        screen_name = "levels"
                        scroll_index = 0
                else:
                    if back_btn and back_btn.collidepoint(event.pos):
                        screen_name = "home"
                    elif "prev_btn" in locals() and prev_btn.collidepoint(event.pos):
                        scroll_index -= max(1, max_btns_for_scroll)
                    elif "next_btn" in locals() and next_btn.collidepoint(event.pos):
                        scroll_index += max(1, max_btns_for_scroll)
                    else:
                        for rect, lvl in level_buttons:
                            if rect.collidepoint(event.pos):
                                pygame.quit()
                                _exec_game(lvl["path"])
            elif event.type == pygame.MOUSEWHEEL and screen_name == "levels":
                # event.y: +1 up, -1 down
                scroll_index -= event.y
            elif event.type == pygame.MOUSEBUTTONDOWN and screen_name == "levels":
                # Compatibility with older wheel events (4/5)
                if event.button == 4:
                    scroll_index -= 1
                elif event.button == 5:
                    scroll_index += 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
