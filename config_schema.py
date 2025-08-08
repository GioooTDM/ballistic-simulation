from dataclasses import dataclass

@dataclass
class GameConfig:
    distanza_iniziale: int = 750
    velocita_attaccante: int = 80
    velocita_intercettore: int = 80
    altezza_lancio: int = 0
    gravita: float = 9.81
    angolo_attaccante: int = 45


class GameConfigOption:
    def __init__(self, label, value, step, min_val=None, max_val=None):
        self.label = label
        self.value = value
        self.step = step
        self.min = min_val
        self.max = max_val

    def increase(self):
        self.value += self.step
        if self.max is not None:
            self.value = min(self.value, self.max)

    def decrease(self):
        self.value -= self.step
        if self.min is not None:
            self.value = max(self.value, self.min)
