#!/usr/bin/env python3
"""
Test script for the gravitational dots and physics.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects import BlueSquare, RedGravitationalDot, PurpleGravitationalDot
from config import *
import math


def test_gravitational_physics():
    """Test the gravitational physics functionality."""
    print("🌍 Testing Gravitational Physics...")

    # Create test objects
    blue_square = BlueSquare()
    red_gravity_dot = RedGravitationalDot()
    purple_gravity_dot = PurpleGravitationalDot()

    print(f"📍 Gravitational Dot Positions:")
    print(f"   Red gravity dot: ({red_gravity_dot.x}, {red_gravity_dot.y})")
    print(f"   Purple gravity dot: ({purple_gravity_dot.x}, {purple_gravity_dot.y})")
    print(f"   Gravity radius: {red_gravity_dot.radius}")
    print(f"   Max gravity distance: {red_gravity_dot.max_distance}")

    # Test scenarios
    test_scenarios = [
        ("Square at red circle center", red_gravity_dot.x, red_gravity_dot.y),
        ("Square near red circle edge", red_gravity_dot.x + 30, red_gravity_dot.y),
        ("Square outside red circle", red_gravity_dot.x + 60, red_gravity_dot.y),
        ("Square at purple circle center", purple_gravity_dot.x, purple_gravity_dot.y),
        ("Square between circles", 0, 0),  # Center of grid
    ]

    for scenario_name, square_x, square_y in test_scenarios:
        print(f"\n🎯 {scenario_name}:")

        # Reset square state
        blue_square.x = square_x
        blue_square.y = square_y
        blue_square.velocity_x = 0.0
        blue_square.velocity_y = 0.0

        # Calculate distances
        red_distance = math.sqrt(
            (square_x - red_gravity_dot.x) ** 2 + (square_y - red_gravity_dot.y) ** 2
        )
        purple_distance = math.sqrt(
            (square_x - purple_gravity_dot.x) ** 2
            + (square_y - purple_gravity_dot.y) ** 2
        )

        print(f"   Square position: ({square_x}, {square_y})")
        print(f"   Distance to red gravity: {red_distance:.1f}")
        print(f"   Distance to purple gravity: {purple_distance:.1f}")

        # Test gravitational effects
        red_applied = red_gravity_dot.apply_gravity_to_object(blue_square)
        red_vel_after = (blue_square.velocity_x, blue_square.velocity_y)

        # Reset velocity and test purple gravity
        blue_square.velocity_x = 0.0
        blue_square.velocity_y = 0.0
        purple_applied = purple_gravity_dot.apply_gravity_to_object(blue_square)
        purple_vel_after = (blue_square.velocity_x, blue_square.velocity_y)

        print(f"   Red gravity applied: {red_applied}")
        if red_applied:
            print(
                f"   Red gravity velocity change: ({red_vel_after[0]:.3f}, {red_vel_after[1]:.3f})"
            )

        print(f"   Purple gravity applied: {purple_applied}")
        if purple_applied:
            print(
                f"   Purple gravity velocity change: ({purple_vel_after[0]:.3f}, {purple_vel_after[1]:.3f})"
            )

    print(f"\n🎉 Gravitational physics test completed!")
    print(
        f"Blue square will be pulled toward gravity dots when overlapping static circles."
    )


if __name__ == "__main__":
    test_gravitational_physics()
