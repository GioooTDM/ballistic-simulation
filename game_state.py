from antimissile.physics import BallisticObject
from config_schema import GameConfig
from constants import COLLISION_RADIUS, WIDTH, HEIGHT, FPS, WHITE, YELLOW, RED, GREEN, BLUE, GROUND_COLOR, SKY_COLOR, GROUND_Y

from dataclasses import dataclass, field
from typing import Optional, List, Tuple

@dataclass
class Explosion:
    pos: Tuple[float, float]
    timer: float  # sec rimanenti

    def update(self, dt: float) -> None:
        self.timer = max(0.0, self.timer - dt)

    @property
    def active(self) -> bool:
        return self.timer > 0


@dataclass
class GameState:
    """Contiene lo stato runtime della simulazione.

    Responsabilità singola: puro contenitore di *dati mutabili* durante una
    partita. Tutta la logica di update/physics è delegata a PhysicsEngine.
    """

    config: GameConfig

    ground_y: int = GROUND_Y
    defender_pos: Tuple[int, int] = field(default_factory=lambda: (100, GROUND_Y))

    # Oggetti dinamici
    attacker: Optional[BallisticObject] = None
    interceptor: Optional[BallisticObject] = None
    
    attacker_trajectory: list[tuple[float, float]] = field(default_factory=list)
    interceptor_trajectory: List[Tuple[float, float]] = field(default_factory=list)

    # Effetti / stato UI
    show_preview: bool = True
    show_axes: bool = False
    show_energy: bool = False

    explosion: Optional[Explosion] = None

    stage: int = 0  # 0: ready, 1: attacker launched, 2: interceptor launched

    # Output dal solver
    vx: float = 0.0
    vy: float = 0.0
    speed: Optional[float] = None
    angle: Optional[float] = None

    # Energie dinamiche
    Ek_att: float = 0.0
    Ep_att: float = 0.0
    Em_att: float = 0.0

    Ek_int: float = 0.0
    Ep_int: float = 0.0
    Em_int: float = 0.0

    # Base statica per disegno
    attacker_base: Optional[Tuple[int, int, int]] = None

    def __post_init__(self):
        if self.config.altezza_lancio > 0:
            alt = self.config.altezza_lancio
            dist = self.config.distanza_iniziale
            x = self.defender_pos[0] + dist
            y = self.ground_y - alt
            self.attacker_base = (x, y, alt)

    # Helper
    @property
    def g(self) -> float:
        return self.config.gravita
    
    @property
    def attacker_launch_pos(self) -> tuple[float, float]:
        """Posizione iniziale dell'attaccante, calcolata rispetto al difensore."""
        x = self.defender_pos[0] + self.config.distanza_iniziale
        y = self.ground_y - self.config.altezza_lancio
        return (x, y)

    @property
    def max_interceptor_speed(self) -> float:
        return self.config.velocita_intercettore