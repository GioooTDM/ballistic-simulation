# antimissile/physics.py

from constants import COLLISION_RADIUS, GROUND_Y


G = 9.81  # accelerazione gravitazionale; nel sistema schermo y cresce verso il basso

class BallisticObject:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def step(self, dt, g=9.81):
        self.x += self.vx * dt
        self.y += self.vy * dt + 0.5 * g * dt * dt
        self.vy += g * dt

def collides(a: BallisticObject, b: BallisticObject, radius: float = COLLISION_RADIUS) -> bool:
        # Evitiamo la sqrt per efficienza: si confrontano le distanze al quadrato.
        dx = a.x - b.x
        dy = a.y - b.y
        return dx * dx + dy * dy <= radius * radius

def compute_trajectory(x0, y0, vx, vy, g=9.81, dt=0.1, steps=500):
    """Ritorna una lista di punti (x, y) che descrivono il moto parabolico."""
    points = []
    x, y = x0, y0
    for _ in range(steps):
        points.append((x, y))
        x += vx * dt
        y += vy * dt + 0.5 * g * dt * dt
        vy += g * dt
        if y > GROUND_Y:  # fuori dallo schermo
            break
    return points
