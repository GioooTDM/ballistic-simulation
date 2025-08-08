from antimissile.physics import BallisticObject, collides
import math

def test_ballistic_step():
    # oggetto lanciato con 100 m/s orizzontale, 50 m/s verticale
    obj = BallisticObject(x=0, y=0, vx=100, vy=50)
    dt = 1.0  # 1 secondo

    obj.step(dt)

    # calcolo manuale aspettato
    # x = x0 + vx * dt
    # y = y0 + vy * dt + 0.5 * g * dt^2
    expected_x = 100.0
    expected_y = 50.0 + 0.5 * 9.81

    assert math.isclose(obj.x, expected_x, rel_tol=1e-4)
    assert math.isclose(obj.y, expected_y, rel_tol=1e-4)

def test_collision_detection():
    a = BallisticObject(x=100, y=100, vx=0, vy=0)
    b = BallisticObject(x=105, y=104, vx=0, vy=0)
    
    # distanza tra i due ≈ sqrt(25 + 16) = sqrt(41) ≈ 6.4
    assert collides(a, b, radius=7.0)
    assert not collides(a, b, radius=5.0)

def test_attacker_trajectory():
    attacker = BallisticObject(x=500, y=100, vx=-50, vy=-30)
    dt = 0.5 # mezzo secondo
    positions = []

    for _ in range(11):  # 5.5 secondi
        attacker.step(dt)
        positions.append((attacker.x, attacker.y))

    # Si muove a sinistra sempre
    for i in range(1, len(positions)):
        assert positions[i][0] < positions[i - 1][0]

    # Sale inizialmente (y scende)
    assert positions[1][1] < positions[0][1]
    assert positions[2][1] < positions[1][1]
    assert positions[3][1] < positions[2][1]

    # Minimo raggiunto intorno a passo 6 (≈ 3s), poi inizia a scendere
    min_y = min(p[1] for p in positions)
    min_index = [p[1] for p in positions].index(min_y)
    assert 5 <= min_index <= 7  # massimo vicino a 3s

    # Dopo il minimo la y aumenta ⇒ sta scendendo
    for i in range(min_index + 1, len(positions)):
        assert positions[i][1] > positions[i - 1][1]