import math
from typing import Optional, Tuple, Callable
from constants import GROUND_Y

def _f(t: float, x0, y0, v0, xt0, yt0, vxt, vyt, g) -> float:
    """Equazione f(t)=0 se l'intercettore di modulo v0 può colpire il bersaglio."""
    if t <= 0:
        return 1e9
    xt = xt0 + vxt * t # x_B(t): posizione orizzontale del bersaglio
    yt = yt0 + vyt * t + 0.5 * g * t * t # y_B(t): posizione verticale del bersaglio
    dx = xt - x0
    dy = yt - y0 -  0.5 * g * t * t
    return (dx*dx + dy*dy) - (v0*v0 * t*t)

def _bisect(f: Callable[[float], float], a: float, b: float, tol=1e-4, max_iter=60):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return None
    for _ in range(max_iter):
        mid = (a + b) / 2
        fm = f(mid)
        if abs(fm) < tol:
            return mid
        if fa * fm < 0:
            b, fb = mid, fm
        else:
            a, fa = mid, fm
    return mid

def _first_ground_hit_time(yt0: float, vyt: float, g: float, ground_y: float) -> Optional[float]:
    # yt(t) = yt0 + vyt t + 0.5 g t^2 = ground_y
    a = 0.5 * g
    b = vyt
    c = yt0 - ground_y
    D = b*b - 4*a*c
    if D < 0:
        return None
    r1 = (-b - math.sqrt(D)) / (2*a)
    r2 = (-b + math.sqrt(D)) / (2*a)
    candidates = [t for t in (r1, r2) if t > 0]
    return min(candidates) if candidates else None

def solve_intercept_fixed_speed(
    shooter_pos: Tuple[float, float],
    target_pos:  Tuple[float, float],
    target_vel:  Tuple[float, float],
    speed: float,
    *,
    g=9.81,
    t_min=0.05,
    t_max=7.0,
    ground_y = GROUND_Y
) -> Optional[Tuple[float, float, float, float]]:
    x0, y0        = shooter_pos
    xt0, yt0      = target_pos
    vxt, vyt      = target_vel

    # 1) taglia la ricerca al primo impatto col suolo del bersaglio
    t_ground = _first_ground_hit_time(yt0, vyt, g, ground_y)
    if t_ground is not None:
        if t_ground <= t_min:
            return None
        t_max = min(t_max, t_ground)

    # 2) trova un intervallo [a,b] dove f(a)*f(b) < 0
    a, b = t_min, t_min
    step = 0.1
    while b <= t_max:
        if _f(a, x0, y0, speed, xt0, yt0, vxt, vyt, g) * \
           _f(b, x0, y0, speed, xt0, yt0, vxt, vyt, g) < 0:
            break
        a, b = b, b + step
    else:
        return None  # mai cambiato segno ⇒ nessuna soluzione

    # 3) bisezione
    t_hit = _bisect(lambda t: _f(t, x0, y0, speed, xt0, yt0, vxt, vyt, g), a, b)
    if t_hit is None:
        return None

    # 4) ricava angolo e componenti velocità
    xt = xt0 + vxt * t_hit
    yt = yt0 + vyt * t_hit + 0.5 * g * t_hit * t_hit
    vx = (xt - x0) / t_hit
    vy = (yt - y0) / t_hit - 0.5 * g * t_hit
    angle = math.degrees(math.atan2(-vy, vx)) % 360
    return angle, t_hit, vx, vy
