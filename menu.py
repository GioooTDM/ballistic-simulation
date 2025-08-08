import pygame
from constants import WHITE, YELLOW

from config_schema import GameConfig, GameConfigOption

GREY = (80, 80, 80)

def create_default_options(defaults: GameConfig | None = None) -> list[GameConfigOption]:
    values = defaults if defaults else GameConfig()
    return [
        GameConfigOption("Distanza iniziale", values.distanza_iniziale, 50, 300, 800),
        GameConfigOption("Velocita attaccante", values.velocita_attaccante, 10, 10, 200),
        GameConfigOption("Velocita intercettore", values.velocita_intercettore, 10, 10, 200),
        GameConfigOption("Altezza lancio", values.altezza_lancio, 20, 0, 200),
        GameConfigOption("Gravita", values.gravita, 0.5, 1, 20),
        GameConfigOption("Angolo attaccante", values.angolo_attaccante, 5, 5, 85),
    ]

class Menu:
    def __init__(self, screen, font, defaults=None):
        self.screen = screen
        self.font = font
        self.options = create_default_options(defaults)
        self.index = 0

    def draw(self):
        self.screen.fill((15, 15, 15))
        title = self.font.render("Configurazione Simulazione", True, YELLOW)
        self.screen.blit(title, (50, 30))

        for i, opt in enumerate(self.options):
            color = WHITE if i == self.index else GREY
            text = self.font.render(f"{opt.label}: {opt.value}", True, color)
            self.screen.blit(text, (60, 100 + i * 40))

        info = self.font.render("ENTER = Avvia   |   Frecce = Seleziona/Modifica", True, GREY)
        self.screen.blit(info, (50, 400))

    def handle_input(self, event):

        if event.type == pygame.KEYDOWN:
            current = self.options[self.index]
            if event.key == pygame.K_UP:
                self.index = (self.index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.index = (self.index + 1) % len(self.options)
            elif event.key == pygame.K_RIGHT:
                current.increase()
            elif event.key == pygame.K_LEFT:
                current.decrease()

    def get_config(self) -> GameConfig:
        kwargs = {opt.label.replace(" ", "_").lower(): opt.value for opt in self.options}
        return GameConfig(**kwargs)
