import pygame
from pathlib import Path

# Colors (warm, "fast food flyer" vibe)
INK = (27, 24, 20)
PAPER = (255, 250, 242)
PAPER_2 = (255, 238, 214)
TOMATO = (222, 29, 29)
TOMATO_DARK = (168, 18, 18)
MUSTARD = (255, 197, 46)
SHADOW = (0, 0, 0, 70)

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 620
FLAGS = 0
if hasattr(pygame, "SCALED"):
    FLAGS |= pygame.SCALED
if hasattr(pygame, "RESIZABLE"):
    FLAGS |= pygame.RESIZABLE
screen = pygame.display.set_mode((WIDTH, HEIGHT), FLAGS)
pygame.display.set_caption("Cursed McDonald's Season 1 Level 1")

# Assets live next to this file
HERE = Path(__file__).resolve().parent

# Icon/logo (best-effort; keep game runnable if missing)
fallback_icon = pygame.Surface((32, 32), pygame.SRCALPHA)
fallback_icon.fill(PAPER)
pygame.display.set_icon(fallback_icon)
for candidate in ("Cursed McDonalds Logo.ico", "Cursed McDonalds Logo.png"):
    try:
        icon = pygame.image.load(str(HERE / candidate))
        pygame.display.set_icon(icon)
        break
    except Exception:
        pass

logo_image = None
try:
    raw_logo = pygame.image.load(str(HERE / "Cursed McDonalds Logo.png")).convert_alpha()
    max_h = 76
    scale = max_h / raw_logo.get_height()
    lw = int(raw_logo.get_width() * scale)
    lh = int(raw_logo.get_height() * scale)
    logo_image = pygame.transform.smoothscale(raw_logo, (lw, lh))
except Exception:
    logo_image = None

def get_font(names, size, bold=False):
    for name in names:
        font = pygame.font.SysFont(name, size, bold=bold)
        if font:
            return font
    return pygame.font.Font(None, size)

# Typography
font_title = get_font(["Palatino", "Palatino Linotype", "Georgia"], 44, bold=True)
font_body = get_font(["Palatino", "Palatino Linotype", "Georgia"], 28, bold=False)
font_ui = get_font(["Avenir Next", "Avenir", "Verdana", "Arial"], 22, bold=True)
font_hint = get_font(["Avenir Next", "Avenir", "Verdana", "Arial"], 16, bold=False)

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

def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

def render_wrapped_lines(text, font, color, max_width):
    # Basic word wrapping for story text (keeps UI readable on resize).
    words = text.split()
    if not words:
        return [font.render("", True, color)]

    lines = []
    current = words[0]
    for word in words[1:]:
        trial = current + " " + word
        if font.size(trial)[0] <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return [font.render(line, True, color) for line in lines]

def draw_shadowed_roundrect(surface, rect, fill, radius=18, shadow_offset=(0, 8)):
    shadow = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    pygame.draw.rect(shadow, SHADOW, shadow.get_rect(), border_radius=radius)
    surface.blit(shadow, (rect.x + shadow_offset[0], rect.y + shadow_offset[1]))
    pygame.draw.rect(surface, fill, rect, border_radius=radius)

def draw_button(surface, text, rect, hovered, pressed, alpha=255):
    # Button with subtle hover/press motion.
    if hovered:
        fill_rgb = PAPER
        text_rgb = TOMATO
        border_rgb = TOMATO
    else:
        fill_rgb = TOMATO
        text_rgb = (255, 255, 255)
        border_rgb = None

    fill = (*fill_rgb, alpha)

    bsurf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    pygame.draw.rect(bsurf, fill, bsurf.get_rect(), border_radius=16)

    if border_rgb is not None:
        pygame.draw.rect(bsurf, (*border_rgb, alpha), bsurf.get_rect(), width=2, border_radius=16)

    label = font_ui.render(text, True, text_rgb)
    label.set_alpha(alpha)
    label_rect = label.get_rect(center=(rect.w // 2, rect.h // 2))
    bsurf.blit(label, label_rect)

    # Shadow behind button on the main surface.
    shadow = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    pygame.draw.rect(shadow, SHADOW, shadow.get_rect(), border_radius=16)
    surface.blit(shadow, (rect.x, rect.y + 6))

    offset_y = 2 if pressed else 0
    surface.blit(bsurf, (rect.x, rect.y + offset_y))

# Story data
story = {
    'start': ('You go to McDonalds. It has a weird logo', ['Go in it', 'Walk away']),
    'Go in it': ('A Ronald comes and says hi. He wants to tell you something', ['Listen', 'Ignore']),
    'Walk away': ('A Ronald tells you to go in', ['Listen to him', 'Ignore him']),
    'Listen': ('He becomes your friend', ['Buy a burger', 'Go home']),
    'Ignore': ('Ronald gets angry and gets a knife', ['Run for your life', 'Ask for him to listen']),
    'Listen to him': ('You go into McDonalds. You have to buy a burger. Choose a combo', ['Super special ultra combo', 'Normal combo', 'Death combo']),
    'Ignore him': ('Ronald kills you. "Death by a bloodthirsty evil devilish Ronald"', []),
    'Buy a burger': ('The burgers are way too expensive', ['Cheap Burger', 'Fancy Burger']),
    'Go home': ('You trip on a rock. You are unconscious. Ronald takes you to McDonalds and makes you into a burger. "Extra special burger ending"', []),
    'Super special ultra combo': ('There is a human. You get hanged for cannibalism. "Hanged ending"', []),
    'Normal combo': ('You pay your whole wallet', ['Loan', 'Quit life', 'Sue McDonalds']),
    'Death combo': ('It was actually good. You are surprised', ['Run', 'Go back home', 'Pay', 'Stare', 'Eat Ronald', 'Go to hospital']),
    'Run for your life': ('You trip and get killed', []),
    'Ask for him to listen': ('He kills you', []),
    'Cheap Burger': ('You die of every disease. "Every death with disease ending"', []),
    'Fancy Burger': ('It has fancy poisons. You die. "Fancy poisoning ending"', []),
    'Loan': ('Banker denies and you go out and trip. You die. "Broke Ending"', []),
    'Quit life': ('Guess what happens', []),
    'Sue McDonalds': ('McDonalds shut down, But it will return. "Win ending"', []),
    'Run': ('Ronald kills you. "No payment ending"', []),
    'Go back home': ('Ronald kills you. "No payment ending"', []),
    'Pay': ('You are $1 short. "No payment ending"', []),
    'Eat Ronald': ('"Why did you choose this ending?"', []),
    'Go to hospital': ('There is an evil doctor, "OOF ending"', [])
}

current_scene = "start"
transition_start_ms = pygame.time.get_ticks()
mouse_down_prev = False

def change_scene(scene):
    global current_scene, transition_start_ms
    current_scene = scene
    transition_start_ms = pygame.time.get_ticks()

def game_loop():
    global current_scene, mouse_down_prev
    running = True
    clock = pygame.time.Clock()
    
    while running:
        w, h = screen.get_size()
        draw_vertical_gradient(screen, PAPER, PAPER_2)

        # Decorative "mustard blobs" for a bit of atmosphere.
        pygame.draw.circle(screen, (MUSTARD[0], MUSTARD[1], MUSTARD[2]), (int(w * 0.12), int(h * 0.18)), 120)
        pygame.draw.circle(screen, (255, 216, 94), (int(w * 0.88), int(h * 0.10)), 90)
        pygame.draw.circle(screen, (255, 190, 70), (int(w * 0.86), int(h * 0.74)), 140)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    # 1..9 quick choice select
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        choices = story[current_scene][1]
                        if not choices and current_scene in story:
                            choices = ["Restart"]
                        if idx < len(choices):
                            choice = choices[idx]
                            if choice == "Restart":
                                change_scene("start")
                            else:
                                change_scene(choice)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass
        
        now = pygame.time.get_ticks()
        t = (now - transition_start_ms) / 220.0
        alpha = int(255 * ease_out_cubic(t))
        alpha = max(0, min(255, alpha))

        # Main panel layout
        panel_w = min(760, int(w * 0.88))
        panel_h = min(520, int(h * 0.86))
        panel_x = (w - panel_w) // 2
        panel_y = (h - panel_h) // 2
        panel = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        draw_shadowed_roundrect(screen, panel, PAPER, radius=26, shadow_offset=(0, 10))

        # Title
        title = font_title.render("Cursed McDonald's", True, INK)
        title.set_alpha(alpha)
        screen.blit(title, (panel.x + 24, panel.y + 18))

        if logo_image:
            logo = logo_image.copy()
            logo.set_alpha(alpha)
            screen.blit(logo, (panel.right - 24 - logo.get_width(), panel.y + 22))

        subtitle = font_body.render("Season 1 - Level 1", True, (70, 62, 54))
        subtitle.set_alpha(alpha)
        screen.blit(subtitle, (panel.x + 26, panel.y + 70))

        # Divider
        divider_y = panel.y + 110
        pygame.draw.line(screen, (235, 220, 201), (panel.x + 22, divider_y), (panel.right - 22, divider_y), 2)

        # Story text (wrapped)
        story_text = story[current_scene][0]
        text_area = pygame.Rect(panel.x + 28, divider_y + 18, panel.w - 56, int(panel.h * 0.40))
        lines = render_wrapped_lines(story_text, font_body, INK, text_area.w)
        y = text_area.y
        for line_surf in lines:
            line_surf.set_alpha(alpha)
            screen.blit(line_surf, (text_area.x, y))
            y += line_surf.get_height() + 6
        
        # Display choices
        choices = list(story[current_scene][1])
        if not choices:
            # Endings: provide a way out.
            choices = ["Restart"]

        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        clicked = pressed and not mouse_down_prev

        btn_area = pygame.Rect(panel.x + 28, panel.y + int(panel.h * 0.60), panel.w - 56, panel.bottom - (panel.y + int(panel.h * 0.60)) - 18)
        btn_w = min(520, btn_area.w)
        btn_h = 52
        gap = 14
        btn_x = btn_area.x + (btn_area.w - btn_w) // 2
        total_h = len(choices) * btn_h + (len(choices) - 1) * gap
        start_y = btn_area.y + max(0, (btn_area.h - total_h) // 2)

        for idx, choice in enumerate(choices):
            rect = pygame.Rect(btn_x, start_y + idx * (btn_h + gap), btn_w, btn_h)
            hovered = rect.collidepoint(mouse)
            draw_button(screen, f"{idx+1}. {choice}", rect, hovered=hovered, pressed=pressed and hovered, alpha=alpha)

            if hovered and clicked:
                if choice == "Restart":
                    change_scene("start")
                else:
                    change_scene(choice)

        # Footer hints
        hint = font_hint.render("Keys: 1-9 choose, Esc quit", True, (110, 100, 88))
        hint.set_alpha(min(220, alpha))
        screen.blit(hint, (panel.x + 28, panel.bottom - 26))
        
        pygame.display.flip()
        mouse_down_prev = pressed
        clock.tick(60)  # Smoother UI
    
    pygame.quit()

game_loop()
