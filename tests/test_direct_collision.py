"""
Direct test of the player collision physics function.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from config import *
import math


def test_direct_collision():
    """Test collision function directly."""
    print("🎯 Direct Player Collision Test")

    engine = GameEngine()
    engine.create_purple_dot()

    # Position dots exactly at collision distance
    engine.red_dot.virtual_x = 0
    engine.red_dot.virtual_y = 0
    engine.red_dot.velocity_x = 3.0
    engine.red_dot.velocity_y = 0.0

    engine.purple_dot.virtual_x = 9.5  # Just touching (2 * radius = 10)
    engine.purple_dot.virtual_y = 0
    engine.purple_dot.velocity_x = -1.0
    engine.purple_dot.velocity_y = 0.0

    distance = math.sqrt(
        (engine.red_dot.virtual_x - engine.purple_dot.virtual_x) ** 2
        + (engine.red_dot.virtual_y - engine.purple_dot.virtual_y) ** 2
    )
    print(f"Initial distance: {distance}")
    print(f"Collision threshold: {engine.red_dot.radius + engine.purple_dot.radius}")

    print(f"\nBefore collision:")
    print(
        f"Red: vel=({engine.red_dot.velocity_x:.2f}, {engine.red_dot.velocity_y:.2f})"
    )
    print(
        f"Purple: vel=({engine.purple_dot.velocity_x:.2f}, {engine.purple_dot.velocity_y:.2f})"
    )

    # Calculate expected momentum conservation
    initial_momentum_x = (
        engine.red_dot.mass * engine.red_dot.velocity_x
        + engine.purple_dot.mass * engine.purple_dot.velocity_x
    )
    print(f"Initial momentum: {initial_momentum_x}")

    # Call collision function directly
    engine._handle_player_collision()

    print(f"\nAfter collision:")
    print(
        f"Red: vel=({engine.red_dot.velocity_x:.2f}, {engine.red_dot.velocity_y:.2f})"
    )
    print(
        f"Purple: vel=({engine.purple_dot.velocity_x:.2f}, {engine.purple_dot.velocity_y:.2f})"
    )

    # Check momentum conservation
    final_momentum_x = (
        engine.red_dot.mass * engine.red_dot.velocity_x
        + engine.purple_dot.mass * engine.purple_dot.velocity_x
    )
    print(f"Final momentum: {final_momentum_x}")
    print(f"Momentum difference: {abs(final_momentum_x - initial_momentum_x):.6f}")

    if abs(final_momentum_x - initial_momentum_x) < 0.001:
        print("✅ Momentum conserved!")
    else:
        print("❌ Momentum not conserved")


if __name__ == "__main__":
    test_direct_collision()
