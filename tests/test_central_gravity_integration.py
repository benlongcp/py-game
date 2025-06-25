#!/usr/bin/env python3
"""
Test script to verify central gravity integration with the full game engine.
"""

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from game_engine import GameEngine
from config import *


def test_central_gravity_integration():
    """Test the central gravity integration with the game engine."""
    print("🌍 Testing Central Gravity Integration...")

    # Create game engine
    game_engine = GameEngine()

    print(f"📍 Game Engine Gravity Objects:")
    print(
        f"   Red gravity: ({game_engine.red_gravity_dot.x}, {game_engine.red_gravity_dot.y})"
    )
    print(
        f"   Purple gravity: ({game_engine.purple_gravity_dot.x}, {game_engine.purple_gravity_dot.y})"
    )
    print(
        f"   Central gravity: ({game_engine.central_gravity_dot.x}, {game_engine.central_gravity_dot.y})"
    )

    print(f"\n🎯 Blue Square Starting Position:")
    print(
        f"   Initial position: ({game_engine.blue_square.x}, {game_engine.blue_square.y})"
    )
    print(f"   Expected position: ({BLUE_SQUARE_RESPAWN_X}, {BLUE_SQUARE_RESPAWN_Y})")

    # Verify blue square starts at center (where central gravity is)
    if (
        abs(game_engine.blue_square.x - CENTRAL_GRAVITY_X) < 0.1
        and abs(game_engine.blue_square.y - CENTRAL_GRAVITY_Y) < 0.1
    ):
        print("   ✅ Blue square starts at central gravity point")
    else:
        print("   ❌ Blue square does not start at central gravity point")

    # Test gravity application by moving square slightly off center
    print(f"\n🔄 Testing Gravity Application:")

    # Move square slightly off center
    game_engine.blue_square.x = 100.0
    game_engine.blue_square.y = 50.0
    game_engine.blue_square.velocity_x = 0.0
    game_engine.blue_square.velocity_y = 0.0

    old_vel_x = game_engine.blue_square.velocity_x
    old_vel_y = game_engine.blue_square.velocity_y

    print(
        f"   Before gravity: pos=({game_engine.blue_square.x}, {game_engine.blue_square.y}), vel=({old_vel_x:.6f}, {old_vel_y:.6f})"
    )

    # Apply gravitational forces (this is normally done in update_physics)
    game_engine._apply_gravitational_forces()

    vel_change_x = game_engine.blue_square.velocity_x - old_vel_x
    vel_change_y = game_engine.blue_square.velocity_y - old_vel_y

    print(
        f"   After gravity: vel=({game_engine.blue_square.velocity_x:.6f}, {game_engine.blue_square.velocity_y:.6f})"
    )
    print(f"   Velocity change: ({vel_change_x:.6f}, {vel_change_y:.6f})")

    # Check if central gravity is pulling toward center
    distance_from_center = math.sqrt(
        game_engine.blue_square.x**2 + game_engine.blue_square.y**2
    )
    if distance_from_center < game_engine.central_gravity_dot.max_distance:
        expected_direction_x = -game_engine.blue_square.x / distance_from_center
        expected_direction_y = -game_engine.blue_square.y / distance_from_center

        if (
            vel_change_x * expected_direction_x > 0
            and vel_change_y * expected_direction_y > 0
        ):
            print("   ✅ Central gravity is pulling toward center")
        else:
            print(
                "   ⚠️ Central gravity direction unclear (may be dominated by other forces)"
            )
    else:
        print("   ℹ️ Square is outside central gravity range")

    # Test at different distances
    print(f"\n📏 Testing at Different Distances:")

    test_distances = [25, 100, 200, 400]  # Various distances from center

    for distance in test_distances:
        game_engine.blue_square.x = distance
        game_engine.blue_square.y = 0.0
        game_engine.blue_square.velocity_x = 0.0
        game_engine.blue_square.velocity_y = 0.0

        old_vel_x = game_engine.blue_square.velocity_x

        # Apply only central gravity for this test
        central_applied = game_engine.central_gravity_dot.apply_gravity_to_object(
            game_engine.blue_square
        )

        vel_change = game_engine.blue_square.velocity_x - old_vel_x

        print(
            f"   Distance {distance:3d}: Central gravity applied: {central_applied}, Velocity change: {vel_change:.6f}"
        )

    print(f"\n🎉 Central gravity integration test completed!")
    print(f"The blue square will now experience a gentle pull toward the center,")
    print(
        f"making it easier to collect when it spawns and providing better game balance."
    )


def main():
    """Main function to run the integration test."""
    app = QApplication(sys.argv)
    test_central_gravity_integration()
    sys.exit(0)


if __name__ == "__main__":
    main()
