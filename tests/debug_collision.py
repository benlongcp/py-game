"""
Debug script to see if collision is actually occurring.
"""

from game_engine import GameEngine
from config import *
import math


def debug_collision():
    """Debug collision detection between players."""
    print("🔍 Debugging Player Collision...")

    # Create game engine
    engine = GameEngine()
    engine.create_purple_dot()

    # Position dots very close for guaranteed collision
    engine.red_dot.virtual_x = 0
    engine.red_dot.virtual_y = 0
    engine.red_dot.velocity_x = 5.0
    engine.red_dot.velocity_y = 0.0

    engine.purple_dot.virtual_x = 8  # Within collision distance (2 * radius = 10)
    engine.purple_dot.virtual_y = 0
    engine.purple_dot.velocity_x = -2.0
    engine.purple_dot.velocity_y = 0.0

    print(f"Dot radius: {DOT_RADIUS}")
    print(f"Collision distance should be: {2 * DOT_RADIUS}")

    initial_distance = math.sqrt(
        (engine.red_dot.virtual_x - engine.purple_dot.virtual_x) ** 2
        + (engine.red_dot.virtual_y - engine.purple_dot.virtual_y) ** 2
    )
    print(f"Initial distance: {initial_distance}")

    # Record initial state
    print(f"\nBefore:")
    print(
        f"Red: pos=({engine.red_dot.virtual_x:.1f}, {engine.red_dot.virtual_y:.1f}), vel=({engine.red_dot.velocity_x:.2f}, {engine.red_dot.velocity_y:.2f})"
    )
    print(
        f"Purple: pos=({engine.purple_dot.virtual_x:.1f}, {engine.purple_dot.virtual_y:.1f}), vel=({engine.purple_dot.velocity_x:.2f}, {engine.purple_dot.velocity_y:.2f})"
    )

    # Update one frame
    engine.update_game_state()

    print(f"\nAfter 1 frame:")
    print(
        f"Red: pos=({engine.red_dot.virtual_x:.1f}, {engine.red_dot.virtual_y:.1f}), vel=({engine.red_dot.velocity_x:.2f}, {engine.red_dot.velocity_y:.2f})"
    )
    print(
        f"Purple: pos=({engine.purple_dot.virtual_x:.1f}, {engine.purple_dot.virtual_y:.1f}), vel=({engine.purple_dot.velocity_x:.2f}, {engine.purple_dot.velocity_y:.2f})"
    )

    final_distance = math.sqrt(
        (engine.red_dot.virtual_x - engine.purple_dot.virtual_x) ** 2
        + (engine.red_dot.virtual_y - engine.purple_dot.virtual_y) ** 2
    )
    print(f"Final distance: {final_distance}")

    # Check if collision should have occurred
    collision_distance = engine.red_dot.radius + engine.purple_dot.radius
    print(f"Expected collision distance: {collision_distance}")

    if initial_distance <= collision_distance:
        print("✅ Objects were within collision distance initially")
    else:
        print("❌ Objects were NOT within collision distance initially")


if __name__ == "__main__":
    debug_collision()
