import pygame
from constants import AXIS_COLOR, AXIS_STEP, GRAY, LIGHT_RED, MOUSE_COORDS_COLOR, WIDTH, HEIGHT, WHITE, YELLOW, RED, GREEN, BLUE, GROUND_COLOR, SKY_COLOR
from game_state import GameState

def draw_axes(screen: pygame.Surface, state: GameState):
    tick = 4
    small_font = pygame.font.SysFont(None, 14)

    x0 = state.defender_pos[0]
    y0 = state.ground_y  # origine (0,0)

    # Asse Y
    pygame.draw.line(screen, AXIS_COLOR, (x0, 0), (x0, state.ground_y), 1)
    pygame.draw.polygon(screen, AXIS_COLOR, [(x0-6,8),(x0+6,8),(x0,0)])
    for y in range(0, y0, AXIS_STEP):
        pygame.draw.line(screen, AXIS_COLOR, (x0-tick, y0-y), (x0+tick, y0-y), 1)
        
        if y != 0:
            lbl = small_font.render(str(y), True, AXIS_COLOR)
            screen.blit(lbl, (x0 - 25, y0 - y - 5))

    # Asse X
    pygame.draw.line(screen, AXIS_COLOR, (0, state.ground_y), (WIDTH, state.ground_y), 1)
    pygame.draw.polygon(screen, AXIS_COLOR, [(WIDTH-8,state.ground_y-6),(WIDTH-8,state.ground_y+6),(WIDTH,state.ground_y)])
    for x in range(x0, WIDTH, AXIS_STEP):
        pygame.draw.line(screen, AXIS_COLOR, (x, state.ground_y-tick), (x, state.ground_y+tick), 1)
        if x != x0:
            lbl = small_font.render(str(x-x0), True, AXIS_COLOR)
            screen.blit(lbl, (x-10, state.ground_y+10))

def draw_background(screen: pygame.Surface, ground_y: int):
    screen.fill(SKY_COLOR)
    pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect(0, ground_y, WIDTH, HEIGHT - ground_y))
    pygame.draw.line(screen, (100, 80, 60), (0, ground_y), (WIDTH, ground_y), 2)

def draw_explosion(screen: pygame.Surface, font: pygame.font.Font, pos: tuple[float, float], timer: float):
    r = int(30 * timer / 0.5)
    pygame.draw.circle(screen, YELLOW, (int(pos[0]), int(pos[1])), r)
    screen.blit(font.render("IMPATTO!", True, YELLOW), (WIDTH//2 - 40, 130))

def draw_base_attaccante(screen: pygame.Surface, base: tuple[int, int, int]):
    bx, by, h = base
    pygame.draw.rect(screen, GRAY, pygame.Rect(int(bx) - 15, int(by), 30, h))

def draw_trajectory(screen: pygame.Surface, trajectory: list[tuple[float, float]], color: tuple[int, int, int] = GRAY):
    for i, (x, y) in enumerate(trajectory):
        if i % 2 == 0:
            pygame.draw.circle(screen, color, (int(x), int(y)), 2)

def draw_missile(screen: pygame.Surface, missile, color: tuple[int, int, int], radius: int):
    pygame.draw.circle(screen, color, (int(missile.x), int(missile.y)), radius)

def draw_mouse_coords(screen: pygame.Surface, font: pygame.font.Font, state: GameState):
    """Mostra le coordinate del cursore in basso a destra, rispetto all’origine cartesiana."""
    mx, my          = pygame.mouse.get_pos()           # pixel schermo
    rel_x           = mx - state.defender_pos[0]       # origine X = difensore
    rel_y           = state.ground_y - my              # origine Y = linea del terreno
    txt             = f"({rel_x:.0f}, {rel_y:.0f})"
    surf            = font.render(txt, True, MOUSE_COORDS_COLOR)

    # posizione in basso-a-destra con 10 px di margine
    x = screen.get_width()  - surf.get_width()  - 10
    y = screen.get_height() - surf.get_height() - 10
    screen.blit(surf, (x, y))

def draw_energy_info(screen: pygame.Surface, font: pygame.font.Font, state):
    rows = [
        ("Attaccante", state.Ek_att, state.Ep_att, state.Em_att),
        ("Intercettore", state.Ek_int, state.Ep_int, state.Em_int),
    ]

    # Testo in colonne separate per allineamento perfetto
    labels = ["Ek", "Ep", "Em"]
    padding = 20
    spacing = 10  # spazio tra colonne

    # Pre-render: riga per riga, colonna per colonna
    line_surfs = []
    max_label_width = font.size("Intercettore")[0]
    col_widths = [font.size(f"{label}=0000")[0] for label in labels]

    for title, ek, ep, em in rows:
        col_values = [f"{ek:.0f}", f"{ep:.0f}", f"{em:.0f}"]
        surf_parts = [
            font.render(title, True, WHITE)
        ]
        for i, val in enumerate(col_values):
            text = f"{labels[i]}={val:>4}"
            surf_parts.append(font.render(text, True, WHITE))
        line_surfs.append(surf_parts)

    # Calcola dimensioni del box totale
    line_height = font.get_height()
    total_width = max_label_width + spacing + sum(col_widths) + (spacing * (len(labels) - 1))
    total_height = len(rows) * (line_height + 4)

    x0 = screen.get_width() - total_width - padding
    y0 = 60

    # Sfondo trasparente
    bg = pygame.Surface((total_width + 10, total_height + 10), pygame.SRCALPHA)
    bg.fill((30, 30, 30, 160))
    screen.blit(bg, (x0 - 5, y0 - 5))

    # Disegna ogni riga
    for row_i, surf_parts in enumerate(line_surfs):
        x = x0
        y = y0 + row_i * (line_height + 4)

        # titolo (es: Attaccante)
        screen.blit(surf_parts[0], (x, y))
        x += max_label_width + spacing

        # colonne Ek, Ep, Em
        for i in range(1, len(surf_parts)):
            screen.blit(surf_parts[i], (x, y))
            x += col_widths[i - 1] + spacing


def draw_scene(screen: pygame.Surface, font: pygame.font.Font, state: GameState):
    draw_background(screen, state.ground_y)

    if state.show_energy:
       draw_energy_info(screen, font, state)

    if state.show_axes:
        draw_axes(screen, state)
        draw_mouse_coords(screen, font, state)

    # base attaccante (se alta)
    if state.attacker_base:
        draw_base_attaccante(screen, state.attacker_base)

    # attacker trajectory
    if state.show_preview and state.stage == 0 and state.attacker_trajectory:
        draw_trajectory(screen, state.attacker_trajectory, LIGHT_RED)
        
    # interceptor trajectory
    if state.show_preview and not state.interceptor and state.interceptor_trajectory:
        draw_trajectory(screen, state.interceptor_trajectory, BLUE)

    # entità
    if state.attacker:
        draw_missile(screen, state.attacker, RED, 8)
    if state.interceptor:
        draw_missile(screen, state.interceptor, GREEN, 6)
    pygame.draw.circle(screen, WHITE, state.defender_pos, 6)
    pygame.draw.circle(screen, WHITE, state.attacker_launch_pos, 6)

    # esplosione
    if state.explosion:
        draw_explosion(screen, font, state.explosion.pos, state.explosion.timer)

    # hint
    screen.blit(font.render("[ESC] Menu    [SPACE] Lancio    [T] Traiettoria    [A] Assi    [E] Energia", True, WHITE), (130, 20))
    pygame.display.flip()
