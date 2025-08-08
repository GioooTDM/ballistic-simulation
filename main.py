import pygame
from config_schema import GameConfig
from draw import draw_scene
from game_state import GameState
from logic import handle_events, update_state
from menu import Menu
from constants import WIDTH, HEIGHT, FPS

# ─────────────── Inizializza pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anti‑Missile Simulation")
font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()
prev_cfg: GameConfig | None = None 

show_preview = True
show_axes    = False
show_energy  = False

while True:
    # -------- Menu --------
    menu = Menu(screen, font, defaults=prev_cfg)
    config_selected = False
    while not config_selected:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                cfg = menu.get_config()
                prev_cfg = cfg 
                config_selected = True
            else:
                menu.handle_input(ev)
        menu.draw(); pygame.display.flip(); clock.tick(FPS)

    # -------- Simulazione --------
    game = GameState(
        cfg,
        show_preview=show_preview,
        show_axes=show_axes,
        show_energy=show_energy,
    )
    continue_sim = True
    while continue_sim:
        dt = clock.tick(FPS) / 1000.0
        continue_sim = handle_events(game)
        update_state(game, dt)
        draw_scene(screen, font, game)

    show_preview = game.show_preview
    show_axes    = game.show_axes
    show_energy  = game.show_energy