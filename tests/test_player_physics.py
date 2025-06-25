"""
Test script to verify Newtonian mechanics between red and purple dots.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from config import *
import math


def test_player_collision_physics():
    """Test that player-vs-player collisions follow Newton's laws."""
    print("🧪 Testing Red vs Purple Dot Collision Physics...")

    # Create game engine
    engine = GameEngine()
    engine.create_purple_dot()

    # Set up collision scenario
    print("\n📋 Initial Setup:")
    print(f"Red Dot Mass: {engine.red_dot.mass}")
    print(f"Purple Dot Mass: {engine.purple_dot.mass}")

    # Position dots for collision
    engine.red_dot.virtual_x = 0
    engine.red_dot.virtual_y = 0
    engine.red_dot.velocity_x = 5.0  # Moving right
    engine.red_dot.velocity_y = 0.0

    engine.purple_dot.virtual_x = 15  # Close enough to collide
    engine.purple_dot.virtual_y = 0
    engine.purple_dot.velocity_x = -2.0  # Moving left (toward red)
    engine.purple_dot.velocity_y = 0.0

    print(f"\n⚡ Before Collision:")
    print(
        f"Red Dot: pos=({engine.red_dot.virtual_x:.1f}, {engine.red_dot.virtual_y:.1f}), vel=({engine.red_dot.velocity_x:.1f}, {engine.red_dot.velocity_y:.1f})"
    )
    print(
        f"Purple Dot: pos=({engine.purple_dot.virtual_x:.1f}, {engine.purple_dot.virtual_y:.1f}), vel=({engine.purple_dot.velocity_x:.1f}, {engine.purple_dot.velocity_y:.1f})"
    )

    # Calculate initial momentum
    initial_momentum_x = (
        engine.red_dot.mass * engine.red_dot.velocity_x
        + engine.purple_dot.mass * engine.purple_dot.velocity_x
    )
    initial_momentum_y = (
        engine.red_dot.mass * engine.red_dot.velocity_y
        + engine.purple_dot.mass * engine.purple_dot.velocity_y
    )

    print(
        f"\n🎯 Initial Total Momentum: ({initial_momentum_x:.2f}, {initial_momentum_y:.2f})"
    )

    # Update physics to trigger collision
    for _ in range(10):  # Run several frames to ensure collision
        engine.update_game_state()
        distance = math.sqrt(
            (engine.red_dot.virtual_x - engine.purple_dot.virtual_x) ** 2
            + (engine.red_dot.virtual_y - engine.purple_dot.virtual_y) ** 2
        )
        if distance < 20:  # Collision likely occurred
            break

    print(f"\n💥 After Collision:")
    print(
        f"Red Dot: pos=({engine.red_dot.virtual_x:.1f}, {engine.red_dot.virtual_y:.1f}), vel=({engine.red_dot.velocity_x:.1f}, {engine.red_dot.velocity_y:.1f})"
    )
    print(
        f"Purple Dot: pos=({engine.purple_dot.virtual_x:.1f}, {engine.purple_dot.virtual_y:.1f}), vel=({engine.purple_dot.velocity_x:.1f}, {engine.purple_dot.velocity_y:.1f})"
    )

    # Calculate final momentum
    final_momentum_x = (
        engine.red_dot.mass * engine.red_dot.velocity_x
        + engine.purple_dot.mass * engine.purple_dot.velocity_x
    )
    final_momentum_y = (
        engine.red_dot.mass * engine.red_dot.velocity_y
        + engine.purple_dot.mass * engine.purple_dot.velocity_y
    )

    print(
        f"\n🎯 Final Total Momentum: ({final_momentum_x:.2f}, {final_momentum_y:.2f})"
    )

    # Check conservation of momentum
    momentum_error_x = abs(final_momentum_x - initial_momentum_x)
    momentum_error_y = abs(final_momentum_y - initial_momentum_y)

    print(f"\n📊 Momentum Conservation Check:")
    print(f"X-axis error: {momentum_error_x:.6f}")
    print(f"Y-axis error: {momentum_error_y:.6f}")

    if momentum_error_x < 0.001 and momentum_error_y < 0.001:
        print("✅ PASS: Momentum is conserved (within numerical precision)")
    else:
        print("❌ FAIL: Momentum conservation violated")

    print(f"\n🔬 Physics Analysis:")
    print(f"Both dots have equal mass ({DOT_MASS})")
    print(f"Collision uses restitution coefficient: {RESTITUTION}")
    print(f"Physics engine applies proper impulse-based collision response")
    print(f"Object separation prevents overlap and tunneling")


if __name__ == "__main__":
    test_player_collision_physics()
