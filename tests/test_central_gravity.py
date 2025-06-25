#!/usr/bin/env python3
"""
Test script for the central gravitational point functionality.
"""

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from objects import BlueSquare, CentralGravitationalDot
from config import *


def test_central_gravity():
    """Test the central gravitational point functionality."""
    print("🌍 Testing Central Gravitational Point...")

    # Create objects
    blue_square = BlueSquare()
    central_gravity = CentralGravitationalDot()

    print(f"📍 Central Gravity Properties:")
    print(f"   Position: ({central_gravity.x}, {central_gravity.y})")
    print(f"   Strength: {central_gravity.strength}")
    print(f"   Max distance: {central_gravity.max_distance}")
    print(f"   Radius: {central_gravity.radius}")

    # Test 1: Blue square at center (should have no gravity due to distance < 0.1)
    print(f"\n🎯 Test 1: Square at center")
    blue_square.x = 0.0
    blue_square.y = 0.0
    blue_square.velocity_x = 0.0
    blue_square.velocity_y = 0.0

    old_vel_x = blue_square.velocity_x
    old_vel_y = blue_square.velocity_y

    gravity_applied = central_gravity.apply_gravity_to_object(blue_square)

    print(f"   Square position: ({blue_square.x}, {blue_square.y})")
    print(
        f"   Distance to center: {math.sqrt(blue_square.x**2 + blue_square.y**2):.1f}"
    )
    print(f"   Gravity applied: {gravity_applied}")
    print(
        f"   Velocity change: ({blue_square.velocity_x - old_vel_x:.6f}, {blue_square.velocity_y - old_vel_y:.6f})"
    )

    # Test 2: Blue square near center (should have gravity)
    print(f"\n🎯 Test 2: Square near center")
    blue_square.x = 50.0
    blue_square.y = 0.0
    blue_square.velocity_x = 0.0
    blue_square.velocity_y = 0.0

    old_vel_x = blue_square.velocity_x
    old_vel_y = blue_square.velocity_y

    gravity_applied = central_gravity.apply_gravity_to_object(blue_square)

    print(f"   Square position: ({blue_square.x}, {blue_square.y})")
    print(
        f"   Distance to center: {math.sqrt(blue_square.x**2 + blue_square.y**2):.1f}"
    )
    print(f"   Gravity applied: {gravity_applied}")
    print(
        f"   Velocity change: ({blue_square.velocity_x - old_vel_x:.6f}, {blue_square.velocity_y - old_vel_y:.6f})"
    )

    # Test 3: Blue square at edge of gravity field
    print(f"\n🎯 Test 3: Square at edge of gravity field")
    distance = central_gravity.max_distance - 10  # Just inside the field
    blue_square.x = distance
    blue_square.y = 0.0
    blue_square.velocity_x = 0.0
    blue_square.velocity_y = 0.0

    old_vel_x = blue_square.velocity_x
    old_vel_y = blue_square.velocity_y

    gravity_applied = central_gravity.apply_gravity_to_object(blue_square)

    print(f"   Square position: ({blue_square.x}, {blue_square.y})")
    print(
        f"   Distance to center: {math.sqrt(blue_square.x**2 + blue_square.y**2):.1f}"
    )
    print(f"   Max gravity distance: {central_gravity.max_distance:.1f}")
    print(f"   Gravity applied: {gravity_applied}")
    print(
        f"   Velocity change: ({blue_square.velocity_x - old_vel_x:.6f}, {blue_square.velocity_y - old_vel_y:.6f})"
    )

    # Test 4: Blue square outside gravity field
    print(f"\n🎯 Test 4: Square outside gravity field")
    distance = central_gravity.max_distance + 10  # Outside the field
    blue_square.x = distance
    blue_square.y = 0.0
    blue_square.velocity_x = 0.0
    blue_square.velocity_y = 0.0

    old_vel_x = blue_square.velocity_x
    old_vel_y = blue_square.velocity_y

    gravity_applied = central_gravity.apply_gravity_to_object(blue_square)

    print(f"   Square position: ({blue_square.x}, {blue_square.y})")
    print(
        f"   Distance to center: {math.sqrt(blue_square.x**2 + blue_square.y**2):.1f}"
    )
    print(f"   Max gravity distance: {central_gravity.max_distance:.1f}")
    print(f"   Gravity applied: {gravity_applied}")
    print(
        f"   Velocity change: ({blue_square.velocity_x - old_vel_x:.6f}, {blue_square.velocity_y - old_vel_y:.6f})"
    )

    # Test 5: Compare central gravity to static circle gravity
    print(f"\n📊 Gravity Comparison:")
    print(f"   Central gravity strength: {CENTRAL_GRAVITY_STRENGTH}")
    print(f"   Static circle gravity strength: {GRAVITY_STRENGTH}")
    print(f"   Central gravity max distance: {CENTRAL_GRAVITY_MAX_DISTANCE:.1f}")
    print(f"   Static circle gravity max distance: {GRAVITY_MAX_DISTANCE:.1f}")

    print(f"\n🎉 Central gravitational point test completed!")
    print(f"Blue square will be gently pulled toward the center when within range.")


def main():
    """Main function to run the central gravity test."""
    app = QApplication(sys.argv)
    test_central_gravity()
    sys.exit(0)


if __name__ == "__main__":
    main()
