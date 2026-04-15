import os
import sys
from pathlib import Path

import pygame


def _resolve_game_script() -> Path:
    here = Path(__file__).resolve().parent
    candidates = [
        here / "Cursed McDonalds.py",
        here / "Cursed Mcdonalds.py",
        here / "Cursed McDonalds 1" / "Cursed McDonalds.py",
        here / "Cursed McDonalds 1" / "Cursed Mcdonalds.py",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Could not find game script. Looked for: "
        + ", ".join(str(p) for p in candidates)
    )


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

    try:
        game_script = _resolve_game_script()
    except FileNotFoundError:
        game_script = None

    clock = pygame.time.Clock()
    mouse_down_prev = False
    error_text = None if game_script else "Game file not found."

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

        subtitle = font_body.render("Home", True, (70, 62, 54))
        screen.blit(subtitle, (panel.x + 28, panel.y + 92))

        pygame.draw.line(
            screen,
            (235, 220, 201),
            (panel.x + 22, panel.y + 130),
            (panel.right - 22, panel.y + 130),
            2,
        )

        body_lines = [
            "Press Start to launch the game.",
            "Keys: Enter start, Esc quit",
        ]
        if error_text:
            body_lines = [error_text, "Make sure the game file exists."] + body_lines

        y = panel.y + 156
        for line in body_lines:
            surf = font_body.render(line, True, (90, 80, 70))
            screen.blit(surf, (panel.x + 28, y))
            y += surf.get_height() + 10

        # Button
        btn_w = min(420, panel.w - 56)
        btn_h = 60
        btn = pygame.Rect(panel.x + (panel.w - btn_w) // 2, panel.bottom - 120, btn_w, btn_h)

        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        clicked = pressed and not mouse_down_prev
        hovered = btn.collidepoint(mouse)
        draw_button(screen, "Start", btn, hovered=hovered, pressed=pressed and hovered)

        hint = font_hint.render("If the window is blank, click it to focus.", True, (110, 100, 88))
        screen.blit(hint, (panel.x + 28, panel.bottom - 28))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if game_script:
                        pygame.quit()
                        _exec_game(game_script)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hovered and clicked and game_script:
                    pygame.quit()
                    _exec_game(game_script)

        pygame.display.flip()
        mouse_down_prev = pressed
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
