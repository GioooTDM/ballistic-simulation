import math
import pygame
from typing import Tuple
from antimissile.physics import BallisticObject, collides, compute_trajectory
from antimissile.solver import solve_intercept_fixed_speed
from constants import M
from game_state import Explosion, GameState


def handle_events(state: GameState) -> bool:
    """Gestisce input; ritorna False se l'utente vuole uscire al menu."""
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); exit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                return False
            if ev.key == pygame.K_t:
                state.show_preview = not state.show_preview
            if ev.key == pygame.K_a:
                state.show_axes = not state.show_axes
            if ev.key == pygame.K_e: 
                state.show_energy = not state.show_energy
            if ev.key == pygame.K_SPACE:
                launch_missiles(state)
    return True

def launch_missiles(state: GameState):
    cfg = state.config
    if state.stage == 0:  # lancia attaccante
        rad = math.radians(cfg.angolo_attaccante)
        vx_att = -cfg.velocita_attaccante * math.cos(rad)
        vy_att = -cfg.velocita_attaccante * math.sin(rad)
        x, y = state.attacker_launch_pos
        state.attacker = BallisticObject(
            x=x,
            y=y,
            vx=vx_att,
            vy=vy_att,
        )
        state.stage = 1
    elif state.stage == 1 and state.speed is not None:  # lancia intercettore
        state.interceptor = BallisticObject(state.defender_pos[0], state.defender_pos[1], state.vx, state.vy)
        state.stage = 2

def update_energies(state: GameState):
    # Massa arbitraria
    m = M

    # Energia cinetica: ½ m v², con v = sqrt(vx² + vy²)
    def calc(obj: BallisticObject) -> Tuple[float, float, float]:
        v = math.hypot(obj.vx, obj.vy)
        Ek = 0.5 * m * v * v
        Ep = m * state.g * max(0.0, state.ground_y - obj.y)
        return Ek, Ep, Ek + Ep
    
    if state.attacker:
        state.Ek_att, state.Ep_att, state.Em_att = calc(state.attacker)
    else:
        state.Ek_att = state.Ep_att = state.Em_att = 0.0

    if state.interceptor:
        state.Ek_int, state.Ep_int, state.Em_int = calc(state.interceptor)
    else:
        state.Ek_int = state.Ep_int = state.Em_int = 0.0


def update_state(state: GameState, dt: float):
    if state.stage == 0 and state.show_preview:
        # velocità iniziale in base ai parametri di config
        rad = math.radians(state.config.angolo_attaccante)
        vx_att = -state.config.velocita_attaccante * math.cos(rad)
        vy_att = -state.config.velocita_attaccante * math.sin(rad)

        state.attacker_trajectory = compute_trajectory(
            *state.attacker_launch_pos, vx_att, vy_att, g=state.g
        )

    # --- solver preview
    if state.attacker and state.interceptor is None:
        res = solve_intercept_fixed_speed(
            shooter_pos=state.defender_pos,
            target_pos=(state.attacker.x, state.attacker.y),
            target_vel=(state.attacker.vx, state.attacker.vy),
            g=state.g,
            speed=state.config.velocita_intercettore,
        )

        if res:
            state.speed = state.config.velocita_intercettore
            state.angle, _, _, _ = res
            state.vx = state.speed * math.cos(math.radians(state.angle))
            state.vy = -state.speed * math.sin(math.radians(state.angle))
            state.interceptor_trajectory = compute_trajectory(*state.defender_pos, state.vx, state.vy, g=state.g)
        else:
            state.interceptor_trajectory = []

    # --- fisica oggetti
    for obj_name in ("attacker", "interceptor"):
        obj = getattr(state, obj_name)
        if obj:
            obj.step(dt, g=state.g)
            if obj.y > state.ground_y:
                obj.y = state.ground_y; obj.vy = 0

                if obj_name == "attacker":
                    state.explosion = Explosion((obj.x, state.ground_y), timer=1.0)
                    state.attacker = None
                    state.stage = 0

    # --- collisione
    if state.attacker and state.interceptor and collides(state.attacker, state.interceptor):
        x = (state.attacker.x + state.interceptor.x) / 2
        y = (state.attacker.y + state.interceptor.y) / 2
        state.explosion = Explosion(pos=(x, y), timer=0.75)
        state.attacker = None
        state.interceptor = None
        state.stage = 0

    # --- update esplosione
    if state.explosion:
        state.explosion.update(dt)
        if not state.explosion.active:
            state.explosion = None

    update_energies(state)
